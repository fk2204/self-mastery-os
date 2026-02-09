#!/usr/bin/env python3
"""
Self-Mastery OS - Dashboard Server
Serves the web dashboard with live data from your profile.
"""
import os
import sys
import json
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from datetime import datetime

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

    def serve_data_file(self):
        """Serve JSON files from the data directory."""
        filename = self.path.split('/data/')[-1]
        filepath = os.path.join(BASE_PATH, 'data', filename)

        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.send_json(data)
            except Exception as e:
                self.send_error(500, f"Error reading file: {str(e)}")
        else:
            self.send_error(404, "File not found")

    def send_planning_data(self):
        """Send all planning data (vision, OKRs, weekly plans)."""
        planning = {}

        for filename in ['vision.json', 'quarterly_okrs.json', 'weekly_plans.json']:
            filepath = os.path.join(BASE_PATH, 'data', filename)
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        key = filename.replace('.json', '').replace('_', '')
                        planning[key] = json.load(f)
                except Exception:
                    pass

        self.send_json(planning)

    def send_json(self, data):
        """Send JSON response."""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

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

        self.send_json(data)

    def send_wisdom(self):
        """Send wisdom data (cached by date)."""
        global _wisdom_cache, _wisdom_cache_date

        today = datetime.now().strftime("%Y-%m-%d")

        # Return cached wisdom if available for today
        if _wisdom_cache_date == today and _wisdom_cache:
            self.send_json(_wisdom_cache)
            return

        # Generate new wisdom and cache it
        wisdom = WisdomEngine(dm)
        daily = wisdom.get_daily_wisdom()
        _wisdom_cache = daily
        _wisdom_cache_date = today
        self.send_json(daily)

    def send_habits(self):
        """Toggle habit completion."""
        # This would handle POST in a more complete implementation
        self.send_json({"status": "ok"})


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
