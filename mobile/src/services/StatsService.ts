/**
 * Stats Service - Enhanced Production Version
 * Port from data_manager.py stats methods
 * Calculates aggregated statistics with caching and efficient updates
 * Supports both new and legacy stats formats
 */

import StorageService from './StorageService';
import HabitService from './HabitService';
import CheckinService from './CheckinService';
import { ProgressStats, ModuleLevels, Stats } from '../types';

class StatsService {
  /**
   * Get aggregated statistics for past N days (new web app format)
   * Cached for efficiency
   */
  async getStats(days: number = 30): Promise<Stats> {
    try {
      // Try cache first
      const cached = await StorageService.getCache<Stats>(`stats_${days}`, 300000); // 5 min TTL
      if (cached) {
        return cached;
      }

      // Calculate fresh stats
      const stats = await StorageService.getAggregatedStats(days);

      // Cache the result
      await StorageService.setCache(`stats_${days}`, stats, 300000);

      return stats;
    } catch (error) {
      console.error('StatsService: Failed to get stats', error);
      return this.getDefaultStats();
    }
  }

  /**
   * Get stats for multiple day ranges
   */
  async getStatsForRanges(ranges: number[] = [7, 30, 90]): Promise<Record<number, Stats>> {
    try {
      const result: Record<number, Stats> = {};

      for (const days of ranges) {
        result[days] = await this.getStats(days);
      }

      return result;
    } catch (error) {
      console.error('StatsService: Failed to get stats for ranges', error);
      return {};
    }
  }

  /**
   * Invalidate stats cache
   */
  async invalidateStatsCache(days: number = 30): Promise<void> {
    try {
      await StorageService.invalidateCache(`stats_${days}`);
    } catch (error) {
      console.error('StatsService: Failed to invalidate stats cache', error);
    }
  }

  /**
   * Invalidate all stats caches
   */
  async invalidateAllStatsCache(): Promise<void> {
    try {
      for (const days of [7, 14, 30, 90]) {
        await this.invalidateStatsCache(days);
      }
    } catch (error) {
      console.error('StatsService: Failed to invalidate all stats caches', error);
    }
  }

  /**
   * Generate and save today's stats (legacy format)
   */
  async generateTodayStats(moduleLevels: ModuleLevels): Promise<ProgressStats> {
    try {
      const today = format(new Date(), 'yyyy-MM-dd');
      const existingStats = await this.getStatsForDate(today);

      if (existingStats) {
        return existingStats;
      }

      const dayStreak = await CheckinService.getCheckinStreak();
      const deepWorkHours = await CheckinService.getTotalDeepWorkHours(1);
      const habitCompletion = await HabitService.getCompletionPercentage(1);
      const avgScore = await CheckinService.getAverageDayScore(1);

      const habits = await StorageService.getHabits();
      const habitStreaks: Record<string, number> = {};
      for (const habit of habits) {
        habitStreaks[habit.id] = habit.current_streak;
      }

      const stats: ProgressStats = {
        date: today,
        day_streak: dayStreak,
        deep_work_hours: deepWorkHours,
        habit_completion_percentage: habitCompletion,
        average_day_score: avgScore,
        module_scores: { ...moduleLevels },
        habit_streaks: habitStreaks,
      };

      const allStats = await StorageService.getStats();
      allStats.push(stats);
      await StorageService.saveStats(allStats);

      return stats;
    } catch (error) {
      console.error('StatsService: Failed to generate today stats', error);
      throw error;
    }
  }

  /**
   * Get stats for specific date
   */
  async getStatsForDate(date: string): Promise<ProgressStats | null> {
    try {
      const allStats = await StorageService.getStats();
      return allStats.find(s => s.date === date) || null;
    } catch (error) {
      console.error('StatsService: Failed to get stats for date', error);
      return null;
    }
  }

  /**
   * Get stats for last N days
   */
  async getStatsForRange(days: number = 7): Promise<ProgressStats[]> {
    try {
      const allStats = await StorageService.getStats();
      return allStats.slice(-days);
    } catch (error) {
      console.error('StatsService: Failed to get stats for range', error);
      return [];
    }
  }

