"""
Self-Mastery OS - Action Planner
Generates personalized daily action plans based on user profile and state.
"""
import random
from datetime import datetime
from typing import Dict, List, Optional
from data_manager import DataManager
from utils import MODULE_NAMES, Colors

class ActionPlanner:
    """Generates personalized action plans based on user state."""

    def __init__(self, dm: DataManager):
        self.dm = dm
        self.profile = dm.get_user_profile()

        # Action templates by module
        self.actions = {
            "money": [
                {"text": "Spend 30 min on skill development", "time": 30, "difficulty": 2},
                {"text": "Send 1 networking message to valuable contact", "time": 10, "difficulty": 2},
                {"text": "Review and update income sources spreadsheet", "time": 15, "difficulty": 1},
                {"text": "Research one new income opportunity", "time": 20, "difficulty": 2},
                {"text": "Work on side project for 45 min", "time": 45, "difficulty": 3},
                {"text": "Read 1 chapter of wealth/business book", "time": 20, "difficulty": 1},
                {"text": "Identify 1 way to increase hourly rate", "time": 15, "difficulty": 2},
                {"text": "Apply to one opportunity or pitch one client", "time": 30, "difficulty": 3},
            ],
            "sales": [
                {"text": "Make 5 cold outreach touches (calls/emails)", "time": 30, "difficulty": 3},
                {"text": "Follow up with 3 warm leads", "time": 20, "difficulty": 2},
                {"text": "Practice objection handling for 10 min", "time": 10, "difficulty": 2},
                {"text": "Update CRM/pipeline tracker", "time": 15, "difficulty": 1},
                {"text": "Review and improve one sales script", "time": 20, "difficulty": 2},
                {"text": "Study 1 persuasion technique", "time": 15, "difficulty": 1},
                {"text": "Record and review your pitch", "time": 20, "difficulty": 2},
                {"text": "Ask for 1 referral from existing contact", "time": 10, "difficulty": 2},
            ],
            "finance": [
                {"text": "Review yesterday's spending", "time": 5, "difficulty": 1},
                {"text": "Check investment portfolio", "time": 10, "difficulty": 1},
                {"text": "Transfer to savings (pay yourself first)", "time": 5, "difficulty": 1},
                {"text": "Review monthly budget progress", "time": 15, "difficulty": 1},
                {"text": "Update net worth tracker", "time": 10, "difficulty": 1},
                {"text": "Research one investment topic", "time": 20, "difficulty": 2},
                {"text": "Find 1 expense to cut or optimize", "time": 15, "difficulty": 2},
                {"text": "Review and pay upcoming bills", "time": 10, "difficulty": 1},
            ],
            "dating": [
                {"text": "Start 1 conversation with a stranger", "time": 5, "difficulty": 3},
                {"text": "Send a genuine message to someone new", "time": 10, "difficulty": 2},
                {"text": "Practice active listening in next conversation", "time": 15, "difficulty": 2},
                {"text": "Attend 1 social event or activity", "time": 60, "difficulty": 3},
                {"text": "Reach out to a friend to make plans", "time": 10, "difficulty": 1},
                {"text": "Give 3 genuine compliments today", "time": 5, "difficulty": 2},
                {"text": "Reflect on recent social interaction: what went well?", "time": 10, "difficulty": 1},
                {"text": "Practice conversation opener in mirror", "time": 5, "difficulty": 2},
            ],
            "mindset": [
                {"text": "Morning journaling: intentions and gratitude", "time": 10, "difficulty": 1},
                {"text": "10 min meditation or breathing exercise", "time": 10, "difficulty": 1},
                {"text": "Read 1 chapter of personal development book", "time": 20, "difficulty": 1},
                {"text": "Identify 1 limiting belief and reframe it", "time": 15, "difficulty": 2},
                {"text": "Practice negative visualization (stoic exercise)", "time": 10, "difficulty": 2},
                {"text": "Write down 3 wins from yesterday", "time": 5, "difficulty": 1},
                {"text": "Review your personal rules/principles", "time": 10, "difficulty": 1},
                {"text": "Reflect: What would the best version of me do?", "time": 10, "difficulty": 1},
            ],
            "health": [
                {"text": "Complete workout (strength or cardio)", "time": 45, "difficulty": 3},
                {"text": "Take a 20-30 min walk", "time": 25, "difficulty": 1},
                {"text": "Prepare a healthy, high-protein meal", "time": 30, "difficulty": 2},
                {"text": "Do 10 min mobility/stretching routine", "time": 10, "difficulty": 1},
                {"text": "Get 10 min of morning sunlight", "time": 10, "difficulty": 1},
                {"text": "Drink 2L of water throughout day", "time": 0, "difficulty": 1},
                {"text": "No phone 1 hour before bed", "time": 0, "difficulty": 2},
                {"text": "Meal prep for tomorrow", "time": 30, "difficulty": 2},
            ],
            "lifestyle": [
                {"text": "Do 1 environment micro-improvement", "time": 15, "difficulty": 1},
                {"text": "Remove 1 source of friction from good habit", "time": 10, "difficulty": 1},
                {"text": "Add 1 friction to bad habit", "time": 10, "difficulty": 1},
                {"text": "Declutter one small area", "time": 15, "difficulty": 1},
                {"text": "Audit screen time and adjust", "time": 10, "difficulty": 2},
                {"text": "Unsubscribe from 5 emails", "time": 10, "difficulty": 1},
                {"text": "Prepare environment for tomorrow", "time": 15, "difficulty": 1},
                {"text": "Review and optimize one routine", "time": 20, "difficulty": 2},
            ],
            "business": [
                {"text": "Capture and score 1 new idea (ICE score)", "time": 10, "difficulty": 1},
                {"text": "Work on priority project for 45 min", "time": 45, "difficulty": 3},
                {"text": "Review project progress and next steps", "time": 15, "difficulty": 1},
                {"text": "Reach out to 1 professional contact", "time": 10, "difficulty": 2},
                {"text": "Document 1 process or learning", "time": 15, "difficulty": 1},
                {"text": "Research 1 topic for current project", "time": 20, "difficulty": 2},
                {"text": "Review key metrics for business/career", "time": 15, "difficulty": 1},
                {"text": "Brainstorm solutions to current challenge", "time": 20, "difficulty": 2},
            ],
            "productivity": [
                {"text": "Complete 1 deep work block (90 min)", "time": 90, "difficulty": 3},
                {"text": "Time-block tomorrow's calendar", "time": 15, "difficulty": 1},
                {"text": "Process inbox to zero", "time": 20, "difficulty": 2},
                {"text": "Complete your #1 priority task", "time": 60, "difficulty": 3},
                {"text": "Batch process admin tasks", "time": 30, "difficulty": 2},
                {"text": "Identify and eliminate 1 time waster", "time": 15, "difficulty": 2},
                {"text": "Set up 1 automation or template", "time": 30, "difficulty": 2},
                {"text": "Daily review: what got done, what didn't", "time": 10, "difficulty": 1},
            ]
        }

    def generate_daily_plan(
        self,
        energy_level: int,
        time_available: int = None,
        priorities: List[str] = None
    ) -> Dict:
        """Generate a personalized daily action plan."""

        if time_available is None:
            time_available = self.profile.get("daily_time_available_minutes", 60)

        focus_modules = self.profile.get("focus_modules", ["productivity", "health", "money"])

        plan = {
            "generated_at": datetime.now().isoformat(),
            "energy_level": energy_level,
            "time_available": time_available,
            "actions": [],
            "total_time": 0
        }

        # Adjust difficulty based on energy
        max_difficulty = 3 if energy_level >= 7 else (2 if energy_level >= 4 else 1)

        # Always include productivity and health
        required_modules = ["productivity", "health"]

        # Add focus modules
        selected_modules = list(set(required_modules + focus_modules[:2]))

        # Add variety from other modules
        other_modules = [m for m in MODULE_NAMES.keys() if m not in selected_modules]
        if other_modules:
            selected_modules.append(random.choice(other_modules))

        remaining_time = time_available

        for module in selected_modules:
            if remaining_time <= 0:
                break

            # Get suitable actions for this module
            module_actions = self.actions.get(module, [])
            suitable = [
                a for a in module_actions
                if a["difficulty"] <= max_difficulty and a["time"] <= remaining_time
            ]

            if suitable:
                # Pick 1-2 actions per module
                num_actions = min(2, len(suitable))
                if remaining_time < 30:
                    num_actions = 1

                chosen = random.sample(suitable, num_actions)

                for action in chosen:
                    plan["actions"].append({
                        "module": module,
                        "module_name": MODULE_NAMES[module],
                        "text": action["text"],
                        "time": action["time"],
                        "difficulty": action["difficulty"],
                        "completed": False
                    })
                    remaining_time -= action["time"]
                    plan["total_time"] += action["time"]

        # Sort by module priority
        module_order = {m: i for i, m in enumerate(selected_modules)}
        plan["actions"].sort(key=lambda x: module_order.get(x["module"], 99))

        return plan

    def get_priority_suggestions(self) -> List[str]:
        """Get suggested priorities based on goals and focus areas."""
        suggestions = []
        goals = self.dm.get_goals()

        # From 90-day goals
        quarterly = goals.get("quarterly_goals", {})
        for module, data in quarterly.items():
            if isinstance(data, dict) and data.get("goal"):
                suggestions.append(f"Progress on: {data['goal']}")

        # From top goals
        for goal in self.profile.get("top_goals", []):
            suggestions.append(f"Work toward: {goal}")

        # Generic high-leverage suggestions
        suggestions.extend([
            "Complete most important task first",
            "Deep work on priority project",
            "Move key deal/project forward"
        ])

        return suggestions[:5]

    def print_plan(self, plan: Dict):
        """Print the action plan in a nice format."""
        print(f"\n{Colors.BOLD}{Colors.CYAN}TODAY'S ACTION PLAN{Colors.ENDC}")
        print(f"{Colors.DIM}Energy: {plan['energy_level']}/10 | Time: {plan['time_available']} min{Colors.ENDC}\n")

        current_module = None

        for i, action in enumerate(plan["actions"], 1):
            if action["module"] != current_module:
                current_module = action["module"]
                print(f"\n{Colors.BOLD}[{action['module_name']}]{Colors.ENDC}")

            difficulty_stars = "*" * action["difficulty"]
            time_str = f"{action['time']}m" if action["time"] > 0 else "ongoing"

            status = "[+]" if action["completed"] else "[ ]"

            print(f"  {status} {action['text']}")
            print(f"      {Colors.DIM}({time_str}, {difficulty_stars}){Colors.ENDC}")

        print(f"\n{Colors.DIM}Total estimated time: {plan['total_time']} minutes{Colors.ENDC}")
