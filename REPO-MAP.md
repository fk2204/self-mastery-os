# Self-Mastery OS - Repository Map

## Overview
Personal development tracking system with daily coaching from 60+ world-class mentors across 12 life modules. Built with Python 3.13, vanilla JavaScript, and JSON storage. Features both CLI and web dashboard interfaces.

**Technology:** Python 3.13 | Vanilla JS | JSON Storage | Pytest
**Testing:** 126+ tests, target 80%+ coverage (100% for DataManager and WisdomEngine)
**Lines of Code:** ~10,000+ Python, ~8,000+ JavaScript, ~10,000+ JSON knowledge base

---

## Directory Structure

```
self-mastery-os/
├── .benchmarks/            # Performance benchmarks
├── .claude/                # Claude agent configuration
│   ├── CLAUDE.md           # Project context for Claude
│   ├── DECISIONS.md        # Design decisions log
│   ├── REPO-MAP.md         # This file
│   ├── STRUCTURE.md        # High-level architecture
│   └── settings.local.json # Local settings
├── .git/                   # Git repository
├── .pytest_cache/          # Pytest cache
├── data/                   # JSON data storage (git-ignored)
│   ├── logs/               # Daily logs (YYYY-MM-DD.json)
│   ├── reviews/            # Weekly reviews (week-YYYY-WW.json)
│   ├── goals.json          # Goals hierarchy
│   ├── habits.json         # Habit definitions and completions
│   ├── mentor_conversations.json  # Chat history with mentors
│   ├── mentors_library.json       # Mentor profiles
│   ├── quarterly_okrs.json        # OKR tracking
│   ├── user_profile.json          # User configuration
│   ├── vision.json                # Vision statements
│   └── weekly_plans.json          # Weekly plan data
├── docs/                   # Documentation
│   ├── SPECIFICATION.md    # Detailed specification
│   └── USAGE_GUIDE.md      # User guide
├── htmlcov/                # HTML coverage reports
├── knowledge_base/         # Master teachings
│   ├── masters/            # 12 module JSON files (10,652 lines)
│   │   ├── business_masters.json             (438 lines)
│   │   ├── communication_masters.json        (2247 lines)
│   │   ├── critical_thinking_masters.json    (1972 lines)
│   │   ├── emotional_intelligence_masters.json (1550 lines)
│   │   ├── finance_masters.json              (440 lines)
│   │   ├── health_masters.json               (454 lines)
│   │   ├── lifestyle_masters.json            (443 lines)
│   │   ├── mindset_masters.json              (707 lines)
│   │   ├── money_masters.json                (654 lines)
│   │   ├── productivity_masters.json         (448 lines)
│   │   ├── sales_masters.json                (635 lines)
│   │   └── social_masters.json               (664 lines)
│   ├── geniuses/           # Historical figures (not used)
│   └── *.md                # Module knowledge (legacy)
├── src/                    # Python modules
│   ├── __pycache__/        # Python cache
│   ├── action_planner.py   # Daily action plan generator (231 lines)
│   ├── coaching.py         # Pattern analysis & coaching (285 lines)
│   ├── daily_checkin.py    # Morning/evening workflows (310 lines)
│   ├── data_manager.py     # JSON I/O and data layer (336 lines)
│   ├── main.py             # CLI entry point (629 lines)
│   ├── onboarding.py       # First-time setup (281 lines)
│   ├── utils.py            # Utilities and constants (279 lines)
│   ├── weekly_review.py    # Weekly review workflow (382 lines)
│   └── wisdom_engine.py    # Master teachings delivery (392 lines)
├── tests/                  # Test suite
│   ├── __pycache__/        # Pytest cache
│   ├── fixtures/           # Test data generators
│   ├── integration/        # End-to-end tests
│   ├── unit/               # Unit tests
│   │   ├── test_data_manager.py    (60 tests, ~700 lines)
│   │   ├── test_wisdom_engine.py   (66 tests, ~900 lines)
│   │   └── TEST_COUNT_VERIFICATION.md
│   ├── conftest.py         # Shared fixtures (223 lines)
│   ├── test_fixtures_verify.py     # Fixture validation
│   ├── README.md           # Test documentation
│   └── TEST_COVERAGE_SUMMARY.md    # Coverage breakdown
├── CLAUDE.md               # Project context (root copy)
├── dashboard.html          # Web dashboard SPA (8210 lines)
├── mastery.bat             # Windows CLI shortcut
├── README.md               # Project readme
└── server.py               # HTTP server + API (172 lines)
```

---

## Core Python Files

### server.py (172 lines)
**Purpose:** HTTP server for web dashboard with API endpoints

**Key Components:**
- `DashboardHandler` - Custom request handler extending SimpleHTTPRequestHandler
- `run_server(port)` - Main server runner

