"""
Verification tests for conftest.py fixtures.
Tests that all 16 fixtures load correctly and return expected data structures.
"""
import pytest
from pathlib import Path


class TestFixturesLoading:
  """Verify all fixtures load correctly."""

  def test_temp_test_dir_fixture(self, temp_test_dir):
    """Test temp_test_dir creates proper directory structure."""
    assert temp_test_dir.exists()
    assert (temp_test_dir / "data").exists()
    assert (temp_test_dir / "data" / "logs").exists()
    assert (temp_test_dir / "data" / "reviews").exists()
    assert (temp_test_dir / "knowledge_base" / "masters").exists()

  def test_mock_user_profile_fixture(self, mock_user_profile):
    """Test mock_user_profile returns valid profile data."""
    assert mock_user_profile["name"] == "Boss"
    assert "module_levels" in mock_user_profile
    assert "focus_modules" in mock_user_profile
    assert len(mock_user_profile["module_levels"]) == 12

  def test_mock_daily_log_fixture(self, mock_daily_log):
    """Test mock_daily_log returns complete log structure."""
    assert "date" in mock_daily_log
    assert "am_checkin" in mock_daily_log
    assert "pm_reflection" in mock_daily_log
    assert "metrics" in mock_daily_log
    assert "habits" in mock_daily_log

  def test_mock_am_checkin_fixture(self, mock_am_checkin):
    """Test mock_am_checkin returns checkin data."""
    assert "sleep_hours" in mock_am_checkin
    assert "energy_level" in mock_am_checkin
    assert "top_3_priorities" in mock_am_checkin
    assert len(mock_am_checkin["top_3_priorities"]) == 3

  def test_mock_pm_reflection_fixture(self, mock_pm_reflection):
    """Test mock_pm_reflection returns reflection data."""
    assert "wins" in mock_pm_reflection
    assert "challenges" in mock_pm_reflection
    assert "day_score" in mock_pm_reflection
    assert isinstance(mock_pm_reflection["day_score"], int)

  def test_mock_habits_data_fixture(self, mock_habits_data):
    """Test mock_habits_data returns habits with completions."""
    assert "habits" in mock_habits_data
    assert "completions" in mock_habits_data
    assert len(mock_habits_data["habits"]) > 0
    assert all("id" in h for h in mock_habits_data["habits"])

  def test_mock_goals_fixture(self, mock_goals):
    """Test mock_goals returns goals structure."""
    assert "lifetime_vision" in mock_goals
    assert "yearly_goals" in mock_goals
    assert "quarterly_goals" in mock_goals
    assert isinstance(mock_goals["yearly_goals"], list)

  def test_mock_weekly_review_fixture(self, mock_weekly_review):
    """Test mock_weekly_review returns review data."""
    assert "week" in mock_weekly_review
    assert "wins" in mock_weekly_review
    assert "metrics" in mock_weekly_review
    assert "next_week_focus" in mock_weekly_review

  def test_mock_master_single_fixture(self, mock_master_single):
    """Test mock_master_single returns complete master data."""
    assert "name" in mock_master_single
    assert "expertise" in mock_master_single
    assert "key_principles" in mock_master_single
    assert "daily_practices" in mock_master_single
    assert len(mock_master_single["key_principles"]) > 0

  def test_mock_master_module_complete_fixture(self, mock_master_module_complete):
    """Test mock_master_module_complete returns module structure."""
    assert "module" in mock_master_module_complete
    assert "masters" in mock_master_module_complete
    assert "daily_insights" in mock_master_module_complete
    assert "skill_challenges" in mock_master_module_complete

  def test_mock_all_masters_minimal_fixture(self, mock_all_masters_minimal):
    """Test mock_all_masters_minimal returns all 12 modules."""
    assert len(mock_all_masters_minimal) == 12
    expected_modules = [
      "money", "sales", "finance", "dating", "mindset",
      "health", "lifestyle", "business", "productivity",
      "emotional_intelligence", "critical_thinking", "communication"
    ]
    for module in expected_modules:
      assert module in mock_all_masters_minimal

  def test_data_manager_empty_fixture(self, data_manager_empty):
    """Test data_manager_empty creates empty DataManager."""
    assert data_manager_empty is not None
    assert data_manager_empty.data_path.exists()
    assert data_manager_empty.logs_path.exists()

  def test_data_manager_populated_fixture(self, data_manager_populated):
    """Test data_manager_populated has pre-populated data."""
    profile = data_manager_populated.get_user_profile()
    assert profile is not None
    assert profile["name"] == "Boss"

    habits = data_manager_populated.get_habits()
    assert len(habits["habits"]) > 0

  def test_wisdom_engine_empty_fixture(self, wisdom_engine_empty):
    """Test wisdom_engine_empty creates empty WisdomEngine."""
    assert wisdom_engine_empty is not None
    assert len(wisdom_engine_empty.masters_data) == 0

  def test_wisdom_engine_populated_fixture(self, wisdom_engine_populated):
    """Test wisdom_engine_populated loads all masters data."""
    assert wisdom_engine_populated is not None
    assert len(wisdom_engine_populated.masters_data) == 12

    wisdom = wisdom_engine_populated.get_daily_wisdom()
    assert "master_teaching" in wisdom
    assert "daily_insight" in wisdom
    assert "skill_challenge" in wisdom

  def test_freeze_time_fixture(self, freeze_time):
    """Test freeze_time fixture returns fixed datetime."""
    from datetime import datetime
    frozen = freeze_time
    assert frozen.year == 2026
    assert frozen.month == 2
    assert frozen.day == 7
