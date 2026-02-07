"""
Comprehensive test suite for data_manager.py
Target: 100% code coverage for src/data_manager.py
"""
import os
import json
import pytest
from pathlib import Path
from datetime import datetime, timedelta
from src.data_manager import DataManager


# ==================== Initialization Tests (4) ====================

def test_init_with_custom_path(temp_dir):
  """Test initialization with custom base path."""
  dm = DataManager(base_path=temp_dir)
  assert dm.base_path == Path(temp_dir)
  assert dm.data_path == Path(temp_dir) / "data"
  assert dm.logs_path == Path(temp_dir) / "data" / "logs"
  assert dm.reviews_path == Path(temp_dir) / "data" / "reviews"
  assert dm.kb_path == Path(temp_dir) / "knowledge_base"


def test_init_with_default_path():
  """Test initialization with default path (None)."""
  dm = DataManager()
  expected_base = Path(__file__).parent.parent.parent / "src"
  expected_base = expected_base.parent
  assert dm.base_path == expected_base


def test_init_creates_directories(temp_dir):
  """Test that initialization creates necessary directories."""
  dm = DataManager(base_path=temp_dir)
  assert dm.data_path.exists()
  assert dm.logs_path.exists()
  assert dm.reviews_path.exists()


def test_ensure_directories_idempotent(data_manager):
  """Test that _ensure_directories can be called multiple times safely."""
  data_manager._ensure_directories()
  data_manager._ensure_directories()
  assert data_manager.data_path.exists()
  assert data_manager.logs_path.exists()
  assert data_manager.reviews_path.exists()


# ==================== JSON I/O Tests (7) ====================

def test_read_json_existing_file(data_manager):
  """Test reading existing JSON file."""
  test_data = {"key": "value", "number": 42}
  test_file = data_manager.data_path / "test.json"
  with open(test_file, "w", encoding="utf-8") as f:
    json.dump(test_data, f)
  result = data_manager._read_json(test_file)
  assert result == test_data


def test_read_json_nonexistent_file(data_manager):
  """Test reading non-existent file returns None."""
  result = data_manager._read_json(data_manager.data_path / "nonexistent.json")
  assert result is None


def test_read_json_invalid_json(data_manager, capsys):
  """Test reading invalid JSON file returns None and prints error."""
  test_file = data_manager.data_path / "invalid.json"
  with open(test_file, "w", encoding="utf-8") as f:
    f.write("{ invalid json }")
  result = data_manager._read_json(test_file)
  captured = capsys.readouterr()
  assert result is None
  assert "Error reading" in captured.out


def test_read_json_io_error(data_manager, capsys, monkeypatch):
  """Test reading file with IO error returns None and prints error."""
  test_file = data_manager.data_path / "test.json"
  test_file.touch()

  def mock_open(*args, **kwargs):
    raise IOError("Permission denied")

  monkeypatch.setattr("builtins.open", mock_open)
  result = data_manager._read_json(test_file)
  captured = capsys.readouterr()
  assert result is None
  assert "Error reading" in captured.out


def test_write_json_success(data_manager):
  """Test writing JSON file successfully."""
  test_data = {"key": "value", "list": [1, 2, 3]}
  test_file = data_manager.data_path / "output.json"
  result = data_manager._write_json(test_file, test_data)
  assert result is True
  assert test_file.exists()
  with open(test_file, "r", encoding="utf-8") as f:
    saved_data = json.load(f)
  assert saved_data == test_data


def test_write_json_with_unicode(data_manager):
  """Test writing JSON with unicode characters."""
  test_data = {"message": "Hello 世界", "emoji": "🚀"}
  test_file = data_manager.data_path / "unicode.json"
  result = data_manager._write_json(test_file, test_data)
  assert result is True
  with open(test_file, "r", encoding="utf-8") as f:
    saved_data = json.load(f)
  assert saved_data == test_data


