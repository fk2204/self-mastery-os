/**
 * Checkin Service - Production Version
 * Port from daily_checkin.py
 * Handles morning check-ins and evening reflections
 * Validates and sanitizes inputs
 */

import StorageService from './StorageService';
import { AMCheckin, PMReflection, TodaysCheckin, DailyLog } from '../types';

class CheckinService {
  /**
   * Get today's checkin status
   */
  async getTodaysCheckin(): Promise<TodaysCheckin> {
    try {
      return await StorageService.getTodaysCheckin();
    } catch (error) {
      console.error('CheckinService: Failed to get todays checkin', error);
      return {
        date: this.getTodayString(),
        hasAMCheckin: false,
        hasPMReflection: false,
      };
    }
  }

  /**
   * Save morning check-in
   * @param sleepHours - Hours of sleep
   * @param sleepQuality - Sleep quality rating (1-10)
   * @param energyLevel - Energy level rating (1-10)
   * @param priorities - Top 3 priorities for the day
   * @param winDefinition - What would make today a win
   */
  async saveMorningCheckin(data: {
    sleep_hours: number;
    sleep_quality: number;
    energy_level: number;
    top_3_priorities: string[];
    win_definition: string;
  }): Promise<void> {
    try {
      // Validate inputs
      this.validateMorningInput(data);

      const today = this.getTodayString();
      const log = await StorageService.getOrCreateDailyLog(today);

      const amCheckin: AMCheckin = {
        time: new Date().toISOString(),
        sleep_hours: Math.max(0, Math.min(24, data.sleep_hours)),
        sleep_quality: Math.max(1, Math.min(10, data.sleep_quality)),
        energy_level: Math.max(1, Math.min(10, data.energy_level)),
        top_3_priorities: data.top_3_priorities.slice(0, 3).map((p) => p.trim()),
        win_definition: data.win_definition.trim(),
      };

      log.am_checkin = amCheckin;
      await StorageService.saveDailyLog(log, today);
    } catch (error) {
      console.error('CheckinService: Failed to save morning checkin', error);
      throw error;
    }
  }

  /**
   * Save evening reflection
   * @param wins - Wins/highlights from the day
   * @param challenges - Challenges/obstacles faced
   * @param lessons - Lessons learned
   * @param improvementForTomorrow - One thing to do differently tomorrow
   * @param deepWorkHours - Hours of deep work
   * @param dayScore - Overall day rating (1-10)
   */
  async saveEveningReflection(data: {
    wins: string[];
    challenges: string[];
    lessons: string[];
    improvement_for_tomorrow: string;
    deep_work_hours: number;
    day_score: number;
  }): Promise<void> {
    try {
      // Validate inputs
      this.validateEveningInput(data);

      const today = this.getTodayString();
      const log = await StorageService.getOrCreateDailyLog(today);

      const pmReflection: PMReflection = {
        time: new Date().toISOString(),
        wins: data.wins.slice(0, 10).map((w) => w.trim()),
        challenges: data.challenges.slice(0, 10).map((c) => c.trim()),
        lessons: data.lessons.slice(0, 10).map((l) => l.trim()),
        improvement_for_tomorrow: data.improvement_for_tomorrow.trim(),
        day_score: Math.max(1, Math.min(10, data.day_score)),
        main_win_achieved: this.checkMainWinAchieved(log, data.wins),
      };

      // Update metrics
      log.metrics.deep_work_hours = Math.max(0, Math.min(24, data.deep_work_hours));

      log.pm_reflection = pmReflection;
      await StorageService.saveDailyLog(log, today);
    } catch (error) {
      console.error('CheckinService: Failed to save evening reflection', error);
      throw error;
    }
  }

  /**
   * Check if already checked in this morning
   */
  async checkAlreadyCheckedInMorning(): Promise<boolean> {
    try {
      return await StorageService.checkAlreadyCheckedInMorning();
    } catch (error) {
      console.error('CheckinService: Failed to check morning checkin', error);
      return false;
    }
  }

