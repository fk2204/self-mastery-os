# Self-Mastery OS - React Native + Expo iPhone App

A production-ready React Native application for personal development tracking and daily coaching, built with Expo and TypeScript.

## Overview

Self-Mastery OS is your personal development companion - a daily coaching system that helps you track habits, complete check-ins, and receive wisdom from world-class masters across 12 life modules.

**Key Features:**
- 📱 iOS-optimized with safe area handling and notch support
- 🎯 12 Life Modules with personalized coaching
- 📝 Daily morning check-ins and evening reflections
- 🎯 12 habit tracking with streaks and analytics
- 📚 Daily wisdom from 60+ masters (Naval, Hormozi, Buffett, Turner, Carter, etc.)
- 📔 Journal entries with mood tracking
- 📊 Progress analytics and statistics
- 💾 Offline-first with AsyncStorage
- 🎨 Dark theme "Mission Control" aesthetic
- ⚡ Fast, performant, production-ready code

## Project Structure

```
mobile/
├── app/                        # Expo Router screens (auto-routing)
│   ├── _layout.tsx            # Root layout with tab navigation
│   ├── index.tsx              # Today's dashboard
│   ├── checkin.tsx            # Morning & evening check-in
│   ├── habits.tsx             # Daily habits tracking
│   ├── journal.tsx            # Journaling interface
│   └── profile.tsx            # User profile & settings
├── src/
│   ├── services/              # Business logic layer
│   │   ├── StorageService.ts  # Offline persistence
│   │   ├── WisdomService.ts   # Daily coaching
│   │   ├── HabitService.ts    # Habit management
│   │   ├── CheckinService.ts  # Check-in logic
│   │   ├── StatsService.ts    # Analytics
│   │   └── index.ts           # Barrel export
│   ├── hooks/                 # React hooks
│   │   ├── useWisdom.ts       # Wisdom loading
│   │   ├── useHabits.ts       # Habit management
│   │   └── useCheckin.ts      # Check-in state
│   ├── components/            # Reusable UI components
│   │   ├── WisdomCard.tsx     # Daily wisdom display
│   │   ├── HabitToggle.tsx    # Habit checkbox + stats
│   │   └── StatsBar.tsx       # Statistics display
│   ├── types/                 # TypeScript interfaces
│   │   └── index.ts           # All type definitions
│   ├── constants/             # Constants and config
│   │   ├── theme.ts           # Colors, spacing, typography
│   │   └── modules.ts         # Module names, icons, colors
│   └── assets/
│       └── masters/           # Knowledge base (JSON)
├── app.json                   # Expo configuration
├── package.json               # Dependencies
├── tsconfig.json              # TypeScript config
└── babel.config.js            # Babel configuration
```

## Quick Start

### Prerequisites

- Node.js 18+ and npm/yarn
- Expo CLI: `npm install -g expo-cli`
- iPhone/iOS simulator or physical device
- Xcode (for iOS simulator)

### Installation

1. **Install dependencies:**
   ```bash
   cd mobile
   npm install
   ```

2. **Create `.env` file (optional):**
   ```bash
   cp .env.example .env
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

4. **Open on iPhone:**
   - **Simulator:** Press `i`
   - **Physical device:** Scan QR code with Expo app

### Development Commands

```bash
# Start Expo dev server
npm start

# iOS only
npm run ios

# Android (if needed)
npm run android

# Type checking
npm run type-check