def test_write_json_io_error(data_manager, capsys, monkeypatch):
  """Test writing file with IO error returns False and prints error."""
  test_data = {"key": "value"}
  test_file = data_manager.data_path / "output.json"

  original_open = open
  def mock_open(filepath, mode, **kwargs):
    if "output.json" in str(filepath) and "w" in mode:
      raise IOError("Disk full")
    return original_open(filepath, mode, **kwargs)

  monkeypatch.setattr("builtins.open", mock_open)
  result = data_manager._write_json(test_file, test_data)
  captured = capsys.readouterr()
  assert result is False
  assert "Error writing" in captured.out


# ==================== User Profile Tests (6) ====================

def test_get_user_profile_existing(data_manager, sample_user_profile):
  """Test getting existing user profile."""
  profile_file = data_manager.data_path / "user_profile.json"
  with open(profile_file, "w", encoding="utf-8") as f:
    json.dump(sample_user_profile, f)
  result = data_manager.get_user_profile()
  assert result == sample_user_profile


def test_get_user_profile_nonexistent(data_manager):
  """Test getting non-existent user profile returns None."""
  result = data_manager.get_user_profile()
  assert result is None


def test_save_user_profile_new(data_manager, sample_user_profile):
  """Test saving new user profile."""
  result = data_manager.save_user_profile(sample_user_profile)
  assert result is True
  saved = data_manager.get_user_profile()
  assert saved["name"] == sample_user_profile["name"]
  assert "updated_at" in saved


def test_save_user_profile_updates_timestamp(data_manager, sample_user_profile):
  """Test that save_user_profile adds updated_at timestamp."""
  data_manager.save_user_profile(sample_user_profile)
  saved = data_manager.get_user_profile()
  assert "updated_at" in saved
  datetime.fromisoformat(saved["updated_at"])


def test_user_exists_true(data_manager, sample_user_profile):
  """Test user_exists returns True when profile exists."""
  data_manager.save_user_profile(sample_user_profile)
  assert data_manager.user_exists() is True


def test_user_exists_false(data_manager):
  """Test user_exists returns False when profile does not exist."""
  assert data_manager.user_exists() is False


# ==================== Daily Log Tests (11) ====================

def test_get_daily_log_existing(data_manager, sample_daily_log):
  """Test getting existing daily log."""
  date = "2024-01-15"
  log_file = data_manager.logs_path / f"{date}.json"
  with open(log_file, "w", encoding="utf-8") as f:
    json.dump(sample_daily_log, f)
  result = data_manager.get_daily_log(date)
  assert result == sample_daily_log


def test_get_daily_log_nonexistent(data_manager):
  """Test getting non-existent daily log returns None."""
  result = data_manager.get_daily_log("2024-01-01")
  assert result is None


def test_get_daily_log_default_date(data_manager, freeze_time, sample_daily_log):
  """Test get_daily_log uses current date when date is None."""
  freeze_time.set_date(datetime(2024, 1, 15, 10, 0, 0))
  log_file = data_manager.logs_path / "2024-01-15.json"
  with open(log_file, "w", encoding="utf-8") as f:
    json.dump(sample_daily_log, f)
  result = data_manager.get_daily_log()
  assert result == sample_daily_log


def test_save_daily_log_new(data_manager, sample_daily_log):
  """Test saving new daily log."""
  date = "2024-01-15"
  result = data_manager.save_daily_log(sample_daily_log, date)
  assert result is True
  saved = data_manager.get_daily_log(date)
  assert saved["date"] == date
  assert "updated_at" in saved


def test_save_daily_log_default_date(data_manager, freeze_time):
  """Test save_daily_log uses current date when date is None."""
  freeze_time.set_date(datetime(2024, 1, 15, 10, 0, 0))
  log_data = {"test": "data"}
  result = data_manager.save_daily_log(log_data)
  assert result is True
  saved = data_manager.get_daily_log("2024-01-15")
  assert saved["date"] == "2024-01-15"


def test_save_daily_log_adds_metadata(data_manager):
  """Test save_daily_log adds date and updated_at."""
  log_data = {"test": "data"}
  date = "2024-01-15"
  data_manager.save_daily_log(log_data, date)
  saved = data_manager.get_daily_log(date)
  assert saved["date"] == date
  assert "updated_at" in saved
  datetime.fromisoformat(saved["updated_at"])


