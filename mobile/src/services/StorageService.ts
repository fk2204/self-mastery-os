/**
 * Storage Service - Enhanced Production Version
 * Wrapper around AsyncStorage for offline-first data persistence
 * Uses same JSON structure as web app (data_manager.py)
 * Production-ready TypeScript with proper error handling
 */

import AsyncStorage from '@react-native-async-storage/async-storage';
import {
  StorageData,
  UserProfile,
  Habit,
  DailyCheckin,
  ProgressStats,
  JournalEntry,
  HabitCompletion,
  HabitsData,
  DailyLog,
  Stats,
  TodaysCheckin,
  AMCheckin,
  PMReflection,
} from '../types';

const STORAGE_KEYS = {
  USER_PROFILE: '@smo_user_profile',
  HABITS: '@smo_habits',
  HABIT_COMPLETIONS: '@smo_habit_completions',
  CHECKINS: '@smo_checkins',
  STATS: '@smo_stats',
  JOURNAL_ENTRIES: '@smo_journal_entries',
  DAILY_LOG_PREFIX: '@smo_log_',
  CACHE_PREFIX: '@smo_cache_',
  LAST_SYNC: '@smo_last_sync',
} as const;

class StorageService {
  /**
   * Initialize storage with default data if empty
   */
  async initialize(defaultProfile: UserProfile, defaultHabits: Habit[]): Promise<void> {
    try {
      const existingProfile = await this.getUserProfile();
      if (!existingProfile) {
        await this.setUserProfile(defaultProfile);
      }

      const existingHabits = await this.getHabits();
      if (!existingHabits || existingHabits.length === 0) {
        await this.setHabits(defaultHabits);
      }
    } catch (error) {
      console.error('StorageService: Failed to initialize', error);
      throw error;
    }
  }

  /**
   * User Profile Operations
   */
  async getUserProfile(): Promise<UserProfile | null> {
    try {
      const data = await AsyncStorage.getItem(STORAGE_KEYS.USER_PROFILE);
      return data ? JSON.parse(data) : null;
    } catch (error) {
      console.error('StorageService: Failed to get user profile', error);
      return null;
    }
  }

  async setUserProfile(profile: UserProfile): Promise<void> {
    try {
      const updated = {
        ...profile,
        updated_at: new Date().toISOString(),
      };
      await AsyncStorage.setItem(STORAGE_KEYS.USER_PROFILE, JSON.stringify(updated));
    } catch (error) {
      console.error('StorageService: Failed to set user profile', error);
      throw error;
    }
  }

  /**
   * Habit Operations
   */
  async getHabits(): Promise<Habit[]> {
    try {
      const data = await AsyncStorage.getItem(STORAGE_KEYS.HABITS);
      return data ? JSON.parse(data) : [];
    } catch (error) {
      console.error('StorageService: Failed to get habits', error);
      return [];
    }
  }

  async setHabits(habits: Habit[]): Promise<void> {
    try {
      await AsyncStorage.setItem(STORAGE_KEYS.HABITS, JSON.stringify(habits));
    } catch (error) {
      console.error('StorageService: Failed to set habits', error);
      throw error;
    }
  }

  async updateHabit(habitId: string, updates: Partial<Habit>): Promise<void> {
    try {
      const habits = await this.getHabits();
      const habit = habits.find(h => h.id === habitId);
      if (habit) {
        const updated = { ...habit, ...updates };
        const newHabits = habits.map(h => h.id === habitId ? updated : h);
        await this.setHabits(newHabits);
      }
    } catch (error) {
      console.error('StorageService: Failed to update habit', error);
      throw error;
    }
  }

  /**
   * Habit Completion Operations
   */
  async getHabitCompletions(date?: string): Promise<HabitCompletion[]> {
    try {
      const data = await AsyncStorage.getItem(STORAGE_KEYS.HABIT_COMPLETIONS);
      let completions: HabitCompletion[] = data ? JSON.parse(data) : [];

      if (date) {
        completions = completions.filter(c => c.date === date);
      }

      return completions;
    } catch (error) {
      console.error('StorageService: Failed to get habit completions', error);
      return [];
    }
  }

