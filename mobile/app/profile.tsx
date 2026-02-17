import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  SafeAreaView,
  ActivityIndicator,
  TouchableOpacity,
  Alert,
} from 'react-native';
import { StorageService, StatsService } from '@/services';
import { UserProfile, Stats } from '@/types';
import { StatsBar } from '@/components/StatsBar';
import { COLORS, SPACING, TYPOGRAPHY, BORDER_RADIUS, SHADOWS } from '@/constants/theme';
import { MODULE_DISPLAY_NAMES, MODULE_COLORS, LEVEL_DESCRIPTIONS } from '@/constants/modules';

export default function ProfileScreen() {
  const [userProfile, setUserProfile] = useState<UserProfile | null>(null);
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadProfileData();
  }, []);

  const loadProfileData = async () => {
    try {
      setLoading(true);
      const profile = await StorageService.getUserProfile();
      setUserProfile(profile);

      const aggregatedStats = await StorageService.getAggregatedStats(30);
      setStats(aggregatedStats);
    } catch (error) {
      console.error('Failed to load profile:', error);
      Alert.alert('Error', 'Failed to load profile data');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={COLORS.info} />
      </View>
    );
  }

  if (!userProfile) {
    return (
      <View style={styles.container}>
        <Text style={styles.errorText}>Failed to load profile</Text>
      </View>
    );
  }

  const sortedModules = Object.entries(userProfile.module_levels)
    .sort((a, b) => b[1] - a[1]);

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView style={styles.container} showsVerticalScrollIndicator={false}>
        {/* Profile Header */}
        <View style={styles.headerCard}>
          <Text style={styles.greeting}>Welcome, {userProfile.name}! 👋</Text>
          <Text style={styles.headerSubtitle}>Your Personal Development Journey</Text>
        </View>

        {/* Quick Stats */}
        {stats && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Your Progress (Last 30 Days)</Text>
            <StatsBar
              stats={[
                {
                  label: 'Days Logged',
                  value: stats.total_days_logged,
                  icon: '📅',
                },
                {
                  label: 'Avg Score',
                  value: stats.avg_day_score.toFixed(1),
                  icon: '⭐',
                  color: COLORS.info,
                },
                {
                  label: 'Deep Work',
                  value: `${stats.total_deep_work_hours.toFixed(1)}h`,
                  icon: '⚡',
                  color: MODULE_COLORS.productivity,
                },
              ]}
              variant="horizontal"
            />
          </View>
        )}

        {/* Top Goals */}
        {userProfile.top_goals && userProfile.top_goals.length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Your Top Goals 🎯</Text>
            {userProfile.top_goals.map((goal, index) => (
              <View key={index} style={styles.goalItem}>
                <View style={styles.goalNumber}>
                  <Text style={styles.goalNumberText}>{index + 1}</Text>
                </View>
                <Text style={styles.goalText}>{goal}</Text>
              </View>
            ))}
          </View>
        )}

        {/* Module Levels */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Module Levels</Text>
          {sortedModules.map(([module, level]) => (
            <View key={module} style={styles.moduleItem}>
              <View style={styles.moduleHeader}>
                <View>
                  <Text style={styles.moduleName}>
                    {MODULE_DISPLAY_NAMES[module]}
                  </Text>
                  <Text style={styles.moduleLevelName}>
                    {LEVEL_DESCRIPTIONS[level]}
                  </Text>
                </View>
                <View
                  style={[
                    styles.levelBadge,
                    { backgroundColor: MODULE_COLORS[module] },
                  ]}
                >
                  <Text style={styles.levelText}>{level}/10</Text>
                </View>
              </View>
              <View style={styles.progressBar}>
                <View
                  style={[
                    styles.progressFill,
                    {
                      width: `${(level / 10) * 100}%`,
                      backgroundColor: MODULE_COLORS[module],
                    },
                  ]}
                />
              </View>
            </View>
          ))}
        </View>

        {/* 90-Day Goals */}
        {userProfile.goals_90_day && Object.keys(userProfile.goals_90_day).length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>90-Day Goals 🚀</Text>
            {Object.entries(userProfile.goals_90_day).map(([module, goal]) => (
              <View key={module} style={styles.goalCard}>
                <Text style={[styles.goalCardModule, { color: MODULE_COLORS[module] }]}>
                  {MODULE_DISPLAY_NAMES[module]}
                </Text>
                <Text style={styles.goalCardText}>{goal.goal}</Text>
                <View style={styles.goalProgress}>
                  <View style={styles.progressTrack}>
                    <View
                      style={[
                        styles.progressIndicator,
                        {
                          width: `${((goal.target_level - goal.start_level) / 10) * 100}%`,
                          backgroundColor: MODULE_COLORS[module],
                        },
                      ]}
                    />
                  </View>
                  <Text style={styles.goalProgressText}>
                    Level {goal.start_level} → {goal.target_level}
                  </Text>
                </View>
              </View>
            ))}
          </View>
        )}

        {/* Focus Modules */}
        {userProfile.focus_modules && userProfile.focus_modules.length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Focus Modules</Text>
            <View style={styles.focusModulesGrid}>
              {userProfile.focus_modules.map(module => (
                <View
                  key={module}
                  style={[
                    styles.focusModuleItem,
                    { backgroundColor: MODULE_COLORS[module] + '20' },
                    { borderLeftColor: MODULE_COLORS[module] },
                  ]}
                >
                  <Text style={styles.focusModuleText}>
                    {MODULE_DISPLAY_NAMES[module]}
                  </Text>
                </View>
              ))}
            </View>
          </View>
        )}

        {/* Coaching Info */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Coaching Style</Text>
          <View style={styles.coachingCard}>
            <Text style={styles.coachingStyle}>
              {userProfile.coaching_style.charAt(0).toUpperCase() +
                userProfile.coaching_style.slice(1)}
            </Text>
            <Text style={styles.coachingDescription}>
              {userProfile.coaching_style === 'direct'
                ? "No hand-holding. Direct feedback and actionable advice."
                : userProfile.coaching_style === 'supportive'
                ? "Encouraging and empathetic. You're supported every step."
                : "Balanced approach. Practical and motivational."}
            </Text>
          </View>
        </View>

        {/* Profile Actions */}
        <View style={styles.section}>
          <TouchableOpacity
            style={styles.actionButton}
            onPress={() => {
              Alert.alert('Export Data', 'Export your data as JSON', [
                {
                  text: 'Cancel',
                  style: 'cancel',
                },
                {
                  text: 'Export',
                  onPress: async () => {
                    try {
                      const data = await StorageService.exportAllData();
                      Alert.alert('Success', 'Data exported to clipboard');
                    } catch (error) {
                      Alert.alert('Error', 'Failed to export data');
                    }
                  },
                },
              ]);
            }}
          >
            <Text style={styles.actionButtonText}>📤 Export Data</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.actionButton, styles.dangerButton]}
            onPress={() => {
              Alert.alert('Clear All Data?', 'This cannot be undone.', [
                { text: 'Cancel', style: 'cancel' },
                {
                  text: 'Clear',
                  onPress: async () => {
                    try {
                      await StorageService.clearAll();
                      setUserProfile(null);
                      Alert.alert('Success', 'All data cleared');
                    } catch (error) {
                      Alert.alert('Error', 'Failed to clear data');
                    }
                  },
                  style: 'destructive',
                },
              ]);
            }}
          >
            <Text style={styles.dangerButtonText}>🗑️ Clear All Data</Text>
          </TouchableOpacity>
        </View>

        <View style={{ height: SPACING.xl }} />
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
  errorText: {
    ...TYPOGRAPHY.body,
    color: COLORS.error,
    textAlign: 'center',
    marginTop: SPACING.xl,
  },
  section: {
    marginBottom: SPACING.xl,
  },
  sectionTitle: {
    ...TYPOGRAPHY.h3,
    color: COLORS.text,
    marginBottom: SPACING.md,
  },
  headerCard: {
    backgroundColor: COLORS.surface,
    borderRadius: BORDER_RADIUS.lg,
    paddingHorizontal: SPACING.lg,
    paddingVertical: SPACING.lg,
    marginBottom: SPACING.xl,
    borderLeftWidth: 4,
    borderLeftColor: COLORS.info,
    ...SHADOWS.md,
  },
  greeting: {
    ...TYPOGRAPHY.h2,
    color: COLORS.text,
    marginBottom: SPACING.sm,
  },
  headerSubtitle: {
    ...TYPOGRAPHY.body,
    color: COLORS.textSecondary,
  },
  goalItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: SPACING.md,
    paddingHorizontal: SPACING.md,
    backgroundColor: COLORS.surface,
    borderRadius: BORDER_RADIUS.lg,
    marginBottom: SPACING.md,
    ...SHADOWS.sm,
  },
  goalNumber: {
    width: 36,
    height: 36,
    borderRadius: BORDER_RADIUS.full,
    backgroundColor: COLORS.info,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: SPACING.md,
  },
  goalNumberText: {
    ...TYPOGRAPHY.bodyBold,
    color: COLORS.white,
  },
  goalText: {
    ...TYPOGRAPHY.body,
    color: COLORS.text,
    flex: 1,
  },
  moduleItem: {
    backgroundColor: COLORS.surface,
    borderRadius: BORDER_RADIUS.lg,
    paddingHorizontal: SPACING.lg,
    paddingVertical: SPACING.md,
    marginBottom: SPACING.md,
    ...SHADOWS.sm,
  },
  moduleHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.md,
  },
  moduleName: {
    ...TYPOGRAPHY.bodyBold,
    color: COLORS.text,
    marginBottom: SPACING.xs,
  },
  moduleLevelName: {
    ...TYPOGRAPHY.caption,
    color: COLORS.textSecondary,
  },
  levelBadge: {
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.sm,
    borderRadius: BORDER_RADIUS.md,
  },
  levelText: {
    ...TYPOGRAPHY.captionBold,
    color: COLORS.white,
  },
  progressBar: {
    height: 6,
    backgroundColor: COLORS.surfaceLight,
    borderRadius: BORDER_RADIUS.full,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
  },
  goalCard: {
    backgroundColor: COLORS.surface,
    borderRadius: BORDER_RADIUS.lg,
    paddingHorizontal: SPACING.lg,
    paddingVertical: SPACING.lg,
    marginBottom: SPACING.md,
    ...SHADOWS.sm,
  },
  goalCardModule: {
    ...TYPOGRAPHY.caption,
    fontWeight: '700',
    marginBottom: SPACING.sm,
  },
  goalCardText: {
    ...TYPOGRAPHY.body,
    color: COLORS.text,
    marginBottom: SPACING.md,
  },
  goalProgress: {
    gap: SPACING.sm,
  },
  progressTrack: {
    height: 8,
    backgroundColor: COLORS.surfaceLight,
    borderRadius: BORDER_RADIUS.full,
    overflow: 'hidden',
  },
  progressIndicator: {
    height: '100%',
  },
  goalProgressText: {
    ...TYPOGRAPHY.caption,
    color: COLORS.textSecondary,
    textAlign: 'right',
  },
  focusModulesGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: SPACING.md,
  },
  focusModuleItem: {
    flex: 1,
    minWidth: '45%',
    paddingHorizontal: SPACING.lg,
    paddingVertical: SPACING.md,
    borderRadius: BORDER_RADIUS.lg,
    borderLeftWidth: 3,
  },
  focusModuleText: {
    ...TYPOGRAPHY.bodyBold,
    color: COLORS.text,
  },
  coachingCard: {
    backgroundColor: COLORS.surface,
    borderRadius: BORDER_RADIUS.lg,
    paddingHorizontal: SPACING.lg,
    paddingVertical: SPACING.lg,
    ...SHADOWS.sm,
  },
  coachingStyle: {
    ...TYPOGRAPHY.h3,
    color: COLORS.text,
    marginBottom: SPACING.md,
  },
  coachingDescription: {
    ...TYPOGRAPHY.body,
    color: COLORS.textSecondary,
  },
  actionButton: {
    backgroundColor: COLORS.surface,
    borderRadius: BORDER_RADIUS.lg,
    paddingVertical: SPACING.lg,
    paddingHorizontal: SPACING.lg,
    alignItems: 'center',
    marginBottom: SPACING.md,
    ...SHADOWS.sm,
  },
  actionButtonText: {
    ...TYPOGRAPHY.bodyBold,
    color: COLORS.info,
  },
  dangerButton: {
    backgroundColor: COLORS.error + '15',
  },
  dangerButtonText: {
    ...TYPOGRAPHY.bodyBold,
    color: COLORS.error,
  },
});
