# Self-Mastery OS - Application Specification

## Version 1.0 | Draft

---

## 1. Vision & Purpose

**Self-Mastery OS** is a personal command-line operating system for life optimization. It acts as your daily **Life COO** and **High-Level Mentor**, helping you systematically improve across all critical life domains.

### Core Philosophy
- **Systems over motivation**: Build habits and processes that work regardless of how you feel
- **High standards, sustainable pace**: Push for excellence without burnout
- **Data-driven growth**: Track what matters, adjust based on evidence
- **Behavior-first**: Every insight must translate to specific actions
- **Compound gains**: Small daily improvements lead to massive long-term results

---

## 2. Target User Profile

- Ambitious individual seeking systematic self-improvement
- Willing to invest 30-120 minutes daily in personal development
- Values direct, practical guidance over feel-good motivation
- Wants accountability and tracking, not just advice
- Ready to be challenged and pushed outside comfort zone

---

## 3. Core Modules

### 3.1 Money & Wealth Creation
**Goal**: Increase income, build assets, develop high-income skills
- Income tracking and growth targets
- Skill development roadmap
- Side hustle/business progress
- Leverage optimization

### 3.2 Sales & Persuasion
**Goal**: Master influence, close deals, build pipeline
- Daily outreach targets
- Objection handling practice
- Pipeline management
- Conversion metrics

### 3.3 Personal Finance & Investing
**Goal**: Optimize cash flow, build wealth, achieve financial freedom
- Budget tracking
- Savings rate optimization
- Investment contributions
- Net worth tracking

### 3.4 Dating, Social Skills & Relationships
**Goal**: Build social confidence, improve relationships, expand network
- Social interaction targets
- Conversation practice
- Relationship quality assessment
- Network expansion

### 3.5 Wisdom, Mindset & Emotional Mastery
**Goal**: Develop mental resilience, emotional intelligence, sound judgment
- Daily reflection practice
- Mindset training
- Emotional regulation
- Decision quality

### 3.6 Health, Fitness & Energy
**Goal**: Optimize physical performance, energy, and longevity
- Sleep optimization
- Training consistency
- Nutrition adherence
- Energy management

### 3.7 Lifestyle Design & Environment
**Goal**: Design optimal living conditions and daily structure
- Environment optimization
- Routine design
- Friction removal
- Identity alignment

### 3.8 Smart Ideas, Business & Career
**Goal**: Capture opportunities, execute projects, advance career
- Idea capture and evaluation
- Project progress
- Career advancement
- Strategic experiments

### 3.9 Productivity, Systems & Deep Work
**Goal**: Maximize output, minimize waste, achieve flow states
- Deep work hours
- Task completion rate
- Focus quality
- System effectiveness

---

## 4. Data Model

### 4.1 User Profile (`data/user_profile.json`)
```json
{
  "name": "string",
  "created_at": "datetime",
  "top_goals": ["goal1", "goal2", "goal3"],
  "daily_time_available_minutes": 60,
  "coaching_style": "direct|balanced|gentle",
  "constraints": ["time", "money", "energy", "knowledge"],
  "module_levels": {
    "money": 5,
    "sales": 3,
    "finance": 6,
    "dating": 4,
    "mindset": 7,
    "health": 5,
    "lifestyle": 4,
    "business": 5,
    "productivity": 6
  },
  "focus_modules": ["money", "health", "productivity"],
  "goals_90_day": {},
  "weekly_targets": {}
}
```

### 4.2 Daily Log (`data/logs/YYYY-MM-DD.json`)
```json
{
  "date": "YYYY-MM-DD",
  "am_checkin": {
    "time": "datetime",
    "sleep_hours": 7.5,
    "sleep_quality": 8,
    "energy_level": 7,
    "top_3_priorities": [],
    "win_definition": "string"
  },
  "planned_actions": [],
  "completed_actions": [],
  "pm_reflection": {
    "time": "datetime",
    "wins": [],
    "challenges": [],
    "lessons": [],
    "improvement_for_tomorrow": "string",
    "day_score": 8
  },
  "metrics": {
    "deep_work_hours": 0,
    "workouts": 0,
    "sales_calls": 0,
    "social_interactions": 0
  },
  "habits": {
    "morning_routine": false,
    "workout": false,
    "journaling": false,
    "reading": false
  }
}
```

### 4.3 Weekly Review (`data/reviews/week-YYYY-WW.json`)
```json
{
  "week": "YYYY-WW",
  "start_date": "YYYY-MM-DD",
  "end_date": "YYYY-MM-DD",
  "module_scores": {},
  "goals_progress": {},
  "wins": [],
  "lessons": [],
  "next_week_focus": "string",
  "next_week_targets": {},
  "experiments": []
}
```

### 4.4 Habits & Streaks (`data/habits.json`)
```json
{
  "habits": [
    {
      "id": "string",
      "name": "string",
      "module": "string",
      "frequency": "daily|weekly",
      "current_streak": 0,
      "best_streak": 0,
      "total_completions": 0
    }
  ]
}
```

