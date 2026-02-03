"""
Self-Mastery OS - Daily Check-ins
Handles morning and evening check-in flows.
"""
from datetime import datetime
from typing import Dict, Optional
from data_manager import DataManager
from action_planner import ActionPlanner
from utils import (
    clear_screen, print_header, print_subheader, print_success,
    print_info, print_warning, print_coach, get_input, get_int_input,
    get_float_input, get_list_input, get_yes_no, MODULE_NAMES,
    Colors, pause, progress_bar
)

def morning_checkin(dm: DataManager) -> Dict:
    """Run the morning check-in flow."""
    clear_screen()

    profile = dm.get_user_profile()
    today = datetime.now().strftime("%Y-%m-%d")
    log = dm.get_or_create_daily_log(today)

    # Check if already done today
    if log.get("am_checkin"):
        print_header("MORNING CHECK-IN")
        print_warning("You've already completed your morning check-in today.")

        if not get_yes_no("Would you like to redo it?", False):
            return log

    print_header(f"GOOD MORNING, {profile.get('name', 'Boss').upper()}")

    print_coach(get_morning_greeting(profile))
    print()

    # ==================== Sleep & Energy ====================
    print_subheader("SLEEP & ENERGY")

    sleep_hours = get_float_input("How many hours did you sleep?", 0, 12)
    sleep_quality = get_int_input("Rate your sleep quality", 1, 10)
    energy_level = get_int_input("Current energy level", 1, 10)

    # Sleep feedback
    if sleep_hours < 6:
        print_warning("Low sleep detected. Today's plan will prioritize recovery.")
    elif sleep_hours >= 7.5 and sleep_quality >= 7:
        print_success("Great sleep! You're primed for a high-performance day.")

    # ==================== Priorities ====================
    print_subheader("TODAY'S PRIORITIES")

    planner = ActionPlanner(dm)
    suggestions = planner.get_priority_suggestions()

    print("What are your TOP 3 priorities for today?")
    print(f"{Colors.DIM}Suggestions: {', '.join(suggestions[:3])}{Colors.ENDC}\n")

    priorities = get_list_input("Enter your priorities", min_items=1, max_items=3)

    # ==================== Win Definition ====================
    print_subheader("DEFINE SUCCESS")

    win_definition = get_input(
        "What ONE thing would make today a WIN?",
        priorities[0] if priorities else ""
    )

    # ==================== Generate Action Plan ====================
    print_subheader("YOUR ACTION PLAN")

    plan = planner.generate_daily_plan(
        energy_level=energy_level,
        time_available=profile.get("daily_time_available_minutes", 60)
    )

    planner.print_plan(plan)

    # ==================== Save Check-in ====================
    log["am_checkin"] = {
        "time": datetime.now().isoformat(),
        "sleep_hours": sleep_hours,
        "sleep_quality": sleep_quality,
        "energy_level": energy_level,
        "top_3_priorities": priorities,
        "win_definition": win_definition
    }
    log["planned_actions"] = plan["actions"]

    dm.save_daily_log(log, today)

    # ==================== Closing Message ====================
    print()
    print_coach(get_morning_closing(profile, energy_level))

    pause()
    return log


