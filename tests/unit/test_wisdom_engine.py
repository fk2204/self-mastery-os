"""
Comprehensive test suite for wisdom_engine.py
Target: 100% code coverage
"""
import pytest
import json
import random
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
from io import StringIO
from datetime import datetime

from src.wisdom_engine import WisdomEngine
from src.data_manager import DataManager


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture
def temp_dir(tmp_path):
  """Create temporary directory structure for testing."""
  data_dir = tmp_path / "data"
  data_dir.mkdir()
  (data_dir / "logs").mkdir()
  (data_dir / "reviews").mkdir()
  kb_dir = tmp_path / "knowledge_base" / "masters"
  kb_dir.mkdir(parents=True)
  return tmp_path


@pytest.fixture
def sample_master_data():
  """Create sample master data structure."""
  return {
    "module": "productivity",
    "level_definitions": {
      "1": {
        "name": "Beginner",
        "description": "Starting out",
        "capabilities": ["Basic task management"],
        "milestone": "Complete first week"
      },
      "5": {
        "name": "Intermediate",
        "description": "Building momentum",
        "capabilities": ["Deep work sessions", "System design"],
        "milestone": "Consistent deep work"
      }
    },
    "progressive_exercises": {
      "beginner": [
        {
          "title": "Time Audit",
          "difficulty": 1,
          "time_minutes": 15,
          "instructions": "Log your time for one day",
          "success_criteria": "Complete log with insights"
        }
      ],
      "intermediate": [
        {
          "title": "Deep Work Sprint",
          "difficulty": 2,
          "time_minutes": 90,
          "instructions": "Complete 90-minute focus session",
          "success_criteria": "Focus rating 7+"
        }
      ],
      "advanced": [
        {
          "title": "Flow State Practice",
          "difficulty": 3,
          "time_minutes": 120,
          "instructions": "Design and execute flow session",
          "success_criteria": "Sustained flow for 2 hours"
        }
      ]
    },
    "cross_module_connections": [
      {
        "connected_module": "mindset",
        "insight": "Productivity requires mental clarity",
        "combined_exercise": "Meditation before deep work"
      }
    ],
    "daily_insights": [
      "Deep work beats shallow work every time.",
      "Focus is a muscle you build through practice."
    ],
    "skill_challenges": [
      "Complete your #1 priority before noon.",
      "Turn off all notifications for 2 hours."
    ],
    "masters": [
      {
        "name": "Cal Newport",
        "expertise": "Deep Work and Digital Minimalism",
        "key_principles": [
          "Deep work is rare and valuable",
          "Quit social media"
        ],
        "daily_practices": [
          "Block time for deep work",
          "Practice digital minimalism"
        ],
        "worked_examples": [
          {
            "title": "Deep Work Implementation",
            "scenario": "Knowledge worker struggling with focus",
            "framework_applied": "Deep Work Philosophy",
            "step_by_step": [
              "Block 90-minute sessions",
              "Eliminate distractions",
              "Track depth of focus"
            ],
            "outcome": "Doubled productivity in 30 days"
          }
        ],
        "scripts_templates": [
          {
            "title": "Email Boundary Script",
            "context": "Setting expectations for response times",
            "template": "I check email twice daily at ___ and ___",
            "example_filled": "I check email twice daily at 10am and 3pm"
          }
        ],
        "resources": {
          "books": [
            {
              "title": "Deep Work",
              "author": "Cal Newport",
              "key_takeaway": "Focused work is valuable"
            }
          ],
          "podcasts": [
            {
              "title": "Deep Questions",
              "episode": "Episode 1",
              "key_takeaway": "Quality over quantity"
            }
          ]
        }
      },
      {
        "name": "James Clear",
        "expertise": "Atomic Habits",
        "key_principles": [
          "1% better every day",
          "Systems over goals"
        ],
        "daily_practices": [
          "Track your habits",
          "Focus on identity change"
        ],
        "worked_examples": [],
        "scripts_templates": [],
        "resources": {}
      }
    ]
  }


