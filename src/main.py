#!/usr/bin/env python3
"""
Self-Mastery OS - Main Entry Point
A comprehensive personal development system.

Usage:
    python main.py              # Launch main menu
    python main.py am           # Quick morning check-in
    python main.py pm           # Quick evening reflection
    python main.py week         # Weekly review
    python main.py status       # Show status dashboard
"""
import sys
import os
from datetime import datetime

# Add src directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_manager import DataManager
from onboarding import run_onboarding, needs_onboarding
from daily_checkin import morning_checkin, evening_reflection
from weekly_review import weekly_review, show_progress_dashboard
from action_planner import ActionPlanner
from coaching import Coach
from wisdom_engine import WisdomEngine
from utils import (
    clear_screen, print_header, print_subheader, print_success,
    print_info, print_warning, print_error, print_coach,
    get_input, get_int_input, get_yes_no, get_choice,
    MODULE_NAMES, Colors, pause
)

# Get the base path (parent of src directory)
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main entry point."""
    dm = DataManager(BASE_PATH)

    # Handle command-line shortcuts
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()

        if cmd in ["am", "morning"]:
            if needs_onboarding(dm):
                run_onboarding(dm)
            morning_checkin(dm)
            return

        elif cmd in ["pm", "evening", "reflect"]:
            if needs_onboarding(dm):
                run_onboarding(dm)
            evening_reflection(dm)
            return

        elif cmd in ["week", "weekly", "review"]:
            if needs_onboarding(dm):
                run_onboarding(dm)
            weekly_review(dm)
            return

        elif cmd in ["status", "dash", "dashboard"]:
            if needs_onboarding(dm):
                run_onboarding(dm)
            show_progress_dashboard(dm)
            return

        elif cmd in ["patterns", "analyze"]:
            if needs_onboarding(dm):
                run_onboarding(dm)
            coach = Coach(dm)
            coach.print_pattern_report()
            pause()
            return

        elif cmd in ["wisdom", "w", "daily"]:
            if needs_onboarding(dm):
                run_onboarding(dm)
            wisdom = WisdomEngine(dm)
            clear_screen()
            wisdom.print_daily_wisdom()
            pause()
            return

        elif cmd in ["masters", "mentors"]:
            if needs_onboarding(dm):
                run_onboarding(dm)
            show_masters_library(dm)
            return

        elif cmd in ["help", "-h", "--help"]:
            print_help()
            return

    # Run main menu
    run_main_menu(dm)


def run_main_menu(dm: DataManager):
    """Run the main interactive menu."""

    # Check for onboarding
    if needs_onboarding(dm):
        run_onboarding(dm)

    while True:
        clear_screen()
        profile = dm.get_user_profile()

        # Show header with greeting
        hour = datetime.now().hour
        if hour < 12:
            greeting = "Good morning"
        elif hour < 17:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"

        print(f"""
{Colors.BOLD}{Colors.CYAN}================================================================
                    SELF-MASTERY OS v1.0
