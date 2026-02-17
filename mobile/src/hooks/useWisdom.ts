import { useEffect, useState } from 'react';
import { DailyWisdom, Master } from '@/types';
import WisdomService from '@/services/WisdomService';

export const useWisdom = (module: string, focusModules?: string[]) => {
  const [dailyWisdom, setDailyWisdom] = useState<DailyWisdom | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadWisdom = async () => {
      try {
        setLoading(true);
        const today = new Date().toISOString().split('T')[0];
        const wisdom = await WisdomService.generateDailyWisdom(
          today,
          module,
          focusModules
        );
        setDailyWisdom(wisdom);
        setError(null);
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Failed to load wisdom';
        setError(message);
        setDailyWisdom(null);
      } finally {
        setLoading(false);
      }
    };

    loadWisdom();
  }, [module, focusModules]);

  const refreshWisdom = async () => {
    try {
      setLoading(true);
      const today = new Date().toISOString().split('T')[0];
      const wisdom = await WisdomService.generateDailyWisdom(
        today,
        module,
        focusModules
      );
      setDailyWisdom(wisdom);
      setError(null);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to refresh wisdom';
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return { dailyWisdom, loading, error, refreshWisdom };
};

export const useMaster = (module: string, masterName?: string) => {
  const [master, setMaster] = useState<Master | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadMaster = async () => {
      try {
        setLoading(true);
        let loadedMaster: Master | null;

        if (masterName) {
          loadedMaster = await WisdomService.getMasterByName(module, masterName);
        } else {
          loadedMaster = await WisdomService.getRandomMaster(module);
        }

        setMaster(loadedMaster);
        setError(null);
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Failed to load master';
        setError(message);
        setMaster(null);
      } finally {
        setLoading(false);
      }
    };

    loadMaster();
  }, [module, masterName]);

  return { master, loading, error };
};

export const useSkillChallenges = (module: string, count: number = 3) => {
  const [challenges, setChallenges] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadChallenges = async () => {
      try {
        setLoading(true);
        const data = await WisdomService.getSkillChallenges(module, count);
        setChallenges(data);
        setError(null);
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Failed to load challenges';
        setError(message);
        setChallenges([]);
      } finally {
        setLoading(false);
      }
    };

    loadChallenges();
  }, [module, count]);

  return { challenges, loading, error };
};