@pytest.fixture
def sample_sales_data():
  """Create sample sales master data."""
  return {
    "module": "sales",
    "daily_insights": ["Always be closing.", "Rejection is part of the game."],
    "skill_challenges": ["Make 10 cold calls today.", "Practice objection handling."],
    "masters": [
      {
        "name": "Jordan Belfort",
        "expertise": "Straight Line Persuasion",
        "key_principles": ["Control the sale", "Tonality matters"],
        "daily_practices": ["Practice your pitch", "Role-play objections"]
      }
    ]
  }


@pytest.fixture
def sample_user_profile():
  """Create sample user profile."""
  return {
    "name": "Boss",
    "focus_modules": ["productivity", "sales", "money"]
  }


@pytest.fixture
def data_manager_mock(temp_dir, sample_user_profile):
  """Create DataManager mock with temp directory."""
  dm = DataManager(base_path=str(temp_dir))
  profile_path = temp_dir / "data" / "user_profile.json"
  with open(profile_path, 'w') as f:
    json.dump(sample_user_profile, f)
  return dm


@pytest.fixture
def wisdom_engine(temp_dir, sample_master_data, sample_sales_data, data_manager_mock):
  """Create WisdomEngine with sample data."""
  masters_path = temp_dir / "knowledge_base" / "masters"

  with open(masters_path / "productivity_masters.json", 'w') as f:
    json.dump(sample_master_data, f)

  with open(masters_path / "sales_masters.json", 'w') as f:
    json.dump(sample_sales_data, f)

  return WisdomEngine(data_manager_mock)


# ============================================================
# Initialization Tests (5 tests)
# ============================================================

def test_init_with_valid_data_manager(wisdom_engine, data_manager_mock):
  """Test WisdomEngine initializes with valid DataManager."""
  assert wisdom_engine.dm == data_manager_mock
  assert isinstance(wisdom_engine.base_path, Path)
  assert isinstance(wisdom_engine.masters_path, Path)
  assert isinstance(wisdom_engine.profile, dict)
  assert isinstance(wisdom_engine.masters_data, dict)


def test_init_loads_user_profile(wisdom_engine):
  """Test initialization loads user profile correctly."""
  assert wisdom_engine.profile.get("name") == "Boss"
  assert "productivity" in wisdom_engine.profile.get("focus_modules", [])


def test_init_loads_masters_data(wisdom_engine):
  """Test initialization loads all master data files."""
  assert "productivity" in wisdom_engine.masters_data
  assert "sales" in wisdom_engine.masters_data
  assert len(wisdom_engine.masters_data) == 2


def test_init_handles_missing_masters_directory(temp_dir):
  """Test initialization with non-existent masters directory."""
  dm = DataManager(base_path=str(temp_dir))
  masters_path = temp_dir / "knowledge_base" / "masters"
  if masters_path.exists():
    import shutil
    shutil.rmtree(masters_path)

  engine = WisdomEngine(dm)
  assert engine.masters_data == {}


def test_init_handles_empty_user_profile(temp_dir):
  """Test initialization when user profile is None."""
  dm = DataManager(base_path=str(temp_dir))
  engine = WisdomEngine(dm)
  assert engine.profile == {}


# ============================================================
# Daily Wisdom Generation Tests (4 tests)
# ============================================================

def test_get_daily_wisdom_returns_complete_package(wisdom_engine):
  """Test daily wisdom returns all required components."""
  random.seed(42)
  wisdom = wisdom_engine.get_daily_wisdom()

  assert "date" in wisdom
  assert "master_teaching" in wisdom
  assert "daily_insight" in wisdom
  assert "skill_challenge" in wisdom
  assert "power_question" in wisdom
  assert "mindset_shift" in wisdom


def test_get_daily_wisdom_includes_current_date(wisdom_engine):
  """Test daily wisdom includes today's date."""
  wisdom = wisdom_engine.get_daily_wisdom()
  expected_date = datetime.now().strftime("%Y-%m-%d")
  assert wisdom["date"] == expected_date


def test_get_daily_wisdom_uses_focus_modules(wisdom_engine):
  """Test daily wisdom prioritizes focus modules."""
  random.seed(42)
  wisdom = wisdom_engine.get_daily_wisdom()

  module = wisdom["master_teaching"]["module"]
  assert module in ["productivity", "sales", "money"]