  /**
   * Calculate average metrics over time period
   */
  async getAverageMetrics(days: number = 7): Promise<{
    avgHabitCompletion: number;
    avgDayScore: number;
    avgDeepWork: number;
    totalDeepWork: number;
  }> {
    try {
      const stats = await this.getStatsForRange(days);

      if (stats.length === 0) {
        return {
          avgHabitCompletion: 0,
          avgDayScore: 0,
          avgDeepWork: 0,
          totalDeepWork: 0,
        };
      }

      const avgHabitCompletion = Math.round(
        stats.reduce((sum, s) => sum + s.habit_completion_percentage, 0) / stats.length
      );

      const avgDayScore = Math.round(
        (stats.reduce((sum, s) => sum + s.average_day_score, 0) / stats.length) * 10
      ) / 10;

      const avgDeepWork = Math.round(
        (stats.reduce((sum, s) => sum + s.deep_work_hours, 0) / stats.length) * 10
      ) / 10;

      const totalDeepWork = Math.round(
        stats.reduce((sum, s) => sum + s.deep_work_hours, 0) * 10
      ) / 10;

      return {
        avgHabitCompletion,
        avgDayScore,
        avgDeepWork,
        totalDeepWork,
      };
    } catch (error) {
      console.error('StatsService: Failed to get average metrics', error);
      return {
        avgHabitCompletion: 0,
        avgDayScore: 0,
        avgDeepWork: 0,
        totalDeepWork: 0,
      };
    }
  }

  /**
   * Get progress for a specific module
   */
  async getModuleProgress(module: string, days: number = 30): Promise<number[]> {
    try {
      const stats = await this.getStatsForRange(days);
      return stats.map(s => s.module_scores[module] || 0);
    } catch (error) {
      console.error('StatsService: Failed to get module progress', error);
      return [];
    }
  }

  /**
   * Get habit streak data
   */
  async getHabitStreakData(habitId?: string): Promise<Record<string, number>> {
    try {
      const stats = await StorageService.getStats();
      const latestStats = stats[stats.length - 1];

      if (!latestStats) {
        return {};
      }

      if (habitId) {
        return { [habitId]: latestStats.habit_streaks[habitId] || 0 };
      }

      return latestStats.habit_streaks || {};
    } catch (error) {
      console.error('StatsService: Failed to get habit streak data', error);
      return {};
    }
  }

  /**
   * Calculate week-over-week improvement
   */
  async getWeekOverWeekImprovement(): Promise<{
    habitCompletionChange: number;
    dayScoreChange: number;
    deepWorkChange: number;
  }> {
    try {
      const thisWeekStats = await this.getStatsForRange(7);
      const lastWeekStats = await StorageService.getStats();
      const lastWeekData = lastWeekStats.slice(-14, -7);

      const thisWeekAvg = await this.calculateAverages(thisWeekStats);
      const lastWeekAvg = await this.calculateAverages(lastWeekData);

      return {
        habitCompletionChange: thisWeekAvg.habitCompletion - lastWeekAvg.habitCompletion,
        dayScoreChange: Math.round((thisWeekAvg.dayScore - lastWeekAvg.dayScore) * 10) / 10,
        deepWorkChange: Math.round((thisWeekAvg.deepWork - lastWeekAvg.deepWork) * 10) / 10,
      };
    } catch (error) {
      console.error('StatsService: Failed to get week over week improvement', error);
      return {
        habitCompletionChange: 0,
        dayScoreChange: 0,
        deepWorkChange: 0,
      };
    }
  }

  /**
   * Helper to calculate averages
   */
  private async calculateAverages(stats: ProgressStats[]): Promise<{
    habitCompletion: number;
    dayScore: number;
    deepWork: number;
  }> {
    if (stats.length === 0) {
      return { habitCompletion: 0, dayScore: 0, deepWork: 0 };
    }

    return {
      habitCompletion: Math.round(
        stats.reduce((sum, s) => sum + s.habit_completion_percentage, 0) / stats.length
      ),
      dayScore: Math.round(
        (stats.reduce((sum, s) => sum + s.average_day_score, 0) / stats.length) * 10
      ) / 10,
      deepWork: Math.round(
        (stats.reduce((sum, s) => sum + s.deep_work_hours, 0) / stats.length) * 10
      ) / 10,
    };
  }

  /**
   * Get default empty stats
   */
  private getDefaultStats(): Stats {
    return {
      total_days_logged: 0,
      am_checkins: 0,
      pm_reflections: 0,
      avg_sleep: 0,
      avg_energy: 0,
      avg_day_score: 0,
      total_deep_work_hours: 0,
      total_workouts: 0,
      habit_completion_rate: 0,
    };
  }
}

export default new StatsService();
