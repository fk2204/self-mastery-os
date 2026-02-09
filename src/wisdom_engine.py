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
        self._masters_data = {}  # Lazy-load cache
        self._loaded_modules = set()  # Track which modules are loaded

    def _load_module(self, module: str) -> Dict:
        """Lazy-load a single module's master data."""
        if module in self._loaded_modules:
            return self._masters_data.get(module, {})

        file_path = self.masters_path / f"{module}_masters.json"
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._masters_data[module] = data
                    self._loaded_modules.add(module)
                    return data
            except (json.JSONDecodeError, IOError):
                pass
        return {}

    @property
    def masters_data(self) -> Dict:
        """Get all masters data (loads all modules on first access for backward compatibility)."""
        # Lazy load all modules on first access
        if not self._masters_data and self.masters_path.exists():
            for file in sorted(self.masters_path.glob("*_masters.json")):
                module = file.stem.replace("_masters", "")
                if module not in self._loaded_modules:
                    self._load_module(module)
        return self._masters_data

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
        available_modules = []
        for m in focus_modules:
            if (self.masters_path / f"{m}_masters.json").exists():
                available_modules.append(m)

        if not available_modules:
            # Fall back to any available module
            if self.masters_path.exists():
                available_modules = [f.stem.replace("_masters", "") for f in self.masters_path.glob("*_masters.json")]

        if not available_modules:
            return {"master": "Unknown", "teaching": "No teachings available.", "module": "general"}

        module = random.choice(available_modules)
        module_data = self._load_module(module)
        masters = module_data.get("masters", [])

        if not masters:
            return {"master": "Unknown", "teaching": "No masters found.", "module": module}

        master = random.choice(masters)
        principles = master.get("key_principles", [])
        daily_practices = master.get("daily_practices", ["Apply this today."])

        return {
            "master": master.get("name", "Unknown"),
            "expertise": master.get("expertise", ""),
            "teaching": random.choice(principles) if principles else "No teaching available.",
            "practice": random.choice(daily_practices) if daily_practices else "Apply this today.",
            "module": module
        }

    def _get_daily_insight(self, focus_modules: List[str]) -> str:
        """Get a daily insight from focus modules."""
        all_insights = []

        # Only load focus modules
        for module in focus_modules:
            module_data = self._load_module(module)
            insights = module_data.get("daily_insights", [])
            all_insights.extend(insights)

        # Add some cross-module insights (still lazy-loaded)
        if all_insights:
            return random.choice(all_insights)

        # Fallback: load one additional module for insights
        available_modules = [f.stem.replace("_masters", "") for f in self.masters_path.glob("*_masters.json")]
        if available_modules:
            module = random.choice(available_modules)
            module_data = self._load_module(module)
            insights = module_data.get("daily_insights", [])
            if insights:
                return random.choice(insights)

        return "Show up. Do the work. Repeat."

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
            if self.masters_data:
                relevant_module = random.choice(list(self.masters_data.keys()))
            else:
                return "Take action despite uncertainty. Clarity comes from doing, not thinking."

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

    def get_worked_example(self, module: str = None) -> Optional[Dict]:
        """Get a random worked example from a module or focus modules."""
        if module:
            modules_to_check = [module]
        else:
            modules_to_check = self.profile.get("focus_modules", list(self.masters_data.keys()))

        all_examples = []
        for mod in modules_to_check:
            if mod in self.masters_data:
                for master in self.masters_data[mod].get("masters", []):
                    examples = master.get("worked_examples", [])
                    for ex in examples:
                        all_examples.append({
                            **ex,
                            "master": master["name"],
                            "module": mod
                        })

        return random.choice(all_examples) if all_examples else None

    def get_script_template(self, module: str = None) -> Optional[Dict]:
        """Get a random script/template from a module or focus modules."""
        if module:
            modules_to_check = [module]
        else:
            modules_to_check = self.profile.get("focus_modules", list(self.masters_data.keys()))

        all_templates = []
        for mod in modules_to_check:
            if mod in self.masters_data:
                for master in self.masters_data[mod].get("masters", []):
                    templates = master.get("scripts_templates", [])
                    for tmpl in templates:
                        all_templates.append({
                            **tmpl,
                            "master": master["name"],
                            "module": mod
                        })

        return random.choice(all_templates) if all_templates else None

    def get_level_definition(self, module: str, level: int) -> Optional[Dict]:
        """Get level definition for a module at a specific level."""
        if module not in self.masters_data:
            return None

        level_defs = self.masters_data[module].get("level_definitions", {})
        return level_defs.get(str(level), None)

    def get_progressive_exercise(self, module: str, difficulty: str = "beginner") -> Optional[Dict]:
        """Get a progressive exercise from a module at specified difficulty."""
        if module not in self.masters_data:
            return None

        exercises = self.masters_data[module].get("progressive_exercises", {})
        difficulty_exercises = exercises.get(difficulty, [])

        if not difficulty_exercises:
            return None

        exercise = random.choice(difficulty_exercises)
        return {
            **exercise,
            "module": module,
            "difficulty_level": difficulty
        }

    def get_cross_module_connection(self, module: str) -> Optional[Dict]:
        """Get a cross-module connection insight for a module."""
        if module not in self.masters_data:
            return None

        connections = self.masters_data[module].get("cross_module_connections", [])
        return random.choice(connections) if connections else None

    def get_master_resources(self, module: str, master_name: str) -> Optional[Dict]:
        """Get resources (books, podcasts) for a specific master."""
        if module not in self.masters_data:
            return None

        masters = self.masters_data[module].get("masters", [])
        for master in masters:
            if master["name"].lower() == master_name.lower():
                return master.get("resources", None)

        return None

    def print_worked_example(self, example: Dict):
        """Print a formatted worked example."""
        print(f"\n{Colors.BOLD}{Colors.CYAN}[WORKED EXAMPLE]{Colors.ENDC}")
        print(f"{Colors.YELLOW}{example['title']}{Colors.ENDC}")
        print(f"From: {example['master']} ({example['module'].title()})")
        print(f"\n{Colors.DIM}Scenario:{Colors.ENDC} {example['scenario']}")
        print(f"\n{Colors.GREEN}Framework:{Colors.ENDC} {example['framework_applied']}")
        print(f"\n{Colors.BOLD}Steps:{Colors.ENDC}")
        for i, step in enumerate(example.get('step_by_step', []), 1):
            print(f"  {i}. {step}")
        print(f"\n{Colors.GREEN}Outcome:{Colors.ENDC} {example.get('outcome', 'N/A')}")

    def print_script_template(self, template: Dict):
        """Print a formatted script/template."""
        print(f"\n{Colors.BOLD}{Colors.CYAN}[SCRIPT/TEMPLATE]{Colors.ENDC}")
        print(f"{Colors.YELLOW}{template['title']}{Colors.ENDC}")
        print(f"From: {template['master']} ({template['module'].title()})")
        print(f"\n{Colors.DIM}Context:{Colors.ENDC} {template['context']}")
        print(f"\n{Colors.BOLD}Template:{Colors.ENDC}")
        print(f"{Colors.CYAN}{template['template']}{Colors.ENDC}")
        if template.get('example_filled'):
            print(f"\n{Colors.GREEN}Example:{Colors.ENDC} {template['example_filled']}")
