"""
Self-Mastery OS - Utility Functions
"""
import os
import json
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(text: str):
    """Print a styled header."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}  {text}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}\n")

def print_subheader(text: str):
    """Print a styled subheader."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}--- {text} ---{Colors.ENDC}\n")

def print_success(text: str):
    """Print success message."""
    print(f"{Colors.GREEN}[+] {text}{Colors.ENDC}")

def print_warning(text: str):
    """Print warning message."""
    print(f"{Colors.YELLOW}[!] {text}{Colors.ENDC}")

def print_error(text: str):
    """Print error message."""
    print(f"{Colors.RED}[X] {text}{Colors.ENDC}")

def print_info(text: str):
    """Print info message."""
    print(f"{Colors.CYAN}[i] {text}{Colors.ENDC}")

def print_coach(text: str):
    """Print coaching message."""
    print(f"{Colors.BOLD}{Colors.YELLOW}Coach: {text}{Colors.ENDC}")

def print_menu(options: List[str], title: str = "Options"):
    """Print a numbered menu."""
    print(f"\n{Colors.BOLD}{title}:{Colors.ENDC}")
    for i, option in enumerate(options, 1):
        print(f"  [{i}] {option}")
    print()

def get_input(prompt: str, default: str = "") -> str:
    """Get user input with optional default."""
    if default:
        full_prompt = f"{prompt} [{default}]: "
    else:
        full_prompt = f"{prompt}: "

    response = input(full_prompt).strip()
    return response if response else default

def get_int_input(prompt: str, min_val: int = 1, max_val: int = 10, default: Optional[int] = None) -> int:
    """Get integer input within range."""
    while True:
        try:
            default_str = str(default) if default is not None else ""
            response = get_input(f"{prompt} ({min_val}-{max_val})", default_str)
            value = int(response)
            if min_val <= value <= max_val:
                return value
            print_warning(f"Please enter a number between {min_val} and {max_val}")
        except ValueError:
            print_warning("Please enter a valid number")

def get_float_input(prompt: str, min_val: float = 0, max_val: float = 24, default: Optional[float] = None) -> float:
    """Get float input within range."""
    while True:
        try:
            default_str = str(default) if default is not None else ""
            response = get_input(f"{prompt} ({min_val}-{max_val})", default_str)
            value = float(response)
            if min_val <= value <= max_val:
                return value
            print_warning(f"Please enter a number between {min_val} and {max_val}")
        except ValueError:
            print_warning("Please enter a valid number")

def get_yes_no(prompt: str, default: bool = True) -> bool:
    """Get yes/no input."""
    default_str = "Y/n" if default else "y/N"
    response = get_input(f"{prompt} [{default_str}]").lower()
    if response == "":
        return default
    return response in ["y", "yes", "1", "true"]

def get_choice(prompt: str, options: List[str]) -> int:
    """Get choice from numbered options."""
    print_menu(options, prompt)
    return get_int_input("Your choice", 1, len(options)) - 1

def get_multiple_choice(prompt: str, options: List[str], max_choices: int = 3) -> List[int]:
    """Get multiple choices from options."""
    print_menu(options, prompt)
    print(f"  (Enter up to {max_choices} numbers separated by commas)")

    while True:
        response = get_input("Your choices (e.g., 1,2,3)")
        try:
            choices = [int(x.strip()) - 1 for x in response.split(",")]
            if all(0 <= c < len(options) for c in choices) and len(choices) <= max_choices:
                return choices
            print_warning(f"Please select up to {max_choices} valid options")
        except ValueError:
            print_warning("Please enter numbers separated by commas")

def get_list_input(prompt: str, min_items: int = 1, max_items: int = 5) -> List[str]:
    """Get a list of string inputs."""
    print(f"{prompt} (Enter {min_items}-{max_items} items, one per line. Enter blank line when done)")
    items = []
    while len(items) < max_items:
        item = input(f"  {len(items)+1}. ").strip()
        if not item:
            if len(items) >= min_items:
                break
            print_warning(f"Please enter at least {min_items} items")
            continue
        items.append(item)
    return items

