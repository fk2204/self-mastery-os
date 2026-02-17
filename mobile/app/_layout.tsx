import React, { useEffect, useState } from 'react';
import { Stack, Tabs } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import * as SplashScreen from 'expo-splash-screen';
import { StorageService } from '@/services';
import { UserProfile, Habit } from '@/types';
import { COLORS } from '@/constants/theme';
import { MODULE_ICONS } from '@/constants/modules';
import { DEFAULT_HABITS } from '@/constants/modules';

// Keep splash screen visible while loading
SplashScreen.preventAutoHideAsync();

const DEFAULT_USER_PROFILE: UserProfile = {
  name: 'Boss',
  created_at: new Date().toISOString(),
  updated_at: new Date().toISOString(),
  top_goals: [
    'Build multiple income streams to $10K/month',
    'Master sales, persuasion, and closing',
    'Achieve financial independence through smart investing',
  ],
  daily_time_available_minutes: 90,
  coaching_style: 'direct',
  constraints: ['time'],
  module_levels: {
    money: 5,
    sales: 4,
    finance: 5,
    dating: 5,
    mindset: 6,
    health: 8,
    lifestyle: 5,
    business: 5,
    productivity: 6,
    emotional_intelligence: 3,
    critical_thinking: 3,
    communication: 3,
  },
  focus_modules: ['money', 'sales', 'finance', 'productivity', 'business'],
  goals_90_day: {},
};

const DEFAULT_HABITS_DATA: Habit[] = DEFAULT_HABITS.map(h => ({
  id: h.id,
  name: h.name,
  module: h.module,
  frequency: 'daily',
  created_at: new Date().toISOString(),
  current_streak: 0,
  best_streak: 0,
  total_completions: 0,
}));

export default function RootLayout() {
  const [appIsReady, setAppIsReady] = useState(false);

  useEffect(() => {
    async function prepare() {
      try {
        // Initialize storage with default data
        await StorageService.initialize(DEFAULT_USER_PROFILE, DEFAULT_HABITS_DATA);
        setAppIsReady(true);
      } catch (e) {
        console.warn(e);
        setAppIsReady(true);
      } finally {
        await SplashScreen.hideAsync();
      }
    }

    prepare();
  }, []);

  if (!appIsReady) {
    return null;
  }

  return (
    <SafeAreaProvider>
      <Tabs
        screenOptions={{
          headerShown: true,
          headerStyle: {
            backgroundColor: COLORS.surface,
            borderBottomColor: COLORS.surfaceLight,
            borderBottomWidth: 1,
          },
          headerTintColor: COLORS.text,
          headerTitleStyle: {
            fontWeight: '600',
            fontSize: 18,
          },
          tabBarStyle: {
            backgroundColor: COLORS.surface,
            borderTopColor: COLORS.surfaceLight,
            borderTopWidth: 1,
            paddingBottom: 8,
            paddingTop: 8,
            height: 60,
          },
          tabBarActiveTintColor: COLORS.info,
          tabBarInactiveTintColor: COLORS.textTertiary,
          tabBarLabelStyle: {
            fontSize: 11,
            marginTop: 2,
          },
        }}
      >
        {/* Home/Today Tab */}
        <Tabs.Screen
          name="index"
          options={{
            title: 'Today',
            headerTitle: 'Self-Mastery OS',
            tabBarIcon: ({ color }) => <Text style={{ color, fontSize: 20 }}>🏠</Text>,
            tabBarLabel: 'Today',
          }}
        />

        {/* Check-in Tab */}
        <Tabs.Screen
          name="checkin"
          options={{
            title: 'Check-in',
            headerTitle: 'Daily Check-in',
            tabBarIcon: ({ color }) => <Text style={{ color, fontSize: 20 }}>📝</Text>,
            tabBarLabel: 'Check-in',
          }}
        />

        {/* Habits Tab */}
        <Tabs.Screen
          name="habits"
          options={{
            title: 'Habits',
            headerTitle: 'Daily Habits',
            tabBarIcon: ({ color }) => <Text style={{ color, fontSize: 20 }}>🎯</Text>,
            tabBarLabel: 'Habits',
          }}
        />

        {/* Journal Tab */}
        <Tabs.Screen
          name="journal"
          options={{
            title: 'Journal',
            headerTitle: 'Journaling',
            tabBarIcon: ({ color }) => <Text style={{ color, fontSize: 20 }}>📚</Text>,
            tabBarLabel: 'Journal',
          }}
        />

        {/* Profile Tab */}
        <Tabs.Screen
          name="profile"
          options={{
            title: 'Profile',
            headerTitle: 'Your Profile',
            tabBarIcon: ({ color }) => <Text style={{ color, fontSize: 20 }}>👤</Text>,
            tabBarLabel: 'Profile',
          }}
        />
      </Tabs>

      <StatusBar barStyle="light-content" backgroundColor={COLORS.background} />
    </SafeAreaProvider>
  );
}

// Re-export Text for tab icons
import { Text } from 'react-native';
