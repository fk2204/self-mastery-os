/**
 * Habit Service - Production Version
 * Port from data_manager.py habit methods
 * Incremental streak updates, efficient caching
 * Works with StorageService which uses web app JSON structure
 */

import StorageService from './StorageService';
import { Habit } from '../types';

class HabitService {
  /**
   * Get all habits
   */
  async getHabits(): Promise<Habit[]> {
    try {
      const habitsData = await StorageService.getHabitsData();
      return habitsData.habits || [];
    } catch (error) {
      console.error('HabitService: Failed to get habits', error);
      return [];
    }
  }

  /**
   * Get habit completion status for today
   */
  async getTodayCompletions(): Promise<string[]> {
    try {
      const today = this.getTodayString();
      const habitsData = await StorageService.getHabitsData();
      return habitsData.completions[today] || [];
    } catch (error) {
      console.error('HabitService: Failed to get today completions', error);
      return [];
    }
  }

  /**
   * Check if a specific habit is completed today
   */
  async isHabitCompletedToday(habitId: string): Promise<boolean> {
    try {
      const completions = await this.getTodayCompletions();
      return completions.includes(habitId);
    } catch (error) {
      console.error('HabitService: Failed to check habit completion', error);
      return false;
    }
  }

  /**
   * Complete a habit for today
   */
  async completeHabit(habitId: string, date?: string): Promise<void> {
    try {
      await StorageService.recordHabitCompletion(habitId, date);
      // Invalidate cache
      await StorageService.invalidateCache(`streak_${habitId}`);
    } catch (error) {
      console.error('HabitService: Failed to complete habit', error);
      throw error;
    }
  }

  /**
   * Uncomplete a habit for today
   */
  async uncompleteHabit(habitId: string, date?: string): Promise<void> {
    try {
      const dateStr = date || this.getTodayString();
      const habitsData = await StorageService.getHabitsData();

      if (habitsData.completions[dateStr]) {
        habitsData.completions[dateStr] = habitsData.completions[dateStr].filter(
          (id) => id !== habitId
        );
        await StorageService.saveHabitsData(habitsData);
        await StorageService.invalidateCache(`streak_${habitId}`);
      }
    } catch (error) {
      console.error('HabitService: Failed to uncomplete habit', error);
      throw error;
    }
  }

  /**
   * Get streak for a specific habit
   */
  async getStreak(habitId: string): Promise<number> {
    try {
      // Check cache first
      const cached = await StorageService.getCache<number>(`streak_${habitId}`, 3600000); // 1 hour TTL
      if (cached !== null) {
        return cached;
      }

      const habitsData = await StorageService.getHabitsData();
      const habit = habitsData.habits.find((h) => h.id === habitId);

      if (!habit) return 0;

      const streak = habit.current_streak || 0;
      // Cache the streak
      await StorageService.setCache(`streak_${habitId}`, streak, 3600000);

      return streak;
    } catch (error) {
      console.error('HabitService: Failed to get streak', error);
      return 0;
    }
  }

  /**
   * Get completion rate for habits over N days
   */
  async getCompletionRate(days: number = 7): Promise<number> {
    try {
      return await StorageService.getCompletionRate(days);
    } catch (error) {
      console.error('HabitService: Failed to get completion rate', error);
      return 0;
    }
  }

  /**
   * Get habit completion history
   */
  async getHabitHistory(habitId: string, days: number = 30): Promise<Map<string, boolean>> {
    try {
      const habitsData = await StorageService.getHabitsData();
      const completionDates = new Set<string>();

      Object.entries(habitsData.completions).forEach(([date, habitIds]) => {
        if (habitIds.includes(habitId)) {
          completionDates.add(date);
        }
      });

      const history = new Map<string, boolean>();
      const today = new Date();

      for (let i = 0; i < days; i++) {
        const date = this.formatDate(new Date(today.getTime() - i * 24 * 60 * 60 * 1000));
        history.set(date, completionDates.has(date));
      }

      return history;
    } catch (error) {
      console.error('HabitService: Failed to get habit history', error);
      return new Map();
    }
  }

  /**
   * Get all habits grouped by completion status
   */
  async getHabitsByStatus(): Promise<{ completed: Habit[]; incomplete: Habit[] }> {
    try {
      const habits = await this.getHabits();
      const completedToday = await this.getTodayCompletions();

      return {
        completed: habits.filter((h) => completedToday.includes(h.id)),
        incomplete: habits.filter((h) => !completedToday.includes(h.id)),
      };
    } catch (error) {
      console.error('HabitService: Failed to get habits by status', error);
      return { completed: [], incomplete: [] };
    }
  }

  /**
   * Get habits for a specific module
   */
  async getHabitsByModule(module: string): Promise<Habit[]> {
    try {
      const habits = await this.getHabits();
      return habits.filter((h) => h.module === module);
    } catch (error) {
      console.error('HabitService: Failed to get habits by module', error);
      return [];
    }
  }

  /**
   * Add a new habit
   */
  async addHabit(habit: Habit): Promise<void> {
    try {
      const habitsData = await StorageService.getHabitsData();
      habit.created_at = new Date().toISOString();
      habit.current_streak = 0;
      habit.best_streak = 0;
      habit.total_completions = 0;
      habitsData.habits.push(habit);
      await StorageService.saveHabitsData(habitsData);
    } catch (error) {
      console.error('HabitService: Failed to add habit', error);
      throw error;
    }
  }

  /**
   * Get total completions for a habit
   */
  async getTotalCompletions(habitId: string): Promise<number> {
    try {
      const habit = await this.getHabitById(habitId);
      return habit?.total_completions || 0;
    } catch (error) {
      console.error('HabitService: Failed to get total completions', error);
      return 0;
    }
  }

  /**
   * Get habit by ID
   */
  async getHabitById(habitId: string): Promise<Habit | null> {
    try {
      const habits = await this.getHabits();
      return habits.find((h) => h.id === habitId) || null;
    } catch (error) {
      console.error('HabitService: Failed to get habit by ID', error);
      return null;
    }
  }

  /**
   * Reset all habits for testing
   */
  async resetAllHabits(): Promise<void> {
    try {
      const habitsData = await StorageService.getHabitsData();
      habitsData.habits = habitsData.habits.map((h) => ({
        ...h,
        current_streak: 0,
        best_streak: 0,
        total_completions: 0,
      }));
      habitsData.completions = {};
      await StorageService.saveHabitsData(habitsData);
    } catch (error) {
      console.error('HabitService: Failed to reset habits', error);
      throw error;
    }
  }

  // ==================== Helper Methods ====================

  /**
   * Get today's date as YYYY-MM-DD string
   */
  private getTodayString(): string {
    return this.formatDate(new Date());
  }

  /**
   * Format a date as YYYY-MM-DD
   */
  private formatDate(date: Date): string {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  }
}

export default new HabitService();
