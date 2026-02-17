# Self-Mastery OS: Code Optimization + React Native Mobile App Plan

## Overview
Two-phase approach: (1) Optimize existing Python/JS code, (2) Build React Native + Expo mobile app for daily iPhone use.

---

## Phase 1: Code Efficiency Improvements

### 1.1 Data Manager - Add Caching Layer
**File:** `src/data_manager.py`
- Add in-memory cache dict with TTL for frequently accessed data (profile, habits, stats)
- Cache invalidation on writes
- Batch habit completions (record multiple at once instead of one file write per habit)
- Pre-compute streaks incrementally instead of full recalculation on every completion
- Add atomic writes (write to temp file, then rename) to prevent data corruption

### 1.2 Wisdom Engine - Date-Seeded Deterministic Selection
**File:** `src/wisdom_engine.py`
- Replace `random.choice()` with date-seeded RNG so same wisdom returns all day
- Add `_get_seeded_rng(date_str)` using `hashlib` for deterministic daily selection
- Lazy-load individual modules instead of all-at-once via `masters_data` property
- Move hardcoded power questions and mindset shifts to a JSON config file
- Add wisdom rotation tracking to avoid repeating recent masters

### 1.3 Server.py - Complete API + Performance
**File:** `server.py`
- Add missing POST endpoints: `/api/checkin/morning`, `/api/checkin/evening`, `/api/habits/{id}/complete`, `/api/journal`
- Add gzip compression for JSON responses
- Add ETag caching headers for static knowledge base data
- Add input validation and sanitization on all POST endpoints
- Fix path traversal vulnerability on `/data/*.json` endpoint

