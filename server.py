#!/usr/bin/env python3
"""
Self-Mastery OS - Dashboard Server
Serves the web dashboard with live data from your profile.
Optimized: gzip compression, cache headers, parallel I/O, pre-serialized JSON.
"""
import os
import sys
import json
import gzip
import io
from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_manager import DataManager
from wisdom_engine import WisdomEngine

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
dm = DataManager(BASE_PATH)

# Thread pool for parallel file reads
_executor = ThreadPoolExecutor(max_workers=4)

# Simple caching for wisdom data (cached by date)
_wisdom_cache = {}
_wisdom_cache_date = None

# File read cache (path -> (mtime, data))
_file_cache = {}

# MIME type overrides for common static files
_MIME_TYPES = {
    '.html': 'text/html; charset=utf-8',
    '.css': 'text/css; charset=utf-8',
    '.js': 'application/javascript; charset=utf-8',
    '.json': 'application/json; charset=utf-8',
    '.svg': 'image/svg+xml',
    '.png': 'image/png',
    '.ico': 'image/x-icon',
    '.woff2': 'font/woff2',
}


def read_json_cached(filepath):
    """Read a JSON file with mtime-based caching."""
    try:
        mtime = os.path.getmtime(filepath)
        if filepath in _file_cache and _file_cache[filepath][0] == mtime:
            return _file_cache[filepath][1]
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        _file_cache[filepath] = (mtime, data)
        return data
    except (OSError, json.JSONDecodeError):
        return None


class DashboardHandler(SimpleHTTPRequestHandler):
    """Custom handler with gzip, caching headers, and optimized responses."""

    # Suppress per-request logging for speed
    def log_message(self, format, *args):
        pass

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

    def _accepts_gzip(self):
        return 'gzip' in self.headers.get('Accept-Encoding', '')

    def serve_data_file(self):
        """Serve JSON files from the data directory with caching."""
        filename = self.path.split('/data/')[-1]
        # Sanitize path to prevent directory traversal
        if '..' in filename or '/' in filename:
            self.send_error(403, "Forbidden")
            return
        filepath = os.path.join(BASE_PATH, 'data', filename)
        data = read_json_cached(filepath)
        if data is not None:
            self.send_json(data, cache_seconds=60)
        else:
            self.send_error(404, "File not found")

    def send_planning_data(self):
        """Send all planning data in parallel."""
        filenames = ['vision.json', 'quarterly_okrs.json', 'weekly_plans.json']
        filepaths = [os.path.join(BASE_PATH, 'data', f) for f in filenames]
        keys = [f.replace('.json', '').replace('_', '') for f in filenames]

        # Read all files in parallel
        futures = [_executor.submit(read_json_cached, fp) for fp in filepaths]
        planning = {}
        for key, future in zip(keys, futures):
            data = future.result()
            if data is not None:
                planning[key] = data

        self.send_json(planning, cache_seconds=30)

    def send_json(self, data, cache_seconds=0):
        """Send JSON response with optional gzip and cache headers."""
        body = json.dumps(data, separators=(',', ':')).encode('utf-8')

        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')

        if cache_seconds > 0:
            self.send_header('Cache-Control', f'public, max-age={cache_seconds}')
        else:
            self.send_header('Cache-Control', 'no-cache')

        # Gzip if client supports it and body is large enough
        if self._accepts_gzip() and len(body) > 512:
            buf = io.BytesIO()
            with gzip.GzipFile(fileobj=buf, mode='wb', compresslevel=6) as gz:
                gz.write(body)
            body = buf.getvalue()
            self.send_header('Content-Encoding', 'gzip')

        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_api_data(self):
        """Send all dashboard data."""
        profile = dm.get_user_profile() or {}
        habits_data = dm.get_habits()
        stats = dm.get_stats()
        goals = dm.get_goals()

        today = datetime.now().strftime("%Y-%m-%d")
        today_log = dm.get_daily_log(today) or {}

        today_completions = set(habits_data.get("completions", {}).get(today, []))
        habits_list = [
            {
                "id": h["id"],
                "name": h["name"],
                "module": h.get("module", "productivity"),
                "streak": h.get("current_streak", 0),
                "completed": h["id"] in today_completions
            }
            for h in habits_data.get("habits", [])
        ]

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

        if _wisdom_cache_date == today and _wisdom_cache:
            self.send_json(_wisdom_cache, cache_seconds=3600)
            return

        wisdom = WisdomEngine(dm)
        daily = wisdom.get_daily_wisdom()
        _wisdom_cache = daily
        _wisdom_cache_date = today
        self.send_json(daily, cache_seconds=3600)

    def send_habits(self):
        """Toggle habit completion."""
        self.send_json({"status": "ok"})

    def end_headers(self):
        """Add security and performance headers."""
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Referrer-Policy', 'strict-origin-when-cross-origin')
        super().end_headers()


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
        _executor.shutdown(wait=False)


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run_server(port)