### 4.5 Goals (`data/goals.json`)
```json
{
  "lifetime_vision": "string",
  "yearly_goals": [],
  "quarterly_goals": [],
  "monthly_goals": [],
  "weekly_goals": []
}
```

---

## 5. Core Workflows

### 5.1 Onboarding Flow (First Run)
1. Welcome and system introduction
2. Collect basic info (name, time available)
3. Rate current level in each module (1-10)
4. Identify top 3 life goals
5. Select coaching style preference
6. Identify biggest constraints
7. Set initial 90-day goals for priority modules
8. Generate first week's action plan

### 5.2 Daily AM Check-in (Morning)
1. Log sleep hours and quality
2. Rate current energy level (1-10)
3. Define top 3 priorities for the day
4. State what would make today a "win"
5. System generates personalized action plan based on:
   - Current goals and weekly targets
   - Energy level
   - Time available
   - Module priorities

### 5.3 Daily Action Plan Generation
Based on profile and check-in, propose:
- 1-3 wealth/career actions
- 1 sales/persuasion practice
- 1 finance micro-task
- 1 health action (workout, nutrition, sleep prep)
- 1 social/relationship action (if applicable)
- 1 mindset/reflection practice
- Deep work block recommendation

### 5.4 Daily PM Reflection (Evening)
1. Review planned vs completed actions
2. Log wins and highlights
3. Note challenges and obstacles
4. Extract lessons learned
5. Identify one improvement for tomorrow
6. Rate day overall (1-10)
7. Update metrics and habit streaks

### 5.5 Weekly Review (End of Week)
1. Show progress vs weekly targets
2. Calculate module scores
3. Identify top wins
4. Analyze patterns (energy, sleep, productivity)
5. Extract key lessons
6. Set next week's focus theme
7. Define specific targets
8. Plan experiments/changes

### 5.6 Monthly/90-Day Review
1. Assess progress toward 90-day goals
2. Review all module improvements
3. Celebrate achievements
4. Identify systemic issues
5. Reset or adjust goals
6. Plan next 90-day sprint

---

## 6. Scoring System

### Daily Score (0-10)
- Task completion rate: 40%
- Priority task completion: 30%
- Habit adherence: 20%
- Energy optimization: 10%

### Module Scores (0-10)
Calculated weekly based on:
- Relevant metric progress
- Habit consistency
- Goal advancement
- Self-assessment

### Overall Mastery Score
Weighted average of all module scores

---

## 7. Adaptive Coaching Logic

### Pattern Detection
- Low sleep for 3+ days → Sleep intervention recommendations
- Missed workouts → Simplify fitness targets
- Consistent wins → Increase challenge level
- Repeated failures → Break down into smaller steps

### Coaching Messages
- Context-aware encouragement
- Specific next steps
- Pattern-based insights
- Challenge level adjustments

---

## 8. File Structure

```
self-mastery-os/
├── src/
│   ├── main.py              # Entry point
│   ├── onboarding.py        # Onboarding flow
│   ├── daily_checkin.py     # AM/PM check-ins
│   ├── weekly_review.py     # Weekly review logic
│   ├── action_planner.py    # Action plan generation
│   ├── scoring.py           # Scoring calculations
│   ├── coaching.py          # Adaptive coaching
│   ├── data_manager.py      # Data persistence
│   └── utils.py             # Helper functions
├── data/
│   ├── user_profile.json
│   ├── habits.json
│   ├── goals.json
│   ├── logs/                # Daily logs
│   └── reviews/             # Weekly/monthly reviews
├── knowledge_base/
│   ├── money_wealth.md
│   ├── sales_persuasion.md
│   ├── personal_finance.md
│   ├── dating_social.md
│   ├── mindset_wisdom.md
│   ├── health_fitness.md
│   ├── lifestyle_design.md
│   ├── business_career.md
│   └── productivity_systems.md
└── docs/
    ├── SPECIFICATION.md
    └── USAGE_GUIDE.md
```

---

## 9. CLI Interface Design

### Main Menu
```
╔══════════════════════════════════════╗
║       SELF-MASTERY OS v1.0           ║
╠══════════════════════════════════════╣
║  [1] Morning Check-in                ║
║  [2] View Today's Plan               ║
║  [3] Log Action Complete             ║
║  [4] Evening Reflection              ║
║  [5] Weekly Review                   ║
║  [6] View Progress Dashboard         ║
║  [7] Update Goals                    ║
║  [8] Settings                        ║
║  [0] Exit                            ║
╚══════════════════════════════════════╝
```

### Interaction Style
- Clear prompts and numbered options
- Color-coded feedback (green=success, yellow=warning, red=alert)
- Progress bars for streaks and goals
- Concise, actionable output

---

## 10. Success Criteria

The system is successful when:
1. User engages daily with AM and PM check-ins
2. Habit streaks are maintained and growing
3. Module scores improve over 90-day periods
4. User reports feeling more organized and in control
5. Concrete progress toward stated goals is measurable

---

*This specification will be refined based on user feedback before full implementation.*