# Run tests
npm test
```

## Architecture

### Services Layer (Business Logic)

All business logic is isolated in services that can be tested independently:

- **StorageService**: Offline-first persistence with AsyncStorage (compatible with web app JSON structure)
- **WisdomService**: Daily wisdom generation with seeded RNG (deterministic throughout the day)
- **HabitService**: Habit completion tracking, streak calculation, statistics
- **CheckinService**: Morning check-ins and evening reflections
- **StatsService**: Progress analytics and aggregated statistics

### Hooks Layer (React State Management)

Custom hooks provide clean data binding:

- `useWisdom()` - Load and refresh daily wisdom
- `useMaster()` - Get specific master data
- `useHabits()` - Habit list with completion toggle
- `useHabitStatus()` - Today's completion status
- `useTodayCheckin()` - Today's check-in data
- `useMorningCheckin()` / `useEveningCheckin()` - Check-in workflows

### Components Layer (UI)

Reusable, composable components:

- **WisdomCard**: Full-featured wisdom display with teachings, insights, challenges
- **HabitToggle**: Individual habit toggle with streaks and stats
- **StatsBar**: Flexible statistics display (horizontal/grid layout)

### Screens

Five main screens in Expo Router tabs:

1. **Today** (index.tsx)
   - Daily wisdom card
   - Quick stats (streak, score, deep work)
   - Recent wins
   - 90-day goals

2. **Check-in** (checkin.tsx)
   - Morning check-in (sleep quality, energy, priorities, win definition)
   - Evening reflection (wins, challenges, deep work, day score)
   - Modal forms with sliders and text inputs

3. **Habits** (habits.tsx)
   - All 12 habits grouped by module
   - Today's completion stats
   - Individual habit toggle with streaks
   - Completion percentage

4. **Journal** (journal.tsx)
   - Write and save journal entries
   - Mood tracking (1-10 with emoji)
   - Entry list with preview
   - View/delete entries

5. **Profile** (profile.tsx)
   - User profile summary
   - Module levels with progress bars
   - 90-day goals
   - Focus modules
   - Settings (export data, clear all)

## Data Structures

### Key Types

```typescript
// User profile with module levels and goals
UserProfile {
  name: string
  module_levels: ModuleLevels  // 1-10 per module
  goals_90_day: Record<string, NinetyDayGoal>
  focus_modules: string[]
}

// Daily tracking
DailyCheckin {
  date: string
  morning: MorningCheckin
  evening: EveningCheckin
}

// Habits with streaks
Habit {
  id: string
  name: string
  module: string
  current_streak: number
  best_streak: number
  total_completions: number
}

// Master teachings
Master {
  name: string
  expertise: string
  key_principles: string[]
  daily_practices: string[]
  worked_examples: WorkedExample[]
}
```

## Offline-First Architecture

All data is stored locally in AsyncStorage using the same JSON structure as the web app:

- **User Profile** - Cached, updated rarely
- **Habits** - Cached with completions index
- **Daily Logs** - One per date (YYYY-MM-DD.json format)
- **Statistics** - Aggregated periodically
- **Journal Entries** - Fully local

No backend required - data syncs are optional.

## Theme & Styling

Professional "Mission Control" dark theme:

- **Background**: `#0a0a0a` (true black)
- **Surface**: `#1a1a1a` (dark gray)
- **Text**: `#ffffff` (white)
- **Accents**: Module-specific colors (gold, red, blue, pink, purple, green, etc.)

All styling defined in `src/constants/theme.ts`:
- `COLORS` - Color palette
- `SPACING` - 4px grid (xs, sm, md, lg, xl, xxl, xxxl)
- `TYPOGRAPHY` - Font sizes, weights, line heights
- `BORDER_RADIUS` - Consistent radii
- `SHADOWS` - Elevation system

## Adding New Masters

Add teaching data to `src/assets/masters/{module}_masters.json`:

```json
{
  "name": "Master Name",
  "expertise": "Their area of expertise",
  "key_principles": ["Principle 1", "Principle 2"],
  "daily_practices": ["Practice 1", "Practice 2"],
  "worked_examples": [{
    "title": "Example Title",
    "scenario": "Situation...",
    "framework_applied": "Framework name",
    "step_by_step": ["Step 1", "Step 2"],
    "outcome": "Expected result"
  }],
  "scripts_templates": [{
    "title": "Template Title",
    "context": "When to use",
    "template": "Template text with ___ blanks",
    "example_filled": "Example with blanks filled"
  }],
  "resources": {
    "books": [{"title": "Book", "author": "Author", "key_takeaway": "Insight"}],
    "podcasts": [{"title": "Podcast", "episode": "Name", "key_takeaway": "Insight"}]
  }
}
```