================================================================{Colors.ENDC}
  {greeting}, {profile.get('name', 'User')}
  {datetime.now().strftime('%A, %B %d, %Y')}
{Colors.BOLD}{Colors.CYAN}================================================================{Colors.ENDC}
""")

        # Show proactive wisdom insight
        wisdom = WisdomEngine(dm)
        daily_wisdom = wisdom.get_daily_wisdom()
        teaching = daily_wisdom["master_teaching"]

        print(f"{Colors.YELLOW}[{teaching['master']}]{Colors.ENDC} \"{teaching['teaching'][:80]}...\"")
        print(f"{Colors.DIM}Today's Challenge: {daily_wisdom['skill_challenge']['challenge'][:60]}...{Colors.ENDC}\n")

        # Menu options
        options = [
            "Morning Check-in      Start your day with wisdom",
            "Today's Wisdom        Full daily insights & challenge",
            "View Today's Plan     See your action items",
            "Log Habit/Metric      Quick tracking",
            "Evening Reflection    Review your day",
            "Weekly Review         Analyze & plan",
            "Masters Library       Learn from the greats",
            "Progress Dashboard    See your stats",
            "Pattern Analysis      AI coaching insights",
            "Settings & Profile    Update preferences",
            "Exit"
        ]

        print(f"{Colors.BOLD}MENU:{Colors.ENDC}")
        for i, opt in enumerate(options, 1):
            if i == len(options):
                print(f"  [{Colors.DIM}0{Colors.ENDC}] {opt}")
            else:
                name, desc = opt.split("  ", 1) if "  " in opt else (opt, "")
                print(f"  [{i}] {name:<22} {Colors.DIM}{desc}{Colors.ENDC}")

        print()
        choice = get_input("Select option (0-10)")

        try:
            choice = int(choice)
        except ValueError:
            continue

        if choice == 0 or choice == 11:
            clear_screen()
            print_coach("Keep showing up. Small daily gains compound into life-changing results.")
            print("\nGoodbye!\n")
            break

        elif choice == 1:
            # Show wisdom first, then morning check-in
            wisdom_engine = WisdomEngine(dm)
            clear_screen()
            wisdom_engine.print_daily_wisdom()
            pause()
            morning_checkin(dm)

        elif choice == 2:
            wisdom_engine = WisdomEngine(dm)
            clear_screen()
            wisdom_engine.print_daily_wisdom()
            pause()

        elif choice == 3:
            show_todays_plan(dm)

        elif choice == 4:
            quick_log(dm)

        elif choice == 5:
            evening_reflection(dm)

        elif choice == 6:
            weekly_review(dm)

        elif choice == 7:
            show_masters_library(dm)

        elif choice == 8:
            show_progress_dashboard(dm)

        elif choice == 9:
            coach = Coach(dm)
            clear_screen()
            coach.print_pattern_report()
            pause()

        elif choice == 10:
            settings_menu(dm)


def show_todays_plan(dm: DataManager):
    """Show today's action plan."""
    clear_screen()
    print_header("TODAY'S PLAN")

    today = datetime.now().strftime("%Y-%m-%d")
    log = dm.get_daily_log(today)

    if not log or not log.get("am_checkin"):
        print_warning("No morning check-in found for today.")
        print("Run the Morning Check-in first to generate your plan.")
        pause()
        return

    planner = ActionPlanner(dm)

    # Recreate plan from logged data
    plan = {
        "energy_level": log["am_checkin"].get("energy_level", 5),
        "time_available": dm.get_user_profile().get("daily_time_available_minutes", 60),
        "actions": log.get("planned_actions", []),
        "total_time": sum(a.get("time", 0) for a in log.get("planned_actions", []))
    }

    # Show priorities
    print_subheader("TOP PRIORITIES")
    for i, priority in enumerate(log["am_checkin"].get("top_3_priorities", []), 1):
        print(f"  {i}. {priority}")

    print(f"\n{Colors.BOLD}Win Definition:{Colors.ENDC} {log['am_checkin'].get('win_definition', 'Not set')}")

    # Show action plan
    planner.print_plan(plan)

    # Show completion status
    completed = log.get("completed_actions", [])
    total = len(plan["actions"])
    done = len([a for a in plan["actions"] if a.get("completed")])

    print(f"\n{Colors.BOLD}Progress:{Colors.ENDC} {done}/{total} actions completed")

    pause()


def quick_log(dm: DataManager):
    """Quick logging interface."""
    clear_screen()
    print_header("QUICK LOG")

    options = [
        "Log habit completion",
        "Log metric",
        "Mark task complete",
        "Add note",
        "Back to menu"
    ]

    choice = get_choice("What would you like to log?", options)

    today = datetime.now().strftime("%Y-%m-%d")
    log = dm.get_or_create_daily_log(today)

    if choice == 0:  # Habit
        habits_data = dm.get_habits()
        habits = habits_data.get("habits", [])

        if not habits:
            print_warning("No habits configured yet.")
            pause()
            return

        habit_names = [h["name"] for h in habits]
        habit_choice = get_choice("Select habit", habit_names)

        habit_id = habits[habit_choice]["id"]
        dm.record_habit_completion(habit_id, today)
        print_success(f"Recorded: {habits[habit_choice]['name']}")

    elif choice == 1:  # Metric
        print_subheader("LOG METRIC")

        metrics = log.get("metrics", {})

        metric_options = [
            "Deep work hours",
            "Workouts",
            "Sales calls",
            "Social interactions",
            "Steps",
            "Water (liters)"
        ]
        metric_keys = ["deep_work_hours", "workouts", "sales_calls",
                       "social_interactions", "steps", "water_liters"]

        metric_choice = get_choice("Select metric", metric_options)
        key = metric_keys[metric_choice]

        if key in ["deep_work_hours", "water_liters"]:
            value = get_input(f"Enter value for {metric_options[metric_choice]}")
            metrics[key] = float(value)
        else:
            value = get_input(f"Enter value for {metric_options[metric_choice]}")
            metrics[key] = int(value)

        log["metrics"] = metrics
        dm.save_daily_log(log, today)
        print_success(f"Logged: {metric_options[metric_choice]} = {value}")

    elif choice == 2:  # Task
        actions = log.get("planned_actions", [])

        if not actions:
            print_warning("No planned actions for today.")
            pause()
            return

        incomplete = [a for a in actions if not a.get("completed")]

        if not incomplete:
            print_success("All tasks already completed!")
            pause()
            return

        task_names = [a["text"] for a in incomplete]
        task_choice = get_choice("Select task to complete", task_names)

        incomplete[task_choice]["completed"] = True
        log["planned_actions"] = actions
        dm.save_daily_log(log, today)
        print_success(f"Completed: {incomplete[task_choice]['text']}")

    elif choice == 3:  # Note
        note = get_input("Enter note")
        existing_notes = log.get("notes", "")
        timestamp = datetime.now().strftime("%H:%M")
        log["notes"] = f"{existing_notes}\n[{timestamp}] {note}".strip()
        dm.save_daily_log(log, today)
        print_success("Note added!")

    pause()