  async addHabitCompletion(completion: HabitCompletion): Promise<void> {
    try {
      const completions = await this.getHabitCompletions();
      completions.push(completion);
      await AsyncStorage.setItem(STORAGE_KEYS.HABIT_COMPLETIONS, JSON.stringify(completions));
    } catch (error) {
      console.error('StorageService: Failed to add habit completion', error);
      throw error;
    }
  }

  async removeHabitCompletion(habitId: string, date: string): Promise<void> {
    try {
      const completions = await this.getHabitCompletions();
      const filtered = completions.filter(c => !(c.habit_id === habitId && c.date === date));
      await AsyncStorage.setItem(STORAGE_KEYS.HABIT_COMPLETIONS, JSON.stringify(filtered));
    } catch (error) {
      console.error('StorageService: Failed to remove habit completion', error);
      throw error;
    }
  }

  /**
   * Daily Check-in Operations
   */
  async getDailyCheckins(limit?: number): Promise<DailyCheckin[]> {
    try {
      const data = await AsyncStorage.getItem(STORAGE_KEYS.CHECKINS);
      let checkins: DailyCheckin[] = data ? JSON.parse(data) : [];

      if (limit) {
        checkins = checkins.slice(-limit);
      }

      return checkins;
    } catch (error) {
      console.error('StorageService: Failed to get daily checkins', error);
      return [];
    }
  }

  async getCheckinForDate(date: string): Promise<DailyCheckin | null> {
    try {
      const checkins = await this.getDailyCheckins();
      return checkins.find(c => c.date === date) || null;
    } catch (error) {
      console.error('StorageService: Failed to get checkin for date', error);
      return null;
    }
  }

  async saveCheckin(checkin: DailyCheckin): Promise<void> {
    try {
      const checkins = await this.getDailyCheckins();
      const existingIndex = checkins.findIndex(c => c.date === checkin.date);

      if (existingIndex >= 0) {
        checkins[existingIndex] = checkin;
      } else {
        checkins.push(checkin);
      }

      await AsyncStorage.setItem(STORAGE_KEYS.CHECKINS, JSON.stringify(checkins));
    } catch (error) {
      console.error('StorageService: Failed to save checkin', error);
      throw error;
    }
  }

  /**
   * Stats Operations
   */
  async getStats(): Promise<ProgressStats[]> {
    try {
      const data = await AsyncStorage.getItem(STORAGE_KEYS.STATS);
      return data ? JSON.parse(data) : [];
    } catch (error) {
      console.error('StorageService: Failed to get stats', error);
      return [];
    }
  }

  async saveStats(stats: ProgressStats[]): Promise<void> {
    try {
      await AsyncStorage.setItem(STORAGE_KEYS.STATS, JSON.stringify(stats));
    } catch (error) {
      console.error('StorageService: Failed to save stats', error);
      throw error;
    }
  }

  /**
   * Journal Operations
   */
  async getJournalEntries(): Promise<JournalEntry[]> {
    try {
      const data = await AsyncStorage.getItem(STORAGE_KEYS.JOURNAL_ENTRIES);
      return data ? JSON.parse(data) : [];
    } catch (error) {
      console.error('StorageService: Failed to get journal entries', error);
      return [];
    }
  }

  async addJournalEntry(entry: JournalEntry): Promise<void> {
    try {
      const entries = await this.getJournalEntries();
      entries.push(entry);
      await AsyncStorage.setItem(STORAGE_KEYS.JOURNAL_ENTRIES, JSON.stringify(entries));
    } catch (error) {
      console.error('StorageService: Failed to add journal entry', error);
      throw error;
    }
  }