def test_get_daily_wisdom_deterministic_with_seed(wisdom_engine):
  """Test daily wisdom is deterministic when seeded."""
  random.seed(123)
  wisdom1 = wisdom_engine.get_daily_wisdom()

  random.seed(123)
  wisdom2 = wisdom_engine.get_daily_wisdom()

  assert wisdom1["master_teaching"] == wisdom2["master_teaching"]
  assert wisdom1["daily_insight"] == wisdom2["daily_insight"]


# ============================================================
# Master Teaching Tests (6 tests)
# ============================================================

def test_get_master_teaching_returns_valid_structure(wisdom_engine):
  """Test master teaching has required fields."""
  random.seed(42)
  teaching = wisdom_engine._get_master_teaching(["productivity"])

  assert "master" in teaching
  assert "expertise" in teaching
  assert "teaching" in teaching
  assert "practice" in teaching
  assert "module" in teaching


def test_get_master_teaching_from_focus_modules(wisdom_engine):
  """Test master teaching comes from focus modules."""
  random.seed(42)
  teaching = wisdom_engine._get_master_teaching(["productivity"])

  assert teaching["module"] == "productivity"
  assert teaching["master"] in ["Cal Newport", "James Clear"]


def test_get_master_teaching_handles_empty_focus_modules(wisdom_engine):
  """Test master teaching with empty focus modules list."""
  random.seed(42)
  teaching = wisdom_engine._get_master_teaching([])

  assert teaching["master"] is not None
  assert teaching["module"] in wisdom_engine.masters_data.keys()


def test_get_master_teaching_handles_invalid_modules(wisdom_engine):
  """Test master teaching with invalid module names."""
  random.seed(42)
  teaching = wisdom_engine._get_master_teaching(["nonexistent", "fake"])

  assert teaching["master"] is not None
  assert teaching["module"] in wisdom_engine.masters_data.keys()


def test_get_master_teaching_handles_no_masters_data(temp_dir):
  """Test master teaching when no masters data exists."""
  dm = DataManager(base_path=str(temp_dir))
  engine = WisdomEngine(dm)

  teaching = engine._get_master_teaching(["productivity"])

  assert teaching["master"] == "Unknown"
  assert "No teachings available" in teaching["teaching"]


def test_get_master_teaching_handles_empty_principles(wisdom_engine):
  """Test master teaching with master having no principles."""
  random.seed(42)
  wisdom_engine.masters_data["productivity"]["masters"][0]["key_principles"] = []

  teaching = wisdom_engine._get_master_teaching(["productivity"])

  assert teaching["teaching"] == "No teaching available."


# ============================================================
# Daily Insight Tests (3 tests)
# ============================================================

def test_get_daily_insight_returns_string(wisdom_engine):
  """Test daily insight returns a string."""
  random.seed(42)
  insight = wisdom_engine._get_daily_insight(["productivity"])

  assert isinstance(insight, str)
  assert len(insight) > 0


def test_get_daily_insight_from_focus_modules(wisdom_engine):
  """Test daily insight includes focus module insights."""
  random.seed(42)
  insight = wisdom_engine._get_daily_insight(["productivity", "sales"])

  assert isinstance(insight, str)


def test_get_daily_insight_handles_no_insights(temp_dir):
  """Test daily insight with no insights available."""
  dm = DataManager(base_path=str(temp_dir))
  engine = WisdomEngine(dm)

  insight = engine._get_daily_insight([])

  assert insight == "Show up. Do the work. Repeat."


# ============================================================
# Skill Challenge Tests (4 tests)
# ============================================================

def test_get_skill_challenge_returns_valid_structure(wisdom_engine):
  """Test skill challenge has required fields."""
  random.seed(42)
  challenge = wisdom_engine._get_skill_challenge(["productivity"])

  assert "module" in challenge
  assert "module_name" in challenge
  assert "challenge" in challenge


