import { useEffect, useState, useCallback } from 'react';
import { Habit, HabitCompletion } from '@/types';
import { HabitService, StorageService } from '@/services';

export const useHabits = () => {
  const [habits, setHabits] = useState<Habit[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadHabits = async () => {
      try {
        setLoading(true);
        const data = await StorageService.getHabits();
        setHabits(data);
        setError(null);
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Failed to load habits';
        setError(message);
      } finally {
        setLoading(false);
      }
    };

    loadHabits();
  }, []);

  const completeHabit = useCallback(async (habitId: string, notes?: string) => {
    try {
      await HabitService.completeHabit(habitId, notes);
      const updated = await StorageService.getHabits();
      setHabits(updated);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to complete habit';
      setError(message);
    }
  }, []);

  const uncompleteHabit = useCallback(async (habitId: string) => {
    try {
      await HabitService.uncompleteHabit(habitId);
      const updated = await StorageService.getHabits();
      setHabits(updated);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to uncomplete habit';
      setError(message);
    }
  }, []);

  const refreshHabits = useCallback(async () => {
    try {
      setLoading(true);
      const data = await StorageService.getHabits();
      setHabits(data);
      setError(null);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to refresh habits';
      setError(message);
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    habits,
    loading,
    error,
    completeHabit,
    uncompleteHabit,
    refreshHabits,
  };
};

export const useHabitStatus = () => {
  const [completedToday, setCompletedToday] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadStatus = async () => {
      try {
        setLoading(true);
        const completed = await HabitService.getTodayCompletions();
        setCompletedToday(completed);
        setError(null);
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Failed to load habit status';
        setError(message);
      } finally {
        setLoading(false);
      }
    };

    loadStatus();
  }, []);

  const isCompleted = useCallback((habitId: string): boolean => {
    return completedToday.includes(habitId);
  }, [completedToday]);

  const refreshStatus = useCallback(async () => {
    try {
      setLoading(true);
      const completed = await HabitService.getTodayCompletions();
      setCompletedToday(completed);
      setError(null);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to refresh status';
      setError(message);
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    completedToday,
    loading,
    error,
    isCompleted,
    refreshStatus,
  };
};

export const useHabitStreaks = () => {
  const [streaks, setStreaks] = useState<Record<string, number>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadStreaks = async () => {
      try {
        setLoading(true);
        const habits = await StorageService.getHabits();
        const streakData: Record<string, number> = {};

        for (const habit of habits) {
          streakData[habit.id] = habit.current_streak;
        }

        setStreaks(streakData);
        setError(null);
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Failed to load streaks';
        setError(message);
      } finally {
        setLoading(false);
      }
    };

    loadStreaks();
  }, []);

  return { streaks, loading, error };
};
