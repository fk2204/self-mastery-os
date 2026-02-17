import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  SafeAreaView,
  RefreshControl,
  ActivityIndicator,
} from 'react-native';
import { useHabits, useHabitStatus } from '@/hooks/useHabits';
import { HabitToggle } from '@/components/HabitToggle';
import { StatsBar } from '@/components/StatsBar';
import { HabitService } from '@/services';
import { COLORS, SPACING, TYPOGRAPHY, BORDER_RADIUS, SHADOWS } from '@/constants/theme';
import { MODULE_COLORS, MODULE_DISPLAY_NAMES } from '@/constants/modules';

export default function HabitsScreen() {
  const { habits, loading: habitsLoading, completeHabit, uncompleteHabit, refreshHabits } = useHabits();
  const { completedToday, isCompleted, refreshStatus } = useHabitStatus();
  const [refreshing, setRefreshing] = useState(false);
  const [completionPercentage, setCompletionPercentage] = useState(0);
  const [groupedHabits, setGroupedHabits] = useState<Record<string, typeof habits>>({});

  useEffect(() => {
    loadCompletionPercentage();
    groupHabitsByModule();
  }, [habits, completedToday]);

  const loadCompletionPercentage = async () => {
    try {
      const percentage = await HabitService.getCompletionPercentage(1);
      setCompletionPercentage(percentage);
    } catch (error) {
      console.error('Failed to load completion percentage:', error);
    }
  };

  const groupHabitsByModule = () => {
    const grouped: Record<string, typeof habits> = {};
    habits.forEach(habit => {
      if (!grouped[habit.module]) {
        grouped[habit.module] = [];
      }
      grouped[habit.module].push(habit);
    });
    setGroupedHabits(grouped);
  };

  const handleToggle = async (habitId: string, shouldComplete: boolean) => {
    try {
      if (shouldComplete) {
        await completeHabit(habitId);
      } else {
        await uncompleteHabit(habitId);
      }
      await refreshStatus();
    } catch (error) {
      console.error('Failed to toggle habit:', error);
    }
  };

  const handleRefresh = async () => {
    try {
      setRefreshing(true);
      await Promise.all([refreshHabits(), refreshStatus()]);
      await loadCompletionPercentage();
    } catch (error) {
      console.error('Failed to refresh:', error);
    } finally {
      setRefreshing(false);
    }
  };

  if (habitsLoading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={COLORS.info} />
      </View>
    );
  }

  const completedCount = habits.filter(h => isCompleted(h.id)).length;

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView
        style={styles.container}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={handleRefresh} />}
        showsVerticalScrollIndicator={false}
      >
        {/* Completion Stats */}
        <View style={styles.section}>
          <StatsBar
            stats={[
              {
                label: 'Today',
                value: `${completedCount}/${habits.length}`,
                icon: '✓',
                color: COLORS.success,
              },
              {
                label: 'Completion',
                value: `${completionPercentage}%`,
                icon: '📊',
                color: COLORS.info,
              },
            ]}
            variant="horizontal"
          />
        </View>

        {/* Habits by Module */}
        {Object.entries(groupedHabits).map(([module, moduleHabits]) => (
          <View key={module} style={styles.moduleSection}>
            <View style={styles.moduleHeader}>
              <Text style={[styles.moduleName, { color: MODULE_COLORS[module] }]}>
                {MODULE_DISPLAY_NAMES[module]}
              </Text>
              <Text style={styles.moduleCount}>
                {moduleHabits.filter(h => isCompleted(h.id)).length}/{moduleHabits.length}
              </Text>
            </View>

            {moduleHabits.map(habit => (
              <HabitToggle
                key={habit.id}
                habit={habit}
                isCompleted={isCompleted(habit.id)}
                onToggle={handleToggle}
                showStreak={true}
              />
            ))}
          </View>
        ))}

        {/* Spacing */}
        <View style={{ height: SPACING.lg }} />
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
    paddingHorizontal: SPACING.lg,
    paddingTop: SPACING.lg,
  },
  loadingContainer: {
    flex: 1,
    backgroundColor: COLORS.background,
    justifyContent: 'center',
    alignItems: 'center',
  },
  section: {
    marginBottom: SPACING.xl,
  },
  moduleSection: {
    marginBottom: SPACING.xl,
  },
  moduleHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.md,
    paddingHorizontal: SPACING.sm,
  },
  moduleName: {
    ...TYPOGRAPHY.h3,
    fontWeight: '600',
  },
  moduleCount: {
    ...TYPOGRAPHY.bodyBold,
    color: COLORS.textSecondary,
  },
});