## Building for iOS

### Development Build (EAS)

```bash
# Install EAS CLI
npm install -g eas-cli

# Login to Expo
eas login

# Build for development
eas build --platform ios --profile preview

# Or for production
eas build --platform ios
```

### Manual Build with Xcode

```bash
# Create iOS build
expo prebuild --clean

# Open in Xcode
open ios/SelfMasteryOS.xcworkspace

# Build in Xcode with your signing certificate
```

### TestFlight / App Store

1. Update version in `app.json` and `package.json`
2. Build for production: `eas build --platform ios`
3. Submit to App Store Connect
4. Review and release

## Performance Optimization

- **Lazy loading** of master data (only loaded when needed)
- **Date-seeded RNG** for deterministic daily wisdom (same seed = same wisdom all day)
- **AsyncStorage caching** with TTL for frequently accessed data
- **Memoization** of expensive calculations
- **FlatList/ScrollView** optimization with proper keys
- **Code splitting** with Expo Router (automatic)

## Testing

Add tests in `__tests__/` directory:

```bash
npm run test
```

Example test structure:

```typescript
import { render, screen, fireEvent } from '@testing-library/react-native';
import HabitToggle from '@/components/HabitToggle';

describe('HabitToggle', () => {
  it('toggles habit completion', async () => {
    const { getByRole } = render(
      <HabitToggle habit={mockHabit} isCompleted={false} onToggle={jest.fn()} />
    );
    fireEvent.press(getByRole('button'));
    expect(getByRole('button')).toHaveStyle({ opacity: 0.8 });
  });
});
```

## Troubleshooting

### Common Issues

**App won't start:**
```bash
# Clear cache and reinstall
npm install
npx expo prebuild --clean
npm start
```

**Wisdom not loading:**
- Check that master JSON files exist in `src/assets/masters/`
- Verify file names match module names (e.g., `money_masters.json`)

**Storage issues:**
- AsyncStorage has ~10MB limit on iOS
- Clear old data: Settings > Profile > Clear All Data

**Type errors:**
```bash
npm run type-check
# Fix TypeScript errors before building
```

## Dependencies

### Core
- `expo` - React Native framework
- `expo-router` - File-based routing
- `react-native` - Native UI
- `react` - UI framework

### UI & Styling
- `react-native-screens` - Native screen navigation
- `react-native-gesture-handler` - Gesture support
- `react-native-reanimated` - Animations

### Storage
- `@react-native-async-storage/async-storage` - Offline persistence

### Utilities
- `date-fns` - Date manipulation
- `expo-status-bar` - Status bar handling
- `expo-splash-screen` - Splash screen
- `expo-notifications` - Push notifications
- `expo-haptics` - Haptic feedback

### Development
- `typescript` - Type safety
- `babel-preset-expo` - Babel preset
- `@types/react-native` - Type definitions

## Future Enhancements

- Push notifications for check-ins and habits
- Sync to cloud backend (optional)
- Share progress on social media
- Dark/Light theme toggle
- Custom modules creation
- Workout/health data integration
- Calendar view of habits
- Leaderboards (optional)

## License

MIT - Self-Mastery OS

## Support

For issues or feature requests, open an issue on GitHub or contact support.

## Architecture Decisions

### Why AsyncStorage (not SQLite)?

- Simpler for this use case (JSON data)
- Easier to sync with web app
- Sufficient for data volumes (~1MB/month)
- No migration needed

### Why Expo Router (not React Navigation)?

- File-based routing (faster development)
- Built-in TypeScript support
- Better deep linking
- Cleaner code structure

### Why Date-seeded RNG (not truly random)?

- Same wisdom throughout the day (better UX)
- Deterministic and testable
- No state needed
- Works offline

## Credits

Built with React Native, Expo, and inspired by the Self-Mastery OS web application.

Wisdom from 60+ masters: Naval Ravikant, Alex Hormozi, Warren Buffett, Charlie Munger, Brandon Turner, Nic Carter, David Goggins, Jocko Willink, Marcus Aurelius, and many more.