def evening_reflection(dm: DataManager) -> Dict:
    """Run the evening reflection flow."""
    clear_screen()

    profile = dm.get_user_profile()
    today = datetime.now().strftime("%Y-%m-%d")
    log = dm.get_or_create_daily_log(today)

    # Check if already done today
    if log.get("pm_reflection"):
        print_header("EVENING REFLECTION")
        print_warning("You've already completed your evening reflection today.")

        if not get_yes_no("Would you like to redo it?", False):
            return log

    print_header(f"EVENING REFLECTION")

    # ==================== Review Planned Actions ====================
    print_subheader("ACTION REVIEW")

    planned = log.get("planned_actions", [])
    completed_actions = []

    if planned:
        print("Let's review your planned actions:\n")

        for i, action in enumerate(planned):
            prompt = f"Did you complete: {action['text']}?"
            completed = get_yes_no(prompt, False)
            action["completed"] = completed
            if completed:
                completed_actions.append(action)
                print_success("Marked complete!")
            print()
    else:
        print("No planned actions found for today.\n")

    # ==================== Habit Tracking ====================
    print_subheader("HABIT CHECK")

    habits_data = dm.get_habits()
    daily_habits = [h for h in habits_data.get("habits", []) if h.get("frequency") == "daily"]

    if daily_habits:
        print("Check off completed habits:\n")

        for habit in daily_habits:
            completed = get_yes_no(f"  {habit['name']}?", False)
            if completed:
                dm.record_habit_completion(habit["id"], today)
                print_success(f"  {habit['name']} streak updated!")

    # ==================== Metrics ====================
    print_subheader("DAILY METRICS")

    metrics = log.get("metrics", {})

    metrics["deep_work_hours"] = get_float_input("Hours of deep work today", 0, 12,
                                                  metrics.get("deep_work_hours", 0))

    did_workout = get_yes_no("Did you work out?", False)
    metrics["workouts"] = 1 if did_workout else 0

    # Only ask relevant metrics based on focus
    focus_modules = profile.get("focus_modules", [])

    if "sales" in focus_modules:
        metrics["sales_calls"] = get_int_input("Sales calls/outreach today", 0, 50,
                                               metrics.get("sales_calls", 0))

    if "dating" in focus_modules or "social" in focus_modules:
        metrics["social_interactions"] = get_int_input("New conversations today", 0, 20,
                                                       metrics.get("social_interactions", 0))

    log["metrics"] = metrics

    # ==================== Wins ====================
    print_subheader("WINS & HIGHLIGHTS")

    print("What were your wins today? (Things that went well)")
    wins = get_list_input("Enter wins", min_items=1, max_items=5)

    # Check if main win was achieved
    if log.get("am_checkin", {}).get("win_definition"):
        main_win = log["am_checkin"]["win_definition"]
        achieved = get_yes_no(f"Did you achieve: '{main_win}'?", False)
        if achieved:
            print_success("Excellent! You achieved your main objective!")

    # ==================== Challenges ====================
    print_subheader("CHALLENGES & OBSTACLES")

    print("What challenges or obstacles did you face?")
    challenges = get_list_input("Enter challenges", min_items=0, max_items=3)

    # ==================== Lessons ====================
    print_subheader("LESSONS LEARNED")

    print("What did you learn today?")
    lessons = get_list_input("Enter lessons", min_items=0, max_items=3)

    # ==================== Tomorrow ====================
    print_subheader("LOOKING AHEAD")

    improvement = get_input("What's ONE thing you'll do differently tomorrow?")

    # ==================== Day Score ====================
    print_subheader("DAY SCORE")

    # Calculate suggested score
    completion_rate = len(completed_actions) / len(planned) if planned else 0.5
    suggested = min(10, max(1, round(completion_rate * 7 + 2)))

    print(f"Based on your completion rate ({completion_rate:.0%}), suggested score: {suggested}")
    day_score = get_int_input("Rate your overall day", 1, 10, suggested)

    # ==================== Save Reflection ====================
    log["pm_reflection"] = {
        "time": datetime.now().isoformat(),
        "wins": wins,
        "challenges": challenges,
        "lessons": lessons,
        "improvement_for_tomorrow": improvement,
        "day_score": day_score,
        "main_win_achieved": achieved if log.get("am_checkin", {}).get("win_definition") else None
    }
    log["completed_actions"] = completed_actions

    dm.save_daily_log(log, today)

    # ==================== Summary & Coaching ====================
    clear_screen()
    print_header("DAY SUMMARY")

    print(f"\n{Colors.BOLD}Day Score: {day_score}/10{Colors.ENDC}")
    print(f"Tasks Completed: {len(completed_actions)}/{len(planned)}")
    print(f"Deep Work: {metrics.get('deep_work_hours', 0)} hours")

    if wins:
        print(f"\n{Colors.GREEN}Top Win:{Colors.ENDC} {wins[0]}")

    if lessons:
        print(f"\n{Colors.CYAN}Key Lesson:{Colors.ENDC} {lessons[0]}")

    print(f"\n{Colors.YELLOW}Tomorrow's Focus:{Colors.ENDC} {improvement}")

    print()
    print_coach(get_evening_coaching(profile, day_score, len(completed_actions), len(planned)))

    pause()
    return log


def get_morning_greeting(profile: Dict) -> str:
    """Generate personalized morning greeting."""
    style = profile.get("coaching_style", "balanced")

    greetings = {
        "direct": [
            "Time to execute. Let's make today count.",
            "Another day, another opportunity. No excuses.",
            "Champions show up every day. Let's go."
        ],
        "balanced": [
            "Let's set you up for a productive day.",
            "Good morning! Ready to make progress?",
            "A new day means new opportunities to grow."
        ],
        "gentle": [
            "Welcome to a new day of growth.",
            "Take a moment to set your intentions.",
            "You're showing up, and that matters."
        ]
    }

    import random
    return random.choice(greetings.get(style, greetings["balanced"]))


def get_morning_closing(profile: Dict, energy: int) -> str:
    """Generate morning closing message based on energy."""
    if energy <= 3:
        return "Energy is low today. Focus on essentials, protect your recovery."
    elif energy <= 5:
        return "Moderate energy day. Pick your battles wisely."
    elif energy <= 7:
        return "Good energy level. You can tackle challenging work today."
    else:
        return "High energy! This is the day for your most important work."


def get_evening_coaching(profile: Dict, score: int, completed: int, planned: int) -> str:
    """Generate evening coaching message."""
    style = profile.get("coaching_style", "balanced")

    if completed == planned and planned > 0:
        return "100% completion. That's what execution looks like. Rest well."

    if score >= 8:
        return "Strong day. Build on this momentum tomorrow."
    elif score >= 6:
        return "Solid progress. Focus on what worked and do more of it."
    elif score >= 4:
        return "Some progress made. Tomorrow is a fresh start to do better."
    else:
        if style == "direct":
            return "Tough day. No excuses, no dwelling. Reset and attack tomorrow."
        else:
            return "Some days are harder than others. Rest, recover, and come back stronger."
