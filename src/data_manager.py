"""
Self-Mastery OS - Data Management
Handles all data persistence using JSON files.
"""
import os
import json
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from pathlib import Path

class DataManager:
    """Manages all data storage and retrieval for Self-Mastery OS."""

    def __init__(self, base_path: str = None):
        """Initialize data manager with base path."""
        if base_path is None:
            # Default to parent directory of src
            base_path = Path(__file__).parent.parent

        self.base_path = Path(base_path)
        self.data_path = self.base_path / "data"
        self.logs_path = self.data_path / "logs"
        self.reviews_path = self.data_path / "reviews"
        self.kb_path = self.base_path / "knowledge_base"

        # Ensure directories exist
        self._ensure_directories()

    def _ensure_directories(self):
        """Create necessary directories if they don't exist."""
        for path in [self.data_path, self.logs_path, self.reviews_path]:
            path.mkdir(parents=True, exist_ok=True)

    def _read_json(self, filepath: Path) -> Optional[Dict]:
        """Read JSON file and return data."""
        try:
            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error reading {filepath}: {e}")
        return None

    def _write_json(self, filepath: Path, data: Dict) -> bool:
        """Write data to JSON file."""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Error writing {filepath}: {e}")
            return False

    # ==================== User Profile ====================

    def get_user_profile(self) -> Optional[Dict]:
        """Get user profile data."""
        return self._read_json(self.data_path / "user_profile.json")

    def save_user_profile(self, profile: Dict) -> bool:
        """Save user profile data."""
        profile["updated_at"] = datetime.now().isoformat()
        return self._write_json(self.data_path / "user_profile.json", profile)

    def user_exists(self) -> bool:
        """Check if user profile exists."""
        return (self.data_path / "user_profile.json").exists()

    # ==================== Daily Logs ====================

    def get_daily_log(self, date: str = None) -> Optional[Dict]:
        """Get daily log for specific date (YYYY-MM-DD format)."""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        return self._read_json(self.logs_path / f"{date}.json")

    def save_daily_log(self, log: Dict, date: str = None) -> bool:
        """Save daily log for specific date."""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        log["date"] = date
        log["updated_at"] = datetime.now().isoformat()
        return self._write_json(self.logs_path / f"{date}.json", log)

    def get_or_create_daily_log(self, date: str = None) -> Dict:
        """Get existing daily log or create new one."""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        existing = self.get_daily_log(date)
        if existing:
            return existing

        # Create new log template
        return {
            "date": date,
            "created_at": datetime.now().isoformat(),
            "am_checkin": None,
            "planned_actions": [],
            "completed_actions": [],
            "pm_reflection": None,
            "metrics": {
                "deep_work_hours": 0,
                "workouts": 0,
                "sales_calls": 0,
                "social_interactions": 0,
                "steps": 0,
                "water_liters": 0
            },
            "habits": {},
            "notes": ""
        }

    def get_logs_for_range(self, start_date: str, end_date: str) -> List[Dict]:
        """Get all logs within date range."""
        logs = []
        current = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")

        while current <= end:
            date_str = current.strftime("%Y-%m-%d")
            log = self.get_daily_log(date_str)
            if log:
                logs.append(log)
            current += timedelta(days=1)

        return logs

    def get_recent_logs(self, days: int = 7) -> List[Dict]:
        """Get logs for the past N days."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days-1)
        return self.get_logs_for_range(
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d")
        )

    # ==================== Weekly Reviews ====================

    def get_weekly_review(self, week: str = None) -> Optional[Dict]:
        """Get weekly review (YYYY-WW format)."""
        if week is None:
            week = datetime.now().strftime("%Y-W%W")
        return self._read_json(self.reviews_path / f"week-{week}.json")

    def save_weekly_review(self, review: Dict, week: str = None) -> bool:
        """Save weekly review."""
        if week is None:
            week = datetime.now().strftime("%Y-W%W")
        review["week"] = week
        review["updated_at"] = datetime.now().isoformat()
        return self._write_json(self.reviews_path / f"week-{week}.json", review)

    # ==================== Habits ====================

    def get_habits(self) -> Dict:
        """Get habits data."""
        data = self._read_json(self.data_path / "habits.json")
        if data is None:
            data = {"habits": [], "completions": {}}
        return data

    def save_habits(self, habits: Dict) -> bool:
        """Save habits data."""
        return self._write_json(self.data_path / "habits.json", habits)

    def add_habit(self, habit: Dict) -> bool:
        """Add a new habit."""
        habits_data = self.get_habits()

        # Generate unique ID
        existing_ids = [h.get("id", "") for h in habits_data["habits"]]
        base_id = habit.get("id", habit["name"].lower().replace(" ", "_"))
        habit_id = base_id
        counter = 1
        while habit_id in existing_ids:
            habit_id = f"{base_id}_{counter}"
            counter += 1

        habit["id"] = habit_id
        habit["created_at"] = datetime.now().isoformat()
        habit["current_streak"] = 0
        habit["best_streak"] = 0
        habit["total_completions"] = 0

        habits_data["habits"].append(habit)
        return self.save_habits(habits_data)

    def record_habit_completion(self, habit_id: str, date: str = None) -> bool:
        """Record habit completion for a date."""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        habits_data = self.get_habits()

        # Initialize completions dict if needed
        if "completions" not in habits_data:
            habits_data["completions"] = {}
        if date not in habits_data["completions"]:
            habits_data["completions"][date] = []

        # Add completion if not already recorded
        if habit_id not in habits_data["completions"][date]:
            habits_data["completions"][date].append(habit_id)

            # Update streak for the habit
            for habit in habits_data["habits"]:
                if habit["id"] == habit_id:
                    habit["total_completions"] = habit.get("total_completions", 0) + 1
                    # Recalculate streak
                    completion_dates = [
                        d for d, ids in habits_data["completions"].items()
                        if habit_id in ids
                    ]
                    habit["current_streak"] = self._calculate_streak(completion_dates)
                    habit["best_streak"] = max(
                        habit.get("best_streak", 0),
                        habit["current_streak"]
                    )
                    break

        return self.save_habits(habits_data)

    def _calculate_streak(self, dates: List[str]) -> int:
        """Calculate current streak from dates."""
        if not dates:
            return 0

        dates = sorted([datetime.strptime(d, "%Y-%m-%d") for d in dates], reverse=True)
        today = datetime.now().date()

        streak = 0
        expected = today

        for date in dates:
            if date.date() == expected or date.date() == expected - timedelta(days=1):
                if date.date() == expected - timedelta(days=1):
                    expected = date.date()
                streak += 1
                expected -= timedelta(days=1)
            else:
                break

        return streak

    # ==================== Goals ====================

    def get_goals(self) -> Dict:
        """Get goals data."""
        data = self._read_json(self.data_path / "goals.json")
        if data is None:
            data = {
                "lifetime_vision": "",
                "yearly_goals": [],
                "quarterly_goals": [],
                "monthly_goals": [],
                "weekly_goals": []
            }
        return data

    def save_goals(self, goals: Dict) -> bool:
        """Save goals data."""
        return self._write_json(self.data_path / "goals.json", goals)

    # ==================== Statistics ====================

    def get_stats(self) -> Dict:
        """Get aggregated statistics."""
        logs = self.get_recent_logs(30)
        habits_data = self.get_habits()

        stats = {
            "total_days_logged": len(logs),
            "am_checkins": sum(1 for l in logs if l.get("am_checkin")),
            "pm_reflections": sum(1 for l in logs if l.get("pm_reflection")),
            "avg_sleep": 0,
            "avg_energy": 0,
            "avg_day_score": 0,
            "total_deep_work_hours": 0,
            "total_workouts": 0,
            "habit_completion_rate": 0
        }

        # Calculate averages
        sleep_vals = []
        energy_vals = []
        score_vals = []

        for log in logs:
            if log.get("am_checkin"):
                if log["am_checkin"].get("sleep_hours"):
                    sleep_vals.append(log["am_checkin"]["sleep_hours"])
                if log["am_checkin"].get("energy_level"):
                    energy_vals.append(log["am_checkin"]["energy_level"])

            if log.get("pm_reflection") and log["pm_reflection"].get("day_score"):
                score_vals.append(log["pm_reflection"]["day_score"])

            if log.get("metrics"):
                stats["total_deep_work_hours"] += log["metrics"].get("deep_work_hours", 0)
                stats["total_workouts"] += log["metrics"].get("workouts", 0)

        if sleep_vals:
            stats["avg_sleep"] = sum(sleep_vals) / len(sleep_vals)
        if energy_vals:
            stats["avg_energy"] = sum(energy_vals) / len(energy_vals)
        if score_vals:
            stats["avg_day_score"] = sum(score_vals) / len(score_vals)

        # Calculate habit completion rate
        if habits_data.get("habits") and habits_data.get("completions"):
            total_possible = len(habits_data["habits"]) * len(logs)
            total_completed = sum(
                len(ids) for ids in habits_data["completions"].values()
            )
            if total_possible > 0:
                stats["habit_completion_rate"] = total_completed / total_possible * 100

        return stats

    # ==================== Knowledge Base ====================

    def get_knowledge_base_topics(self) -> List[str]:
        """Get list of knowledge base files."""
        if not self.kb_path.exists():
            return []
        return [f.stem for f in self.kb_path.glob("*.md")]

    def get_knowledge_base_content(self, topic: str) -> Optional[str]:
        """Get knowledge base content for topic."""
        filepath = self.kb_path / f"{topic}.md"
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        return None
