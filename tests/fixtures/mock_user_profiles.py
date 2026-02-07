"""
Mock user profile data for Self-Mastery OS testing.
"""
from typing import Dict


def get_mock_user_profile() -> Dict:
  """Get realistic mock user profile matching production schema."""
  return {
    "name": "Boss",
    "created_at": "2026-02-01T10:00:00",
    "updated_at": "2026-02-07T08:00:00",
    "top_goals": [
      "Build multiple income streams to $10K/month",
      "Master sales, persuasion, and closing",
      "Achieve financial independence through smart investing"
    ],
    "daily_time_available_minutes": 90,
    "coaching_style": "direct",
    "constraints": ["time"],
    "module_levels": {
      "money": 5,
      "sales": 4,
      "finance": 5,
      "dating": 5,
      "mindset": 6,
      "health": 8,
      "lifestyle": 5,
      "business": 5,
      "productivity": 6,
      "emotional_intelligence": 3,
      "critical_thinking": 3,
      "communication": 3
    },
    "focus_modules": ["money", "sales", "finance", "productivity", "business"],
    "goals_90_day": {
      "money": {
        "goal": "Add $3K/month in side income through high-income skills",
        "target_level": 7,
        "start_level": 5,
        "created_at": "2026-02-01T10:00:00"
      },
      "sales": {
        "goal": "Master cold outreach, close 5 new clients, handle any objection",
        "target_level": 7,
        "start_level": 4,
        "created_at": "2026-02-01T10:00:00"
      },
      "finance": {
        "goal": "50% savings rate, max tax-advantaged accounts, build investment system",
        "target_level": 7,
        "start_level": 5,
        "created_at": "2026-02-01T10:00:00"
      },
      "productivity": {
        "goal": "4+ hours deep work daily, bulletproof morning routine",
        "target_level": 8,
        "start_level": 6,
        "created_at": "2026-02-01T10:00:00"
      },
      "business": {
        "goal": "Launch 1 validated side project, build idea evaluation system",
        "target_level": 7,
        "start_level": 5,
        "created_at": "2026-02-01T10:00:00"
      }
    }
  }
