# Self-Mastery OS - Claude Context File

## Overview
Self-Mastery OS is a personal development tracking system designed to help the user become the "boss version" of themselves. It's a web-based dashboard (dashboard.html) that provides daily coaching, habit tracking, and progress monitoring across 9 life modules.

## Core Philosophy
- Proactive coaching with teachings from world-class masters
- Daily skill-building through actionable challenges
- Data-driven progress tracking across all life areas
- Direct, no-BS coaching style (user preference)

## The 9 Life Modules
1. **Money & Wealth** - Building wealth, income streams, financial freedom
2. **Sales & Persuasion** - Closing deals, negotiation, influence
3. **Personal Finance** - Budgeting, investing, debt management
4. **Dating & Social** - Relationships, social skills, confidence
5. **Mindset & Wisdom** - Mental models, stoicism, resilience
6. **Health & Fitness** - Already at level 8 (user works out daily)
7. **Lifestyle Design** - Habits, environment, time management
8. **Business & Career** - Entrepreneurship, leadership, strategy
9. **Productivity & Systems** - Deep work, focus, systems thinking

## User Profile
- Name: Boss (or configured name)
- Coaching Style: Direct (no hand-holding)
- Focus Modules: money, sales, finance, productivity, business, dating, mindset, lifestyle
- Health Level: 8/10 (already exercising daily - no workout tracking needed)

## Key Features

### Daily Workflows
- **Morning Check-in**: Sleep quality, energy level, top 3 priorities, win definition
- **Evening Reflection**: Wins, challenges/lessons, deep work hours, habit completion, day score (1-10)

### Habit Tracking (12 habits)
1. Morning Routine (5:30 AM)
2. Deep Work Block (2+ hours)
3. Sales Outreach (10 contacts)
4. Objection Practice
5. Finance Check (5 min)
6. Skill Learning (30 min)
7. Journaling
8. Reading (30 min)
9. Networking Action
10. Social Interaction Practice
11. Inbox Zero
12. No Phone First Hour

### Wisdom Engine
Delivers daily teachings from 45+ masters including:
- Naval Ravikant, Alex Hormozi, Warren Buffett (Money)
- Jordan Belfort, Grant Cardone, Chris Voss (Sales)
- David Goggins, Jocko Willink, Marcus Aurelius (Mindset)
- Cal Newport, James Clear, Tim Ferriss (Productivity)
- Andrew Huberman, Peter Attia (Health)
- And many more...

### Dashboard Components
- Daily wisdom section (master teaching, insight, skill challenge, power question, mindset shift)
- Today's plan with habits and priorities
- Progress metrics (day streak, deep work hours, habit completion %, avg score)
- Module scores visualization
- Habit streaks
- Masters library with detailed profiles

## File Structure
```
self-mastery-os/
├── dashboard.html          # Main web application (single-page app)
├── server.py               # Python server for API endpoints
├── CLAUDE.md               # This file - context for Claude
├── src/
│   ├── main.py             # CLI entry point
│   ├── data_manager.py     # Data persistence layer
│   ├── wisdom_engine.py    # Proactive coaching engine
│   ├── daily_checkin.py    # Check-in workflows
│   ├── coaching.py         # Coaching logic
│   └── utils.py            # Utilities and constants
├── data/
│   ├── user_profile.json   # User settings and module levels
│   ├── habits.json         # Habit definitions and completions
│   ├── stats.json          # Aggregated statistics
│   └── daily_logs/         # Daily check-in logs (YYYY-MM-DD.json)
└── knowledge_base/
    └── masters/            # Master teachings by module
        ├── money_masters.json
        ├── sales_masters.json
        ├── finance_masters.json
        ├── mindset_masters.json
        ├── productivity_masters.json
        ├── social_masters.json
        ├── business_masters.json
        ├── lifestyle_masters.json
        └── health_masters.json
```

## How to Run
1. **Web Dashboard (Recommended)**: Open `dashboard.html` in browser
2. **With Python Server**: Run `python server.py` for API support
3. **CLI Mode**: Run `python src/main.py` for terminal interface

## Keyboard Shortcuts (Dashboard)
- `R` - Refresh daily wisdom
- `M` - Open morning check-in
- `E` - Open evening reflection

## Data Storage
- **Browser**: LocalStorage (dashboard.html standalone mode)
- **Server Mode**: JSON files in /data directory

## Design Aesthetic
- Dark "Mission Control" theme
- Modern, motivational feel
- Clean typography with good hierarchy
- Accent colors for modules and actions

## When Modifying This App

### Adding New Masters
Add to appropriate `knowledge_base/masters/*_masters.json`:
```json
{
  "name": "Master Name",
  "expertise": "Their area of expertise",
  "key_principles": ["Principle 1", "Principle 2"],
  "daily_practices": ["Practice 1", "Practice 2"],
  "worked_examples": [{
    "title": "Example Title",
    "scenario": "Situation description...",
    "framework_applied": "Framework name",
    "step_by_step": ["Step 1", "Step 2"],
    "outcome": "Expected result"
  }],
  "scripts_templates": [{
    "title": "Template Title",
    "context": "When to use this",
    "template": "The actual template with ___ blanks",
    "example_filled": "Example with blanks filled"
  }],
  "resources": {
    "books": [{"title": "Book", "author": "Author", "key_takeaway": "Main insight"}],
    "podcasts": [{"title": "Podcast", "episode": "Episode name", "key_takeaway": "Main insight"}]
  }
}
```

### Module-Level Schema (Enhanced)
Each module JSON file also contains:
```json
{
  "module": "money",
  "level_definitions": {
    "1": {"name": "Beginner", "description": "...", "capabilities": [...], "milestone": "..."},
    "10": {"name": "Master", "description": "...", "capabilities": [...], "milestone": "..."}
  },
  "progressive_exercises": {
    "beginner": [{"title": "...", "difficulty": 1, "time_minutes": 30, "instructions": "...", "success_criteria": "..."}],
    "intermediate": [...],
    "advanced": [...]
  },
  "cross_module_connections": [{
    "connected_module": "sales",
    "insight": "How these modules relate",
    "combined_exercise": "Practice combining both skills"
  }],
  "masters": [...]
}
```

### Adding New Habits
Update both:
1. `data/habits.json` - habit definitions
2. `dashboard.html` - DEFAULT_DATA.habits array

### Adding New Modules
1. Add to MODULE_NAMES in `src/utils.py`
2. Create `knowledge_base/masters/{module}_masters.json`
3. Update dashboard.html DEFAULT_DATA.modules

## Important Notes
- User does NOT need workout tracking (already exercising daily)
- Coaching style is DIRECT - no fluff, no hand-holding
- Focus on actionable advice from proven masters
- All features should work offline (LocalStorage)
- Keep the dark theme and modern aesthetic