def test_get_or_create_daily_log_existing(data_manager, sample_daily_log):
  """Test get_or_create_daily_log returns existing log."""
  date = "2024-01-15"
  data_manager.save_daily_log(sample_daily_log, date)
  result = data_manager.get_or_create_daily_log(date)
  assert result["date"] == date
  assert result["am_checkin"] == sample_daily_log["am_checkin"]


def test_get_or_create_daily_log_creates_new(data_manager, freeze_time):
  """Test get_or_create_daily_log creates new log with template."""
  freeze_time.set_date(datetime(2024, 1, 15, 10, 0, 0))
  result = data_manager.get_or_create_daily_log("2024-01-15")
  assert result["date"] == "2024-01-15"
  assert result["am_checkin"] is None
  assert result["planned_actions"] == []
  assert result["completed_actions"] == []
  assert result["pm_reflection"] is None
  assert "metrics" in result
  assert result["metrics"]["deep_work_hours"] == 0
  assert result["habits"] == {}
  assert "created_at" in result


def test_get_or_create_daily_log_default_date(data_manager, freeze_time):
  """Test get_or_create_daily_log uses current date when None."""
  freeze_time.set_date(datetime(2024, 1, 15, 10, 0, 0))
  result = data_manager.get_or_create_daily_log()
  assert result["date"] == "2024-01-15"


def test_get_logs_for_range(data_manager):
  """Test getting logs for date range."""
  dates = ["2024-01-10", "2024-01-11", "2024-01-12"]
  for date in dates:
    data_manager.save_daily_log({"test": date}, date)
  result = data_manager.get_logs_for_range("2024-01-10", "2024-01-12")
  assert len(result) == 3
  assert result[0]["test"] == "2024-01-10"
  assert result[2]["test"] == "2024-01-12"


def test_get_recent_logs(data_manager, freeze_time):
  """Test getting recent logs for past N days."""
  freeze_time.set_date(datetime(2024, 1, 15, 10, 0, 0))
  dates = ["2024-01-10", "2024-01-11", "2024-01-12", "2024-01-13", "2024-01-14", "2024-01-15"]
  for date in dates:
    data_manager.save_daily_log({"date": date}, date)
  result = data_manager.get_recent_logs(5)
  assert len(result) == 5
  assert result[0]["date"] == "2024-01-11"
  assert result[4]["date"] == "2024-01-15"


# ==================== Weekly Review Tests (3) ====================

def test_get_weekly_review_existing(data_manager, sample_weekly_review):
  """Test getting existing weekly review."""
  week = "2024-W03"
  review_file = data_manager.reviews_path / f"week-{week}.json"
  with open(review_file, "w", encoding="utf-8") as f:
    json.dump(sample_weekly_review, f)
  result = data_manager.get_weekly_review(week)
  assert result == sample_weekly_review


def test_save_weekly_review(data_manager, sample_weekly_review):
  """Test saving weekly review."""
  week = "2024-W03"
  result = data_manager.save_weekly_review(sample_weekly_review, week)
  assert result is True
  saved = data_manager.get_weekly_review(week)
  assert saved["week"] == week
  assert "updated_at" in saved


def test_weekly_review_default_week(data_manager, freeze_time):
  """Test weekly review uses current week when None."""
  freeze_time.set_date(datetime(2024, 1, 15, 10, 0, 0))
  review_data = {"wins": ["Test win"]}
  data_manager.save_weekly_review(review_data)
  week = freeze_time.frozen_date.strftime("%Y-W%W")
  saved = data_manager.get_weekly_review(week)
  assert saved["week"] == week


# ==================== Habits Tests (15) - CRITICAL ====================

def test_get_habits_existing(data_manager):
  """Test getting existing habits data."""
  habits_data = {
    "habits": [{"id": "morning", "name": "Morning Routine"}],
    "completions": {"2024-01-15": ["morning"]}
  }
  habits_file = data_manager.data_path / "habits.json"
  with open(habits_file, "w", encoding="utf-8") as f:
    json.dump(habits_data, f)
  result = data_manager.get_habits()
  assert result == habits_data


