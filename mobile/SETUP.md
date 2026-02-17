# Quick Start Setup Guide

## One-Minute Setup

```bash
# Navigate to mobile directory
cd mobile

# Install dependencies
npm install

# Start development server
npm start

# Scan QR code with Expo Go app (iPhone)
# OR press 'i' for iOS simulator
```

That's it! The app will open on your device/simulator.

## Full Setup for Development

### 1. Prerequisites

**Install Node.js 18+:**
- Download from https://nodejs.org
- Verify: `node --version` (should be v18+)

**Install Expo CLI:**
```bash
npm install -g expo-cli
```

**For iOS Simulator:**
- macOS with Xcode installed
- Command: `xcode-select --install`

**For Physical Device:**
- Install Expo Go app from App Store
- Same WiFi as development machine

### 2. Clone & Install

```bash
# Clone if needed
git clone <repo>
cd self-mastery-os/mobile

# Install dependencies
npm install

# Verify TypeScript
npm run type-check
```

### 3. Run Development Server

```bash
# Start Expo dev server
npm start

# You'll see a menu:
# i - Open iOS simulator
# a - Open Android emulator
# w - Open web preview
# r - Reload
# q - Quit
```

### 4. Connect Your Device

**Option A: iPhone Simulator**
```bash
npm run ios
# Simulator opens automatically
```

**Option B: Physical iPhone**
```bash
npm start
# Scan QR code with Camera app
# Opens in Expo Go
```

## First Run

When you first open the app:

1. **Splash Screen** - Shows briefly while loading
2. **Today Tab** - Opens with default profile "Boss"
3. **Daily Wisdom** - Shows random wisdom from masters
4. **Default Habits** - 12 habits ready to track

### Try These Actions

1. **Add a Habit Completion**: Go to Habits tab, tap any habit checkbox
2. **Morning Check-in**: Go to Check-in tab, fill out morning form
3. **Write a Journal Entry**: Go to Journal tab, tap + button
4. **View Your Profile**: Go to Profile tab to see module levels

## Configuration

### Change User Profile

Edit default profile in `app/_layout.tsx`:

```typescript
const DEFAULT_USER_PROFILE: UserProfile = {
  name: "Your Name",  // Change this
  coaching_style: "direct",  // or "supportive", "balanced"
  daily_time_available_minutes: 90,
  // ... rest of config
};
```

### Change Theme Colors

Edit `src/constants/theme.ts`:

```typescript
export const COLORS = {
  background: "#0a0a0a",  // Change to your preference
  info: "#4dabf7",
  // ... more colors
};
```

### Add New Masters

1. Add JSON file to `src/assets/masters/{module}_masters.json`
2. Follow the format in existing files
3. Will be loaded automatically

## Development Workflow

### Making Changes

1. **Edit files** in `src/` or `app/`
2. **Save** - App hot-reloads automatically (Fast Refresh)
3. **Test** on device/simulator

### Common Tasks

**Add a new screen:**
```bash
# Create new file in app/ directory
# app/mynewscreen.tsx
# It auto-routes based on filename
```

**Add a new component:**
```bash
# Create in src/components/
# Import in screens
import { MyComponent } from '@/components/MyComponent';
```

**Add a new service:**
```bash
# Create in src/services/
# Import and export in src/services/index.ts
export { default as MyService } from './MyService';
```

### Debug Mode

**View Console Logs:**
```bash
# In dev menu (shake device or Ctrl+M)
# Tap "Debug Remote JS"
# Opens browser dev tools
```

**Type Checking:**
```bash
npm run type-check
# Shows TypeScript errors
```

## Testing on Device

### Prerequisites for Physical iPhone

1. **WiFi Network:**
   - Mac and iPhone on same WiFi
   - Not enterprise/restricted WiFi

2. **Expo Go App:**
   - Download from App Store
   - Free, no account needed (can sign up)

3. **QR Code:**
   - Show when you run `npm start`
   - Point iPhone camera at it
   - Tap Expo Go link

### Troubleshooting Connection

```bash
# If QR code doesn't work:
# 1. Make sure both devices are on same network
# 2. Check firewall isn't blocking port 19000-19001
# 3. Try tunnel mode:
npm start -- --tunnel

# Or use LAN mode (default):
npm start -- --lan
```

## Build for TestFlight

```bash
# Install EAS CLI
npm install -g eas-cli

# Login to Expo
eas login

# Build for iOS
eas build --platform ios --profile preview

# Get download link after build completes
# Upload to TestFlight in App Store Connect
```

## Data Storage

### Where Data is Stored

**iPhone (Simulator & Device):**
- AsyncStorage in app's document directory
- Path: `~/Library/Developer/CoreSimulator/Devices/.../data/.../NoSQL/`
- Persists between app restarts

**Web App Compatibility:**
- Uses same JSON format as web dashboard
- Can export and import

### Backup Data

```
Profile > Export Data → saves JSON
```

### Clear All Data

```
Profile > Clear All Data → resets to defaults
```

## Performance Tips

### Speed Up Initial Load

```bash
# Clear cache
npm start -- --clear

# Reinstall if still slow
rm -rf node_modules
npm install
```

### Debug Performance

1. Open dev menu (shake or Ctrl+M)
2. Tap "Perf Monitor"
3. Watch FPS and memory usage

## Common Issues

### "Cannot find module '@/services'"

```bash
# Path alias not working
# Make sure app.json has:
"plugins": ["babel-preset-expo"]

# Restart dev server:
npm start --clear
```

### "AsyncStorage key not found"

```bash
# Data not initialized
# Go to Profile tab and check
# Or clear data and restart
```

### "Wisdom card won't load"

```bash
# Check masters JSON files exist:
ls src/assets/masters/

# If missing, copy them:
cp ../knowledge_base/masters/*.json src/assets/masters/
```

### "Habit won't toggle"

```bash
# Storage error
# Clear app data and restart
# Go to Profile > Clear All Data
```

## Next Steps

1. **Explore the UI** - Click around all tabs
2. **Complete a morning check-in** - Get the flow
3. **Mark some habits** - See streaks work
4. **Read the code** - Understand architecture
5. **Make a change** - Edit a component
6. **Build and test** - Deploy to TestFlight

## Getting Help

### Documentation

- [React Native Docs](https://reactnative.dev)
- [Expo Docs](https://docs.expo.dev)
- [TypeScript Docs](https://www.typescriptlang.org/docs)
- [AsyncStorage Docs](https://react-native-async-storage.github.io/async-storage/)

### Debug Resources

- Check console logs in dev menu
- Use React DevTools browser extension
- Read type errors in `npm run type-check`

## What's Next?

After setup is working:

1. **Customize** the user profile
2. **Add more masters** to knowledge base
3. **Sync to backend** (optional)
4. **Build for App Store**
5. **Deploy TestFlight beta**
6. **Iterate with feedback**

Happy coding! 🚀
