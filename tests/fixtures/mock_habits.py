"""
Mock habits data for Self-Mastery OS testing.
"""
from typing import Dict


def get_mock_habits_data() -> Dict:
  """Get mock habits data with completions."""
  return {
    "habits": [
      {
        "id": "morning_routine",
        "name": "Morning Routine (full)",
        "module": "productivity",
        "frequency": "daily",
        "created_at": "2026-02-01T10:00:00",
        "current_streak": 7,
        "best_streak": 12,
        "total_completions": 35
      },
      {
        "id": "deep_work_90",
        "name": "Deep Work Block (90+ min)",
        "module": "productivity",
        "frequency": "daily",
        "created_at": "2026-02-01T10:00:00",
        "current_streak": 5,
        "best_streak": 10,
        "total_completions": 28
      },
      {
        "id": "sales_outreach",
        "name": "Sales Outreach (10+ touches)",
        "module": "sales",
        "frequency": "daily",
        "created_at": "2026-02-01T10:00:00",
        "current_streak": 6,
        "best_streak": 15,
        "total_completions": 32
      },
      {
        "id": "objection_practice",
        "name": "Objection Handling Practice",
        "module": "sales",
        "frequency": "daily",
        "created_at": "2026-02-01T10:00:00",
        "current_streak": 0,
        "best_streak": 8,
        "total_completions": 18
      },
      {
        "id": "finance_review",
        "name": "Finance Check (spending/budget)",
        "module": "finance",
        "frequency": "daily",
        "created_at": "2026-02-01T10:00:00",
        "current_streak": 7,
        "best_streak": 14,
        "total_completions": 30
      },
      {
        "id": "journaling",
        "name": "Journaling (AM or PM)",
        "module": "mindset",
        "frequency": "daily",
        "created_at": "2026-02-01T10:00:00",
        "current_streak": 4,
        "best_streak": 20,
        "total_completions": 25
      }
    ],
    "completions": {
      "2026-02-01": ["morning_routine", "deep_work_90", "sales_outreach", "finance_review"],
      "2026-02-02": ["morning_routine", "deep_work_90", "sales_outreach", "finance_review", "journaling"],
      "2026-02-03": ["morning_routine", "deep_work_90", "sales_outreach", "finance_review"],
      "2026-02-04": ["morning_routine", "deep_work_90", "sales_outreach", "finance_review", "journaling"],
      "2026-02-05": ["morning_routine", "deep_work_90", "sales_outreach", "finance_review", "journaling"],
      "2026-02-06": ["morning_routine", "sales_outreach", "finance_review", "journaling"],
      "2026-02-07": ["morning_routine", "deep_work_90", "sales_outreach", "finance_review"]
    }
  }