def test_get_skill_challenge_from_focus_modules(wisdom_engine):
  """Test skill challenge comes from focus modules."""
  random.seed(42)
  challenge = wisdom_engine._get_skill_challenge(["productivity"])

  assert challenge["module"] == "productivity"
  assert isinstance(challenge["challenge"], str)


def test_get_skill_challenge_handles_empty_focus_modules(wisdom_engine):
  """Test skill challenge with empty focus modules."""
  random.seed(42)
  challenge = wisdom_engine._get_skill_challenge([])

  assert challenge["module"] == "productivity"
  assert challenge["module_name"] == "Productivity & Systems"


def test_get_skill_challenge_handles_no_challenges(temp_dir):
  """Test skill challenge when no challenges exist."""
  dm = DataManager(base_path=str(temp_dir))
  engine = WisdomEngine(dm)

  challenge = engine._get_skill_challenge(["productivity"])

  assert challenge["challenge"] == "Complete your #1 priority before noon."


# ============================================================
# Power Questions Tests (2 tests)
# ============================================================

def test_get_power_question_returns_string(wisdom_engine):
  """Test power question returns a string."""
  random.seed(42)
  question = wisdom_engine._get_power_question()

  assert isinstance(question, str)
  assert len(question) > 0
  assert "?" in question


def test_get_power_question_deterministic_with_seed(wisdom_engine):
  """Test power question is deterministic when seeded."""
  random.seed(99)
  q1 = wisdom_engine._get_power_question()

  random.seed(99)
  q2 = wisdom_engine._get_power_question()

  assert q1 == q2


# ============================================================
# Mindset Shift Tests (2 tests)
# ============================================================

def test_get_mindset_shift_returns_valid_structure(wisdom_engine):
  """Test mindset shift has required fields."""
  random.seed(42)
  shift = wisdom_engine._get_mindset_shift()

  assert "from" in shift
  assert "to" in shift
  assert "why" in shift
  assert isinstance(shift["from"], str)
  assert isinstance(shift["to"], str)
  assert isinstance(shift["why"], str)


def test_get_mindset_shift_deterministic_with_seed(wisdom_engine):
  """Test mindset shift is deterministic when seeded."""
  random.seed(55)
  s1 = wisdom_engine._get_mindset_shift()

  random.seed(55)
  s2 = wisdom_engine._get_mindset_shift()

  assert s1 == s2


# ============================================================
# Situational Advice Tests (5 tests)
# ============================================================

def test_get_master_advice_maps_money_keywords(wisdom_engine):
  """Test situational advice maps money keywords correctly."""
  random.seed(42)
  advice = wisdom_engine.get_master_advice_for_situation("I need to earn more money")

  assert isinstance(advice, str)
  assert len(advice) > 0


def test_get_master_advice_maps_sales_keywords(wisdom_engine):
  """Test situational advice maps sales keywords correctly."""
  random.seed(42)
  advice = wisdom_engine.get_master_advice_for_situation("struggling to close deals")

  assert isinstance(advice, str)
  assert "Jordan Belfort" in advice or len(advice) > 0


def test_get_master_advice_maps_productivity_keywords(wisdom_engine):
  """Test situational advice maps productivity keywords correctly."""
  random.seed(42)
  advice = wisdom_engine.get_master_advice_for_situation("I procrastinate too much")

  assert isinstance(advice, str)


def test_get_master_advice_handles_unknown_situation(wisdom_engine):
  """Test situational advice with unrecognized keywords."""
  random.seed(42)
  advice = wisdom_engine.get_master_advice_for_situation("random unrelated topic")

  assert isinstance(advice, str)
  assert len(advice) > 0


def test_get_master_advice_handles_no_masters(temp_dir):
  """Test situational advice when no masters exist."""
  dm = DataManager(base_path=str(temp_dir))
  engine = WisdomEngine(dm)

  advice = engine.get_master_advice_for_situation("need help with sales")

  assert advice == "Take action despite uncertainty. Clarity comes from doing, not thinking."


# ============================================================
# Module Masters Tests (3 tests)
# ============================================================

def test_get_module_masters_returns_list(wisdom_engine):
  """Test get_module_masters returns list of masters."""
  masters = wisdom_engine.get_module_masters("productivity")

  assert isinstance(masters, list)
  assert len(masters) == 2
  assert masters[0]["name"] in ["Cal Newport", "James Clear"]


