"""
Self-Mastery OS - Weekly Review
Handles weekly review and planning flows.
"""
from datetime import datetime, timedelta
from typing import Dict, List
from data_manager import DataManager
from utils import (
    clear_screen, print_header, print_subheader, print_success,
    print_info, print_warning, print_coach, print_score,
    get_input, get_int_input, get_list_input, get_yes_no,
    get_choice, MODULE_NAMES, Colors, pause, progress_bar
)

def weekly_review(dm: DataManager) -> Dict:
    """Run the weekly review flow."""
    clear_screen()

    profile = dm.get_user_profile()

    # Get date range for the week
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)

    week_str = today.strftime("%Y-W%W")

    # Check for existing review
    existing_review = dm.get_weekly_review(week_str)
    if existing_review:
        print_header("WEEKLY REVIEW")
        print_warning("You've already completed a review for this week.")

        if not get_yes_no("Would you like to redo it?", False):
            return existing_review

    print_header("WEEKLY REVIEW")
    print(f"Week: {week_start.strftime('%b %d')} - {week_end.strftime('%b %d, %Y')}\n")

    # ==================== Gather Week Data ====================
    logs = dm.get_logs_for_range(
        week_start.strftime("%Y-%m-%d"),
        week_end.strftime("%Y-%m-%d")
    )

    # Calculate stats
    stats = calculate_week_stats(logs)

    # ==================== Progress Summary ====================
    print_subheader("WEEK AT A GLANCE")

    print(f"Days Logged: {stats['days_logged']}/7")
    print(f"AM Check-ins: {stats['am_checkins']}/7")
    print(f"PM Reflections: {stats['pm_reflections']}/7")
    print()

    if stats['avg_day_score'] > 0:
        print_score("Average Day Score", stats['avg_day_score'])
    if stats['avg_sleep'] > 0:
        print(f"  Average Sleep: {stats['avg_sleep']:.1f} hours")
    if stats['avg_energy'] > 0:
        print_score("Average Energy", stats['avg_energy'])

    print(f"\n  Deep Work Hours: {stats['total_deep_work']:.1f}")
    print(f"  Workouts: {stats['total_workouts']}")
    print(f"  Task Completion: {progress_bar(stats['tasks_completed'], stats['tasks_planned'])}")

    pause()

    # ==================== Habit Analysis ====================
    clear_screen()
    print_subheader("HABIT STREAKS")

    habits_data = dm.get_habits()
    daily_habits = [h for h in habits_data.get("habits", []) if h.get("frequency") == "daily"]

    for habit in daily_habits:
        streak = habit.get("current_streak", 0)
        best = habit.get("best_streak", 0)

        streak_bar = progress_bar(min(streak, 7), 7)
        flame = " [FIRE]" if streak >= 7 else ""

        print(f"  {habit['name']}: {streak} days {streak_bar}{flame}")
        if best > streak:
            print(f"    {Colors.DIM}(Best: {best} days){Colors.ENDC}")

    pause()

    # ==================== Module Scores ====================
    clear_screen()
    print_subheader("MODULE PERFORMANCE")

    print("Rate your performance in each focus area this week:\n")

    module_scores = {}
    focus_modules = profile.get("focus_modules", ["productivity", "health", "money"])

    for module in focus_modules:
        name = MODULE_NAMES.get(module, module.title())
        score = get_int_input(f"  {name}", 1, 10)
        module_scores[module] = score

    # ==================== Wins & Lessons ====================
    clear_screen()
    print_subheader("TOP WINS THIS WEEK")

    # Show wins from daily logs
    all_wins = []
    for log in logs:
        if log.get("pm_reflection", {}).get("wins"):
            all_wins.extend(log["pm_reflection"]["wins"])

    if all_wins:
        print("Wins from your daily reflections:")
        for win in all_wins[:5]:
            print(f"  - {win}")
        print()

    print("What were your TOP 3 wins this week?")
    top_wins = get_list_input("Enter wins", min_items=1, max_items=3)

    clear_screen()
    print_subheader("KEY LESSONS")

    # Show lessons from daily logs
    all_lessons = []
    for log in logs:
        if log.get("pm_reflection", {}).get("lessons"):
            all_lessons.extend(log["pm_reflection"]["lessons"])

    if all_lessons:
        print("Lessons from your daily reflections:")
        for lesson in all_lessons[:5]:
            print(f"  - {lesson}")
        print()

    print("What were your KEY lessons this week?")
    key_lessons = get_list_input("Enter lessons", min_items=1, max_items=3)

    # ==================== What Worked / What Didn't ====================
    clear_screen()
    print_subheader("ANALYSIS")

    print("What MOVED THE NEEDLE most this week?")
    needle_movers = get_list_input("Enter what worked", min_items=1, max_items=3)

    print("\nWhat was a WASTE OF TIME this week?")
    time_wasters = get_list_input("Enter time wasters", min_items=0, max_items=3)

    print("\nWhat SYSTEMS or HABITS need adjustment?")
    adjustments = get_list_input("Enter adjustments", min_items=0, max_items=3)

    # ==================== Next Week Planning ====================
    clear_screen()
    print_subheader("NEXT WEEK PLANNING")

    # Focus theme
    print("Choose a focus theme for next week:\n")
    themes = [
        "Deep Work Sprint - Maximize focused output",
        "Sales/Outreach Push - Increase activity volume",
        "Health Reset - Prioritize sleep, exercise, nutrition",
        "Learning Focus - Skill development priority",
        "Social Expansion - More connections and interactions",
        "Business Building - Project and revenue focus",
        "Recovery Week - Lighter load, consolidate gains",
        "Custom theme"
    ]

    theme_choice = get_choice("Select theme", themes)

    if theme_choice == len(themes) - 1:
        focus_theme = get_input("Enter your custom theme")
    else:
        focus_theme = themes[theme_choice].split(" - ")[0]

    # Specific targets
    print(f"\n{Colors.BOLD}Set targets for next week:{Colors.ENDC}\n")

    next_week_targets = {}

    for module in focus_modules:
        name = MODULE_NAMES.get(module, module.title())
        target = get_input(f"  {name} target")
        if target:
            next_week_targets[module] = target

    # Experiments
    print("\nWhat NEW experiment or behavior will you try next week?")
    experiments = get_list_input("Enter experiments", min_items=0, max_items=2)

    # ==================== Save Review ====================
    review = {
        "week": week_str,
        "start_date": week_start.strftime("%Y-%m-%d"),
        "end_date": week_end.strftime("%Y-%m-%d"),
        "created_at": datetime.now().isoformat(),
        "stats": stats,
        "module_scores": module_scores,
        "top_wins": top_wins,
        "key_lessons": key_lessons,
        "needle_movers": needle_movers,
        "time_wasters": time_wasters,
        "adjustments": adjustments,
        "next_week_focus": focus_theme,
        "next_week_targets": next_week_targets,
        "experiments": experiments
    }

    dm.save_weekly_review(review, week_str)

    # ==================== Summary ====================
    clear_screen()
    print_header("WEEKLY REVIEW COMPLETE")

    overall_score = sum(module_scores.values()) / len(module_scores) if module_scores else 5

    print(f"\n{Colors.BOLD}Overall Week Score: {overall_score:.1f}/10{Colors.ENDC}")
    print(f"Next Week Theme: {Colors.CYAN}{focus_theme}{Colors.ENDC}")

    print(f"\n{Colors.BOLD}Top Win:{Colors.ENDC}")
    print(f"  {top_wins[0]}")

    print(f"\n{Colors.BOLD}Key Lesson:{Colors.ENDC}")
    print(f"  {key_lessons[0]}")

    if experiments:
        print(f"\n{Colors.BOLD}Experiment:{Colors.ENDC}")
        print(f"  {experiments[0]}")

    print()
    print_coach(get_weekly_coaching(profile, overall_score, stats))

    pause()
    return review