  /**
   * Check if already completed evening reflection
   */
  async checkAlreadyReflectedEvening(): Promise<boolean> {
    try {
      return await StorageService.checkAlreadyReflectedEvening();
    } catch (error) {
      console.error('CheckinService: Failed to check evening reflection', error);
      return false;
    }
  }

  /**
   * Get average day score for last N days
   */
  async getAverageDayScore(days: number = 7): Promise<number> {
    try {
      const logs = await StorageService.getRecentLogs(days);
      const scores = logs
        .filter((l) => l.pm_reflection?.day_score)
        .map((l) => l.pm_reflection!.day_score);

      if (scores.length === 0) return 0;
      return Math.round((scores.reduce((a, b) => a + b, 0) / scores.length) * 10) / 10;
    } catch (error) {
      console.error('CheckinService: Failed to get average day score', error);
      return 0;
    }
  }

  /**
   * Get total deep work hours for last N days
   */
  async getTotalDeepWorkHours(days: number = 7): Promise<number> {
    try {
      return await StorageService.calculateDeepWorkHours(days);
    } catch (error) {
      console.error('CheckinService: Failed to get total deep work hours', error);
      return 0;
    }
  }

  /**
   * Get recent wins
   */
  async getRecentWins(days: number = 7): Promise<string[]> {
    try {
      const logs = await StorageService.getRecentLogs(days);
      const wins: string[] = [];

      logs.forEach((log) => {
        if (log.pm_reflection?.wins) {
          wins.push(...log.pm_reflection.wins);
        }
      });

      return wins;
    } catch (error) {
      console.error('CheckinService: Failed to get recent wins', error);
      return [];
    }
  }

  /**
   * Get recent challenges/lessons
   */
  async getRecentChallenges(days: number = 7): Promise<string[]> {
    try {
      const logs = await StorageService.getRecentLogs(days);
      const challenges: string[] = [];

      logs.forEach((log) => {
        if (log.pm_reflection?.challenges) {
          challenges.push(...log.pm_reflection.challenges);
        }
      });

      return challenges;
    } catch (error) {
      console.error('CheckinService: Failed to get recent challenges', error);
      return [];
    }
  }

  // ==================== Helper Methods ====================

  /**
   * Validate morning check-in input
   */
  private validateMorningInput(data: any): void {
    if (data.sleep_hours < 0 || data.sleep_hours > 24) {
      throw new Error('Invalid sleep hours');
    }
    if (data.sleep_quality < 1 || data.sleep_quality > 10) {
      throw new Error('Invalid sleep quality');
    }
    if (data.energy_level < 1 || data.energy_level > 10) {
      throw new Error('Invalid energy level');
    }
    if (!Array.isArray(data.top_3_priorities) || data.top_3_priorities.length === 0) {
      throw new Error('Must provide at least one priority');
    }
    if (!data.win_definition || data.win_definition.trim().length === 0) {
      throw new Error('Win definition cannot be empty');
    }
  }

  /**
   * Validate evening reflection input
   */
  private validateEveningInput(data: any): void {
    if (!Array.isArray(data.wins) || data.wins.length === 0) {
      throw new Error('Must provide at least one win');
    }
    if (data.day_score < 1 || data.day_score > 10) {
      throw new Error('Invalid day score');
    }
    if (data.deep_work_hours < 0 || data.deep_work_hours > 24) {
      throw new Error('Invalid deep work hours');
    }
  }

  /**
   * Check if main win was achieved
   */
  private checkMainWinAchieved(log: DailyLog, wins: string[]): boolean {
    if (!log.am_checkin?.win_definition) return false;

    const mainWin = log.am_checkin.win_definition.toLowerCase();
    return wins.some((w) => w.toLowerCase().includes(mainWin) || mainWin.includes(w.toLowerCase()));
  }

  /**
   * Get today's date as YYYY-MM-DD string
   */
  private getTodayString(): string {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  }
}

export default new CheckinService();