  async deleteJournalEntry(id: string): Promise<void> {
    try {
      const entries = await this.getJournalEntries();
      const filtered = entries.filter(e => e.id !== id);
      await AsyncStorage.setItem(STORAGE_KEYS.JOURNAL_ENTRIES, JSON.stringify(filtered));
    } catch (error) {
      console.error('StorageService: Failed to delete journal entry', error);
      throw error;
    }
  }

  /**
   * Sync Operations
   */
  async getLastSync(): Promise<number> {
    try {
      const data = await AsyncStorage.getItem(STORAGE_KEYS.LAST_SYNC);
      return data ? parseInt(data, 10) : 0;
    } catch (error) {
      console.error('StorageService: Failed to get last sync', error);
      return 0;
    }
  }

  async setLastSync(timestamp: number): Promise<void> {
    try {
      await AsyncStorage.setItem(STORAGE_KEYS.LAST_SYNC, timestamp.toString());
    } catch (error) {
      console.error('StorageService: Failed to set last sync', error);
      throw error;
    }
  }

  // ==================== Daily Logs (web app compatible) ====================

  /**
   * Get daily log for a specific date (YYYY-MM-DD format)
   * @param date - Date string (defaults to today)
   * @returns Daily log or null
   */
  async getDailyLog(date?: string): Promise<DailyLog | null> {
    try {
      const dateStr = date || this.getTodayString();
      const data = await AsyncStorage.getItem(`${STORAGE_KEYS.DAILY_LOG_PREFIX}${dateStr}`);
      return data ? JSON.parse(data) : null;
    } catch (error) {
      console.error(`StorageService: Failed to get daily log for ${date}`, error);
      return null;
    }
  }

  /**
   * Save daily log for a specific date
   * @param log - Daily log to save
   * @param date - Date string (defaults to today)
   */
  async saveDailyLog(log: DailyLog, date?: string): Promise<void> {
    try {
      const dateStr = date || this.getTodayString();
      const updated = {
        ...log,
        date: dateStr,
        updated_at: new Date().toISOString(),
      };
      await AsyncStorage.setItem(
        `${STORAGE_KEYS.DAILY_LOG_PREFIX}${dateStr}`,
        JSON.stringify(updated)
      );
    } catch (error) {
      console.error(`StorageService: Failed to save daily log for ${date}`, error);
      throw error;
    }
  }

  /**
   * Get or create daily log for a date
   * @param date - Date string (defaults to today)
   * @returns Existing or new daily log
   */
  async getOrCreateDailyLog(date?: string): Promise<DailyLog> {
    const dateStr = date || this.getTodayString();
    const existing = await this.getDailyLog(dateStr);

    if (existing) return existing;

    // Create new log template
    return {
      date: dateStr,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      am_checkin: null,
      planned_actions: [],
      completed_actions: [],
      pm_reflection: null,
      metrics: {
        deep_work_hours: 0,
        workouts: 0,
        sales_calls: 0,
        social_interactions: 0,
        steps: 0,
        water_liters: 0,
      },
      habits: {},
      notes: '',
    };
  }

  /**
   * Get logs for a date range
   * @param startDate - Start date (YYYY-MM-DD)
   * @param endDate - End date (YYYY-MM-DD)
   * @returns Array of daily logs
   */
  async getLogsForRange(startDate: string, endDate: string): Promise<DailyLog[]> {
    try {
      const logs: DailyLog[] = [];
      const current = new Date(startDate);
      const end = new Date(endDate);

      while (current <= end) {
        const dateStr = this.formatDate(current);
        const log = await this.getDailyLog(dateStr);
        if (log) {
          logs.push(log);
        }
        current.setDate(current.getDate() + 1);
      }

      return logs;
    } catch (error) {
      console.error('StorageService: Failed to get logs for range', error);
      return [];
    }
  }