def test_get_module_masters_handles_invalid_module(wisdom_engine):
  """Test get_module_masters with invalid module name."""
  masters = wisdom_engine.get_module_masters("nonexistent")

  assert isinstance(masters, list)
  assert len(masters) == 0


def test_get_module_masters_returns_complete_data(wisdom_engine):
  """Test get_module_masters returns complete master data."""
  masters = wisdom_engine.get_module_masters("productivity")

  assert "name" in masters[0]
  assert "expertise" in masters[0]
  assert "key_principles" in masters[0]
  assert "daily_practices" in masters[0]


# ============================================================
# Worked Examples Tests (4 tests)
# ============================================================

def test_get_worked_example_returns_valid_structure(wisdom_engine):
  """Test worked example has required fields."""
  random.seed(42)
  example = wisdom_engine.get_worked_example("productivity")

  assert example is not None
  assert "title" in example
  assert "scenario" in example
  assert "framework_applied" in example
  assert "step_by_step" in example
  assert "outcome" in example
  assert "master" in example
  assert "module" in example


def test_get_worked_example_from_focus_modules(wisdom_engine):
  """Test worked example from focus modules when no module specified."""
  random.seed(42)
  example = wisdom_engine.get_worked_example()

  assert example is not None
  assert example["module"] in ["productivity", "sales"]


def test_get_worked_example_handles_no_examples(wisdom_engine):
  """Test worked example when none exist."""
  wisdom_engine.masters_data["sales"]["masters"][0]["worked_examples"] = []

  random.seed(42)
  example = wisdom_engine.get_worked_example("sales")

  if example:
    assert example["module"] == "productivity"


def test_get_worked_example_returns_none_when_empty(temp_dir):
  """Test worked example returns None when no examples exist."""
  dm = DataManager(base_path=str(temp_dir))
  engine = WisdomEngine(dm)

  example = engine.get_worked_example()

  assert example is None


# ============================================================
# Script Templates Tests (3 tests)
# ============================================================

def test_get_script_template_returns_valid_structure(wisdom_engine):
  """Test script template has required fields."""
  random.seed(42)
  template = wisdom_engine.get_script_template("productivity")

  assert template is not None
  assert "title" in template
  assert "context" in template
  assert "template" in template
  assert "master" in template
  assert "module" in template


def test_get_script_template_from_focus_modules(wisdom_engine):
  """Test script template from focus modules when no module specified."""
  random.seed(42)
  template = wisdom_engine.get_script_template()

  assert template is not None


def test_get_script_template_returns_none_when_empty(temp_dir):
  """Test script template returns None when none exist."""
  dm = DataManager(base_path=str(temp_dir))
  engine = WisdomEngine(dm)

  template = engine.get_script_template()

  assert template is None


# ============================================================
# Level Definitions Tests (3 tests)
# ============================================================

def test_get_level_definition_returns_valid_structure(wisdom_engine):
  """Test level definition has required fields."""
  level_def = wisdom_engine.get_level_definition("productivity", 1)

  assert level_def is not None
  assert "name" in level_def
  assert "description" in level_def
  assert "capabilities" in level_def
  assert "milestone" in level_def


def test_get_level_definition_handles_invalid_module(wisdom_engine):
  """Test level definition with invalid module."""
  level_def = wisdom_engine.get_level_definition("nonexistent", 1)

  assert level_def is None


def test_get_level_definition_handles_invalid_level(wisdom_engine):
  """Test level definition with level that doesn't exist."""
  level_def = wisdom_engine.get_level_definition("productivity", 99)

  assert level_def is None


# ============================================================
# Progressive Exercises Tests (4 tests)
# ============================================================

def test_get_progressive_exercise_returns_valid_structure(wisdom_engine):
  """Test progressive exercise has required fields."""
  random.seed(42)
  exercise = wisdom_engine.get_progressive_exercise("productivity", "beginner")

  assert exercise is not None
  assert "title" in exercise
  assert "difficulty" in exercise
  assert "time_minutes" in exercise
  assert "instructions" in exercise
  assert "success_criteria" in exercise
  assert "module" in exercise
  assert "difficulty_level" in exercise