def settings_menu(dm: DataManager):
    """Settings and profile menu."""
    while True:
        clear_screen()
        print_header("SETTINGS & PROFILE")

        profile = dm.get_user_profile()

        print(f"Name: {profile.get('name', 'Not set')}")
        print(f"Daily Time: {profile.get('daily_time_available_minutes', 60)} minutes")
        print(f"Coaching Style: {profile.get('coaching_style', 'balanced').title()}")
        print(f"Focus Areas: {', '.join(MODULE_NAMES.get(m, m) for m in profile.get('focus_modules', []))}")
        print()

        options = [
            "Update daily time",
            "Change coaching style",
            "Update focus modules",
            "Update module levels",
            "Manage habits",
            "View knowledge base",
            "Reset all data",
            "Back to menu"
        ]

        choice = get_choice("Select option", options)

        if choice == 0:  # Daily time
            time = get_int_input("Daily time available (minutes)", 15, 240)
            profile["daily_time_available_minutes"] = time
            dm.save_user_profile(profile)
            print_success("Updated!")

        elif choice == 1:  # Coaching style
            styles = ["Direct & Intense", "Balanced", "Gentle & Supportive"]
            style_choice = get_choice("Select style", styles)
            profile["coaching_style"] = ["direct", "balanced", "gentle"][style_choice]
            dm.save_user_profile(profile)
            print_success("Updated!")

        elif choice == 2:  # Focus modules
            from utils import get_multiple_choice
            module_list = list(MODULE_NAMES.values())
            focus_indices = get_multiple_choice("Select focus areas (up to 3)", module_list, 3)
            profile["focus_modules"] = [list(MODULE_NAMES.keys())[i] for i in focus_indices]
            dm.save_user_profile(profile)
            print_success("Updated!")

        elif choice == 3:  # Module levels
            print_subheader("UPDATE LEVELS")
            for key, name in MODULE_NAMES.items():
                current = profile.get("module_levels", {}).get(key, 5)
                new_level = get_int_input(f"  {name} (current: {current})", 1, 10, current)
                profile.setdefault("module_levels", {})[key] = new_level
            dm.save_user_profile(profile)
            print_success("Updated!")

        elif choice == 4:  # Manage habits
            manage_habits(dm)

        elif choice == 5:  # Knowledge base
            view_knowledge_base(dm)

        elif choice == 6:  # Reset
            if get_yes_no("Are you SURE you want to reset ALL data? This cannot be undone.", False):
                import shutil
                data_path = dm.data_path
                if data_path.exists():
                    shutil.rmtree(data_path)
                print_success("All data has been reset.")
                print_info("Please restart the application.")
                pause()
                sys.exit(0)

        elif choice == 7:
            break

        pause()


def manage_habits(dm: DataManager):
    """Manage habits interface."""
    clear_screen()
    print_subheader("MANAGE HABITS")

    habits_data = dm.get_habits()
    habits = habits_data.get("habits", [])

    print("Current habits:")
    for i, habit in enumerate(habits, 1):
        streak = habit.get("current_streak", 0)
        print(f"  {i}. {habit['name']} (Streak: {streak})")

    print()
    options = ["Add new habit", "Remove habit", "Back"]
    choice = get_choice("Select option", options)

    if choice == 0:  # Add
        name = get_input("Habit name")
        module_list = list(MODULE_NAMES.keys())
        module_names = list(MODULE_NAMES.values())
        module_choice = get_choice("Related module", module_names)

        dm.add_habit({
            "name": name,
            "module": module_list[module_choice],
            "frequency": "daily"
        })
        print_success(f"Added habit: {name}")

    elif choice == 1:  # Remove
        if habits:
            habit_names = [h["name"] for h in habits]
            remove_choice = get_choice("Select habit to remove", habit_names)
            habits.pop(remove_choice)
            habits_data["habits"] = habits
            dm.save_habits(habits_data)
            print_success("Habit removed.")