### 1.4 Dashboard.html - Modular Loading
**File:** `dashboard.html`
- Extract masters data loading to lazy-load from JSON files (don't embed 655KB in HTML)
- Add service worker for offline caching of knowledge base
- Debounce localStorage writes (batch saves instead of saving on every tiny change)
- Add loading states for async operations

---

## Phase 2: React Native Mobile App (Expo)

### 2.1 Project Setup
- Initialize Expo project in `/mobile` directory
- Configure for iOS (iPhone target)
- Set up TypeScript
- Install core dependencies: `expo-router` (navigation), `@react-native-async-storage/async-storage` (offline data), `expo-notifications` (daily reminders), `expo-haptics` (native feedback)

### 2.2 Shared Business Logic (`/mobile/src/services/`)
Extract and rewrite in TypeScript:

**StorageService** - AsyncStorage wrapper with the same JSON structure as web app
```
- get/set/remove with typed keys
- Migration support for data format changes
- Export/import for backup
```

**WisdomService** - Port from wisdom_engine.py
```
- Date-seeded deterministic daily wisdom
- Lazy module loading from bundled JSON
- Master teaching, insight, challenge, question, mindset shift
- Rotation tracking to avoid repeats
```

**HabitService** - Port from data_manager.py habit methods
```
- CRUD operations on habits
- Streak calculation (incremental, not full recalc)
- Completion tracking by date
- Completion rate analytics
```

**CheckinService** - Port from daily_checkin.py
```
- Morning check-in data model + validation
- Evening reflection data model + validation
- Action plan generation (port from action_planner.py)
- Deduplication (warn if already checked in today)
```

**CoachingService** - Port from coaching.py
```
- Pattern analysis over configurable windows
- Coaching message selection by context + style
- Strength/improvement identification
```

**StatsService** - Port from data_manager.py stats methods
```
- Aggregation with configurable date ranges
- Cached computation with invalidation
- Module score tracking
```

### 2.3 App Navigation (`expo-router`)
```
Tab Bar (bottom):
├── Home (Today)      - Daily wisdom + today's plan + quick habit toggles
├── Check-in          - Morning/Evening flows
├── Habits            - Full habit list + streaks + analytics
├── Journal           - Journal entries + prompts
└── Profile           - Stats, modules, masters library, settings
```

### 2.4 Core Screens

**Home Screen (Today Tab)**
- Daily wisdom card (master teaching, insight, challenge)
- Power question of the day
- Quick habit toggle chips (tap to complete)
- Today's stats bar (streak, deep work, completion %)
- Motivational quote rotation

**Morning Check-in Screen**
- Sleep quality slider (1-10)
- Energy level slider (1-10)
- Top 3 priorities (text inputs)
- Win definition (text input)
- Auto-generates action plan on submit
- Haptic feedback on completion

**Evening Reflection Screen**
- Review today's planned actions (checkboxes)
- Wins (text input)
- Challenges & lessons (text input)
- Deep work hours (number input)
- Day score slider (1-10)
- Coaching message based on score

**Habits Screen**
- List of 12 habits with toggle switches
- Current streak badges
- Completion calendar (heat map)
- Add/edit habits
- Weekly completion chart

**Journal Screen**
- Daily journal entry with framework prompts
- History list with search
- Pattern insights from entries

**Profile/Stats Screen**
- Module levels radar chart
- 30-day stats overview
- Masters library (browsable by module)
- Settings (name, coaching style, focus modules)
- Data export

### 2.5 Native Features
- **Push Notifications**: Morning reminder (configurable time), evening reflection reminder
- **Haptic Feedback**: On habit completion, check-in submission, streak milestones
- **Dark Mode**: Match existing "Mission Control" aesthetic (dark blacks, gold accents)
- **Widgets** (future): Today's wisdom, habit completion status

### 2.6 Data & Offline Strategy
- **Primary storage**: AsyncStorage (device-local, works offline)
- **Data format**: Same JSON structure as web app for compatibility
- **Knowledge base**: Bundled in app binary (masters JSON files)
- **No server required**: Fully standalone app, no backend dependency
- **Backup**: Export data as JSON file (share sheet)

### 2.7 Design System
Match existing dashboard aesthetic:
- **Background**: `#0a0a0b`, `#111113`, `#18181b`
- **Accent Gold**: `#d4a847`
- **Accent Blue**: `#3b82f6`
- **Text**: White/gray hierarchy
- **Cards**: Subtle borders, rounded corners, slight gradients
- **Typography**: System font (SF Pro on iOS), clean hierarchy

---

## File Structure

```
mobile/
├── app.json                    # Expo config
├── package.json
├── tsconfig.json
├── app/                        # Expo Router screens
│   ├── _layout.tsx            # Root layout (tab navigator)
│   ├── index.tsx              # Home/Today screen
│   ├── checkin.tsx            # Check-in screen
│   ├── habits.tsx             # Habits screen
│   ├── journal.tsx            # Journal screen
│   └── profile.tsx            # Profile/Stats screen
├── src/
│   ├── services/              # Business logic (TypeScript)
│   │   ├── StorageService.ts
│   │   ├── WisdomService.ts
│   │   ├── HabitService.ts
│   │   ├── CheckinService.ts
│   │   ├── CoachingService.ts
│   │   └── StatsService.ts
│   ├── components/            # Reusable UI components
│   │   ├── WisdomCard.tsx
│   │   ├── HabitToggle.tsx
│   │   ├── StatsBar.tsx
│   │   ├── SliderInput.tsx
│   │   ├── ModuleChip.tsx
│   │   └── CoachingMessage.tsx
│   ├── hooks/                 # React hooks
│   │   ├── useWisdom.ts
│   │   ├── useHabits.ts
│   │   ├── useCheckin.ts
│   │   └── useStats.ts
│   ├── constants/             # Theme, module config
│   │   ├── theme.ts
│   │   ├── modules.ts
│   │   └── masters.ts
│   ├── types/                 # TypeScript types
│   │   └── index.ts
│   └── assets/                # Bundled knowledge base
│       └── masters/           # Copy of knowledge_base/masters/*.json
└── ios/                       # Generated iOS project (via Expo)
```

---

## Implementation Order

1. **Phase 1 backend fixes** (~4 files, efficiency improvements)
2. **Expo project init** + TypeScript setup
3. **Services layer** (StorageService → WisdomService → HabitService → CheckinService → StatsService → CoachingService)
4. **Theme + constants** (dark mode, module config)
5. **Core screens** (Home → Habits → Check-in → Journal → Profile)
6. **Native features** (notifications, haptics)
7. **Testing on iPhone** via Expo Go app
