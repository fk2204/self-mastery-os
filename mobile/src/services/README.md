# React Native Services Layer - Self-Mastery OS Mobile

Production-ready TypeScript services for offline-first data management and business logic.

## Overview

The services layer provides a complete abstraction for:
- **Offline-first data persistence** using AsyncStorage
- **Web app compatibility** - same JSON structure as web dashboard
- **Efficient caching** with TTL-based invalidation
- **Type-safe operations** with strict TypeScript
- **Comprehensive error handling**

## Architecture

```
┌─────────────────────────────────────────┐
│         React Native Components         │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│    Service Layer (This Directory)       │
├──────────────────────────────────────────┤
│ - StorageService (data persistence)     │
│ - WisdomService (wisdom engine)         │
│ - HabitService (habit tracking)         │
│ - CheckinService (daily check-ins)      │
│ - StatsService (analytics)              │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│    AsyncStorage (Local Data)            │
└──────────────────────────────────────────┘
```

## Services

### 1. StorageService.ts

Core data persistence layer using AsyncStorage. All data stored locally with same structure as web app.

**Key Methods:**

```typescript
// User Profile
async getUserProfile(): Promise<UserProfile | null>
async saveUserProfile(profile: UserProfile): Promise<boolean>

// Daily Logs (web app format)
async getDailyLog(date?: string): Promise<DailyLog | null>
async saveDailyLog(log: DailyLog, date?: string): Promise<boolean>
async getOrCreateDailyLog(date?: string): Promise<DailyLog>
async getRecentLogs(days: number = 7): Promise<DailyLog[]>

// Habits (web app format with completions dict)
async getHabitsData(): Promise<HabitsData>
async saveHabitsData(habitsData: HabitsData): Promise<boolean>
async recordHabitCompletion(habitId: string, date?: string): Promise<boolean>

// Statistics
async getAggregatedStats(days: number = 30): Promise<Stats>
async calculateDeepWorkHours(days: number = 7): Promise<number>
async getStreak(): Promise<number>

// Caching
async getCache<T>(key: string, ttlMs?: number): Promise<T | null>
async setCache<T>(key: string, value: T, ttlMs?: number): Promise<void>
async invalidateCache(key: string): Promise<void>
```

**Data Structure:**
- All timestamps in ISO 8601 format
- Dates as YYYY-MM-DD strings
- Same JSON schema as web app for compatibility
- Offline-first: no network calls

---

### 2. WisdomService.ts

Proactive wisdom delivery from 60+ masters. Port of Python `wisdom_engine.py`.

**Key Methods:**

```typescript
// Daily wisdom (deterministic via date-seeded RNG)
async getDailyWisdom(
  focusModules?: string[],
  date?: string
): Promise<DailyWisdom | null>

// Load masters data (lazy-loaded by module)
async loadMastersModule(module: string): Promise<MastersModule | null>
async getMasters(module: string): Promise<Master[]>
async getMasterByName(module: string, name: string): Promise<Master | null>

// Wisdom components
async getDailyInsights(module: string, count?: number): Promise<string[]>
async getSkillChallenges(module: string, count?: number): Promise<string[]>
async getWorkedExamples(module: string): Promise<WorkedExample[]>
```

**Key Features:**
- **Date-seeded RNG**: Same wisdom all day (deterministic)
- **Lazy loading**: Modules load on-demand to minimize memory
- **12 life modules**: money, sales, finance, dating, mindset, health, lifestyle, business, productivity, emotional_intelligence, critical_thinking, communication
- **60+ masters**: Naval Ravikant, Alex Hormozi, Grant Cardone, David Goggins, etc.
- **Daily wisdom includes**: master teaching, insight, skill challenge, power question, mindset shift

**Example Usage:**

```typescript
// Get wisdom for today (same all day)
const wisdom = await WisdomService.getDailyWisdom(['money', 'sales']);

// Returns:
{
  date: '2026-02-17',
  master_teaching: {
    master: 'Naval Ravikant',
    expertise: 'Wealth Building',
    teaching: 'Wealth is created by...',
    practice: 'Apply this today...',
    module: 'money'
  },
  daily_insight: 'Insight text...',
  skill_challenge: { module: 'money', challenge: '...' },
  power_question: 'What would the best version...',
  mindset_shift: { from: '...', to: '...', why: '...' }
}
```

