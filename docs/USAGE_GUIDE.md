# Self-Mastery OS - Usage Guide

## Quick Start

### 1. First Run - Onboarding

```bash
cd C:\Users\fkozi\self-mastery-os
python src/main.py
```

The first time you run the app, it will guide you through onboarding:
- Set your name and daily time availability
- Choose your coaching style (direct, balanced, gentle)
- Rate your current level in each life area
- Select your top 3 focus areas
- Define your 90-day goals

### 2. Daily Workflow

**Morning (5-10 minutes):**
```bash
python src/main.py am
```
Or launch the app and select "Morning Check-in"

1. Log your sleep hours and quality
2. Rate your current energy level
3. Set your TOP 3 priorities for the day
4. Define what would make today a "WIN"
5. Review your personalized action plan

**Throughout the Day:**
- Use the Quick Log feature to:
  - Mark habits complete
  - Log metrics (deep work hours, workouts, etc.)
  - Mark tasks as done

**Evening (5-10 minutes):**
```bash
python src/main.py pm
```
Or launch the app and select "Evening Reflection"

1. Review and check off completed tasks
2. Update habit completions
3. Log daily metrics
4. Record wins and lessons
5. Score your day
6. Set one improvement for tomorrow

### 3. Weekly Review (30-60 minutes, end of week)

```bash
python src/main.py week
```

1. Review your week's statistics
2. Analyze habit streaks
3. Score each module's performance
4. Identify top wins and lessons
5. Set next week's focus theme
6. Plan experiments

---

## Command Line Shortcuts

| Command | Description |
|---------|-------------|
| `python src/main.py` | Launch main menu |
| `python src/main.py am` | Quick morning check-in |
| `python src/main.py pm` | Quick evening reflection |
| `python src/main.py week` | Weekly review |
| `python src/main.py status` | Progress dashboard |
| `python src/main.py patterns` | AI pattern analysis |

---

## Understanding Your Data

### Daily Logs
Stored in: `data/logs/YYYY-MM-DD.json`

Each day's log contains:
- Morning check-in data (sleep, energy, priorities)
- Planned actions
- Completed actions
- Evening reflection (wins, lessons, score)
- Metrics and habits

### Weekly Reviews
Stored in: `data/reviews/week-YYYY-WW.json`

Contains:
- Week statistics
- Module scores
- Wins and lessons
- Next week's plan

### Habits
Stored in: `data/habits.json`

Tracks:
- Habit definitions
- Completion dates
- Current and best streaks
- Total completions

---

## Scoring System

### Daily Score (0-10)
Based on:
- Task completion rate (40%)
- Priority task completion (30%)
- Habit adherence (20%)
- Self-assessment (10%)

**Guidelines:**
- 9-10: Exceptional day, all priorities achieved
- 7-8: Strong day, most tasks completed
- 5-6: Average day, some progress made
- 3-4: Below average, significant tasks missed
- 1-2: Tough day, minimal progress

### Module Scores (0-10)
Self-rated weekly based on:
- Progress toward goals
- Relevant habit consistency
- Metric improvements
- Overall effort

---

## The 9 Modules

1. **Money & Wealth** - Income, skills, leverage
2. **Sales & Persuasion** - Outreach, deals, influence
3. **Personal Finance** - Budget, savings, investing
4. **Dating & Social** - Relationships, confidence
5. **Mindset & Wisdom** - Emotional mastery, journaling
6. **Health & Fitness** - Sleep, exercise, nutrition
7. **Lifestyle Design** - Environment, routines
8. **Business & Career** - Projects, ideas, career
9. **Productivity** - Deep work, systems, focus

---

## Coaching Styles

### Direct
- High accountability
- No sugarcoating
- Push for maximum performance
- Focuses on standards and execution

### Balanced
- Firm but supportive
- Celebrates wins while addressing issues
- Practical and constructive
- Best for most users

### Gentle
- Encouraging and supportive
- Focuses on progress not perfection
- Lower pressure
- Good for building consistency

---

## Tips for Success

### Daily Habits
1. **Check in every morning** - Even if brief, set intentions
2. **Reflect every evening** - Compound learning happens here
3. **Be honest in scores** - Self-deception slows progress
4. **Start small** - Consistency beats intensity

### Weekly Reviews
1. **Block 30-60 minutes** - Don't rush this
2. **Look for patterns** - What's working? What isn't?
3. **Set specific targets** - Vague goals produce vague results
4. **Run experiments** - Try new approaches each week

### Using the Knowledge Base
Access via Settings → View Knowledge Base

Each module has:
- Core principles
- Key metrics to track
- Daily/weekly actions
- Common mistakes
- Frameworks and checklists

---

## Customization

### Adding Habits
Settings → Manage Habits → Add new habit

### Adjusting Focus
Settings → Update focus modules

### Changing Style
Settings → Change coaching style

### Updating Goals
Edit `data/goals.json` directly or through weekly reviews

---

## Troubleshooting

### App won't start
```bash
# Verify Python is installed
python --version

# Navigate to correct directory
cd C:\Users\fkozi\self-mastery-os
python src/main.py
```

### Reset all data
Settings → Reset all data

Or manually delete the `data/` folder.

### Colors not displaying
Windows Command Prompt may need:
```bash
# Enable virtual terminal processing
# Or use Windows Terminal instead
```

---

## File Structure

```
self-mastery-os/
├── src/
│   ├── main.py           # Entry point
│   ├── onboarding.py     # First-time setup
│   ├── daily_checkin.py  # AM/PM flows
│   ├── weekly_review.py  # Weekly review
│   ├── action_planner.py # Plan generation
│   ├── coaching.py       # Adaptive coaching
│   ├── data_manager.py   # Data storage
│   └── utils.py          # Helpers
├── data/
│   ├── user_profile.json
│   ├── habits.json
│   ├── goals.json
│   ├── logs/             # Daily logs
│   └── reviews/          # Weekly reviews
├── knowledge_base/       # Reference material
└── docs/
    ├── SPECIFICATION.md
    └── USAGE_GUIDE.md
```

---

## Evolving the System

### Adding New Metrics
Edit `data_manager.py` to add new fields

### Customizing Actions
Edit `action_planner.py` to modify action templates

### Adding Modules
Update `utils.py` MODULE_NAMES and add knowledge base file

---

## Philosophy

This system is built on these principles:

1. **Systems over motivation** - Don't rely on feeling motivated
2. **Compound gains** - Small daily improvements add up
3. **Data-driven** - Track, measure, adjust
4. **Behavior-first** - Actions, not just intentions
5. **High standards, sustainable pace** - Push but don't burn out

---

**Remember:** The best system is one you actually use. Start simple, stay consistent, and let the compound effect work its magic.