  /**
   * Get logs for the past N days
   * @param days - Number of days to retrieve
   * @returns Array of daily logs
   */
  async getRecentLogs(days: number = 7): Promise<DailyLog[]> {
    try {
      const endDate = new Date();
      const startDate = new Date();
      startDate.setDate(startDate.getDate() - (days - 1));

      return this.getLogsForRange(this.formatDate(startDate), this.formatDate(endDate));
    } catch (error) {
      console.error('StorageService: Failed to get recent logs', error);
      return [];
    }
  }

  // ==================== Habits (web app compatible) ====================

  /**
   * Get habits data with completions
   * @returns Habits data
   */
  async getHabitsData(): Promise<HabitsData> {
    try {
      const data = await AsyncStorage.getItem(STORAGE_KEYS.HABITS);
      if (data) {
        const parsed = JSON.parse(data);
        return parsed;
      }
      return { habits: [], completions: {} };
    } catch (error) {
      console.error('StorageService: Failed to get habits data', error);
      return { habits: [], completions: {} };
    }
  }

  /**
   * Save habits data
   * @param habitsData - Habits data to save
   */
  async saveHabitsData(habitsData: HabitsData): Promise<void> {
    try {
      await AsyncStorage.setItem(STORAGE_KEYS.HABITS, JSON.stringify(habitsData));
    } catch (error) {
      console.error('StorageService: Failed to save habits data', error);
      throw error;
    }
  }

  /**
   * Record habit completion for a date (incremental update)
   * @param habitId - Habit ID
   * @param date - Date string (defaults to today)
   */
  async recordHabitCompletion(habitId: string, date?: string): Promise<void> {
    try {
      const dateStr = date || this.getTodayString();
      const habitsData = await this.getHabitsData();

      // Initialize completions dict if needed
      if (!habitsData.completions) {
        habitsData.completions = {};
      }
      if (!habitsData.completions[dateStr]) {
        habitsData.completions[dateStr] = [];
      }

      // Add completion if not already recorded
      if (!habitsData.completions[dateStr].includes(habitId)) {
        habitsData.completions[dateStr].push(habitId);

        // Update streak incrementally
        const habitIndex = habitsData.habits.findIndex((h) => h.id === habitId);
        if (habitIndex >= 0) {
          const habit = habitsData.habits[habitIndex];
          habit.total_completions = (habit.total_completions || 0) + 1;

          // Recalculate streak
          const completionDates = Object.keys(habitsData.completions).filter((d) =>
            habitsData.completions[d].includes(habitId)
          );
          const newStreak = this.calculateStreak(completionDates);
          habit.current_streak = newStreak;
          habit.best_streak = Math.max(habit.best_streak || 0, newStreak);
        }
      }

      await this.saveHabitsData(habitsData);
    } catch (error) {
      console.error('StorageService: Failed to record habit completion', error);
      throw error;
    }
  }

  // ==================== Statistics (web app compatible) ====================