def test_get_habits_nonexistent(data_manager):
  """Test get_habits returns default structure when file does not exist."""
  result = data_manager.get_habits()
  assert result == {"habits": [], "completions": {}}


def test_save_habits(data_manager):
  """Test saving habits data."""
  habits_data = {
    "habits": [{"id": "test", "name": "Test Habit"}],
    "completions": {}
  }
  result = data_manager.save_habits(habits_data)
  assert result is True
  saved = data_manager.get_habits()
  assert saved == habits_data


def test_add_habit_new(data_manager, sample_habit):
  """Test adding new habit."""
  result = data_manager.add_habit(sample_habit)
  assert result is True
  habits = data_manager.get_habits()
  assert len(habits["habits"]) == 1
  added = habits["habits"][0]
  assert added["name"] == sample_habit["name"]
  assert "id" in added
  assert "created_at" in added
  assert added["current_streak"] == 0
  assert added["best_streak"] == 0
  assert added["total_completions"] == 0


def test_add_habit_generates_id(data_manager):
  """Test add_habit generates ID from name if not provided."""
  habit = {"name": "Deep Work Block"}
  data_manager.add_habit(habit)
  habits = data_manager.get_habits()
  assert habits["habits"][0]["id"] == "deep_work_block"


def test_add_habit_uses_provided_id(data_manager):
  """Test add_habit uses provided ID if available."""
  habit = {"id": "custom_id", "name": "Custom Habit"}
  data_manager.add_habit(habit)
  habits = data_manager.get_habits()
  assert habits["habits"][0]["id"] == "custom_id"


def test_add_habit_duplicate_id_increments(data_manager):
  """Test add_habit increments ID when duplicate exists."""
  habit1 = {"id": "morning", "name": "Morning Routine"}
  habit2 = {"id": "morning", "name": "Morning Workout"}
  habit3 = {"id": "morning", "name": "Morning Meditation"}
  data_manager.add_habit(habit1)
  data_manager.add_habit(habit2)
  data_manager.add_habit(habit3)
  habits = data_manager.get_habits()
  ids = [h["id"] for h in habits["habits"]]
  assert "morning" in ids
  assert "morning_1" in ids
  assert "morning_2" in ids


def test_record_habit_completion_new(data_manager, freeze_time):
  """Test recording habit completion for first time."""
  freeze_time.set_date(datetime(2024, 1, 15, 10, 0, 0))
  habit = {"id": "morning", "name": "Morning Routine"}
  data_manager.add_habit(habit)
  result = data_manager.record_habit_completion("morning", "2024-01-15")
  assert result is True
  habits = data_manager.get_habits()
  assert "2024-01-15" in habits["completions"]
  assert "morning" in habits["completions"]["2024-01-15"]


def test_record_habit_completion_updates_streak(data_manager, freeze_time):
  """Test recording completion updates streak counters."""
  freeze_time.set_date(datetime(2024, 1, 15, 10, 0, 0))
  habit = {"id": "morning", "name": "Morning Routine"}
  data_manager.add_habit(habit)
  data_manager.record_habit_completion("morning", "2024-01-15")
  habits = data_manager.get_habits()
  habit_data = habits["habits"][0]
  assert habit_data["total_completions"] == 1
  assert habit_data["current_streak"] == 1
  assert habit_data["best_streak"] == 1


def test_record_habit_completion_default_date(data_manager, freeze_time):
  """Test record_habit_completion uses current date when None."""
  freeze_time.set_date(datetime(2024, 1, 15, 10, 0, 0))
  habit = {"id": "morning", "name": "Morning Routine"}
  data_manager.add_habit(habit)
  data_manager.record_habit_completion("morning")
  habits = data_manager.get_habits()
  assert "2024-01-15" in habits["completions"]


def test_record_habit_completion_duplicate_ignored(data_manager):
  """Test recording same habit twice on same date is ignored."""
  habit = {"id": "morning", "name": "Morning Routine"}
  data_manager.add_habit(habit)
  data_manager.record_habit_completion("morning", "2024-01-15")
  data_manager.record_habit_completion("morning", "2024-01-15")
  habits = data_manager.get_habits()
  assert habits["completions"]["2024-01-15"].count("morning") == 1
  assert habits["habits"][0]["total_completions"] == 1