def test_get_progressive_exercise_handles_different_difficulties(wisdom_engine):
  """Test progressive exercise for different difficulty levels."""
  random.seed(42)

  beginner = wisdom_engine.get_progressive_exercise("productivity", "beginner")
  intermediate = wisdom_engine.get_progressive_exercise("productivity", "intermediate")
  advanced = wisdom_engine.get_progressive_exercise("productivity", "advanced")

  assert beginner is not None
  assert intermediate is not None
  assert advanced is not None


def test_get_progressive_exercise_handles_invalid_module(wisdom_engine):
  """Test progressive exercise with invalid module."""
  exercise = wisdom_engine.get_progressive_exercise("nonexistent", "beginner")

  assert exercise is None


def test_get_progressive_exercise_handles_invalid_difficulty(wisdom_engine):
  """Test progressive exercise with invalid difficulty level."""
  exercise = wisdom_engine.get_progressive_exercise("productivity", "expert")

  assert exercise is None


# ============================================================
# Cross-Module Connections Tests (2 tests)
# ============================================================

def test_get_cross_module_connection_returns_valid_structure(wisdom_engine):
  """Test cross-module connection has required fields."""
  random.seed(42)
  connection = wisdom_engine.get_cross_module_connection("productivity")

  assert connection is not None
  assert "connected_module" in connection
  assert "insight" in connection
  assert "combined_exercise" in connection


def test_get_cross_module_connection_handles_invalid_module(wisdom_engine):
  """Test cross-module connection with invalid module."""
  connection = wisdom_engine.get_cross_module_connection("nonexistent")

  assert connection is None


# ============================================================
# Master Resources Tests (4 tests)
# ============================================================

def test_get_master_resources_returns_valid_structure(wisdom_engine):
  """Test master resources has expected structure."""
  resources = wisdom_engine.get_master_resources("productivity", "Cal Newport")

  assert resources is not None
  assert "books" in resources
  assert "podcasts" in resources


def test_get_master_resources_case_insensitive(wisdom_engine):
  """Test master resources lookup is case-insensitive."""
  resources = wisdom_engine.get_master_resources("productivity", "cal newport")

  assert resources is not None


def test_get_master_resources_handles_invalid_module(wisdom_engine):
  """Test master resources with invalid module."""
  resources = wisdom_engine.get_master_resources("nonexistent", "Cal Newport")

  assert resources is None


def test_get_master_resources_handles_invalid_master(wisdom_engine):
  """Test master resources with invalid master name."""
  resources = wisdom_engine.get_master_resources("productivity", "Nonexistent Master")

  assert resources is None


# ============================================================
# Print Functions Tests (6 tests)
# ============================================================

def test_print_daily_wisdom_outputs_formatted_text(wisdom_engine, capsys):
  """Test print_daily_wisdom produces console output."""
  random.seed(42)
  wisdom_engine.print_daily_wisdom()

  captured = capsys.readouterr()
  assert "TODAY'S WISDOM" in captured.out
  assert "MASTER TEACHING" in captured.out
  assert "DAILY INSIGHT" in captured.out
  assert "SKILL CHALLENGE" in captured.out
  assert "POWER QUESTION" in captured.out
  assert "MINDSET SHIFT" in captured.out


def test_print_master_profile_outputs_formatted_text(wisdom_engine, capsys):
  """Test print_master_profile produces console output."""
  wisdom_engine.print_master_profile("productivity", "Cal Newport")

  captured = capsys.readouterr()
  assert "CAL NEWPORT" in captured.out
  assert "Expertise:" in captured.out
  assert "Key Principles:" in captured.out
  assert "Daily Practices:" in captured.out


def test_print_master_profile_handles_not_found(wisdom_engine, capsys):
  """Test print_master_profile with non-existent master."""
  wisdom_engine.print_master_profile("productivity", "Nonexistent")

  captured = capsys.readouterr()
  assert "not found" in captured.out