def format_date(dt: datetime = None) -> str:
    """Format datetime as YYYY-MM-DD."""
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d")

def format_datetime(dt: datetime = None) -> str:
    """Format datetime as YYYY-MM-DD HH:MM."""
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M")

def format_week(dt: datetime = None) -> str:
    """Format datetime as YYYY-WW."""
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-W%W")

def get_week_range(dt: datetime = None) -> tuple:
    """Get start and end dates of the week."""
    if dt is None:
        dt = datetime.now()
    start = dt - timedelta(days=dt.weekday())
    end = start + timedelta(days=6)
    return start, end

def progress_bar(current: float, total: float, width: int = 30) -> str:
    """Generate a text-based progress bar."""
    if total == 0:
        percent = 0
    else:
        percent = current / total

    filled = int(width * percent)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {percent*100:.0f}%"

def score_to_grade(score: float) -> str:
    """Convert numeric score (0-10) to letter grade."""
    if score >= 9:
        return "A+"
    elif score >= 8:
        return "A"
    elif score >= 7:
        return "B"
    elif score >= 6:
        return "C"
    elif score >= 5:
        return "D"
    else:
        return "F"

def score_to_color(score: float) -> str:
    """Get color code based on score."""
    if score >= 7:
        return Colors.GREEN
    elif score >= 5:
        return Colors.YELLOW
    else:
        return Colors.RED

def print_score(label: str, score: float, max_score: float = 10):
    """Print a colored score."""
    color = score_to_color(score)
    grade = score_to_grade(score)
    print(f"  {label}: {color}{score:.1f}/{max_score} ({grade}){Colors.ENDC}")

def print_streak(label: str, current: int, best: int = None):
    """Print streak information."""
    flame = "🔥" if current >= 7 else ""
    best_str = f" (Best: {best})" if best and best > current else ""
    print(f"  {label}: {current} days {flame}{best_str}")

def calculate_streak(dates: List[str]) -> int:
    """Calculate current streak from list of date strings."""
    if not dates:
        return 0

    dates = sorted([datetime.strptime(d, "%Y-%m-%d") for d in dates], reverse=True)
    today = datetime.now().date()

    streak = 0
    expected = today

    for date in dates:
        if date.date() == expected:
            streak += 1
            expected -= timedelta(days=1)
        elif date.date() == expected - timedelta(days=1):
            expected = date.date()
            streak += 1
            expected -= timedelta(days=1)
        else:
            break

    return streak

# Module name mappings
MODULE_NAMES = {
    "money": "Money & Wealth",
    "sales": "Sales & Persuasion",
    "finance": "Personal Finance",
    "dating": "Dating & Social",
    "mindset": "Mindset & Wisdom",
    "health": "Health & Fitness",
    "lifestyle": "Lifestyle Design",
    "business": "Business & Career",
    "productivity": "Productivity & Systems",
    "emotional_intelligence": "Emotional Intelligence",
    "critical_thinking": "Critical Thinking",
    "communication": "Communication & Influence"
}

MODULE_ICONS = {
    "money": "$",
    "sales": "S",
    "finance": "F",
    "dating": "D",
    "mindset": "M",
    "health": "H",
    "lifestyle": "L",
    "business": "B",
    "productivity": "P",
    "emotional_intelligence": "E",
    "critical_thinking": "C",
    "communication": "I"
}

def get_module_name(key: str) -> str:
    """Get full module name from key."""
    return MODULE_NAMES.get(key, key.title())

def get_module_icon(key: str) -> str:
    """Get module icon from key."""
    return MODULE_ICONS.get(key, "?")

def pause():
    """Pause for user to read."""
    input(f"\n{Colors.DIM}Press Enter to continue...{Colors.ENDC}")