def calculate_week_stats(logs: List[Dict]) -> Dict:
    """Calculate statistics from daily logs."""
    stats = {
        "days_logged": len(logs),
        "am_checkins": 0,
        "pm_reflections": 0,
        "avg_day_score": 0,
        "avg_sleep": 0,
        "avg_energy": 0,
        "total_deep_work": 0,
        "total_workouts": 0,
        "tasks_completed": 0,
        "tasks_planned": 0
    }

    day_scores = []
    sleep_hours = []
    energy_levels = []

    for log in logs:
        if log.get("am_checkin"):
            stats["am_checkins"] += 1
            if log["am_checkin"].get("sleep_hours"):
                sleep_hours.append(log["am_checkin"]["sleep_hours"])
            if log["am_checkin"].get("energy_level"):
                energy_levels.append(log["am_checkin"]["energy_level"])

        if log.get("pm_reflection"):
            stats["pm_reflections"] += 1
            if log["pm_reflection"].get("day_score"):
                day_scores.append(log["pm_reflection"]["day_score"])

        if log.get("metrics"):
            stats["total_deep_work"] += log["metrics"].get("deep_work_hours", 0)
            stats["total_workouts"] += log["metrics"].get("workouts", 0)

        stats["tasks_completed"] += len(log.get("completed_actions", []))
        stats["tasks_planned"] += len(log.get("planned_actions", []))

    if day_scores:
        stats["avg_day_score"] = sum(day_scores) / len(day_scores)
    if sleep_hours:
        stats["avg_sleep"] = sum(sleep_hours) / len(sleep_hours)
    if energy_levels:
        stats["avg_energy"] = sum(energy_levels) / len(energy_levels)

    return stats