---

### 3. HabitService.ts

Habit tracking with streak management. Port of Python `data_manager.py` habit methods.

**Key Methods:**

```typescript
// Habit management
async getHabits(): Promise<Habit[]>
async getHabitById(habitId: string): Promise<Habit | null>
async addHabit(habit: Habit): Promise<void>

// Completions
async completeHabit(habitId: string, date?: string): Promise<void>
async uncompleteHabit(habitId: string, date?: string): Promise<void>
async isHabitCompletedToday(habitId: string): Promise<boolean>
async getTodayCompletions(): Promise<string[]>

// Streaks (cached for efficiency)
async getStreak(habitId: string): Promise<number>
async getTotalCompletions(habitId: string): Promise<number>
async getHabitHistory(habitId: string, days?: number): Promise<Map<string, boolean>>

// Queries
async getHabitsByStatus(): Promise<{ completed: Habit[]; incomplete: Habit[] }>
async getHabitsByModule(module: string): Promise<Habit[]>
async getCompletionRate(days?: number): Promise<number>
```

**Streaks:**
- Incremental updates (not full recalculation)
- Cached with 1-hour TTL
- Handles gap logic correctly
- Tracks both current and best streaks

---

### 4. CheckinService.ts

Daily check-in workflows. Port of Python `daily_checkin.py`.

**Key Methods:**

```typescript
// Check-in status
async getTodaysCheckin(): Promise<TodaysCheckin>
async checkAlreadyCheckedInMorning(): Promise<boolean>
async checkAlreadyReflectedEvening(): Promise<boolean>

// Morning check-in (with validation)
async saveMorningCheckin(data: {
  sleep_hours: number;
  sleep_quality: number;
  energy_level: number;
  top_3_priorities: string[];
  win_definition: string;
}): Promise<void>

// Evening reflection (with validation)
async saveEveningReflection(data: {
  wins: string[];
  challenges: string[];
  lessons: string[];
  improvement_for_tomorrow: string;
  deep_work_hours: number;
  day_score: number;
}): Promise<void>

// Statistics
async getAverageDayScore(days?: number): Promise<number>
async getTotalDeepWorkHours(days?: number): Promise<number>
async getRecentWins(days?: number): Promise<string[]>
async getRecentChallenges(days?: number): Promise<string[]>
```

**Features:**
- Input validation & sanitization
- Auto-clamps values to valid ranges
- Detects if main win was achieved
- Supports partial updates

---

### 5. StatsService.ts

Aggregated statistics and analytics. Port of Python `data_manager.py` stats methods.

**Key Methods:**

```typescript
// Statistics (cached)
async getStats(days?: number): Promise<Stats>
async getStatsForRanges(ranges?: number[]): Promise<Record<number, Stats>>

// Cache management
async invalidateStatsCache(days?: number): Promise<void>
async invalidateAllStatsCache(): Promise<void>

// Legacy methods
async generateTodayStats(moduleLevels: ModuleLevels): Promise<ProgressStats>
async getModuleProgress(module: string, days?: number): Promise<number[]>
async getWeekOverWeekImprovement(): Promise<{...}>
```

**Cached Metrics (5-minute TTL):**
- Days logged
- Check-ins completed
- Average sleep, energy, day score
- Deep work hours
- Habit completion rate

---

## Usage Examples

### Morning Check-in

```typescript
import { CheckinService } from '@/services';

// Save morning check-in
await CheckinService.saveMorningCheckin({
  sleep_hours: 7.5,
  sleep_quality: 8,
  energy_level: 8,
  top_3_priorities: [
    'Complete sales outreach',
    'Write blog post',
    'Client meeting prep'
  ],
  win_definition: 'Close one new client'
});
```

### Complete a Habit

```typescript
import { HabitService } from '@/services';

// Mark habit as complete for today
await HabitService.completeHabit('deep_work_90');

// Get updated streak
const streak = await HabitService.getStreak('deep_work_90');
console.log(`Current streak: ${streak} days`);
```

### Get Daily Wisdom