def view_knowledge_base(dm: DataManager):
    """View knowledge base content."""
    clear_screen()
    print_subheader("KNOWLEDGE BASE")

    topics = dm.get_knowledge_base_topics()

    if not topics:
        print_warning("No knowledge base files found.")
        pause()
        return

    # Create readable names
    topic_names = [t.replace("_", " ").title() for t in sorted(topics)]
    topic_names.append("Back")

    choice = get_choice("Select topic", topic_names)

    if choice < len(topics):
        content = dm.get_knowledge_base_content(sorted(topics)[choice])
        if content:
            clear_screen()
            # Just show the first part
            lines = content.split("\n")[:50]
            for line in lines:
                print(line)
            print(f"\n{Colors.DIM}... (showing first 50 lines){Colors.ENDC}")
            pause()


def show_masters_library(dm: DataManager):
    """Browse the masters library - teachings from world-class experts."""
    wisdom = WisdomEngine(dm)

    while True:
        clear_screen()
        print_header("MASTERS LIBRARY")

        print("Learn from the world's best in each domain:\n")

        # Get all masters organized by module
        modules_with_masters = []
        for module in MODULE_NAMES.keys():
            masters = wisdom.get_module_masters(module)
            if masters:
                modules_with_masters.append((module, masters))

        # Display modules
        for i, (module, masters) in enumerate(modules_with_masters, 1):
            module_name = MODULE_NAMES.get(module, module.title())
            master_names = ", ".join([m["name"] for m in masters[:3]])
            print(f"  [{i}] {module_name}")
            print(f"      {Colors.DIM}{master_names}{Colors.ENDC}")

        print(f"\n  [0] Back to menu")

        choice = get_input(f"\nSelect module (0-{len(modules_with_masters)})")

        try:
            choice = int(choice)
        except ValueError:
            continue

        if choice == 0:
            break

        if 1 <= choice <= len(modules_with_masters):
            module, masters = modules_with_masters[choice - 1]
            browse_module_masters(dm, module, masters)


def browse_module_masters(dm: DataManager, module: str, masters: list):
    """Browse masters within a specific module."""
    while True:
        clear_screen()
        module_name = MODULE_NAMES.get(module, module.title())
        print_header(f"{module_name.upper()} MASTERS")

        for i, master in enumerate(masters, 1):
            print(f"  [{i}] {master['name']}")
            print(f"      {Colors.DIM}{master.get('expertise', '')}{Colors.ENDC}")

        print(f"\n  [0] Back")

        choice = get_input(f"\nSelect master (0-{len(masters)})")

        try:
            choice = int(choice)
        except ValueError:
            continue

        if choice == 0:
            break

        if 1 <= choice <= len(masters):
            show_master_detail(masters[choice - 1])


def show_master_detail(master: dict):
    """Show detailed view of a single master."""
    clear_screen()

    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}")
    print(f"  {master['name'].upper()}")
    print(f"{'='*60}{Colors.ENDC}")
    print(f"\n{Colors.YELLOW}Expertise:{Colors.ENDC} {master.get('expertise', 'N/A')}")

    print(f"\n{Colors.BOLD}KEY PRINCIPLES:{Colors.ENDC}")
    for i, principle in enumerate(master.get("key_principles", []), 1):
        print(f"\n  {i}. \"{principle}\"")

    print(f"\n{Colors.BOLD}DAILY PRACTICES:{Colors.ENDC}")
    for practice in master.get("daily_practices", []):
        print(f"  - {practice}")

    print(f"\n{Colors.CYAN}{'='*60}{Colors.ENDC}")
    pause()


def print_help():
    """Print help information."""
    print(f"""
{Colors.BOLD}SELF-MASTERY OS - Command Line Usage{Colors.ENDC}

Usage: python main.py [command]

Commands:
  (no command)    Launch interactive menu
  am, morning     Run morning check-in
  pm, evening     Run evening reflection
  week, review    Run weekly review
  wisdom, daily   Show today's wisdom & insights
  masters         Browse masters library
  status, dash    Show progress dashboard
  patterns        Show pattern analysis
  help            Show this help message

Examples:
  python main.py              # Start the app
  python main.py am           # Quick morning check-in
  python main.py wisdom       # Get today's wisdom
  python main.py masters      # Browse expert teachings
""")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.DIM}Goodbye!{Colors.ENDC}\n")
        sys.exit(0)