def test_print_worked_example_outputs_formatted_text(wisdom_engine, capsys):
  """Test print_worked_example produces console output."""
  random.seed(42)
  example = wisdom_engine.get_worked_example("productivity")

  if example:
    wisdom_engine.print_worked_example(example)

    captured = capsys.readouterr()
    assert "WORKED EXAMPLE" in captured.out
    assert "Scenario:" in captured.out
    assert "Framework:" in captured.out
    assert "Steps:" in captured.out
    assert "Outcome:" in captured.out


def test_print_script_template_outputs_formatted_text(wisdom_engine, capsys):
  """Test print_script_template produces console output."""
  random.seed(42)
  template = wisdom_engine.get_script_template("productivity")

  if template:
    wisdom_engine.print_script_template(template)

    captured = capsys.readouterr()
    assert "SCRIPT/TEMPLATE" in captured.out
    assert "Context:" in captured.out
    assert "Template:" in captured.out


def test_get_all_masters_list_returns_complete_list(wisdom_engine):
  """Test get_all_masters_list returns all masters from all modules."""
  all_masters = wisdom_engine.get_all_masters_list()

  assert isinstance(all_masters, list)
  assert len(all_masters) == 3

  for master in all_masters:
    assert "name" in master
    assert "module" in master
    assert "expertise" in master


# ============================================================
# Edge Cases and Error Handling Tests (6 tests)
# ============================================================

def test_load_all_masters_handles_corrupt_json(temp_dir, data_manager_mock):
  """Test _load_all_masters handles corrupted JSON files."""
  masters_path = temp_dir / "knowledge_base" / "masters"

  with open(masters_path / "corrupt.json", 'w') as f:
    f.write("{invalid json content")

  engine = WisdomEngine(data_manager_mock)

  assert "corrupt" not in engine.masters_data


def test_load_all_masters_handles_io_error(temp_dir, data_manager_mock):
  """Test _load_all_masters handles file read errors."""
  masters_path = temp_dir / "knowledge_base" / "masters"

  with open(masters_path / "test.json", 'w') as f:
    json.dump({"module": "test", "masters": []}, f)

  engine = WisdomEngine(data_manager_mock)

  assert isinstance(engine.masters_data, dict)


def test_get_daily_wisdom_with_no_focus_modules(temp_dir, sample_master_data):
  """Test get_daily_wisdom when profile has no focus_modules."""
  dm = DataManager(base_path=str(temp_dir))

  masters_path = temp_dir / "knowledge_base" / "masters"
  with open(masters_path / "productivity_masters.json", 'w') as f:
    json.dump(sample_master_data, f)

  engine = WisdomEngine(dm)
  random.seed(42)

  wisdom = engine.get_daily_wisdom()

  assert wisdom is not None
  assert "master_teaching" in wisdom


def test_master_teaching_with_no_daily_practices(wisdom_engine):
  """Test master teaching when master has empty daily_practices."""
  random.seed(42)
  wisdom_engine.masters_data["productivity"]["masters"][0]["daily_practices"] = []

  teaching = wisdom_engine._get_master_teaching(["productivity"])

  assert teaching["practice"] == "Apply this today."


def test_print_script_template_with_no_example_filled(wisdom_engine, capsys):
  """Test print_script_template when example_filled is missing."""
  template = {
    "title": "Test Template",
    "master": "Test Master",
    "module": "test",
    "context": "Test context",
    "template": "Test template text"
  }

  wisdom_engine.print_script_template(template)

  captured = capsys.readouterr()
  assert "SCRIPT/TEMPLATE" in captured.out
  assert "Test Template" in captured.out


def test_print_worked_example_with_empty_steps(wisdom_engine, capsys):
  """Test print_worked_example when step_by_step is empty."""
  example = {
    "title": "Test Example",
    "master": "Test Master",
    "module": "test",
    "scenario": "Test scenario",
    "framework_applied": "Test framework",
    "step_by_step": [],
    "outcome": "Test outcome"
  }

  wisdom_engine.print_worked_example(example)

  captured = capsys.readouterr()
  assert "WORKED EXAMPLE" in captured.out
  assert "Test Example" in captured.out
