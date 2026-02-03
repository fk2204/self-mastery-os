"""
Self-Mastery OS - Proactive Wisdom Engine
Delivers daily insights, teachings, and skill challenges from world-class masters.
"""
import os
import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from data_manager import DataManager
from utils import Colors, MODULE_NAMES, print_header, print_subheader, print_coach

class WisdomEngine:
    """Proactive wisdom delivery from world-class masters."""

    def __init__(self, dm: DataManager):
        self.dm = dm
        self.base_path = Path(dm.base_path)
        self.masters_path = self.base_path / "knowledge_base" / "masters"
        self.profile = dm.get_user_profile() or {}
        self.masters_data = self._load_all_masters()

    def _load_all_masters(self) -> Dict:
        """Load all masters data from JSON files."""
        masters = {}
        if not self.masters_path.exists():
            return masters

        for file in self.masters_path.glob("*.json"):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    module = data.get("module", file.stem.replace("_masters", ""))
                    masters[module] = data
            except (json.JSONDecodeError, IOError):
                continue

        return masters

    def get_daily_wisdom(self) -> Dict:
        """Generate comprehensive daily wisdom package."""
        focus_modules = self.profile.get("focus_modules", list(self.masters_data.keys())[:3])

        wisdom = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "master_teaching": self._get_master_teaching(focus_modules),
            "daily_insight": self._get_daily_insight(focus_modules),
            "skill_challenge": self._get_skill_challenge(focus_modules),
            "power_question": self._get_power_question(),
            "mindset_shift": self._get_mindset_shift()
        }

        return wisdom

    def _get_master_teaching(self, focus_modules: List[str]) -> Dict:
        """Get a teaching from a master in focus areas."""
        available_modules = [m for m in focus_modules if m in self.masters_data]
        if not available_modules:
            available_modules = list(self.masters_data.keys())

        if not available_modules:
            return {"master": "Unknown", "teaching": "No teachings available.", "module": "general"}

        module = random.choice(available_modules)
        module_data = self.masters_data.get(module, {})
        masters = module_data.get("masters", [])

        if not masters:
            return {"master": "Unknown", "teaching": "No masters found.", "module": module}

        master = random.choice(masters)
        principles = master.get("key_principles", [])

        return {
            "master": master.get("name", "Unknown"),
            "expertise": master.get("expertise", ""),
            "teaching": random.choice(principles) if principles else "No teaching available.",
            "practice": random.choice(master.get("daily_practices", ["Apply this today."])),
            "module": module
        }

    def _get_daily_insight(self, focus_modules: List[str]) -> str:
        """Get a daily insight from focus modules."""
        all_insights = []

        for module in focus_modules:
            if module in self.masters_data:
                insights = self.masters_data[module].get("daily_insights", [])
                all_insights.extend(insights)

        # Add some cross-module insights
        for module_data in self.masters_data.values():
            all_insights.extend(module_data.get("daily_insights", [])[:2])

        return random.choice(all_insights) if all_insights else "Show up. Do the work. Repeat."

    def _get_skill_challenge(self, focus_modules: List[str]) -> Dict:
        """Get a skill challenge for today."""
        # Prioritize focus modules
        module = random.choice(focus_modules) if focus_modules else "productivity"

        if module in self.masters_data:
            challenges = self.masters_data[module].get("skill_challenges", [])
            if challenges:
                return {
                    "module": module,
                    "module_name": MODULE_NAMES.get(module, module.title()),
                    "challenge": random.choice(challenges)
                }

        return {
            "module": "productivity",
            "module_name": "Productivity",
            "challenge": "Complete your #1 priority before noon."
        }

    def _get_power_question(self) -> str:
        """Get a power question for self-reflection."""
        questions = [
            "What would the best version of me do right now?",
            "What am I avoiding that I know I should do?",
            "If I only accomplished one thing today, what should it be?",
            "What would I do if I knew I couldn't fail?",
            "Am I being productive or just busy?",
            "What's the ONE thing that would make everything else easier?",
            "Who do I need to become to achieve my goals?",
            "What belief is limiting me right now?",
            "If today repeated for a year, where would I end up?",
            "What would make today a 10/10?",
            "What's the hard thing I'm pretending isn't my responsibility?",
            "Am I playing to win or playing not to lose?",
            "What's the conversation I'm avoiding?",
            "How can I provide 10x more value today?",
            "What skill, if mastered, would change everything?",
            "Is this the best use of my next hour?",
            "What would I tell my best friend to do in my situation?",
            "What am I tolerating that I shouldn't?",
            "If I had 6 months to live, would I be doing this?",
            "What's the smallest step I can take right now?"
        ]
        return random.choice(questions)

    def _get_mindset_shift(self) -> Dict:
        """Get a mindset reframe for the day."""
        shifts = [
            {"from": "I don't have time", "to": "It's not a priority", "why": "Own your choices. If it mattered, you'd find time."},
            {"from": "I can't do this", "to": "I can't do this YET", "why": "Growth mindset. Skills are built, not born."},
            {"from": "I failed", "to": "I learned what doesn't work", "why": "Failure is data. Collect it and adjust."},
            {"from": "I'm not ready", "to": "I'll figure it out as I go", "why": "Readiness is a myth. Action creates clarity."},
            {"from": "What if it goes wrong?", "to": "What if it goes right?", "why": "You're imagining the future anyway. Imagine the upside."},
            {"from": "I'm too tired", "to": "I'll do it for just 5 minutes", "why": "Energy follows action. Start small."},
            {"from": "That's not fair", "to": "What can I control?", "why": "Fairness is irrelevant. Adaptation is everything."},
            {"from": "I need motivation", "to": "I need discipline", "why": "Motivation is fleeting. Discipline is reliable."},
            {"from": "I'm overwhelmed", "to": "What's the ONE next step?", "why": "You can only do one thing at a time. Pick it."},
            {"from": "They're better than me", "to": "What can I learn from them?", "why": "Comparison kills. Learn and apply."},
            {"from": "It's too hard", "to": "It's supposed to be hard", "why": "Hard is what makes it valuable."},
            {"from": "I'm not talented enough", "to": "I haven't practiced enough", "why": "Talent is overrated. Reps are underrated."}
        ]
        return random.choice(shifts)

    def get_master_advice_for_situation(self, situation: str) -> str:
        """Get relevant master advice for a specific situation."""
        situation_lower = situation.lower()

        # Map situations to modules
        module_keywords = {
            "money": ["money", "income", "salary", "wealth", "earn", "rich", "broke"],
            "sales": ["sell", "close", "pitch", "client", "deal", "reject", "cold call", "outreach"],
            "finance": ["save", "invest", "budget", "debt", "expense", "retire"],
            "dating": ["social", "date", "friend", "relationship", "confidence", "approach", "talk to"],
            "mindset": ["fear", "anxiety", "stress", "doubt", "mindset", "belief", "mental", "stuck"],
            "productivity": ["focus", "distract", "procrastinate", "productive", "time", "busy", "work"],
            "business": ["business", "startup", "idea", "launch", "customer", "product"],
            "lifestyle": ["habit", "routine", "environment", "clutter", "phone", "social media"]
        }

        # Find relevant module
        relevant_module = None
        for module, keywords in module_keywords.items():
            if any(kw in situation_lower for kw in keywords):
                relevant_module = module
                break

        if not relevant_module:
            relevant_module = random.choice(list(self.masters_data.keys()))

        # Get advice from that module's masters
        module_data = self.masters_data.get(relevant_module, {})
        masters = module_data.get("masters", [])

        if masters:
            master = random.choice(masters)
            principle = random.choice(master.get("key_principles", ["Keep pushing forward."]))
            practice = random.choice(master.get("daily_practices", ["Take action now."]))

            return f'{master["name"]} says: "{principle}"\n\nApply it: {practice}'

        return "Take action despite uncertainty. Clarity comes from doing, not thinking."

    def print_daily_wisdom(self):
        """Print today's complete wisdom package."""
        wisdom = self.get_daily_wisdom()

        print(f"\n{Colors.BOLD}{Colors.CYAN}================================================================")
        print(f"                    TODAY'S WISDOM")
        print(f"                 {wisdom['date']}")
        print(f"================================================================{Colors.ENDC}\n")

        # Master Teaching
        teaching = wisdom["master_teaching"]
        print(f"{Colors.BOLD}[MASTER TEACHING]{Colors.ENDC}")
        print(f"{Colors.YELLOW}{teaching['master']}{Colors.ENDC} - {teaching['expertise']}")
        print(f'"{teaching["teaching"]}"')
        print(f"\n{Colors.GREEN}Apply it:{Colors.ENDC} {teaching['practice']}")

        # Daily Insight
        print(f"\n{Colors.BOLD}[DAILY INSIGHT]{Colors.ENDC}")
        print(f"{wisdom['daily_insight']}")

        # Skill Challenge
        challenge = wisdom["skill_challenge"]
        print(f"\n{Colors.BOLD}[TODAY'S SKILL CHALLENGE]{Colors.ENDC}")
        print(f"Module: {challenge['module_name']}")
        print(f"{Colors.CYAN}{challenge['challenge']}{Colors.ENDC}")

        # Power Question
        print(f"\n{Colors.BOLD}[POWER QUESTION]{Colors.ENDC}")
        print(f"{wisdom['power_question']}")

        # Mindset Shift
        shift = wisdom["mindset_shift"]
        print(f"\n{Colors.BOLD}[MINDSET SHIFT]{Colors.ENDC}")
        print(f'{Colors.RED}FROM:{Colors.ENDC} "{shift["from"]}"')
        print(f'{Colors.GREEN}TO:{Colors.ENDC} "{shift["to"]}"')
        print(f'{Colors.DIM}Why: {shift["why"]}{Colors.ENDC}')

        print(f"\n{Colors.BOLD}{Colors.CYAN}================================================================{Colors.ENDC}")
        print(f"{Colors.DIM}Execute. Review. Improve. Repeat.{Colors.ENDC}\n")

    def get_module_masters(self, module: str) -> List[Dict]:
        """Get all masters for a specific module."""
        module_data = self.masters_data.get(module, {})
        return module_data.get("masters", [])

    def print_master_profile(self, module: str, master_name: str):
        """Print detailed profile of a specific master."""
        masters = self.get_module_masters(module)

        for master in masters:
            if master["name"].lower() == master_name.lower():
                print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}")
                print(f"  {master['name'].upper()}")
                print(f"{'='*60}{Colors.ENDC}")
                print(f"\n{Colors.YELLOW}Expertise:{Colors.ENDC} {master['expertise']}")

                print(f"\n{Colors.BOLD}Key Principles:{Colors.ENDC}")
                for i, principle in enumerate(master.get("key_principles", []), 1):
                    print(f"  {i}. {principle}")

                print(f"\n{Colors.BOLD}Daily Practices:{Colors.ENDC}")
                for practice in master.get("daily_practices", []):
                    print(f"  - {practice}")

                print()
                return

        print(f"Master '{master_name}' not found in {module}")

    def get_all_masters_list(self) -> List[Dict]:
        """Get list of all available masters."""
        all_masters = []
        for module, data in self.masters_data.items():
            for master in data.get("masters", []):
                all_masters.append({
                    "name": master["name"],
                    "module": module,
                    "expertise": master.get("expertise", "")
                })
        return all_masters
