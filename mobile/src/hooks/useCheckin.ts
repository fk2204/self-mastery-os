import { useEffect, useState, useCallback } from 'react';
import { DailyCheckin } from '@/types';
import CheckinService from '@/services/CheckinService';

export const useTodayCheckin = () => {
  const [checkin, setCheckin] = useState<DailyCheckin | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadCheckin = async () => {
      try {
        setLoading(true);
        const data = await CheckinService.getTodayCheckin();
        setCheckin(data);
        setError(null);
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Failed to load checkin';
        setError(message);
      } finally {
        setLoading(false);
      }
    };

    loadCheckin();
  }, []);

  const refreshCheckin = useCallback(async () => {
    try {
      setLoading(true);
      const data = await CheckinService.getTodayCheckin();
      setCheckin(data);
      setError(null);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to refresh checkin';
      setError(message);
    } finally {
      setLoading(false);
    }
  }, []);

  return { checkin, loading, error, refreshCheckin };
};

export const useMorningCheckin = () => {
  const [isComplete, setIsComplete] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkCompletion = async () => {
      try {
        setLoading(true);
        const complete = await CheckinService.isMorningCheckinComplete();
        setIsComplete(complete);
      } catch (err) {
        console.error('Failed to check morning checkin completion', err);
      } finally {
        setLoading(false);
      }
    };

    checkCompletion();
  }, []);

  const saveMorningCheckin = useCallback(
    async (
      sleepQuality: number,
      energyLevel: number,
      top3Priorities: string[],
      winDefinition: string
    ) => {
      try {
        await CheckinService.saveMorningCheckin(sleepQuality, energyLevel, top3Priorities, winDefinition);
        setIsComplete(true);
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Failed to save morning checkin';
        throw new Error(message);
      }
    },
    []
  );

  return { isComplete, loading, saveMorningCheckin };
};

export const useEveningCheckin = () => {
  const [isComplete, setIsComplete] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkCompletion = async () => {
      try {
        setLoading(true);
        const complete = await CheckinService.isEveningCheckinComplete();
        setIsComplete(complete);
      } catch (err) {
        console.error('Failed to check evening checkin completion', err);
      } finally {
        setLoading(false);
      }
    };

    checkCompletion();
  }, []);

  const saveEveningCheckin = useCallback(
    async (
      wins: string[],
      challengesLessons: string[],
      deepWorkHours: number,
      habitsCompleted: string[],
      dayScore: number
    ) => {
      try {
        await CheckinService.saveEveningCheckin(wins, challengesLessons, deepWorkHours, habitsCompleted, dayScore);
        setIsComplete(true);
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Failed to save evening checkin';
        throw new Error(message);
      }
    },
    []
  );

  return { isComplete, loading, saveEveningCheckin };
};

export const useCheckinStats = () => {
  const [stats, setStats] = useState({
    dayStreak: 0,
    avgScore: 0,
    deepWorkHours: 0,
    recentWins: [] as string[],
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadStats = async () => {
      try {
        setLoading(true);
        const [dayStreak, avgScore, deepWorkHours, recentWins] = await Promise.all([
          CheckinService.getCheckinStreak(),
          CheckinService.getAverageDayScore(7),
          CheckinService.getTotalDeepWorkHours(7),
          CheckinService.getRecentWins(7),
        ]);

        setStats({
          dayStreak,
          avgScore,
          deepWorkHours,
          recentWins,
        });
        setError(null);
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Failed to load stats';
        setError(message);
      } finally {
        setLoading(false);
      }
    };

    loadStats();
  }, []);

  const refreshStats = useCallback(async () => {
    try {
      setLoading(true);
      const [dayStreak, avgScore, deepWorkHours, recentWins] = await Promise.all([
        CheckinService.getCheckinStreak(),
        CheckinService.getAverageDayScore(7),
        CheckinService.getTotalDeepWorkHours(7),
        CheckinService.getRecentWins(7),
      ]);

      setStats({
        dayStreak,
        avgScore,
        deepWorkHours,
        recentWins,
      });
      setError(null);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to refresh stats';
      setError(message);
    } finally {
      setLoading(false);
    }
  }, []);

  return { stats, loading, error, refreshStats };
};