def test_record_habit_completion_initializes_completions(data_manager):
  """Test record_habit_completion initializes completions dict if missing."""
  habit = {"id": "morning", "name": "Morning Routine"}
  data_manager.add_habit(habit)
  habits = data_manager.get_habits()
  del habits["completions"]
  data_manager.save_habits(habits)
  data_manager.record_habit_completion("morning", "2024-01-15")
  habits = data_manager.get_habits()
  assert "completions" in habits
  assert "2024-01-15" in habits["completions"]


def test_calculate_streak_empty(data_manager):
  """Test _calculate_streak with no dates returns 0."""
  result = data_manager._calculate_streak([])
  assert result == 0


def test_calculate_streak_single_today(data_manager, freeze_time):
  """Test _calculate_streak with single date today."""
  freeze_time.set_date(datetime(2024, 1, 15, 10, 0, 0))
  result = data_manager._calculate_streak(["2024-01-15"])
  assert result == 1


def test_calculate_streak_consecutive_days(data_manager, freeze_time):
  """Test _calculate_streak with consecutive days."""
  freeze_time.set_date(datetime(2024, 1, 15, 10, 0, 0))
  dates = ["2024-01-13", "2024-01-14", "2024-01-15"]
  result = data_manager._calculate_streak(dates)
  assert result == 3


def test_calculate_streak_broken_streak(data_manager, freeze_time):
  """Test _calculate_streak stops at gap in dates."""
  freeze_time.set_date(datetime(2024, 1, 15, 10, 0, 0))
  dates = ["2024-01-10", "2024-01-14", "2024-01-15"]
  result = data_manager._calculate_streak(dates)
  assert result == 2


# ==================== Goals Tests (3) ====================

def test_get_goals_existing(data_manager, sample_goals):
  """Test getting existing goals."""
  goals_file = data_manager.data_path / "goals.json"
  with open(goals_file, "w", encoding="utf-8") as f:
    json.dump(sample_goals, f)
  result = data_manager.get_goals()
  assert result == sample_goals


def test_get_goals_nonexistent(data_manager):
  """Test get_goals returns default structure when file does not exist."""
  result = data_manager.get_goals()
  assert "lifetime_vision" in result
  assert "yearly_goals" in result
  assert result["yearly_goals"] == []


def test_save_goals(data_manager, sample_goals):
  """Test saving goals data."""
  result = data_manager.save_goals(sample_goals)
  assert result is True
  saved = data_manager.get_goals()
  assert saved == sample_goals


# ==================== Statistics Tests (6) ====================

def test_get_stats_empty(data_manager):
  """Test get_stats with no data returns zero values."""
  result = data_manager.get_stats()
  assert result["total_days_logged"] == 0
  assert result["am_checkins"] == 0
  assert result["pm_reflections"] == 0
  assert result["avg_sleep"] == 0
  assert result["avg_energy"] == 0
  assert result["avg_day_score"] == 0


def test_get_stats_with_logs(data_manager, freeze_time):
  """Test get_stats calculates values from logs."""
  freeze_time.set_date(datetime(2024, 1, 15, 10, 0, 0))
  for i in range(5):
    date = (datetime(2024, 1, 15) - timedelta(days=i)).strftime("%Y-%m-%d")
    log = {
      "am_checkin": {"sleep_hours": 7 + i * 0.5, "energy_level": 8},
      "pm_reflection": {"day_score": 7 + i},
      "metrics": {"deep_work_hours": 4, "workouts": 1}
    }
    data_manager.save_daily_log(log, date)
  result = data_manager.get_stats()
  assert result["total_days_logged"] == 5
  assert result["am_checkins"] == 5
  assert result["pm_reflections"] == 5
  assert result["avg_sleep"] == 8.0
  assert result["avg_energy"] == 8.0
  assert result["total_deep_work_hours"] == 20


