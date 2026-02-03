"""
Self-Mastery OS - Onboarding Flow
Collects initial user information and sets up the system.
"""
from datetime import datetime
from typing import Dict
from data_manager import DataManager
from utils import (
    clear_screen, print_header, print_subheader, print_success,
    print_info, print_coach, get_input, get_int_input, get_float_input,
    get_choice, get_multiple_choice, get_list_input, get_yes_no,
    MODULE_NAMES, pause, Colors
)

def run_onboarding(dm: DataManager) -> Dict:
    """Run the complete onboarding flow."""
    clear_screen()

    print_header("SELF-MASTERY OS - ONBOARDING")

    print(f"""
{Colors.CYAN}Welcome to your personal Self-Mastery Operating System.{Colors.ENDC}

This system will help you systematically improve across all critical
areas of your life through:

  - Daily planning and check-ins
  - Habit and metric tracking
  - Weekly reviews and coaching
  - Adaptive guidance based on your progress

Let's set up your profile so I can customize the experience for you.
""")

    pause()

    profile = {}

    # ==================== Basic Info ====================
    clear_screen()
    print_subheader("STEP 1: Basic Information")

    profile["name"] = get_input("What should I call you?", "Boss")
    profile["created_at"] = datetime.now().isoformat()

    print(f"\nGood to meet you, {profile['name']}.\n")

    # Time available
    print("How much time can you dedicate to personal growth each day?")
    time_options = [
        "30 minutes (Minimal - focused actions only)",
        "60 minutes (Standard - balanced growth)",
        "90 minutes (Committed - accelerated progress)",
        "120+ minutes (All-in - maximum growth mode)"
    ]
    time_choice = get_choice("Daily time commitment", time_options)
    time_values = [30, 60, 90, 120]
    profile["daily_time_available_minutes"] = time_values[time_choice]

    # ==================== Coaching Style ====================
    clear_screen()
    print_subheader("STEP 2: Coaching Style")

    print("How do you prefer to be coached?\n")
    style_options = [
        "Direct & Intense - High accountability, no sugarcoating, push me hard",
        "Balanced - Firm but supportive, celebrate wins but address issues",
        "Gentle & Supportive - Encouraging, focus on progress not perfection"
    ]
    style_choice = get_choice("Preferred coaching style", style_options)
    style_values = ["direct", "balanced", "gentle"]
    profile["coaching_style"] = style_values[style_choice]

    # ==================== Module Levels ====================
    clear_screen()
    print_subheader("STEP 3: Current Level Assessment")

    print("Rate your current level in each life area (1-10):")
    print("  1-3: Beginner / Struggling")
    print("  4-6: Intermediate / Okay")
    print("  7-9: Advanced / Good")
    print("  10: Mastery\n")

    profile["module_levels"] = {}

    for key, name in MODULE_NAMES.items():
        level = get_int_input(f"  {name}", 1, 10)
        profile["module_levels"][key] = level

    # ==================== Focus Modules ====================
    clear_screen()
    print_subheader("STEP 4: Priority Focus Areas")

    print("Which areas do you want to focus on first?")
    print("(You can work on all areas, but we'll prioritize these)\n")

    module_list = list(MODULE_NAMES.values())
    module_keys = list(MODULE_NAMES.keys())

    focus_indices = get_multiple_choice(
        "Select your top 3 focus areas",
        module_list,
        max_choices=3
    )
    profile["focus_modules"] = [module_keys[i] for i in focus_indices]

    # ==================== Top Goals ====================
    clear_screen()
    print_subheader("STEP 5: Top Life Goals")

    print("What are your TOP 3 life goals right now?")
    print("Be specific. These will guide your daily actions.\n")

    profile["top_goals"] = get_list_input(
        "Enter your goals",
        min_items=1,
        max_items=3
    )

    # ==================== Constraints ====================
    clear_screen()
    print_subheader("STEP 6: Current Constraints")

    print("What are your biggest constraints right now?")
    print("(Select all that apply)\n")

    constraint_options = [
        "Time - Very busy schedule",
        "Money - Limited budget for tools/courses",
        "Energy - Often tired or low energy",
        "Knowledge - Need to learn more",
        "Environment - Living situation not ideal",
        "Social - Limited support network"
    ]

    constraint_indices = get_multiple_choice(
        "Select your constraints",
        constraint_options,
        max_choices=4
    )
    constraint_keys = ["time", "money", "energy", "knowledge", "environment", "social"]
    profile["constraints"] = [constraint_keys[i] for i in constraint_indices]

    # ==================== 90-Day Goals ====================
    clear_screen()
    print_subheader("STEP 7: 90-Day Goals")

    print("Let's set specific 90-day goals for your focus areas.\n")

    profile["goals_90_day"] = {}

    for module_key in profile["focus_modules"]:
        module_name = MODULE_NAMES[module_key]
        print(f"\n{Colors.BOLD}{module_name}{Colors.ENDC}")
        print(f"(Current level: {profile['module_levels'][module_key]}/10)")

        goal = get_input(f"What do you want to achieve in 90 days for {module_name}?")
        target_level = get_int_input(
            f"Target level in 90 days",
            profile["module_levels"][module_key],
            10,
            min(profile["module_levels"][module_key] + 2, 10)
        )

        profile["goals_90_day"][module_key] = {
            "goal": goal,
            "target_level": target_level,
            "start_level": profile["module_levels"][module_key],
            "created_at": datetime.now().isoformat()
        }

    # ==================== Initial Habits ====================
    clear_screen()
    print_subheader("STEP 8: Core Habits")

    print("I'll set up some core habits for you to track.")
    print("You can customize these later.\n")

    default_habits = [
        {"id": "morning_routine", "name": "Morning Routine", "module": "productivity", "frequency": "daily"},
        {"id": "workout", "name": "Workout", "module": "health", "frequency": "daily"},
        {"id": "deep_work", "name": "Deep Work Block", "module": "productivity", "frequency": "daily"},
        {"id": "journaling", "name": "Journaling", "module": "mindset", "frequency": "daily"},
        {"id": "reading", "name": "Reading (20+ min)", "module": "mindset", "frequency": "daily"}
    ]

    print("Default habits:")
    for h in default_habits:
        print(f"  - {h['name']} ({h['module'].title()})")

    if get_yes_no("\nUse these default habits?", True):
        profile["initial_habits"] = default_habits
    else:
        profile["initial_habits"] = []
        print("\nEnter your custom habits (you can add more later):")
        custom_habits = get_list_input("Habit names", min_items=1, max_items=5)
        for i, name in enumerate(custom_habits):
            profile["initial_habits"].append({
                "id": f"custom_{i+1}",
                "name": name,
                "module": "productivity",
                "frequency": "daily"
            })

    # ==================== Summary & Confirmation ====================
    clear_screen()
    print_header("PROFILE SUMMARY")

    print(f"Name: {profile['name']}")
    print(f"Daily Time: {profile['daily_time_available_minutes']} minutes")
    print(f"Coaching Style: {profile['coaching_style'].title()}")
    print(f"\nFocus Areas: {', '.join(MODULE_NAMES[k] for k in profile['focus_modules'])}")
    print(f"Constraints: {', '.join(profile['constraints'])}")

    print(f"\n{Colors.BOLD}Top Goals:{Colors.ENDC}")
    for goal in profile["top_goals"]:
        print(f"  - {goal}")

    print(f"\n{Colors.BOLD}90-Day Goals:{Colors.ENDC}")
    for key, data in profile["goals_90_day"].items():
        print(f"  {MODULE_NAMES[key]}: {data['goal']}")
        print(f"    (Target: {data['start_level']} → {data['target_level']})")

    print()
    if not get_yes_no("Does this look correct?", True):
        print_info("You can update your profile anytime from Settings.")

    # Save profile
    dm.save_user_profile(profile)

    # Initialize habits
    for habit in profile.get("initial_habits", []):
        dm.add_habit(habit)

    # Initialize goals
    dm.save_goals({
        "lifetime_vision": "",
        "yearly_goals": [],
        "quarterly_goals": profile["goals_90_day"],
        "monthly_goals": [],
        "weekly_goals": []
    })

    # Final message
    clear_screen()
    print_header("SETUP COMPLETE")

    print_coach(f"""
{profile['name']}, your Self-Mastery OS is now configured.

Here's what happens next:

1. Every MORNING, run the AM Check-in to:
   - Log your sleep and energy
   - Set your top 3 priorities
   - Get a personalized action plan

2. Throughout the DAY:
   - Mark habits and tasks as complete
   - Track your metrics

3. Every EVENING, run the PM Reflection to:
   - Review your wins and lessons
   - Score your day
   - Prepare for tomorrow

4. Every WEEK, run the Weekly Review to:
   - Analyze your progress
   - Adjust your approach
   - Set next week's targets

Let's start strong. Run the AM Check-in to begin your first day.
""")

    pause()
    return profile

def needs_onboarding(dm: DataManager) -> bool:
    """Check if user needs to complete onboarding."""
    return not dm.user_exists()
