"""
Self-Mastery OS - Adaptive Coaching
Provides pattern-based coaching and guidance.
"""
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from data_manager import DataManager
from utils import (
    print_coach, print_warning, print_info, print_success,
    MODULE_NAMES, Colors
)

class Coach:
    """Adaptive coaching system based on user patterns."""

    def __init__(self, dm: DataManager):
        self.dm = dm
        self.profile = dm.get_user_profile()
        self.style = self.profile.get("coaching_style", "balanced")

    def analyze_patterns(self) -> Dict:
        """Analyze user patterns from recent data."""
        logs = self.dm.get_recent_logs(14)  # Two weeks

        patterns = {
            "sleep_trend": self._analyze_sleep(logs),
            "energy_trend": self._analyze_energy(logs),
            "consistency": self._analyze_consistency(logs),
            "completion_rate": self._analyze_completion(logs),
            "habit_issues": self._analyze_habits(),
            "strengths": [],
            "areas_for_improvement": []
        }

        # Identify strengths and improvements
        if patterns["sleep_trend"]["average"] >= 7:
            patterns["strengths"].append("solid sleep habits")
        else:
            patterns["areas_for_improvement"].append("sleep optimization")

        if patterns["consistency"]["checkin_rate"] >= 0.8:
            patterns["strengths"].append("consistent daily check-ins")
        else:
            patterns["areas_for_improvement"].append("daily check-in consistency")

        if patterns["completion_rate"]["rate"] >= 0.7:
            patterns["strengths"].append("strong task execution")
        else:
            patterns["areas_for_improvement"].append("task completion")

        return patterns

    def _analyze_sleep(self, logs: List[Dict]) -> Dict:
        """Analyze sleep patterns."""
        sleep_hours = []
        for log in logs:
            if log.get("am_checkin", {}).get("sleep_hours"):
                sleep_hours.append(log["am_checkin"]["sleep_hours"])

        if not sleep_hours:
            return {"average": 0, "trend": "unknown", "low_days": 0}

        avg = sum(sleep_hours) / len(sleep_hours)
        low_days = sum(1 for h in sleep_hours if h < 6)

        # Calculate trend
        if len(sleep_hours) >= 5:
            first_half = sum(sleep_hours[:len(sleep_hours)//2]) / (len(sleep_hours)//2)
            second_half = sum(sleep_hours[len(sleep_hours)//2:]) / (len(sleep_hours) - len(sleep_hours)//2)

            if second_half > first_half + 0.5:
                trend = "improving"
            elif second_half < first_half - 0.5:
                trend = "declining"
            else:
                trend = "stable"
        else:
            trend = "insufficient_data"

        return {"average": avg, "trend": trend, "low_days": low_days}

    def _analyze_energy(self, logs: List[Dict]) -> Dict:
        """Analyze energy patterns."""
        energy_levels = []
        for log in logs:
            if log.get("am_checkin", {}).get("energy_level"):
                energy_levels.append(log["am_checkin"]["energy_level"])

        if not energy_levels:
            return {"average": 0, "trend": "unknown", "low_days": 0}

        avg = sum(energy_levels) / len(energy_levels)
        low_days = sum(1 for e in energy_levels if e < 5)

        return {"average": avg, "trend": "stable", "low_days": low_days}

    def _analyze_consistency(self, logs: List[Dict]) -> Dict:
        """Analyze consistency of check-ins."""
        am_checkins = sum(1 for log in logs if log.get("am_checkin"))
        pm_reflections = sum(1 for log in logs if log.get("pm_reflection"))

        return {
            "days_logged": len(logs),
            "am_checkins": am_checkins,
            "pm_reflections": pm_reflections,
            "checkin_rate": am_checkins / 14 if logs else 0,
            "reflection_rate": pm_reflections / 14 if logs else 0
        }

    def _analyze_completion(self, logs: List[Dict]) -> Dict:
        """Analyze task completion rates."""
        total_planned = 0
        total_completed = 0

        for log in logs:
            planned = len(log.get("planned_actions", []))
            completed = len(log.get("completed_actions", []))
            total_planned += planned
            total_completed += completed

        rate = total_completed / total_planned if total_planned > 0 else 0

        return {
            "total_planned": total_planned,
            "total_completed": total_completed,
            "rate": rate
        }

    def _analyze_habits(self) -> List[str]:
        """Analyze habit performance issues."""
        habits_data = self.dm.get_habits()
        issues = []

        for habit in habits_data.get("habits", []):
            streak = habit.get("current_streak", 0)
            best = habit.get("best_streak", 0)

            # Detect broken streaks
            if best > 5 and streak == 0:
                issues.append(f"'{habit['name']}' streak broken (was {best} days)")

            # Detect never-started habits
            if habit.get("total_completions", 0) == 0:
                issues.append(f"'{habit['name']}' never completed")

        return issues

    def get_daily_insight(self) -> Optional[str]:
        """Get a contextual insight for today."""
        patterns = self.analyze_patterns()
        insights = []

        # Sleep insights
        sleep = patterns["sleep_trend"]
        if sleep["low_days"] >= 3:
            insights.append(
                "You've had multiple low-sleep days recently. "
                "Sleep debt compounds. Prioritize recovery tonight."
            )
        elif sleep["trend"] == "improving":
            insights.append(
                "Your sleep has been improving. Keep protecting your bedtime."
            )

        # Consistency insights
        if patterns["consistency"]["checkin_rate"] < 0.5:
            insights.append(
                "You've missed several check-ins. The system works best with daily input. "
                "Even a quick check-in is better than none."
            )

        # Completion insights
        if patterns["completion_rate"]["rate"] < 0.5:
            insights.append(
                "Task completion has been low. Consider reducing the number of planned tasks "
                "or breaking them into smaller pieces."
            )
        elif patterns["completion_rate"]["rate"] >= 0.9:
            insights.append(
                "You're crushing your tasks. Time to raise the bar and add more challenge."
            )

        # Habit insights
        if patterns["habit_issues"]:
            issue = patterns["habit_issues"][0]
            insights.append(f"Habit alert: {issue}. Restart with a smaller commitment.")

        return random.choice(insights) if insights else None

    def get_coaching_message(self, context: str, data: Dict = None) -> str:
        """Get a coaching message for a specific context."""

        messages = {
            "low_energy": {
                "direct": "Energy is low. Do the essentials, skip the extras. Rest is productive.",
                "balanced": "Low energy day. Focus on must-dos and be kind to yourself.",
                "gentle": "Take it easy today. Even small progress counts."
            },
            "high_energy": {
                "direct": "High energy. Attack your hardest tasks. No wasting this day.",
                "balanced": "Great energy! Use it for challenging work.",
                "gentle": "You're feeling good. A perfect day for meaningful work."
            },
            "missed_workout": {
                "direct": "Missed the workout. Non-negotiable. Make it happen tomorrow.",
                "balanced": "Workout missed today. Schedule it first thing tomorrow.",
                "gentle": "No workout today, and that's okay. Tomorrow is a new chance."
            },
            "streak_broken": {
                "direct": "Streak broken. Don't chain failures. Start fresh NOW.",
                "balanced": "Streak ended. What matters is starting again immediately.",
                "gentle": "The streak ended, but you can start a new one today."
            },
            "good_score": {
                "direct": "Good day. Now do it again. Consistency beats intensity.",
                "balanced": "Solid performance today. Keep building momentum.",
                "gentle": "You did well today. Celebrate this progress."
            },
            "poor_score": {
                "direct": "Below standard. Identify what failed. Fix it tomorrow.",
                "balanced": "Tough day. Learn from it and move forward.",
                "gentle": "Some days are hard. Rest and try again tomorrow."
            }
        }

        context_messages = messages.get(context, {})
        return context_messages.get(self.style, context_messages.get("balanced", "Keep going."))

    def print_pattern_report(self):
        """Print a full pattern analysis report."""
        patterns = self.analyze_patterns()

        print(f"\n{Colors.BOLD}{Colors.CYAN}PATTERN ANALYSIS{Colors.ENDC}\n")

        # Sleep
        sleep = patterns["sleep_trend"]
        print(f"Sleep:")
        print(f"  Average: {sleep['average']:.1f} hours")
        print(f"  Trend: {sleep['trend']}")
        if sleep["low_days"] > 0:
            print(f"  {Colors.YELLOW}Warning: {sleep['low_days']} low-sleep days{Colors.ENDC}")

        # Energy
        energy = patterns["energy_trend"]
        print(f"\nEnergy:")
        print(f"  Average: {energy['average']:.1f}/10")
        if energy["low_days"] > 0:
            print(f"  {Colors.YELLOW}Warning: {energy['low_days']} low-energy days{Colors.ENDC}")

        # Consistency
        cons = patterns["consistency"]
        print(f"\nConsistency:")
        print(f"  Check-in rate: {cons['checkin_rate']*100:.0f}%")
        print(f"  Reflection rate: {cons['reflection_rate']*100:.0f}%")

        # Completion
        comp = patterns["completion_rate"]
        print(f"\nTask Completion:")
        print(f"  Rate: {comp['rate']*100:.0f}%")
        print(f"  ({comp['total_completed']}/{comp['total_planned']} tasks)")

        # Strengths & Improvements
        if patterns["strengths"]:
            print(f"\n{Colors.GREEN}Strengths:{Colors.ENDC}")
            for s in patterns["strengths"]:
                print(f"  + {s}")

        if patterns["areas_for_improvement"]:
            print(f"\n{Colors.YELLOW}Areas for Improvement:{Colors.ENDC}")
            for a in patterns["areas_for_improvement"]:
                print(f"  - {a}")

        # Habit issues
        if patterns["habit_issues"]:
            print(f"\n{Colors.RED}Habit Alerts:{Colors.ENDC}")
            for issue in patterns["habit_issues"]:
                print(f"  ! {issue}")

        # Coaching recommendation
        insight = self.get_daily_insight()
        if insight:
            print(f"\n{Colors.BOLD}Coach's Note:{Colors.ENDC}")
            print_coach(insight)