def test_get_stats_calculates_averages(data_manager, freeze_time):
  """Test get_stats calculates correct averages."""
  freeze_time.set_date(datetime(2024, 1, 15, 10, 0, 0))
  logs = [
    {"am_checkin": {"sleep_hours": 6, "energy_level": 5}, "pm_reflection": {"day_score": 6}},
    {"am_checkin": {"sleep_hours": 8, "energy_level": 9}, "pm_reflection": {"day_score": 8}},
    {"am_checkin": {"sleep_hours": 7, "energy_level": 7}, "pm_reflection": {"day_score": 7}}
  ]
  for i, log in enumerate(logs):
    date = (datetime(2024, 1, 15) - timedelta(days=i)).strftime("%Y-%m-%d")
    data_manager.save_daily_log(log, date)
  result = data_manager.get_stats()
  assert result["avg_sleep"] == 7.0
  assert result["avg_energy"] == 7.0
  assert result["avg_day_score"] == 7.0


def test_get_stats_handles_missing_fields(data_manager, freeze_time):
  """Test get_stats handles logs with missing fields."""
  freeze_time.set_date(datetime(2024, 1, 15, 10, 0, 0))
  log1 = {"am_checkin": {"sleep_hours": 7}}
  log2 = {"pm_reflection": {"day_score": 8}}
  log3 = {}
  data_manager.save_daily_log(log1, "2024-01-15")
  data_manager.save_daily_log(log2, "2024-01-14")
  data_manager.save_daily_log(log3, "2024-01-13")
  result = data_manager.get_stats()
  assert result["total_days_logged"] == 3
  assert result["am_checkins"] == 1
  assert result["pm_reflections"] == 1


def test_get_stats_habit_completion_rate(data_manager, freeze_time):
  """Test get_stats calculates habit completion rate."""
  freeze_time.set_date(datetime(2024, 1, 15, 10, 0, 0))
  habit1 = {"id": "morning", "name": "Morning"}
  habit2 = {"id": "evening", "name": "Evening"}
  data_manager.add_habit(habit1)
  data_manager.add_habit(habit2)
  for i in range(3):
    date = (datetime(2024, 1, 15) - timedelta(days=i)).strftime("%Y-%m-%d")
    data_manager.save_daily_log({}, date)
    data_manager.record_habit_completion("morning", date)
  result = data_manager.get_stats()
  expected_rate = (3 / 6) * 100
  assert result["habit_completion_rate"] == expected_rate


def test_get_stats_no_habits_zero_completion(data_manager, freeze_time):
  """Test get_stats returns 0 completion rate with no habits."""
  freeze_time.set_date(datetime(2024, 1, 15, 10, 0, 0))
  data_manager.save_daily_log({}, "2024-01-15")
  result = data_manager.get_stats()
  assert result["habit_completion_rate"] == 0


# ==================== Knowledge Base Tests (3) ====================

def test_get_knowledge_base_topics(data_manager):
  """Test getting list of knowledge base topics."""
  kb_path = data_manager.kb_path
  kb_path.mkdir(parents=True, exist_ok=True)
  (kb_path / "money.md").write_text("# Money Content")
  (kb_path / "sales.md").write_text("# Sales Content")
  result = data_manager.get_knowledge_base_topics()
  assert "money" in result
  assert "sales" in result


def test_get_knowledge_base_topics_empty(data_manager):
  """Test get_knowledge_base_topics returns empty list when dir does not exist."""
  result = data_manager.get_knowledge_base_topics()
  assert result == []


def test_get_knowledge_base_content(data_manager):
  """Test getting knowledge base content for topic."""
  kb_path = data_manager.kb_path
  kb_path.mkdir(parents=True, exist_ok=True)
  content = "# Money Mastery\n\nContent here"
  (kb_path / "money.md").write_text(content, encoding="utf-8")
  result = data_manager.get_knowledge_base_content("money")
  assert result == content


def test_get_knowledge_base_content_nonexistent(data_manager):
  """Test get_knowledge_base_content returns None for non-existent topic."""
  result = data_manager.get_knowledge_base_content("nonexistent")
  assert result is None