def get_weekly_coaching(profile: Dict, score: float, stats: Dict) -> str:
    """Generate weekly coaching message."""

    messages = []

    # Score-based message
    if score >= 8:
        messages.append("Excellent week! You're building serious momentum.")
    elif score >= 6:
        messages.append("Solid progress. Keep refining your systems.")
    elif score >= 4:
        messages.append("Room for improvement, but you showed up. That counts.")
    else:
        messages.append("Tough week. Learn from it, reset, and come back stronger.")

    # Sleep insight
    if stats.get("avg_sleep", 0) < 6.5:
        messages.append("Watch your sleep - it's the foundation of performance.")

    # Consistency insight
    if stats.get("am_checkins", 0) < 4:
        messages.append("More consistent check-ins will help you stay on track.")

    # Deep work insight
    if stats.get("total_deep_work", 0) < 10:
        messages.append("Consider protecting more deep work time next week.")

    return " ".join(messages[:3])


def show_progress_dashboard(dm: DataManager):
    """Show a progress dashboard."""
    clear_screen()
    print_header("PROGRESS DASHBOARD")

    profile = dm.get_user_profile()
    stats = dm.get_stats()
    habits_data = dm.get_habits()

    # ==================== Overview ====================
    print_subheader("30-DAY OVERVIEW")

    print(f"  Days Logged: {stats['total_days_logged']}")
    print(f"  AM Check-ins: {stats['am_checkins']}")
    print(f"  PM Reflections: {stats['pm_reflections']}")
    print()

    if stats['avg_day_score'] > 0:
        print_score("Average Day Score", stats['avg_day_score'])
    if stats['avg_sleep'] > 0:
        print(f"  Average Sleep: {stats['avg_sleep']:.1f} hours")
    if stats['avg_energy'] > 0:
        print_score("Average Energy", stats['avg_energy'])

    print(f"\n  Total Deep Work: {stats['total_deep_work_hours']:.1f} hours")
    print(f"  Total Workouts: {stats['total_workouts']}")

    if stats['habit_completion_rate'] > 0:
        print(f"  Habit Completion: {stats['habit_completion_rate']:.0f}%")

    # ==================== Habit Streaks ====================
    print_subheader("CURRENT STREAKS")

    habits = habits_data.get("habits", [])
    for habit in habits:
        streak = habit.get("current_streak", 0)
        best = habit.get("best_streak", 0)
        total = habit.get("total_completions", 0)

        flame = " [FIRE]" if streak >= 7 else ""
        print(f"  {habit['name']}: {streak} days{flame}")
        print(f"    {Colors.DIM}Best: {best} | Total: {total}{Colors.ENDC}")

    # ==================== 90-Day Goals ====================
    print_subheader("90-DAY GOALS PROGRESS")

    goals = dm.get_goals()
    quarterly = goals.get("quarterly_goals", {})

    for module, data in quarterly.items():
        if isinstance(data, dict):
            name = MODULE_NAMES.get(module, module.title())
            start = data.get("start_level", 5)
            target = data.get("target_level", 10)
            current = profile.get("module_levels", {}).get(module, start)

            progress = (current - start) / (target - start) if target > start else 0

            print(f"  {name}: {current}/10 (Target: {target})")
            print(f"    {progress_bar(progress, 1)}")
            print(f"    {Colors.DIM}Goal: {data.get('goal', 'Not set')}{Colors.ENDC}")
            print()

    pause()