```typescript
import { WisdomService } from '@/services';

const wisdom = await WisdomService.getDailyWisdom(
  ['money', 'sales', 'productivity']
);

console.log(`Today's teaching from: ${wisdom.master_teaching.master}`);
console.log(`Challenge: ${wisdom.skill_challenge.challenge}`);
```

### Get Statistics

```typescript
import { StatsService } from '@/services';

// Get stats for last 30 days
const stats = await StatsService.getStats(30);

console.log(`Days logged: ${stats.total_days_logged}`);
console.log(`Avg day score: ${stats.avg_day_score}`);
console.log(`Deep work hours: ${stats.total_deep_work_hours}`);
```

---

## Data Structures

### Daily Log (Web App Format)

```typescript
{
  date: "2026-02-17",
  created_at: "2026-02-17T08:00:00Z",
  am_checkin: {
    time: "2026-02-17T08:05:00Z",
    sleep_hours: 7,
    sleep_quality: 8,
    energy_level: 8,
    top_3_priorities: ["Priority 1", "Priority 2", "Priority 3"],
    win_definition: "What would make today a win"
  },
  pm_reflection: {
    time: "2026-02-17T20:00:00Z",
    wins: ["Win 1", "Win 2"],
    challenges: ["Challenge 1"],
    lessons: ["Lesson 1"],
    improvement_for_tomorrow: "Next action",
    day_score: 9,
    main_win_achieved: true
  },
  metrics: {
    deep_work_hours: 4,
    workouts: 1,
    sales_calls: 5,
    social_interactions: 2,
    steps: 8000,
    water_liters: 2
  },
  habits: {},
  notes: ""
}
```

### Habits Data (Web App Format)

```typescript
{
  habits: [
    {
      id: "deep_work_90",
      name: "Deep Work Block (90+ min)",
      module: "productivity",
      frequency: "daily",
      created_at: "2025-02-03T10:00:00Z",
      current_streak: 15,
      best_streak: 25,
      total_completions: 42
    }
  ],
  completions: {
    "2026-02-16": ["deep_work_90", "morning_routine"],
    "2026-02-17": ["deep_work_90", "morning_routine", "sales_outreach"]
  }
}
```

---

## Offline-First Design

All services operate offline:
- No network calls required
- Data synced to AsyncStorage immediately
- Works in airplane mode
- Optional server sync (implement in future)

---

## Error Handling

All services include:
- Try-catch blocks for all async operations
- Detailed error logging
- Graceful degradation (returns sensible defaults)
- Input validation & sanitization

**Example:**

```typescript
try {
  await CheckinService.saveMorningCheckin(data);
} catch (error) {
  if (error.message === 'Invalid sleep hours') {
    // Handle validation error
  }
  console.error(error);
}
```

---

## Performance Optimizations

### Caching
- Habit streaks: 1-hour TTL
- Statistics: 5-minute TTL
- Wisdom: No cache (date-seeded for consistency)

### Lazy Loading
- Masters data loaded by module on-demand
- Minimal memory footprint
- Fast initial load

### Incremental Updates
- Habit completions update streaks incrementally
- No full recalculation on every update

---

## Type Safety

All services fully typed with TypeScript (strict mode):

```typescript
// Self-documented, IDE auto-complete
const wisdom: DailyWisdom = await WisdomService.getDailyWisdom();
const habits: Habit[] = await HabitService.getHabits();
const stats: Stats = await StatsService.getStats(30);
```

---

## Testing

Services are designed to be testable:
- All async operations can be mocked
- Deterministic date-seeded RNG for testing wisdom
- Can reset/clear data for test isolation

---

## Future Enhancements

- [ ] Server sync (optional, offline-first always maintained)
- [ ] Biometric tracking integration
- [ ] Cloud backup
- [ ] Cross-device sync
- [ ] Advanced analytics

---

## Files

- `StorageService.ts` - 500+ lines, data persistence
- `WisdomService.ts` - 400+ lines, wisdom delivery
- `HabitService.ts` - 250+ lines, habit tracking
- `CheckinService.ts` - 300+ lines, daily check-ins
- `StatsService.ts` - 300+ lines, analytics
- `index.ts` - Exports all services

**Total:** ~1,750 lines of production TypeScript

---

## Related Files

- `/mobile/src/types/index.ts` - All TypeScript type definitions
- `/knowledge_base/masters/` - Master data (JSON)
- `/mobile/src/constants/` - App constants
