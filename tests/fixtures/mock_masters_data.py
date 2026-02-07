"""
Mock masters data for Self-Mastery OS testing.
"""
from typing import Dict


def get_mock_master() -> Dict:
  """Get single mock master with complete structure."""
  return {
    "name": "Naval Ravikant",
    "expertise": "Wealth creation, leverage, and specific knowledge",
    "key_principles": [
      "Seek wealth, not money or status",
      "Give society what it wants but doesn't know how to get at scale",
      "Learn to sell. Learn to build. If you can do both, you will be unstoppable",
      "Specific knowledge is found by pursuing your genuine curiosity"
    ],
    "daily_practices": [
      "Read for 1-2 hours daily across multiple disciplines",
      "Build specific knowledge through genuine curiosity",
      "Think long-term and compound your knowledge",
      "Seek leverage through code, media, or people"
    ],
    "worked_examples": [
      {
        "title": "Building Specific Knowledge",
        "scenario": "You want to increase your income but don't know what skill to develop",
        "framework_applied": "Specific Knowledge Discovery",
        "step_by_step": [
          "List 10 things you know that others ask you about",
          "Identify which feel like play to you but work to others",
          "Choose one that has market value",
          "Spend 6 months building public proof of that knowledge",
          "Package it into a service or product"
        ],
        "outcome": "You develop a unique skill that can't be trained and commands premium pay"
      }
    ],
    "scripts_templates": [
      {
        "title": "Leverage Assessment Template",
        "context": "When evaluating a business opportunity or project",
        "template": "Does this give me leverage through: [Code/Media/Capital/People]? Can this scale without my time? Will this compound over time?",
        "example_filled": "Freelance writing: Media leverage (yes), scales without time (yes, via products), compounds (yes, via audience growth)"
      }
    ],
    "resources": {
      "books": [
        {
          "title": "The Almanack of Naval Ravikant",
          "author": "Eric Jorgenson",
          "key_takeaway": "Complete compilation of Naval's wisdom on wealth and happiness"
        }
      ],
      "podcasts": [
        {
          "title": "Naval Podcast",
          "episode": "How to Get Rich (Without Getting Lucky)",
          "key_takeaway": "Complete framework for building wealth through leverage"
        }
      ]
    }
  }


def get_mock_masters_module(module: str = "money") -> Dict:
  """Get complete module JSON with multiple masters."""
  module_configs = {
    "money": {
      "module": "money",
      "daily_insights": [
        "Wealth is assets that earn while you sleep",
        "Your time is finite. Leverage is infinite.",
        "Build specific knowledge that can't be trained"
      ],
      "skill_challenges": [
        "Identify one skill gap preventing your next income level",
        "Calculate your true hourly rate today",
        "Research one new income stream opportunity"
      ]
    },
    "sales": {
      "module": "sales",
      "daily_insights": [
        "People buy emotionally and justify logically",
        "The fortune is in the follow-up",
        "Handle objections before they arise"
      ],
      "skill_challenges": [
        "Make 10 cold outreach contacts today",
        "Practice handling price objections for 15 minutes",
        "Ask for one referral from an existing client"
      ]
    },
    "productivity": {
      "module": "productivity",
      "daily_insights": [
        "Deep work produces disproportionate results",
        "Your environment shapes your behavior",
        "Energy management beats time management"
      ],
      "skill_challenges": [
        "Complete one 90-minute deep work block",
        "Eliminate your #1 distraction today",
        "Batch all meetings to one time block"
      ]
    }
  }

  config = module_configs.get(module, module_configs["money"])
  config["module"] = module

  config["level_definitions"] = {
    "1": {
      "name": "Awareness",
      "description": f"Beginning your {module} journey",
      "capabilities": ["Basic awareness", "Initial understanding"],
      "milestone": "Complete first learning milestone"
    },
    "5": {
      "name": "Competent",
      "description": f"Solid foundation in {module}",
      "capabilities": ["Consistent execution", "Good fundamentals"],
      "milestone": "Demonstrate consistent results"
    },
    "10": {
      "name": "Master",
      "description": f"Elite-level {module} mastery",
      "capabilities": ["Teaching others", "Creating new frameworks"],
      "milestone": "Recognized expert in field"
    }
  }

  config["progressive_exercises"] = {
    "beginner": [
      {
        "title": f"Intro to {module.title()}",
        "difficulty": 1,
        "time_minutes": 20,
        "instructions": f"Complete foundational exercise for {module}",
        "success_criteria": "Written reflection on key insights"
      }
    ],
    "intermediate": [
      {
        "title": f"Advanced {module.title()} Practice",
        "difficulty": 2,
        "time_minutes": 45,
        "instructions": f"Apply intermediate concepts in {module}",
        "success_criteria": "Demonstrated practical application"
      }
    ],
    "advanced": [
      {
        "title": f"Master-Level {module.title()}",
        "difficulty": 3,
        "time_minutes": 90,
        "instructions": f"Create new framework or teach {module}",
        "success_criteria": "Novel contribution or mentorship"
      }
    ]
  }

  config["cross_module_connections"] = [
    {
      "connected_module": "productivity",
      "insight": f"Combining {module} with productivity multiplies results",
      "combined_exercise": f"Apply deep work to your {module} practice"
    }
  ]

  config["masters"] = [get_mock_master()]

  return config