**API Endpoints:**
- `GET /` or `/dashboard` - Serves dashboard.html
- `GET /api/data` - All dashboard data (profile, habits, stats, today's log)
- `GET /api/wisdom` - Daily wisdom package
- `GET /api/habits` - Habit data
- `GET /api/planning` - Vision, OKRs, weekly plans
- `GET /data/*.json` - Direct JSON file access

**Dependencies:** DataManager, WisdomEngine, http.server, json, pathlib

**Usage:**
```bash
python server.py        # Start on port 8080
python server.py 3000   # Custom port
```

---

### src/data_manager.py (336 lines)
**Purpose:** Central data persistence layer. All file I/O goes through this module.

**Class: DataManager**

**Initialization:**
- `__init__(base_path)` - Sets up paths (data/, logs/, reviews/, knowledge_base/)
- `_ensure_directories()` - Creates required directories

**Core Methods:**
- `_read_json(filepath)` → Optional[Dict] - Read JSON file (returns None on error)
- `_write_json(filepath, data)` → bool - Write JSON file (returns False on error)

**User Profile:**
- `get_user_profile()` → Optional[Dict] - Get user profile
- `save_user_profile(profile)` → bool - Save with updated_at timestamp
- `user_exists()` → bool - Check if profile exists

**Daily Logs:**
- `get_daily_log(date)` → Optional[Dict] - Get log for date (YYYY-MM-DD)
- `save_daily_log(log, date)` → bool - Save log with timestamps
- `get_or_create_daily_log(date)` → Dict - Get existing or create new template
- `get_logs_for_range(start, end)` → List[Dict] - Get logs in date range
- `get_recent_logs(days=7)` → List[Dict] - Get last N days

**Weekly Reviews:**
- `get_weekly_review(week)` → Optional[Dict] - Get review (YYYY-WW format)
- `save_weekly_review(review, week)` → bool - Save review

**Habits:**
- `get_habits()` → Dict - Get habits data (returns default if missing)
- `save_habits(habits)` → bool - Save habits data
- `add_habit(habit)` → bool - Add new habit with unique ID
- `record_habit_completion(habit_id, date)` → bool - Mark habit complete
- `_calculate_streak(dates)` → int - Calculate current streak (internal)

**Goals:**
- `get_goals()` → Dict - Get goals data (lifetime, yearly, quarterly, monthly, weekly)
- `save_goals(goals)` → bool - Save goals

**Statistics:**
- `get_stats()` → Dict - Aggregated stats from last 30 days:
  - total_days_logged, am_checkins, pm_reflections
  - avg_sleep, avg_energy, avg_day_score
  - total_deep_work_hours, total_workouts
  - habit_completion_rate

**Knowledge Base:**
- `get_knowledge_base_topics()` → List[str] - List of .md files
- `get_knowledge_base_content(topic)` → Optional[str] - Read .md file

**Error Handling:** All I/O errors caught and printed to stderr. Returns None/False on failure.

**Test Coverage:** 100% (60 tests in test_data_manager.py)

---

### src/wisdom_engine.py (392 lines)
**Purpose:** Proactive coaching system delivering daily teachings from 60+ masters

**Class: WisdomEngine**

**Initialization:**
- `__init__(dm: DataManager)` - Loads all master JSON files from knowledge_base/masters/

**Daily Wisdom:**
- `get_daily_wisdom()` → Dict - Complete package:
  - master_teaching (master, expertise, teaching, practice)
  - daily_insight (motivational message)
  - skill_challenge (actionable task)
  - power_question (reflection prompt)
  - mindset_shift (reframe from/to/why)

**Master Teachings:**
- `_get_master_teaching(focus_modules)` → Dict - Random teaching from focus areas
- `_get_daily_insight(focus_modules)` → str - Insight from masters
- `_get_skill_challenge(focus_modules)` → Dict - Daily challenge
- `_get_power_question()` → str - One of 20 reflection questions
- `_get_mindset_shift()` → Dict - Cognitive reframe

**Situational Advice:**
- `get_master_advice_for_situation(situation)` → str - Context-aware advice
  - Maps keywords to modules (e.g., "sales", "money", "fear")
  - Returns relevant master principle and practice

**Module Masters:**
- `get_module_masters(module)` → List[Dict] - All masters for module
- `get_all_masters_list()` → List[Dict] - All masters across modules
- `print_master_profile(module, master_name)` - Display full profile

**Advanced Features:**
- `get_worked_example(module)` → Optional[Dict] - Detailed scenario walkthrough
- `get_script_template(module)` → Optional[Dict] - Copy-paste template
- `get_level_definition(module, level)` → Optional[Dict] - Level descriptions
- `get_progressive_exercise(module, difficulty)` → Optional[Dict] - Practice exercise
- `get_cross_module_connection(module)` → Optional[Dict] - Inter-module insights
- `get_master_resources(module, master_name)` → Optional[Dict] - Books, podcasts

**Print Functions:**
- `print_daily_wisdom()` - Formatted daily package
- `print_worked_example(example)` - Formatted example
- `print_script_template(template)` - Formatted template

**Data Structure (masters JSON):**
```json
{
  "module": "money",
  "level_definitions": { "1": {...}, "10": {...} },
  "progressive_exercises": { "beginner": [...], "advanced": [...] },
  "cross_module_connections": [...],
  "daily_insights": [...],
  "skill_challenges": [...],
  "masters": [
    {
      "name": "Naval Ravikant",
      "expertise": "Wealth creation, startups, philosophy",
      "key_principles": [...],
      "daily_practices": [...],
      "worked_examples": [
        {
          "title": "...",
          "scenario": "...",
          "framework_applied": "...",
          "step_by_step": [...],
          "outcome": "..."
        }
      ],
      "scripts_templates": [
        {
          "title": "...",
          "context": "...",
          "template": "...",
          "example_filled": "..."
        }
      ],
      "resources": {
        "books": [...],
        "podcasts": [...]
      }
    }
  ]
}
```

**Test Coverage:** 100% (66 tests in test_wisdom_engine.py)

---

### src/main.py (629 lines)
**Purpose:** CLI entry point and interactive menu system

**Command Line Shortcuts:**
```bash
python main.py           # Interactive menu
python main.py am        # Morning check-in
python main.py pm        # Evening reflection
python main.py week      # Weekly review
python main.py status    # Dashboard
python main.py patterns  # Pattern analysis
python main.py wisdom    # Daily wisdom
python main.py masters   # Masters library
python main.py help      # Help message
```

**Main Functions:**
- `main()` - Entry point, routes to commands or menu
- `run_main_menu(dm)` - Interactive menu loop

**Menu Options:**
1. Morning Check-in - Starts with wisdom, then planning
2. Today's Wisdom - Full daily package
3. View Today's Plan - Show action items
4. Log Habit/Metric - Quick logging
5. Evening Reflection - Review day
6. Weekly Review - Analyze week
7. Masters Library - Browse teachings
8. Progress Dashboard - Show stats
9. Pattern Analysis - AI coaching
10. Settings & Profile - Configure
11. Exit

**Sub-Menus:**
- `show_todays_plan(dm)` - Display planned actions
- `quick_log(dm)` - Log habit/metric/task/note
- `settings_menu(dm)` - Update profile, habits, modules
- `manage_habits(dm)` - Add/remove habits
- `view_knowledge_base(dm)` - Browse .md files
- `show_masters_library(dm)` - Browse by module
- `browse_module_masters(dm, module, masters)` - Select master
- `show_master_detail(master)` - Display full profile
- `print_help()` - CLI usage info

**User Experience:**
- Dynamic greeting based on time of day
- Shows mini-wisdom snippet on menu
- Colorized output with terminal colors
- Pause for reading, clear screen between sections

**Dependencies:** All other src/ modules

---

### src/utils.py (279 lines)
**Purpose:** Shared utilities, constants, and terminal UI functions

**Terminal Colors (class Colors):**
```python
HEADER, BLUE, CYAN, GREEN, YELLOW, RED, ENDC, BOLD, DIM
```

**Screen Management:**
- `clear_screen()` - Clear terminal
- `pause()` - Wait for Enter key

**Print Functions:**
- `print_header(text)` - Styled header
- `print_subheader(text)` - Styled subheader
- `print_success(text)` - Green [+] message
- `print_warning(text)` - Yellow [!] message
- `print_error(text)` - Red [X] message
- `print_info(text)` - Cyan [i] message
- `print_coach(text)` - Yellow coach message
- `print_menu(options, title)` - Numbered menu
- `print_score(label, score, max)` - Colored score with grade
- `print_streak(label, current, best)` - Streak with flame emoji

**Input Functions:**
- `get_input(prompt, default)` → str - Get string input
- `get_int_input(prompt, min, max, default)` → int - Get integer in range
- `get_float_input(prompt, min, max, default)` → float - Get float in range
- `get_yes_no(prompt, default)` → bool - Get yes/no answer
- `get_choice(prompt, options)` → int - Get numbered choice (0-indexed)
- `get_multiple_choice(prompt, options, max)` → List[int] - Get multiple choices
- `get_list_input(prompt, min, max)` → List[str] - Get list of strings

**Date/Time Utilities:**
- `format_date(dt)` → str - YYYY-MM-DD
- `format_datetime(dt)` → str - YYYY-MM-DD HH:MM
- `format_week(dt)` → str - YYYY-WW
- `get_week_range(dt)` → tuple - (start_date, end_date)

**Display Utilities:**
- `progress_bar(current, total, width)` → str - Text progress bar
- `score_to_grade(score)` → str - Convert 0-10 to letter grade
- `score_to_color(score)` → str - Get color code for score
- `calculate_streak(dates)` → int - Calculate streak from date list

**Module Constants:**
```python
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

MODULE_ICONS = { "money": "$", "sales": "S", ... }
```

**Module Helpers:**
- `get_module_name(key)` → str - Full name from key
- `get_module_icon(key)` → str - Icon character

---

### src/daily_checkin.py (310 lines)
**Purpose:** Morning and evening check-in workflows

**Morning Check-in:**
- `morning_checkin(dm)` → Dict - Returns updated log

**Flow:**
1. Check if already done (option to redo)
2. Sleep & Energy
   - Sleep hours (0-12), quality (1-10), energy level (1-10)
   - Feedback based on sleep
3. Top 3 Priorities
   - Shows suggestions from ActionPlanner
   - User enters 1-3 priorities
4. Win Definition
   - "What ONE thing would make today a WIN?"
5. Action Plan Generation
   - Uses ActionPlanner based on energy & time
   - Displays categorized actions
6. Save to daily log
7. Closing message based on energy

**Evening Reflection:**
- `evening_reflection(dm)` → Dict - Returns updated log

**Flow:**
1. Check if already done
2. Action Review
   - Mark each planned action complete/incomplete
3. Habit Check
   - Check off completed daily habits
   - Updates streaks via DataManager
4. Daily Metrics
   - Deep work hours (0-12)
   - Workout (yes/no)
   - Sales calls (if sales in focus)
   - Social interactions (if dating/social in focus)
5. Wins & Highlights (1-5 items)
6. Challenges & Obstacles (0-3 items)
7. Lessons Learned (0-3 items)
8. Looking Ahead
   - One thing to do differently tomorrow
9. Day Score (1-10)
   - Auto-suggests based on completion rate
10. Save to daily log
11. Summary & Coaching

**Helper Functions:**
- `get_morning_greeting(profile)` → str - Style-based greeting
- `get_morning_closing(profile, energy)` → str - Energy-based message
- `get_evening_coaching(profile, score, completed, planned)` → str - Performance feedback

**Coaching Styles:**
- Direct: "No excuses", "Attack tomorrow"
- Balanced: "Solid progress", "Learn and move forward"
- Gentle: "Some days are harder", "Tomorrow is a fresh start"

---

### src/weekly_review.py (382 lines)
**Purpose:** Weekly review and planning workflow

**Weekly Review:**
- `weekly_review(dm)` → Dict - Complete review data

**Flow:**
1. Check for existing review (option to redo)
2. Week At A Glance
   - Days logged, check-ins, reflections
   - Avg day score, sleep, energy
   - Deep work hours, workouts, task completion
3. Habit Streaks
   - Show current and best streaks
   - Highlight 7+ day streaks
4. Module Performance
   - Rate each focus module 1-10
5. Top Wins (1-3)
   - Shows wins from daily logs
   - User selects top 3
6. Key Lessons (1-3)
   - Shows lessons from daily logs
   - User selects key lessons
7. Analysis
   - What moved the needle? (1-3)
   - What was a waste of time? (0-3)
   - What needs adjustment? (0-3)
8. Next Week Planning
   - Choose focus theme (8 options + custom)
   - Set targets for focus modules
   - Define experiments to try
9. Save review
10. Summary & Coaching

**Progress Dashboard:**
- `show_progress_dashboard(dm)` - Display stats

**Sections:**
1. 30-Day Overview
   - Days logged, check-ins, reflections
   - Averages: day score, sleep, energy
   - Totals: deep work, workouts
   - Habit completion rate
2. Current Streaks
   - All habits with current/best/total
   - Flame emoji for 7+ day streaks
3. 90-Day Goals Progress
   - Each module: current/target levels
   - Progress bar
   - Goal description

**Helper Functions:**
- `calculate_week_stats(logs)` → Dict - Aggregate week data
- `get_weekly_coaching(profile, score, stats)` → str - Multi-part coaching message

**Themes:**
- Deep Work Sprint, Sales Push, Health Reset, Learning Focus
- Social Expansion, Business Building, Recovery Week, Custom

---

### src/coaching.py (285 lines)
**Purpose:** Pattern analysis and adaptive coaching

**Class: Coach**

**Initialization:**
- `__init__(dm)` - Loads profile and coaching style

**Pattern Analysis:**
- `analyze_patterns()` → Dict - Comprehensive analysis from last 14 days:
  - sleep_trend: average, trend, low_days
  - energy_trend: average, trend, low_days
  - consistency: checkin_rate, reflection_rate
  - completion_rate: rate, total_planned, total_completed
  - habit_issues: broken streaks, never-started habits
  - strengths: list of positive patterns
  - areas_for_improvement: list of issues

**Trend Detection:**
- `_analyze_sleep(logs)` → Dict - Sleep patterns
  - Compares first half vs second half
  - Trends: improving, declining, stable
- `_analyze_energy(logs)` → Dict - Energy patterns
- `_analyze_consistency(logs)` → Dict - Check-in adherence
- `_analyze_completion(logs)` → Dict - Task execution
- `_analyze_habits()` → List[str] - Habit issues

**Contextual Coaching:**
- `get_daily_insight()` → Optional[str] - Today's insight based on patterns
  - Sleep debt warnings
  - Consistency reminders
  - Completion rate feedback
  - Habit alerts
- `get_coaching_message(context, data)` → str - Context-specific coaching

**Contexts:**
- low_energy, high_energy
- missed_workout, streak_broken
- good_score, poor_score

**Coaching by Style:**
- Direct: "No excuses", "Attack your hardest tasks"
- Balanced: "Focus on must-dos", "Learn from it"
- Gentle: "Be kind to yourself", "Tomorrow is a new chance"

**Output:**
- `print_pattern_report()` - Full analysis with recommendations

---

### src/action_planner.py (231 lines)
**Purpose:** Generate personalized daily action plans

**Class: ActionPlanner**

**Initialization:**
- `__init__(dm)` - Loads profile and action templates

**Action Templates:**
- 8 modules × 8 actions each = 64 total actions
- Each action has: text, time (minutes), difficulty (1-3)

**Template Categories:**
- Money: Skill development, networking, income research, side project
- Sales: Cold outreach, follow-ups, objection practice, CRM updates
- Finance: Spending review, portfolio check, budget tracking, research
- Dating: Conversations, social events, active listening, compliments
- Mindset: Journaling, meditation, reading, belief reframing
- Health: Workout, walk, meal prep, mobility, sunlight
- Lifestyle: Environment optimization, habit friction, decluttering
- Business: Project work, networking, documentation, research
- Productivity: Deep work, time-blocking, inbox zero, automation

**Plan Generation:**
- `generate_daily_plan(energy_level, time_available, priorities)` → Dict

**Algorithm:**
1. Adjust max difficulty based on energy (low=1, medium=2, high=3)
2. Select modules: always productivity + health, plus 2 focus modules
3. For each module:
   - Filter actions by difficulty and time
   - Pick 1-2 suitable actions
   - Add to plan until time exhausted
4. Sort by module priority
5. Return plan with metadata

**Priority Suggestions:**
- `get_priority_suggestions()` → List[str] - Suggestions from:
  - Quarterly goals
  - Top goals
  - Generic high-leverage items

**Display:**
- `print_plan(plan)` - Formatted action list:
  - Groups by module
  - Shows time and difficulty (stars)
  - Checkbox for completion status
  - Total estimated time

---

### src/onboarding.py (281 lines)
**Purpose:** First-time user setup

**Onboarding Flow:**
- `run_onboarding(dm)` → Dict - Complete profile

**Steps:**
1. Basic Information
   - Name (default: "Boss")
   - Daily time commitment (30/60/90/120+ minutes)
2. Coaching Style
   - Direct & Intense
   - Balanced
   - Gentle & Supportive
3. Current Level Assessment
   - Rate all 12 modules (1-10)
4. Priority Focus Areas
   - Select top 3 modules
5. Top Life Goals
   - Enter 1-3 specific goals
6. Current Constraints
   - Select from: time, money, energy, knowledge, environment, social
7. 90-Day Goals
   - For each focus module:
     - Specific goal description
     - Target level (current to 10)
8. Core Habits
   - Accept defaults or create custom
   - Default: morning routine, workout, deep work, journaling, reading
9. Summary & Confirmation
   - Review all settings
   - Save profile, habits, goals
10. Final Instructions
    - Explains daily workflows
    - Encourages first check-in

**Helper Functions:**
- `needs_onboarding(dm)` → bool - Check if profile exists

**Default Habits:**
```python
[
  {"id": "morning_routine", "name": "Morning Routine", "module": "productivity"},
  {"id": "workout", "name": "Workout", "module": "health"},
  {"id": "deep_work", "name": "Deep Work Block", "module": "productivity"},
  {"id": "journaling", "name": "Journaling", "module": "mindset"},
  {"id": "reading", "name": "Reading (20+ min)", "module": "mindset"}
]
```

---

## Data Schemas

### user_profile.json
```json
{
  "name": "Boss",
  "created_at": "2025-02-03T10:00:00",
  "updated_at": "2025-02-03T10:30:00",
  "top_goals": ["Goal 1", "Goal 2", "Goal 3"],
  "daily_time_available_minutes": 90,
  "coaching_style": "direct",
  "constraints": ["time"],
  "module_levels": {
    "money": 5,
    "sales": 4,
    "finance": 5,
    "dating": 5,
    "mindset": 6,
    "health": 8,
    "lifestyle": 5,
    "business": 5,
    "productivity": 6,
    "emotional_intelligence": 3,
    "critical_thinking": 3,
    "communication": 3
  },
  "focus_modules": ["money", "sales", "finance"],
  "goals_90_day": {
    "money": {
      "goal": "Add $3K/month in side income",
      "target_level": 7,
      "start_level": 5,
      "created_at": "2025-02-03T10:00:00"
    }
  }
}
```

### habits.json
```json
{
  "habits": [
    {
      "id": "morning_routine",
      "name": "Morning Routine (full)",
      "module": "productivity",
      "frequency": "daily",
      "created_at": "2025-02-03T10:00:00",
      "current_streak": 0,
      "best_streak": 0,
      "total_completions": 0
    }
  ],
  "completions": {
    "2025-02-03": ["morning_routine", "deep_work_90"]
  }
}
```

### data/logs/YYYY-MM-DD.json
```json
{
  "date": "2026-02-03",
  "created_at": "2026-02-03T08:06:56.873928",
  "updated_at": "2026-02-03T08:09:26.700940",
  "am_checkin": {
    "time": "2026-02-03T08:09:26.700928",
    "sleep_hours": 7.0,
    "sleep_quality": 6,
    "energy_level": 6,
    "top_3_priorities": ["Priority 1", "Priority 2", "Priority 3"],
    "win_definition": "Main win for today"
  },
  "planned_actions": [
    {
      "module": "money",
      "module_name": "Money & Wealth",
      "text": "Action description",
      "time": 30,
      "difficulty": 2,
      "completed": false
    }
  ],
  "completed_actions": [],
  "pm_reflection": {
    "time": "2026-02-03T20:00:00.000000",
    "wins": ["Win 1", "Win 2"],
    "challenges": ["Challenge 1"],
    "lessons": ["Lesson 1"],
    "improvement_for_tomorrow": "One thing to improve",
    "day_score": 7,
    "main_win_achieved": true
  },
  "metrics": {
    "deep_work_hours": 3.5,
    "workouts": 1,
    "sales_calls": 5,
    "social_interactions": 2,
    "steps": 8000,
    "water_liters": 2.5
  },
  "habits": {},
  "notes": "[10:30] Quick note about the day"
}
```

### goals.json
```json
{
  "lifetime_vision": "Financial freedom and complete life mastery",
  "yearly_goals": [
    "Reach $150K+ total income",
    "Master sales and close deals consistently"
  ],
  "quarterly_goals": {
    "money": {
      "goal": "Add $3K/month in side income",
      "target_level": 7,
      "start_level": 5,
      "created_at": "2025-02-03T10:00:00"
    }
  },
  "monthly_goals": [],
  "weekly_goals": []
}
```

### data/reviews/week-YYYY-WW.json
```json
{
  "week": "2026-W05",
  "start_date": "2026-02-02",
  "end_date": "2026-02-08",
  "created_at": "2026-02-08T20:00:00.000000",
  "updated_at": "2026-02-08T20:15:00.000000",
  "stats": {
    "days_logged": 7,
    "am_checkins": 6,
    "pm_reflections": 5,
    "avg_day_score": 7.2,
    "avg_sleep": 7.1,
    "avg_energy": 6.8,
    "total_deep_work": 18.5,
    "total_workouts": 5,
    "tasks_completed": 35,
    "tasks_planned": 42
  },
  "module_scores": {
    "money": 7,
    "sales": 6,
    "productivity": 8
  },
  "top_wins": ["Win 1", "Win 2", "Win 3"],
  "key_lessons": ["Lesson 1", "Lesson 2"],
  "needle_movers": ["What worked 1", "What worked 2"],
  "time_wasters": ["Time waster 1"],
  "adjustments": ["Adjustment 1"],
  "next_week_focus": "Deep Work Sprint",
  "next_week_targets": {
    "money": "Build 1 income stream MVP",
    "sales": "Close 2 deals"
  },
  "experiments": ["Try waking at 5 AM", "No social media before noon"]
}
```

---

## Master Data Files

### knowledge_base/masters/ (10,652 total lines)

**12 Module Files:**
1. **money_masters.json** (654 lines)
   - Masters: Naval Ravikant, Alex Hormozi, Warren Buffett, Brandon Turner, Nic Carter
   - Focus: Wealth creation, crypto, real estate, startups

2. **sales_masters.json** (635 lines)
   - Masters: Jordan Belfort, Grant Cardone, Chris Voss, Jill Konrath, Aaron Ross
   - Focus: Cold calling, negotiation, enterprise sales, predictable revenue

3. **finance_masters.json** (440 lines)
   - Masters: Ramit Sethi, Robert Kiyosaki, John Bogle, Morgan Housel
   - Focus: Personal finance, investing, wealth psychology

4. **social_masters.json** (664 lines)
   - Masters: Dale Carnegie, Mark Manson, John Gottman, Esther Perel
   - Focus: Relationships, social skills, intimacy

5. **mindset_masters.json** (707 lines)
   - Masters: David Goggins, Marcus Aurelius, Jocko Willink, Alan Watts, Carl Jung
   - Focus: Mental toughness, stoicism, Eastern philosophy, shadow work

6. **health_masters.json** (454 lines)
   - Masters: Andrew Huberman, Peter Attia, Kelly Starrett
   - Focus: Neuroscience, longevity, mobility

7. **productivity_masters.json** (448 lines)
   - Masters: Cal Newport, James Clear, David Allen, Tim Ferriss
   - Focus: Deep work, habits, GTD, lifestyle design

8. **business_masters.json** (438 lines)
   - Masters: Peter Thiel, Clayton Christensen, Eric Ries, Sam Altman
   - Focus: Zero to one, disruption, lean startup, Y Combinator

9. **lifestyle_masters.json** (443 lines)
   - Masters: Marie Kondo, Nir Eyal, Atomic Habits frameworks
   - Focus: Environment design, habit architecture

10. **emotional_intelligence_masters.json** (1550 lines)
    - Masters: Daniel Goleman, Marc Brackett, Susan David, Paul Ekman
    - Focus: RULER method, emotional agility, micro-expressions
    - 200+ emotion vocabulary

11. **critical_thinking_masters.json** (1972 lines)
    - Masters: Daniel Kahneman, Charlie Munger, Shane Parrish, Annie Duke
    - Focus: 50+ mental models, cognitive biases, decision frameworks

12. **communication_masters.json** (2247 lines)
    - Masters: Patrick King, Julian Treasure, Vinh Giang, Marshall Rosenberg
    - Focus: Active listening, public speaking, nonviolent communication

**Total Masters:** 60+

---

## Dashboard (dashboard.html) - 8210 lines

**Purpose:** Single-page web application (SPA) for visual interface

**Technology Stack:**
- Vanilla JavaScript (no frameworks)
- HTML5 + CSS3
- LocalStorage for offline mode
- Fetch API for server mode

**Key Features:**
1. **Mastermind Alliance** - Display of mentors by module
2. **Daily Wisdom** - Master teaching, insight, challenge
3. **Command Center** - OKR tracking, quarterly goals
4. **Mastery Roadmaps** - Progressive skill paths
5. **Personal Life College** - 80+ mentors across modules
6. **Mentor Chat System** - Conversational interface
7. **Habit Tracking** - 12 core habits with streaks
8. **Progress Dashboard** - Stats, scores, completion rates

**Keyboard Shortcuts:**
- `R` - Refresh daily wisdom
- `M` - Open morning check-in
- `E` - Open evening reflection

**Data Storage:**
- **Standalone mode:** Browser LocalStorage
- **Server mode:** Fetch from `/api/*` endpoints

**Default Data Structure:**
```javascript
DEFAULT_DATA = {
  profile: { name, coaching_style, focus_modules },
  habits: [ { id, name, module, streak, completed } ],
  modules: { money: 5, sales: 4, ... },
  stats: { dayStreak, deepWorkHours, habitCompletion, avgScore },
  todayLog: { hasAM, hasPM, priorities, energy }
}
```

**Styling:**
- Dark "Mission Control" theme (#0a0e27 background)
- Modern gradient accents
- Card-based layout
- Responsive design

---

## Commands & Usage

### Running the Application

**Web Dashboard (Recommended):**
```bash
python server.py        # Starts server at http://localhost:8080
python server.py 3000   # Custom port
```

**CLI Mode:**
```bash
python src/main.py              # Interactive menu
python src/main.py am           # Morning check-in
python src/main.py pm           # Evening reflection
python src/main.py week         # Weekly review
python src/main.py status       # Status dashboard
python src/main.py wisdom       # Daily wisdom
python src/main.py masters      # Masters library
python src/main.py patterns     # Pattern analysis
python src/main.py help         # Show help

# Windows shortcut
mastery.bat                     # Runs main.py
```

### Testing

**Run All Tests:**
```bash
python -m pytest tests/ -v
```

**Run Specific Test Files:**
```bash
python -m pytest tests/unit/test_data_manager.py -v
python -m pytest tests/unit/test_wisdom_engine.py -v
```

**Coverage Reports:**
```bash
# Generate coverage report
python -m pytest tests/unit/test_data_manager.py --cov=src.data_manager --cov-report=term-missing

# Generate HTML coverage report
python -m pytest tests/ --cov=src --cov-report=html
# Open: htmlcov/index.html

# Fail if coverage < 80%
python -m pytest tests/ --cov=src --cov-fail-under=80
```

**Test by Pattern:**
```bash
python -m pytest tests/ -k "habit" -v         # All habit tests
python -m pytest tests/ -k "streak" -v        # All streak tests
```

**Useful Flags:**
```bash
-v          # Verbose output
-s          # Show print statements
-x          # Stop on first failure
--lf        # Run last failed tests
--pdb       # Drop into debugger on failure
```

---

## Test Coverage Requirements

**Overall Target:** 80%+ coverage

**Critical Modules (100% Coverage Required):**
1. ✅ **data_manager.py** - 100% (60 tests)
   - All JSON I/O paths
   - Streak calculation logic
   - Date range queries
   - Error handling

2. ✅ **wisdom_engine.py** - 100% (66 tests)
   - Master loading
   - Daily wisdom generation
   - Template/example retrieval
   - Print functions

**Other Modules (80%+ Target):**
- daily_checkin.py
- weekly_review.py
- coaching.py
- action_planner.py
- onboarding.py
- main.py
- utils.py
- server.py

**Current Status:**
```
Module                 Coverage    Tests    Status
-----------------------------------------------------
data_manager.py        100%        60       ✅ Complete
wisdom_engine.py       100%        66       ✅ Complete
Overall                ~60%        126+     🔄 In Progress
```

---

## Key Design Decisions

### 1. Storage: JSON Files
**Why:** Simple, human-readable, version-controllable, no database setup
- Each daily log is a separate file (data/logs/YYYY-MM-DD.json)
- Profile, habits, goals are single files
- Easy to backup, inspect, and migrate

### 2. Interface: Dual CLI + Web
**Why:** Flexibility and user preference
- CLI for fast power-users and scripting
- Web for visual learners and exploration
- Both share same data layer (DataManager)

### 3. Frontend: Vanilla JavaScript
**Why:** No build step, no dependencies, fast load, offline-first
- Single HTML file (dashboard.html)
- LocalStorage for offline mode
- Optional server for shared data

### 4. Backend: Python 3.13
**Why:** Rich ecosystem, easy to read, cross-platform
- Standard library only (no external deps for core)
- Type hints for clarity
- Pytest for testing

### 5. Wisdom: 60+ Masters, 10K+ Lines JSON
**Why:** Comprehensive, actionable, evidence-based
- 12 life modules for complete coverage
- Real frameworks from proven experts
- Worked examples and templates for application

### 6. Coaching: Pattern-Based, Not Generic
**Why:** Personalized insights beat generic advice
- Analyzes last 14 days of data
- Detects trends (sleep, energy, completion)
- Tailored to coaching style (direct/balanced/gentle)

### 7. Testing: 100% for Core, 80%+ Overall
**Why:** Data integrity and wisdom delivery are critical
- DataManager: All JSON I/O must be bulletproof
- WisdomEngine: Master loading and retrieval must never fail
- Other modules: 80%+ for bug prevention

### 8. No Workout Tracking for User
**Why:** User already exercises daily at level 8
- Health module focuses on sleep, nutrition, recovery
- No need for workout logging

### 9. 12 Modules, Not 9
**Why:** Added 3 new modules for complete life mastery
- Emotional Intelligence: Self-awareness, regulation, empathy
- Critical Thinking: Mental models, biases, decisions
- Communication: Active listening, speaking, influence

### 10. Single-File Dashboard (8210 lines)
**Why:** No build process, easy deployment, fast load
- Inline CSS and JavaScript
- LocalStorage for offline mode
- Fetch for server mode
- No bundler, no npm, no complexity

---

## Testing Strategy

### Unit Tests
**Focus:** Individual functions and methods
**Location:** `tests/unit/`
**Coverage:** 100% for DataManager and WisdomEngine, 80%+ for others

**Fixtures (conftest.py):**
- `temp_dir` - Temporary directory with auto-cleanup
- `data_manager` - DataManager instance with temp dir
- `freeze_time` - Mock datetime.now() for deterministic tests
- `sample_user_profile` - Example user profile dict
- `sample_habit` - Example habit definition
- `sample_daily_log` - Example daily log
- `sample_weekly_review` - Example weekly review
- `sample_goals` - Example goals structure

**Test Organization:**
```
test_data_manager.py (60 tests)
├── Initialization (4 tests)
├── JSON I/O (7 tests)
├── User Profile (6 tests)
├── Daily Logs (11 tests)
├── Weekly Reviews (3 tests)
├── Habits (15 tests) - Critical streak logic
├── Goals (3 tests)
├── Statistics (6 tests)
└── Knowledge Base (3 tests)

test_wisdom_engine.py (66 tests)
├── Initialization (5 tests)
├── Daily Wisdom (4 tests)
├── Master Teaching (6 tests)
├── Daily Insight (3 tests)
├── Skill Challenge (4 tests)
├── Power Questions (2 tests)
├── Mindset Shift (2 tests)
├── Situational Advice (5 tests)
├── Module Masters (3 tests)
├── Worked Examples (4 tests)
├── Script Templates (3 tests)
├── Level Definitions (3 tests)
├── Progressive Exercises (4 tests)
├── Cross-Module Connections (2 tests)
├── Master Resources (4 tests)
├── Print Functions (6 tests)
└── Edge Cases (6 tests)
```

### Integration Tests
**Focus:** End-to-end workflows
**Location:** `tests/integration/`
**Status:** 🔄 To be implemented

**Planned Tests:**
- Complete morning check-in → evening reflection cycle
- Weekly review with real data
- Onboarding → first check-in
- Pattern analysis with 14 days of data
- CLI command execution

### Fixtures
**Focus:** Test data generators
**Location:** `tests/fixtures/`
**Status:** ✅ Available in conftest.py

---

## Common Development Tasks

### Adding a New Master
1. Open appropriate `knowledge_base/masters/{module}_masters.json`
2. Add to `masters` array:
```json
{
  "name": "Master Name",
  "expertise": "Area of expertise",
  "key_principles": ["Principle 1", "Principle 2"],
  "daily_practices": ["Practice 1", "Practice 2"],
  "worked_examples": [
    {
      "title": "Example Title",
      "scenario": "Situation description",
      "framework_applied": "Framework name",
      "step_by_step": ["Step 1", "Step 2"],
      "outcome": "Expected result"
    }
  ],
  "scripts_templates": [
    {
      "title": "Template Title",
      "context": "When to use",
      "template": "Template with ___ blanks",
      "example_filled": "Filled example"
    }
  ],
  "resources": {
    "books": [{"title": "Book", "author": "Author", "key_takeaway": "Insight"}],
    "podcasts": [{"title": "Podcast", "episode": "Episode", "key_takeaway": "Insight"}]
  }
}
```

### Adding a New Module
1. Add to `MODULE_NAMES` in `src/utils.py`
2. Create `knowledge_base/masters/{module}_masters.json`
3. Update `dashboard.html` DEFAULT_DATA.modules
4. Add action templates to `src/action_planner.py`

### Adding a New Habit
1. **Via CLI:** Settings → Manage Habits → Add new habit
2. **Via Code:** Update `data/habits.json` or `DEFAULT_DATA.habits` in dashboard.html

### Debugging Data Issues
1. Check JSON files in `data/` directory
2. Use `python -c "import json; print(json.load(open('data/user_profile.json')))"`
3. Verify DataManager methods with unit tests
4. Check server.py logs for API errors

### Running Coverage Analysis
```bash
# Full coverage report
python -m pytest tests/ --cov=src --cov-report=html

# Open report
start htmlcov/index.html   # Windows
open htmlcov/index.html    # Mac
```

### Checking Code Quality
```bash
# Type checking (if using mypy)
mypy src/

# Linting (if using flake8)
flake8 src/ --max-line-length=120

# Formatting (if using black)
black src/ tests/
```

---

## Dependencies

### Python (Runtime)
- **Python 3.13+** (standard library only)
- No external packages required for core functionality

### Python (Development)
```bash
pip install pytest pytest-cov
```

### Web Dashboard
- Modern browser (Chrome, Firefox, Edge, Safari)
- JavaScript enabled
- LocalStorage support (for offline mode)

---

## File Patterns

### Naming Conventions
- **Python files:** snake_case (data_manager.py, daily_checkin.py)
- **JSON files:** snake_case (user_profile.json, habits.json)
- **Daily logs:** YYYY-MM-DD.json (2026-02-03.json)
- **Weekly reviews:** week-YYYY-WW.json (week-2026-W05.json)
- **Classes:** PascalCase (DataManager, WisdomEngine)
- **Functions:** snake_case (get_user_profile, morning_checkin)
- **Constants:** UPPER_SNAKE_CASE (MODULE_NAMES, DEFAULT_DATA)

### Directory Purposes
- `src/` - Core Python modules
- `data/` - User data (git-ignored)
- `knowledge_base/` - Master teachings (committed)
- `tests/` - Test suite
- `docs/` - Documentation
- `htmlcov/` - Coverage reports (git-ignored)
- `.claude/` - Claude agent config

---

## Error Handling

### DataManager (data_manager.py)
- **Read errors:** Returns `None`, prints to stderr
- **Write errors:** Returns `False`, prints to stderr
- **Missing files:** Returns default structures (habits, goals)
- **Invalid JSON:** Caught by json.JSONDecodeError, returns None

### WisdomEngine (wisdom_engine.py)
- **Missing master files:** Silently skips, continues with available files
- **Empty modules:** Returns fallback messages ("No masters found")
- **Invalid JSON:** Caught during _load_all_masters(), skips file

### CLI (main.py, daily_checkin.py, etc.)
- **KeyboardInterrupt:** Catches at top level, prints "Goodbye!"
- **User input errors:** Retries until valid input
- **File I/O errors:** Handled by DataManager, prints warning to user

### Server (server.py)
- **File not found:** Returns 404
- **JSON errors:** Returns 500 with error message
- **All endpoints:** Always return 200 with JSON (even on error)

---

## Next Steps

### Immediate Priorities
1. ✅ Complete DataManager tests (60 tests, 100% coverage)
2. ✅ Complete WisdomEngine tests (66 tests, 100% coverage)
3. ⏳ Add integration tests for workflows
4. ⏳ Reach 80%+ overall test coverage
5. ⏳ Set up CI/CD pipeline

### Feature Enhancements
- Mobile-friendly dashboard design
- Export data to CSV/PDF
- Habit streak graphs
- Module progress charts
- Weekly review PDF reports
- Integration with calendar apps

### Technical Debt
- Refactor dashboard.html (8210 lines → modular components)
- Add API error handling (return proper HTTP codes)
- Implement caching for master data
- Add logging framework (replace print statements)
- Type hints for all functions

---

## Resources

### Documentation
- `CLAUDE.md` - Project context and rules
- `docs/SPECIFICATION.md` - Detailed specification
- `docs/USAGE_GUIDE.md` - User guide
- `tests/README.md` - Test documentation
- `tests/TEST_COVERAGE_SUMMARY.md` - Coverage details

### Key Files for AI Agents
- `CLAUDE.md` - Start here for project understanding
- `REPO-MAP.md` - This file (navigation and architecture)
- `src/data_manager.py` - Understand data layer
- `src/wisdom_engine.py` - Understand coaching system
- `tests/conftest.py` - Understand test fixtures

### External Resources
- Master teachings: See individual JSON files in `knowledge_base/masters/`
- Pytest docs: https://docs.pytest.org/
- Python 3.13 docs: https://docs.python.org/3.13/

---

**Last Updated:** 2026-02-07
**Project Version:** 1.0
**Test Coverage:** 60% overall, 100% DataManager, 100% WisdomEngine
**Total Lines:** ~30,000 (Python + JS + JSON)
