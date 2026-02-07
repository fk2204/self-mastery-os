"""
Self-Mastery OS - Pytest Configuration and Shared Fixtures
Provides all test fixtures for DataManager, WisdomEngine, and integration tests.
"""
import os
import sys
import json
import tempfile
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict
from io import StringIO
import pytest

# Add src and tests to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent))

from data_manager import DataManager
from wisdom_engine import WisdomEngine
from fixtures.mock_user_profiles import get_mock_user_profile
from fixtures.mock_daily_logs import (
  get_mock_daily_log,
  get_mock_am_checkin,
  get_mock_pm_reflection
)
from fixtures.mock_masters_data import get_mock_master, get_mock_masters_module
from fixtures.mock_habits import get_mock_habits_data

# ==================== Test Directory Setup ====================

@pytest.fixture
def temp_test_dir(tmp_path):
  """Create temporary directory structure for testing."""
  base_dir = tmp_path / "test_self_mastery"
  data_dir = base_dir / "data"
  logs_dir = data_dir / "logs"
  reviews_dir = data_dir / "reviews"
  kb_dir = base_dir / "knowledge_base"
  masters_dir = kb_dir / "masters"

  for directory in [data_dir, logs_dir, reviews_dir, kb_dir, masters_dir]:
    directory.mkdir(parents=True, exist_ok=True)

  yield base_dir

  # Cleanup after test
  if base_dir.exists():
    shutil.rmtree(base_dir)

# ==================== User Profile Fixtures ====================

@pytest.fixture
def mock_user_profile() -> Dict:
  """Mock user profile with realistic data."""
  return get_mock_user_profile()

# ==================== Daily Log Fixtures ====================

@pytest.fixture
def mock_daily_log() -> Dict:
  """Mock complete daily log with AM checkin and PM reflection."""
  return get_mock_daily_log()

@pytest.fixture
def mock_am_checkin() -> Dict:
  """Mock morning check-in data."""
  return get_mock_am_checkin()

@pytest.fixture
def mock_pm_reflection() -> Dict:
  """Mock evening reflection data."""
  return get_mock_pm_reflection()

# ==================== Habits Fixtures ====================

@pytest.fixture
def mock_habits_data() -> Dict:
  """Mock habits data with completions."""
  return get_mock_habits_data()

# ==================== Goals Fixtures ====================

@pytest.fixture
def mock_goals() -> Dict:
  """Mock goals data structure."""
  return {
    "lifetime_vision": "Financial freedom, elite-level skills, high-value network, and complete life mastery",
    "yearly_goals": [
      "Reach $150K+ total income through multiple streams",
      "Master sales and close deals consistently",
      "Build a strong investment portfolio"
    ],
    "quarterly_goals": {
      "money": {
        "goal": "Add $3K/month in side income",
        "target_level": 7,
        "start_level": 5,
        "created_at": "2026-02-01T10:00:00"
      },
      "sales": {
        "goal": "Close 5 new clients",
        "target_level": 7,
        "start_level": 4,
        "created_at": "2026-02-01T10:00:00"
      }
    },
    "monthly_goals": [],
    "weekly_goals": []
  }

# ==================== Weekly Review Fixtures ====================

@pytest.fixture
def mock_weekly_review() -> Dict:
  """Mock weekly review data."""
  return {
    "week": "2026-W05",
    "created_at": "2026-02-07T18:00:00",
    "updated_at": "2026-02-07T18:30:00",
    "wins": [
      "Closed first client this week",
      "Hit 4 hours deep work 5 days straight",
      "Completed all sales outreach targets"
    ],
    "challenges": [
      "Still struggling with morning routine consistency",
      "Need better objection handling frameworks"
    ],
    "lessons": [
      "Cold outreach works best in the morning",
      "Following up 3x increases close rate significantly"
    ],
    "metrics": {
      "days_logged": 7,
      "total_deep_work_hours": 28.5,
      "habit_completion_rate": 78.5,
      "avg_day_score": 7.2
    },
    "next_week_focus": [
      "Master top 5 objection responses",
      "Increase daily outreach to 15 contacts",
      "Lock in morning routine at 5:30 AM"
    ]
  }

# ==================== Master Data Fixtures ====================

@pytest.fixture
def mock_master_single() -> Dict:
  """Single master with complete data structure."""
  return get_mock_master()

@pytest.fixture
def mock_master_module_complete() -> Dict:
  """Complete module JSON with multiple masters."""
  return get_mock_masters_module()

@pytest.fixture
def mock_all_masters_minimal() -> Dict:
  """Minimal masters data for all 12 modules."""
  modules = [
    "money", "sales", "finance", "dating", "mindset",
    "health", "lifestyle", "business", "productivity",
    "emotional_intelligence", "critical_thinking", "communication"
  ]
  masters_data = {}
  for module in modules:
    masters_data[module] = get_mock_masters_module(module)
  return masters_data

