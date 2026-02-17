import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { Habit } from '@/types';
import { COLORS, SPACING, TYPOGRAPHY, BORDER_RADIUS, SHADOWS } from '@/constants/theme';
import { MODULE_COLORS, MODULE_ICONS } from '@/constants/modules';

interface HabitToggleProps {
  habit: Habit;
  isCompleted: boolean;
  onToggle: (habitId: string, isCompleted: boolean) => Promise<void>;
  showStreak?: boolean;
}

export const HabitToggle: React.FC<HabitToggleProps> = ({
  habit,
  isCompleted,
  onToggle,
  showStreak = true,
}) => {
  const [loading, setLoading] = useState(false);
  const moduleColor = MODULE_COLORS[habit.module as keyof typeof MODULE_COLORS] || COLORS.info;
  const moduleIcon = MODULE_ICONS[habit.module as keyof typeof MODULE_ICONS] || '🎯';

  const handleToggle = async () => {
    try {
      setLoading(true);
      await onToggle(habit.id, !isCompleted);
    } catch (error) {
      Alert.alert('Error', 'Failed to update habit');
      console.error('Failed to toggle habit:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <TouchableOpacity
      style={[
        styles.container,
        isCompleted && styles.completedContainer,
        { borderLeftColor: moduleColor },
      ]}
      onPress={handleToggle}
      disabled={loading}
    >
      <View style={styles.content}>
        {/* Checkbox */}
        <View
          style={[
            styles.checkbox,
            isCompleted && styles.checkboxCompleted,
            { backgroundColor: isCompleted ? moduleColor : 'transparent' },
            { borderColor: moduleColor },
          ]}
        >
          {isCompleted && <Text style={styles.checkmark}>✓</Text>}
        </View>

        {/* Habit Info */}
        <View style={styles.habitInfo}>
          <View style={styles.habitHeader}>
            <Text style={styles.habitName}>{habit.name}</Text>
            <Text style={styles.moduleIcon}>{moduleIcon}</Text>
          </View>
          {showStreak && habit.current_streak > 0 && (
            <Text style={styles.streak}>🔥 {habit.current_streak} day streak</Text>
          )}
        </View>

        {/* Loading Indicator */}
        {loading && <ActivityIndicator color={moduleColor} size="small" />}
      </View>

      {/* Stats Row */}
      {showStreak && (
        <View style={styles.statsRow}>
          <View style={styles.stat}>
            <Text style={styles.statLabel}>Current</Text>
            <Text style={[styles.statValue, { color: moduleColor }]}>
              {habit.current_streak}
            </Text>
          </View>
          <View style={styles.divider} />
          <View style={styles.stat}>
            <Text style={styles.statLabel}>Best</Text>
            <Text style={[styles.statValue, { color: moduleColor }]}>
              {habit.best_streak}
            </Text>
          </View>
          <View style={styles.divider} />
          <View style={styles.stat}>
            <Text style={styles.statLabel}>Total</Text>
            <Text style={[styles.statValue, { color: moduleColor }]}>
              {habit.total_completions}
            </Text>
          </View>
        </View>
      )}
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: COLORS.surface,
    borderRadius: BORDER_RADIUS.lg,
    borderLeftWidth: 4,
    marginBottom: SPACING.md,
    overflow: 'hidden',
    ...SHADOWS.sm,
  },
  completedContainer: {
    opacity: 0.8,
  },
  content: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: SPACING.lg,
    paddingVertical: SPACING.md,
    gap: SPACING.md,
  },
  checkbox: {
    width: 28,
    height: 28,
    borderRadius: BORDER_RADIUS.md,
    borderWidth: 2,
    justifyContent: 'center',
    alignItems: 'center',
    flexShrink: 0,
  },
  checkboxCompleted: {
    backgroundColor: 'transparent',
  },
  checkmark: {
    fontSize: 16,
    fontWeight: '700',
    color: COLORS.white,
  },
  habitInfo: {
    flex: 1,
  },
  habitHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.xs,
  },
  habitName: {
    ...TYPOGRAPHY.body,
    color: COLORS.text,
    flex: 1,
  },
  moduleIcon: {
    fontSize: 18,
    marginLeft: SPACING.sm,
  },
  streak: {
    ...TYPOGRAPHY.caption,
    color: COLORS.warning,
  },
  statsRow: {
    flexDirection: 'row',
    alignItems: 'center',
    borderTopWidth: 1,
    borderTopColor: COLORS.surfaceLight,
    paddingHorizontal: SPACING.lg,
    paddingVertical: SPACING.sm,
  },
  stat: {
    flex: 1,
    alignItems: 'center',
  },
  statLabel: {
    ...TYPOGRAPHY.caption,
    color: COLORS.textSecondary,
    marginBottom: SPACING.xs,
  },
  statValue: {
    ...TYPOGRAPHY.bodyBold,
  },
  divider: {
    width: 1,
    height: 20,
    backgroundColor: COLORS.surfaceLight,
    marginHorizontal: SPACING.sm,
  },
});