  /**
   * Get aggregated statistics for past N days
   * @param days - Number of days (default 30)
   * @returns Statistics object
   */
  async getAggregatedStats(days: number = 30): Promise<Stats> {
    try {
      const logs = await this.getRecentLogs(days);
      const habitsData = await this.getHabitsData();

      const stats: Stats = {
        total_days_logged: logs.length,
        am_checkins: 0,
        pm_reflections: 0,
        avg_sleep: 0,
        avg_energy: 0,
        avg_day_score: 0,
        total_deep_work_hours: 0,
        total_workouts: 0,
        habit_completion_rate: 0,
      };

      // Calculate averages
      const sleepValues: number[] = [];
      const energyValues: number[] = [];
      const scoreValues: number[] = [];

      logs.forEach((log) => {
        if (log.am_checkin) {
          stats.am_checkins++;
          if (log.am_checkin.sleep_hours) {
            sleepValues.push(log.am_checkin.sleep_hours);
          }
          if (log.am_checkin.energy_level) {
            energyValues.push(log.am_checkin.energy_level);
          }
        }

        if (log.pm_reflection) {
          stats.pm_reflections++;
          if (log.pm_reflection.day_score) {
            scoreValues.push(log.pm_reflection.day_score);
          }
        }

        if (log.metrics) {
          stats.total_deep_work_hours += log.metrics.deep_work_hours || 0;
          stats.total_workouts += log.metrics.workouts || 0;
        }
      });

      if (sleepValues.length > 0) {
        stats.avg_sleep = sleepValues.reduce((a, b) => a + b) / sleepValues.length;
      }
      if (energyValues.length > 0) {
        stats.avg_energy = energyValues.reduce((a, b) => a + b) / energyValues.length;
      }
      if (scoreValues.length > 0) {
        stats.avg_day_score = scoreValues.reduce((a, b) => a + b) / scoreValues.length;
      }

      // Calculate habit completion rate
      if (habitsData.habits.length > 0 && Object.keys(habitsData.completions).length > 0) {
        const totalCompleted = Object.values(habitsData.completions).reduce(
          (sum, ids) => sum + ids.length,
          0
        );
        const totalPossible = habitsData.habits.length * logs.length;
        if (totalPossible > 0) {
          stats.habit_completion_rate = (totalCompleted / totalPossible) * 100;
        }
      }

      return stats;
    } catch (error) {
      console.error('StorageService: Failed to get aggregated stats', error);
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

  /**
   * Calculate deep work hours for past N days
   * @param days - Number of days
   * @returns Total deep work hours
   */
  async calculateDeepWorkHours(days: number = 7): Promise<number> {
    try {
      const logs = await this.getRecentLogs(days);
      return logs.reduce((total, log) => total + (log.metrics?.deep_work_hours || 0), 0);
    } catch (error) {
      console.error('StorageService: Failed to calculate deep work hours', error);
      return 0;
    }
  }

  /**
   * Get current streak
   * @returns Current streak count
   */
  async getStreak(): Promise<number> {
    try {
      const habitsData = await this.getHabitsData();
      const completionDates = Object.keys(habitsData.completions || {}).sort().reverse();
      return this.calculateStreak(completionDates);
    } catch (error) {
      console.error('StorageService: Failed to get streak', error);
      return 0;
    }
  }

  /**
   * Get today's check-in status
   * @returns Check-in status for today
   */
  async getTodaysCheckin(): Promise<TodaysCheckin> {
    try {
      const today = this.getTodayString();
      const log = await this.getDailyLog(today);

      return {
        date: today,
        hasAMCheckin: !!log?.am_checkin,
        hasPMReflection: !!log?.pm_reflection,
        morningCheckin: log?.am_checkin || undefined,
        eveningReflection: log?.pm_reflection || undefined,
      };
    } catch (error) {
      console.error('StorageService: Failed to get todays checkin', error);
      return {
        date: this.getTodayString(),
        hasAMCheckin: false,
        hasPMReflection: false,
      };
    }
  }

  /**
   * Check if already checked in this morning
   * @returns Boolean
   */
  async checkAlreadyCheckedInMorning(): Promise<boolean> {
    try {
      const today = this.getTodayString();
      const log = await this.getDailyLog(today);
      return !!log?.am_checkin;
    } catch (error) {
      console.error('StorageService: Failed to check morning checkin', error);
      return false;
    }
  }

  /**
   * Check if already completed evening reflection
   * @returns Boolean
   */
  async checkAlreadyReflectedEvening(): Promise<boolean> {
    try {
      const today = this.getTodayString();
      const log = await this.getDailyLog(today);
      return !!log?.pm_reflection;
    } catch (error) {
      console.error('StorageService: Failed to check evening reflection', error);
      return false;
    }
  }

  // ==================== Caching ====================

  /**
   * Get cached value with TTL
   * @param key - Cache key
   * @param ttlMs - Time to live in milliseconds
   * @returns Cached value or null
   */
  async getCache<T>(key: string, ttlMs: number = 300000): Promise<T | null> {
    try {
      const cacheKey = `${STORAGE_KEYS.CACHE_PREFIX}${key}`;
      const data = await AsyncStorage.getItem(cacheKey);

      if (!data) return null;

      const cached = JSON.parse(data) as { value: T; timestamp: number };
      const age = Date.now() - cached.timestamp;

      if (age > ttlMs) {
        await AsyncStorage.removeItem(cacheKey);
        return null;
      }

      return cached.value;
    } catch (error) {
      console.error(`StorageService: Failed to get cache for key ${key}`, error);
      return null;
    }
  }

  /**
   * Set cached value with TTL
   * @param key - Cache key
   * @param value - Value to cache
   * @param ttlMs - Time to live in milliseconds
   */
  async setCache<T>(key: string, value: T, ttlMs: number = 300000): Promise<void> {
    try {
      const cacheKey = `${STORAGE_KEYS.CACHE_PREFIX}${key}`;
      await AsyncStorage.setItem(
        cacheKey,
        JSON.stringify({ value, timestamp: Date.now() })
      );
    } catch (error) {
      console.error(`StorageService: Failed to set cache for key ${key}`, error);
      throw error;
    }
  }

  /**
   * Invalidate cache for a key
   * @param key - Cache key
   */
  async invalidateCache(key: string): Promise<void> {
    try {
      const cacheKey = `${STORAGE_KEYS.CACHE_PREFIX}${key}`;
      await AsyncStorage.removeItem(cacheKey);
    } catch (error) {
      console.error(`StorageService: Failed to invalidate cache for key ${key}`, error);
      throw error;
    }
  }

  // ==================== Helper Methods ====================

  /**
   * Get today's date as YYYY-MM-DD string
   * @returns Date string
   */
  private getTodayString(): string {
    return this.formatDate(new Date());
  }

  /**
   * Format a date as YYYY-MM-DD
   * @param date - Date to format
   * @returns Formatted date string
   */
  private formatDate(date: Date): string {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  }

  /**
   * Calculate streak from list of date strings
   * @param dates - Array of date strings (YYYY-MM-DD)
   * @returns Current streak count
   */
  private calculateStreak(dates: string[]): number {
    if (dates.length === 0) return 0;

    const sortedDates = dates
      .map((d) => new Date(d))
      .sort((a, b) => b.getTime() - a.getTime());

    const today = new Date();
    let streak = 0;
    let expected = new Date(today.getFullYear(), today.getMonth(), today.getDate());

    for (const date of sortedDates) {
      const dateOnly = new Date(date.getFullYear(), date.getMonth(), date.getDate());

      if (dateOnly.getTime() === expected.getTime()) {
        streak++;
        expected.setDate(expected.getDate() - 1);
      } else if (
        dateOnly.getTime() ===
        new Date(expected.getFullYear(), expected.getMonth(), expected.getDate() - 1).getTime()
      ) {
        expected.setDate(expected.getDate() - 1);
        streak++;
        expected.setDate(expected.getDate() - 1);
      } else {
        break;
      }
    }

    return streak;
  }

  /**
   * Clear all data (for testing/reset)
   */
  async clearAll(): Promise<void> {
    try {
      await AsyncStorage.multiRemove(Object.values(STORAGE_KEYS));
    } catch (error) {
      console.error('StorageService: Failed to clear all', error);
      throw error;
    }
  }

  /**
   * Export all data
   */
  async exportAllData(): Promise<StorageData> {
    try {
      return {
        userProfile: (await this.getUserProfile()) || ({} as UserProfile),
        habits: await this.getHabits(),
        habitCompletions: await this.getHabitCompletions(),
        checkins: await this.getDailyCheckins(),
        stats: await this.getStats(),
        journalEntries: await this.getJournalEntries(),
      };
    } catch (error) {
      console.error('StorageService: Failed to export data', error);
      throw error;
    }
  }
}

export default new StorageService();