# ==================== DataManager Fixtures ====================

@pytest.fixture
def data_manager_empty(temp_test_dir):
  """DataManager instance with empty test directory."""
  return DataManager(base_path=str(temp_test_dir))

@pytest.fixture
def data_manager_populated(temp_test_dir, mock_user_profile, mock_habits_data, mock_goals):
  """DataManager with pre-populated test data."""
  dm = DataManager(base_path=str(temp_test_dir))

  # Write initial data files
  dm.save_user_profile(mock_user_profile)
  dm.save_habits(mock_habits_data)
  dm.save_goals(mock_goals)

  # Create sample daily log
  sample_log = get_mock_daily_log()
  dm.save_daily_log(sample_log, "2026-02-07")

  return dm

# ==================== WisdomEngine Fixtures ====================

@pytest.fixture
def wisdom_engine_empty(temp_test_dir):
  """WisdomEngine with no masters data."""
  dm = DataManager(base_path=str(temp_test_dir))
  return WisdomEngine(dm)

@pytest.fixture
def wisdom_engine_populated(temp_test_dir, mock_user_profile, mock_all_masters_minimal):
  """WisdomEngine with full masters data loaded."""
  dm = DataManager(base_path=str(temp_test_dir))
  dm.save_user_profile(mock_user_profile)

  # Write all masters JSON files
  masters_dir = temp_test_dir / "knowledge_base" / "masters"
  for module, data in mock_all_masters_minimal.items():
    file_path = masters_dir / f"{module}_masters.json"
    with open(file_path, "w", encoding="utf-8") as f:
      json.dump(data, f, indent=2)

  return WisdomEngine(dm)

# ==================== Utility Fixtures ====================

@pytest.fixture
def freeze_time(monkeypatch):
  """Freeze datetime.now() to a fixed time."""
  fixed_datetime = datetime(2026, 2, 7, 12, 0, 0)

  class FrozenTime:
    def __init__(self):
      self.frozen_date = fixed_datetime

    def set_date(self, new_datetime):
      """Change the frozen datetime."""
      self.frozen_date = new_datetime

    @property
    def year(self):
      return self.frozen_date.year

    @property
    def month(self):
      return self.frozen_date.month

    @property
    def day(self):
      return self.frozen_date.day

    @property
    def hour(self):
      return self.frozen_date.hour

    @property
    def minute(self):
      return self.frozen_date.minute

    @property
    def second(self):
      return self.frozen_date.second

  frozen_time_obj = FrozenTime()

  class MockDatetime:
    @classmethod
    def now(cls):
      return frozen_time_obj.frozen_date

    @classmethod
    def strptime(cls, *args, **kwargs):
      return datetime.strptime(*args, **kwargs)

    def __getattr__(cls, name):
      return getattr(datetime, name)

  monkeypatch.setattr("datetime.datetime", MockDatetime)
  monkeypatch.setattr("data_manager.datetime", MockDatetime)
  return frozen_time_obj

@pytest.fixture
def capture_stdout():
  """Capture stdout for testing print statements."""
  captured = StringIO()
  original_stdout = sys.stdout
  sys.stdout = captured
  yield captured
  sys.stdout = original_stdout

@pytest.fixture
def mock_random_seed():
  """Set random seed for reproducible random choices in tests."""
  import random
  random.seed(42)
  yield
  random.seed()

# ==================== Fixture Aliases for Backward Compatibility ====================

@pytest.fixture
def temp_dir(temp_test_dir):
  """Alias for temp_test_dir."""
  return temp_test_dir

@pytest.fixture
def data_manager(data_manager_empty):
  """Alias for data_manager_empty (default)."""
  return data_manager_empty

@pytest.fixture
def sample_user_profile(mock_user_profile):
  """Alias for mock_user_profile."""
  return mock_user_profile

@pytest.fixture
def sample_daily_log(mock_daily_log):
  """Alias for mock_daily_log."""
  return mock_daily_log

@pytest.fixture
def sample_weekly_review(mock_weekly_review):
  """Alias for mock_weekly_review."""
  return mock_weekly_review

@pytest.fixture
def sample_goals(mock_goals):
  """Alias for mock_goals."""
  return mock_goals

@pytest.fixture
def sample_habit():
  """Single habit fixture for testing individual habit operations."""
  return {
    "id": "morning_routine",
    "name": "Morning Routine (5:30 AM)",
    "module": "lifestyle",
    "frequency": "daily",
    "current_streak": 7,
    "best_streak": 14,
    "total_completions": 45,
    "created_at": "2026-01-01T08:00:00"
  }
