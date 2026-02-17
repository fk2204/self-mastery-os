#!/usr/bin/env python3
"""
Self-Mastery OS - Dashboard Server
Serves the web dashboard with live data from your profile.
Optimized for mobile apps with POST endpoints, compression, and caching.
"""
import os
import sys
import json
import gzip
import hashlib
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse, parse_qs

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_manager import DataManager
from wisdom_engine import WisdomEngine

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
dm = DataManager(BASE_PATH)

# Simple caching for wisdom data (cached by date)
_wisdom_cache = {}
_wisdom_cache_date = None

class DashboardHandler(SimpleHTTPRequestHandler):
    """Custom handler that serves dashboard with dynamic data."""

    def do_GET(self):
        if self.path == '/' or self.path == '/dashboard':
            self.path = '/dashboard.html'
        elif self.path == '/api/data':
            self.send_api_data()
            return
        elif self.path == '/api/wisdom':
            self.send_wisdom()
            return
        elif self.path == '/api/habits':
            self.send_habits()
            return
        elif self.path == '/api/planning':
            self.send_planning_data()
            return
        elif self.path.startswith('/data/') and self.path.endswith('.json'):
            self.serve_data_file()
            return

        return super().do_GET()

    def do_POST(self):
        """Handle POST requests from mobile app and web clients."""
        content_length = int(self.headers.get('Content-Length', 0))

        # Validate content length (max 1MB for mobile efficiency)
        if content_length > 1048576:
            self.send_error(413, "Payload too large")
            return

        try:
            body = self.rfile.read(content_length)
            request_data = json.loads(body.decode('utf-8')) if body else {}
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            self.send_error_json(400, f"Invalid JSON: {str(e)}")
            return

        # Route POST requests
        if self.path == '/api/checkin/morning':
            self.save_morning_checkin(request_data)
        elif self.path == '/api/checkin/evening':
            self.save_evening_reflection(request_data)
        elif self.path.startswith('/api/habits/') and self.path.endswith('/complete'):
            habit_id = self.path.split('/')[3]
            self.complete_habit(habit_id, request_data)
        elif self.path == '/api/journal':
            self.save_journal_entry(request_data)
        else:
            self.send_error_json(404, "Endpoint not found")

    def save_morning_checkin(self, data: dict):
        """Save morning check-in data. POST /api/checkin/morning"""
        try:
            # Validate required fields
            if not isinstance(data, dict):
                self.send_error_json(400, "Request body must be JSON object")
                return

            # Optional fields with defaults
            today = datetime.now().strftime("%Y-%m-%d")

            # Get or create today's log
            log = dm.get_or_create_daily_log(today)

            # Update with new check-in data (whitelist fields)
            am_checkin = {
                "timestamp": datetime.now().isoformat(),
                "sleep_hours": self._validate_number(data.get("sleep_hours"), 0, 16),
                "energy_level": self._validate_number(data.get("energy_level"), 1, 10),
                "top_3_priorities": self._validate_list(data.get("top_3_priorities", []), str, 3),
                "win_definition": str(data.get("win_definition", ""))[:500]  # Max 500 chars
            }

            log["am_checkin"] = am_checkin

            # Save and respond
            if dm.save_daily_log(log, today):
                self.send_json_response(200, {
                    "status": "success",
                    "message": "Morning check-in saved",
                    "date": today,
                    "data": am_checkin
                })
            else:
                self.send_error_json(500, "Failed to save morning check-in")
        except Exception as e:
            self.send_error_json(500, f"Error saving morning check-in: {str(e)}")

    def save_evening_reflection(self, data: dict):
        """Save evening reflection data. POST /api/checkin/evening"""
        try:
            if not isinstance(data, dict):
                self.send_error_json(400, "Request body must be JSON object")
                return

            today = datetime.now().strftime("%Y-%m-%d")
            log = dm.get_or_create_daily_log(today)

            # Update with reflection data (whitelist fields)
            pm_reflection = {
                "timestamp": datetime.now().isoformat(),
                "wins": self._validate_list(data.get("wins", []), str, 5),
                "challenges": self._validate_list(data.get("challenges", []), str, 5),
                "deep_work_hours": self._validate_number(data.get("deep_work_hours"), 0, 24),
                "day_score": self._validate_number(data.get("day_score"), 1, 10),
                "lessons": str(data.get("lessons", ""))[:1000]  # Max 1000 chars
            }

            log["pm_reflection"] = pm_reflection

            # Save and respond
            if dm.save_daily_log(log, today):
                self.send_json_response(200, {
                    "status": "success",
                    "message": "Evening reflection saved",
                    "date": today,
                    "data": pm_reflection
                })
            else:
                self.send_error_json(500, "Failed to save evening reflection")
        except Exception as e:
            self.send_error_json(500, f"Error saving evening reflection: {str(e)}")

    def complete_habit(self, habit_id: str, data: dict):
        """Mark habit complete for a date. POST /api/habits/{id}/complete"""
        try:
            # Validate habit_id (alphanumeric + underscore only)
            if not self._is_valid_id(habit_id):
                self.send_error_json(400, "Invalid habit ID format")
                return

            # Get optional date from request, default to today
            date = data.get("date") if isinstance(data, dict) else None
            if date and not self._is_valid_date(date):
                self.send_error_json(400, "Invalid date format (use YYYY-MM-DD)")
                return

            # Record completion
            if dm.record_habit_completion(habit_id, date):
                today = date or datetime.now().strftime("%Y-%m-%d")
                self.send_json_response(200, {
                    "status": "success",
                    "message": f"Habit '{habit_id}' marked complete",
                    "habit_id": habit_id,
                    "date": today
                })
            else:
                self.send_error_json(500, "Failed to record habit completion")
        except Exception as e:
            self.send_error_json(500, f"Error completing habit: {str(e)}")

    def save_journal_entry(self, data: dict):
        """Save journal entry. POST /api/journal"""
        try:
            if not isinstance(data, dict):
                self.send_error_json(400, "Request body must be JSON object")
                return

            content = str(data.get("content", "")).strip()
            if not content:
                self.send_error_json(400, "Journal content cannot be empty")
                return

            if len(content) > 10000:  # Max 10KB per entry
                self.send_error_json(400, "Journal entry too long (max 10000 chars)")
                return

            today = datetime.now().strftime("%Y-%m-%d")
            log = dm.get_or_create_daily_log(today)

            # Append to notes (or create journal array if preferred)
            journal_entry = {
                "timestamp": datetime.now().isoformat(),
                "content": content,
                "mood": str(data.get("mood", ""))[:50],
                "tags": self._validate_list(data.get("tags", []), str, 10)
            }

            if "journal_entries" not in log:
                log["journal_entries"] = []

            log["journal_entries"].append(journal_entry)

            # Keep only last 100 entries per day
            if len(log["journal_entries"]) > 100:
                log["journal_entries"] = log["journal_entries"][-100:]

            # Save and respond
            if dm.save_daily_log(log, today):
                self.send_json_response(200, {
                    "status": "success",
                    "message": "Journal entry saved",
                    "date": today,
                    "entry_id": len(log["journal_entries"]) - 1
                })
            else:
                self.send_error_json(500, "Failed to save journal entry")
        except Exception as e:
            self.send_error_json(500, f"Error saving journal: {str(e)}")

    def serve_data_file(self):
        """Serve JSON files from data directory with security checks."""
        try:
            # Extract filename and sanitize (prevent path traversal)
            filename = self.path.split('/data/')[-1]

            # Security: only allow safe filenames
            if not self._is_safe_filename(filename):
                self.send_error_json(403, "Access denied")
                return

            filepath = os.path.join(BASE_PATH, 'data', filename)

            # Security: verify file is in data directory
            real_path = os.path.realpath(filepath)
            real_base = os.path.realpath(os.path.join(BASE_PATH, 'data'))

            if not real_path.startswith(real_base):
                self.send_error_json(403, "Access denied")
                return

            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    # Generate ETag for caching
                    etag = self._generate_etag(json.dumps(data))

                    # Check If-None-Match header
                    if self.headers.get('If-None-Match') == etag:
                        self.send_response(304)  # Not Modified
                        self.end_headers()
                        return

                    self.send_json_response(200, data, etag=etag)
                except Exception as e:
                    self.send_error_json(500, f"Error reading file: {str(e)}")
            else:
                self.send_error_json(404, "File not found")
        except Exception as e:
            self.send_error_json(500, f"Error: {str(e)}")

    def send_planning_data(self):
        """Send all planning data (vision, OKRs, weekly plans)."""
        planning = {}

        for filename in ['vision.json', 'quarterly_okrs.json', 'weekly_plans.json']:
            if not self._is_safe_filename(filename):
                continue

            filepath = os.path.join(BASE_PATH, 'data', filename)
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        key = filename.replace('.json', '').replace('_', '')
                        planning[key] = json.load(f)
                except Exception:
                    pass

        self.send_json_response(200, planning)

    def send_json_response(self, status_code: int, data: dict, etag: str = None):
        """Send JSON response with optional compression and caching headers."""
        json_data = json.dumps(data)

        # Apply gzip compression for mobile efficiency
        accept_encoding = self.headers.get('Accept-Encoding', '')
        use_gzip = 'gzip' in accept_encoding and len(json_data) > 500  # Only compress if >500 bytes

        if use_gzip:
            compressed = gzip.compress(json_data.encode())
            self.send_response(status_code)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Encoding', 'gzip')
            self.send_header('Vary', 'Accept-Encoding')
            if etag:
                self.send_header('ETag', etag)
                self.send_header('Cache-Control', 'public, max-age=3600')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Length', len(compressed))
            self.end_headers()
            self.wfile.write(compressed)
        else:
            self.send_response(status_code)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            if etag:
                self.send_header('ETag', etag)
                self.send_header('Cache-Control', 'public, max-age=3600')
            self.send_header('Content-Length', len(json_data))
            self.end_headers()
            self.wfile.write(json_data.encode())

    def send_error_json(self, status_code: int, message: str):
        """Send error response as JSON."""
        error_data = {
            "status": "error",
            "code": status_code,
            "message": message
        }
        self.send_json_response(status_code, error_data)

    def send_json(self, data):
        """Legacy method for backwards compatibility."""
        self.send_json_response(200, data)

    def send_api_data(self):
        """Send all dashboard data."""
        profile = dm.get_user_profile() or {}
        habits_data = dm.get_habits()
        stats = dm.get_stats()
        goals = dm.get_goals()

        # Get today's log
        today = datetime.now().strftime("%Y-%m-%d")
        today_log = dm.get_daily_log(today) or {}

        # Build habits list with completion status
        habits_list = []
        today_completions = habits_data.get("completions", {}).get(today, [])

        for habit in habits_data.get("habits", []):
            habits_list.append({
                "id": habit["id"],
                "name": habit["name"],
                "module": habit.get("module", "productivity"),
                "streak": habit.get("current_streak", 0),
                "completed": habit["id"] in today_completions
            })

        data = {
            "profile": {
                "name": profile.get("name", "Boss"),
                "coaching_style": profile.get("coaching_style", "direct"),
                "focus_modules": profile.get("focus_modules", [])
            },
            "habits": habits_list,
            "modules": profile.get("module_levels", {}),
            "goals": goals.get("quarterly_goals", {}),
            "stats": {
                "dayStreak": stats.get("total_days_logged", 0),
                "deepWorkHours": stats.get("total_deep_work_hours", 0),
                "habitCompletion": round(stats.get("habit_completion_rate", 0)),
                "avgScore": round(stats.get("avg_day_score", 0), 1)
            },
            "todayLog": {
                "hasAM": bool(today_log.get("am_checkin")),
                "hasPM": bool(today_log.get("pm_reflection")),
                "priorities": today_log.get("am_checkin", {}).get("top_3_priorities", []),
                "energy": today_log.get("am_checkin", {}).get("energy_level", 0)
            }
        }

        self.send_json_response(200, data)

    def send_wisdom(self):
        """Send wisdom data (cached by date)."""
        global _wisdom_cache, _wisdom_cache_date

        today = datetime.now().strftime("%Y-%m-%d")

        # Return cached wisdom if available for today
        if _wisdom_cache_date == today and _wisdom_cache:
            # Generate ETag for caching
            etag = self._generate_etag(json.dumps(_wisdom_cache))

            # Check If-None-Match header
            if self.headers.get('If-None-Match') == etag:
                self.send_response(304)  # Not Modified
                self.end_headers()
                return

            self.send_json_response(200, _wisdom_cache, etag=etag)
            return

        # Generate new wisdom and cache it
        wisdom = WisdomEngine(dm)
        daily = wisdom.get_daily_wisdom()
        _wisdom_cache = daily
        _wisdom_cache_date = today

        etag = self._generate_etag(json.dumps(daily))
        self.send_json_response(200, daily, etag=etag)

    def send_habits(self):
        """Get habits data."""
        habits_data = dm.get_habits()
        today = datetime.now().strftime("%Y-%m-%d")

        # Transform to mobile-friendly format
        response = {
            "habits": habits_data.get("habits", []),
            "today_completions": habits_data.get("completions", {}).get(today, [])
        }

        self.send_json_response(200, response)

    # ==================== Utility Methods ====================

    def _validate_number(self, value, min_val: int, max_val: int) -> float:
        """Validate and constrain numeric input."""
        try:
            num = float(value) if value is not None else 0
            return max(min_val, min(max_val, num))
        except (TypeError, ValueError):
            return 0

    def _validate_list(self, value, item_type=str, max_items: int = 10) -> list:
        """Validate and constrain list input."""
        if not isinstance(value, list):
            return []

        result = []
        for item in value[:max_items]:  # Limit items
            try:
                if item_type == str:
                    result.append(str(item)[:500])  # Max 500 chars per item
                else:
                    result.append(item_type(item))
            except (TypeError, ValueError):
                continue

        return result

    def _is_valid_id(self, habit_id: str) -> bool:
        """Validate habit ID format (alphanumeric + underscore)."""
        if not habit_id or len(habit_id) > 100:
            return False
        return all(c.isalnum() or c == '_' for c in habit_id)

    def _is_valid_date(self, date_str: str) -> bool:
        """Validate date format (YYYY-MM-DD)."""
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def _is_safe_filename(self, filename: str) -> bool:
        """Prevent path traversal attacks."""
        if not filename or len(filename) > 255:
            return False

        # Only allow alphanumeric, underscore, hyphen, dot
        if not all(c.isalnum() or c in '_-.' for c in filename):
            return False

        # Prevent directory traversal
        if '..' in filename or '/' in filename or '\\' in filename:
            return False

        # Only allow .json files
        if not filename.endswith('.json'):
            return False

        return True

    def _generate_etag(self, content: str) -> str:
        """Generate ETag hash for content."""
        return f'"{hashlib.md5(content.encode()).hexdigest()}"'


def run_server(port=8080):
    """Run the dashboard server."""
    os.chdir(BASE_PATH)

    server = HTTPServer(('localhost', port), DashboardHandler)
    url = f'http://localhost:{port}'

    print("\n================================================================")
    print("           SELF-MASTERY OS DASHBOARD")
    print("================================================================")
    print(f"  Server running at: {url}")
    print("")
    print("  Press Ctrl+C to stop the server")
    print("================================================================\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.shutdown()


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run_server(port)
