"""
Mock daily log data for Self-Mastery OS testing.
"""
from typing import Dict


def get_mock_am_checkin() -> Dict:
  """Get mock morning check-in data."""
  return {
    "time": "2026-02-07T06:30:00",
    "sleep_hours": 7.5,
    "sleep_quality": 8,
    "energy_level": 7,
    "top_3_priorities": [
      "Complete sales outreach to 10 leads",
      "Deep work on side project for 2 hours",
      "Review finances and update budget"
    ],
    "win_definition": "Close one deal and ship feature update"
  }


def get_mock_pm_reflection() -> Dict:
  """Get mock evening reflection data."""
  return {
    "time": "2026-02-07T21:00:00",
    "wins": [
      "Closed deal with new client worth $2K",
      "Completed 2.5 hours deep work on project",
      "Had productive networking call"
    ],
    "challenges": [
      "Got distracted by email mid-morning",
      "Didn't handle one objection well on sales call"
    ],
    "lessons": [
      "Turn off email notifications during deep work blocks",
      "Need to practice price objection responses more"
    ],
    "day_score": 8,
    "gratitude": [
      "Client said yes to proposal",
      "Friend made helpful intro",
      "Felt energized all day"
    ]
  }


def get_mock_daily_log() -> Dict:
  """Get complete mock daily log with all sections."""
  return {
    "date": "2026-02-07",
    "created_at": "2026-02-07T06:30:00",
    "updated_at": "2026-02-07T21:00:00",
    "am_checkin": get_mock_am_checkin(),
    "planned_actions": [
      {
        "module": "sales",
        "module_name": "Sales & Persuasion",
        "text": "Cold outreach to 10 qualified leads",
        "time": 30,
        "difficulty": 2,
        "completed": True
      },
      {
        "module": "productivity",
        "module_name": "Productivity & Systems",
        "text": "Deep work block: ship feature update",
        "time": 120,
        "difficulty": 3,
        "completed": True
      },
      {
        "module": "finance",
        "module_name": "Personal Finance",
        "text": "Review weekly spending and adjust budget",
        "time": 15,
        "difficulty": 1,
        "completed": True
      }
    ],
    "completed_actions": [
      "Cold outreach to 10 qualified leads",
      "Deep work block: ship feature update",
      "Review weekly spending and adjust budget"
    ],
    "pm_reflection": get_mock_pm_reflection(),
    "metrics": {
      "deep_work_hours": 2.5,
      "workouts": 1,
      "sales_calls": 5,
      "social_interactions": 2,
      "steps": 8500,
      "water_liters": 2.5
    },
    "habits": {
      "morning_routine": True,
      "deep_work_90": True,
      "sales_outreach": True,
      "objection_practice": False,
      "finance_review": True,
      "skill_learning": True,
      "journaling": True,
      "reading": True,
      "networking": True,
      "social_interaction": True,
      "inbox_zero": True,
      "no_phone_morning": True
    },
    "notes": "Great day overall. Need to work on objection handling."
  }
