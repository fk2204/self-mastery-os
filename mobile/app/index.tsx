import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
  SafeAreaView,
  RefreshControl,
} from 'react-native';
import { useWisdom } from '@/hooks/useWisdom';
import { useCheckinStats } from '@/hooks/useCheckin';
import { StorageService, StatsService } from '@/services';
import { UserProfile, ProgressStats } from '@/types';
import { WisdomCard } from '@/components/WisdomCard';
import { StatsBar } from '@/components/StatsBar';
import { COLORS, SPACING, TYPOGRAPHY, BORDER_RADIUS, SHADOWS } from '@/constants/theme';
import { MODULE_COLORS } from '@/constants/modules';

export default function HomeScreen() {
  const [userProfile, setUserProfile] = useState<UserProfile | null>(null);
  const [stats, setStats] = useState<ProgressStats | null>(null);
  const [refreshing, setRefreshing] = useState(false);
  const [loadingProfile, setLoadingProfile] = useState(true);

  const { dailyWisdom, loading: wisdomLoading, error: wisdomError, refreshWisdom } = useWisdom(
    'money',
    ['money', 'sales', 'finance', 'productivity', 'business']
  );

  const { stats: checkinStats, loading: statsLoading, refreshStats } = useCheckinStats();

  useEffect(() => {
    const loadInitialData = async () => {
      try {
        setLoadingProfile(true);
        const profile = await StorageService.getUserProfile();
        setUserProfile(profile);

        const todayStats = await StatsService.generateTodayStats(profile?.module_levels || {});
        setStats(todayStats);
      } catch (error) {
        console.error('Failed to load home screen data:', error);
      } finally {
        setLoadingProfile(false);
      }
    };

    loadInitialData();
  }, []);

  const handleRefresh = async () => {
    try {
      setRefreshing(true);
      await Promise.all([refreshWisdom(), refreshStats()]);

      const profile = await StorageService.getUserProfile();
      if (profile) {
        const todayStats = await StatsService.generateTodayStats(profile.module_levels);
        setStats(todayStats);
      }
    } catch (error) {
      console.error('Failed to refresh:', error);
    } finally {
      setRefreshing(false);
    }
  };

  if (loadingProfile) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={COLORS.info} />
      </View>
    );
  }

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView
        style={styles.container}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={handleRefresh} />}
        showsVerticalScrollIndicator={false}
      >
        {/* Welcome Section */}
        {userProfile && (
          <View style={styles.welcomeSection}>
            <Text style={styles.welcomeText}>Welcome back, {userProfile.name}!</Text>
            <Text style={styles.dateText}>{new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' })}</Text>
          </View>
        )}

        {/* Quick Stats */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Your Progress</Text>
          <StatsBar
            stats={[
              {
                label: 'Day Streak',
                value: checkinStats.dayStreak,
                icon: '🔥',
                color: COLORS.warning,
              },
              {
                label: 'Avg Score',
                value: `${checkinStats.avgScore}/10`,
                icon: '⭐',
                color: COLORS.info,
              },
              {
                label: 'Deep Work',
                value: `${checkinStats.deepWorkHours}h`,
                icon: '⚡',
                color: MODULE_COLORS.productivity,
              },
            ]}
            variant="horizontal"
          />
        </View>

        {/* Daily Wisdom */}
        {wisdomLoading ? (
          <View style={styles.wisdomLoadingContainer}>
            <ActivityIndicator size="small" color={COLORS.info} />
            <Text style={styles.loadingText}>Loading daily wisdom...</Text>
          </View>
        ) : dailyWisdom ? (
          <View style={styles.section}>
            <View style={styles.wisdomHeader}>
              <Text style={styles.sectionTitle}>Today's Coaching</Text>
              <TouchableOpacity onPress={refreshWisdom}>
                <Text style={styles.refreshIcon}>🔄</Text>
              </TouchableOpacity>
            </View>
            <WisdomCard
              wisdom={dailyWisdom}
              loading={wisdomLoading}
              onRefresh={refreshWisdom}
            />
          </View>
        ) : null}

        {/* Today's Goals Section */}
        {userProfile?.goals_90_day && Object.keys(userProfile.goals_90_day).length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>90-Day Goals</Text>
            {Object.entries(userProfile.goals_90_day).slice(0, 3).map(([module, goal]) => (
              <View key={module} style={styles.goalCard}>
                <Text style={styles.goalModule}>{module.toUpperCase()}</Text>
                <Text style={styles.goalText}>{goal.goal}</Text>
                <View style={styles.goalProgress}>
                  <View
                    style={[
                      styles.progressBar,
                      { width: `${(goal.target_level / 10) * 100}%` },
                    ]}
                  />
                </View>
              </View>
            ))}
          </View>
        )}

        {/* Recent Wins */}
        {checkinStats.recentWins.length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Recent Wins 🏆</Text>
            {checkinStats.recentWins.map((win, index) => (
              <View key={index} style={styles.winCard}>
                <Text style={styles.winText}>{win}</Text>
              </View>
            ))}
          </View>
        )}

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
  welcomeSection: {
    marginBottom: SPACING.xl,
  },
  welcomeText: {
    ...TYPOGRAPHY.h2,
    color: COLORS.text,
    marginBottom: SPACING.sm,
  },
  dateText: {
    ...TYPOGRAPHY.subtitle,
    color: COLORS.textSecondary,
  },
  section: {
    marginBottom: SPACING.xl,
  },
  sectionTitle: {
    ...TYPOGRAPHY.h3,
    color: COLORS.text,
    marginBottom: SPACING.md,
  },
  wisdomHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.md,
  },
  refreshIcon: {
    fontSize: 20,
  },
  wisdomLoadingContainer: {
    backgroundColor: COLORS.surface,
    borderRadius: BORDER_RADIUS.lg,
    paddingVertical: SPACING.xl,
    alignItems: 'center',
    ...SHADOWS.sm,
    marginBottom: SPACING.xl,
  },
  loadingText: {
    ...TYPOGRAPHY.body,
    color: COLORS.textSecondary,
    marginTop: SPACING.md,
  },
  goalCard: {
    backgroundColor: COLORS.surface,
    borderRadius: BORDER_RADIUS.lg,
    paddingHorizontal: SPACING.lg,
    paddingVertical: SPACING.md,
    marginBottom: SPACING.md,
    ...SHADOWS.sm,
  },
  goalModule: {
    ...TYPOGRAPHY.caption,
    color: COLORS.info,
    marginBottom: SPACING.xs,
  },
  goalText: {
    ...TYPOGRAPHY.body,
    color: COLORS.text,
    marginBottom: SPACING.md,
  },
  goalProgress: {
    height: 6,
    backgroundColor: COLORS.surfaceLight,
    borderRadius: BORDER_RADIUS.full,
    overflow: 'hidden',
  },
  progressBar: {
    height: '100%',
    backgroundColor: COLORS.info,
  },
  winCard: {
    backgroundColor: COLORS.surface,
    borderRadius: BORDER_RADIUS.lg,
    paddingHorizontal: SPACING.lg,
    paddingVertical: SPACING.md,
    marginBottom: SPACING.md,
    borderLeftWidth: 4,
    borderLeftColor: COLORS.success,
    ...SHADOWS.sm,
  },
  winText: {
    ...TYPOGRAPHY.body,
    color: COLORS.text,
  },
});
