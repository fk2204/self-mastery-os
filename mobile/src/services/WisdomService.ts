/**
 * Wisdom Service - Production Version
 * Delivers daily wisdom from masters
 * Port from wisdom_engine.py with date-seeded RNG for deterministic wisdom
 * Lazy-loads master data by module to minimize memory footprint
 */

import {
  DailyWisdom,
  MastersModule,
  Master,
  WorkedExample,
  MasterTeaching,
  SkillChallenge,
  MindsetShift,
} from '../types';
import StorageService from './StorageService';

interface SeededRandom {
  next(): number;
}

class WisdomService {
  private mastersCache: Map<string, MastersModule> = new Map();
  private loadedModules: Set<string> = new Set();
  private powerQuestions: string[] = [
    'What would the best version of me do right now?',
    'What am I avoiding that I know I should do?',
    'If I only accomplished one thing today, what should it be?',
    'What would I do if I knew I couldn\'t fail?',
    'Am I being productive or just busy?',
    'What\'s the ONE thing that would make everything else easier?',
    'Who do I need to become to achieve my goals?',
    'What belief is limiting me right now?',
    'If today repeated for a year, where would I end up?',
    'What would make today a 10/10?',
    'What\'s the hard thing I\'m pretending isn\'t my responsibility?',
    'Am I playing to win or playing not to lose?',
    'What\'s the conversation I\'m avoiding?',
    'How can I provide 10x more value today?',
    'What skill, if mastered, would change everything?',
    'Is this the best use of my next hour?',
    'What would I tell my best friend to do in my situation?',
    'What am I tolerating that I shouldn\'t?',
    'If I had 6 months to live, would I be doing this?',
    'What\'s the smallest step I can take right now?',
  ];

  private mindsetShifts: MindsetShift[] = [
    { from: 'I don\'t have time', to: 'It\'s not a priority', why: 'Own your choices. If it mattered, you\'d find time.' },
    { from: 'I can\'t do this', to: 'I can\'t do this YET', why: 'Growth mindset. Skills are built, not born.' },
    { from: 'I failed', to: 'I learned what doesn\'t work', why: 'Failure is data. Collect it and adjust.' },
    { from: 'I\'m not ready', to: 'I\'ll figure it out as I go', why: 'Readiness is a myth. Action creates clarity.' },
    { from: 'What if it goes wrong?', to: 'What if it goes right?', why: 'You\'re imagining the future anyway. Imagine the upside.' },
    { from: 'I\'m too tired', to: 'I\'ll do it for just 5 minutes', why: 'Energy follows action. Start small.' },
    { from: 'That\'s not fair', to: 'What can I control?', why: 'Fairness is irrelevant. Adaptation is everything.' },
    { from: 'I need motivation', to: 'I need discipline', why: 'Motivation is fleeting. Discipline is reliable.' },
    { from: 'I\'m overwhelmed', to: 'What\'s the ONE next step?', why: 'You can only do one thing at a time. Pick it.' },
    { from: 'They\'re better than me', to: 'What can I learn from them?', why: 'Comparison kills. Learn and apply.' },
    { from: 'It\'s too hard', to: 'It\'s supposed to be hard', why: 'Hard is what makes it valuable.' },
    { from: 'I\'m not talented enough', to: 'I haven\'t practiced enough', why: 'Talent is overrated. Reps are underrated.' },
  ];

  /**
   * Load masters data for a specific module
   */
  async loadMastersModule(module: string): Promise<MastersModule | null> {
    try {
      // Check cache first
      if (this.mastersCache.has(module)) {
        return this.mastersCache.get(module) || null;
      }

      // Try to require the module file
      const mastersData = require(`@/assets/masters/${module}_masters.json`);
      this.mastersCache.set(module, mastersData);
      this.loadedModules.add(module);
      return mastersData;
    } catch (error) {
      console.error(`WisdomService: Failed to load masters for module ${module}`, error);
      return null;
    }
  }

  /**
   * Ensure all modules are loaded
   */
  async ensureAllModulesLoaded(): Promise<void> {
    const unloaded = MODULE_NAMES.filter(m => !this.loadedModules.has(m));

    for (const module of unloaded) {
      await this.loadMastersModule(module);
    }
  }

  /**
   * Get a random master from a module
   */
  async getRandomMaster(module: string): Promise<Master | null> {
    try {
      const mastersModule = await this.loadMastersModule(module);
      if (!mastersModule || !mastersModule.masters || mastersModule.masters.length === 0) {
        return null;
      }

      const randomIndex = Math.floor(Math.random() * mastersModule.masters.length);
      return mastersModule.masters[randomIndex];
    } catch (error) {
      console.error(`WisdomService: Failed to get random master from ${module}`, error);
      return null;
    }
  }

  /**
   * Get a random master from focus modules
   */
  async getRandomFocusMaster(focusModules: string[]): Promise<{ master: Master | null; module: string }> {
    try {
      const module = focusModules[Math.floor(Math.random() * focusModules.length)];
      const master = await this.getRandomMaster(module);
      return { master, module };
    } catch (error) {
      console.error('WisdomService: Failed to get random focus master', error);
      return { master: null, module: '' };
    }
  }

  /**
   * Get all masters from a module
   */
  async getMasters(module: string): Promise<Master[]> {
    try {
      const mastersModule = await this.loadMastersModule(module);
      return mastersModule?.masters || [];
    } catch (error) {
      console.error(`WisdomService: Failed to get masters for module ${module}`, error);
      return [];
    }
  }

  /**
   * Get a specific master by name
   */
  async getMasterByName(module: string, name: string): Promise<Master | null> {
    try {
      const masters = await this.getMasters(module);
      return masters.find(m => m.name === name) || null;
    } catch (error) {
      console.error(`WisdomService: Failed to get master ${name}`, error);
      return null;
    }
  }

  /**
   * Get daily wisdom for a date and focus modules
   * Uses date-seeded RNG so same wisdom is returned all day
   */
  async getDailyWisdom(
    focusModules: string[] = [],
    date: string = this.getTodayString()
  ): Promise<DailyWisdom | null> {
    try {
      // Get seeded RNG for deterministic wisdom throughout the day
      const rng = this.getSeededRandom(date);

      // Get master teaching
      const masterTeaching = await this.getMasterTeaching(focusModules, rng);
      if (!masterTeaching) {
        return null;
      }

      // Get other wisdom components
      const dailyInsight = await this.getDailyInsightForDate(focusModules, rng);
      const skillChallenge = await this.getSkillChallengeForDate(focusModules, rng);
      const powerQuestion = this.getPowerQuestionForDate(rng);
      const mindsetShift = this.getMindsetShiftForDate(rng);

      return {
        date,
        master_teaching: masterTeaching,
        daily_insight: dailyInsight,
        skill_challenge: skillChallenge,
        power_question: powerQuestion,
        mindset_shift: mindsetShift,
      };
    } catch (error) {
      console.error('WisdomService: Failed to get daily wisdom', error);
      return null;
    }
  }

  /**
   * Get master teaching for the day
   */
  private async getMasterTeaching(
    focusModules: string[] = [],
    rng: SeededRandom
  ): Promise<MasterTeaching | null> {
    try {
      // Find available modules
      const availableModules: string[] = [];

      for (const module of focusModules) {
        const moduleData = await this.loadMastersModule(module);
        if (moduleData) {
          availableModules.push(module);
        }
      }

      if (availableModules.length === 0) {
        return null;
      }

      const module = availableModules[Math.floor(rng.next() * availableModules.length)];
      const moduleData = await this.loadMastersModule(module);

      if (!moduleData || !moduleData.masters || moduleData.masters.length === 0) {
        return null;
      }

      const master = moduleData.masters[Math.floor(rng.next() * moduleData.masters.length)];
      const principles = master.key_principles || [];
      const practices = master.daily_practices || ['Apply this today.'];

      return {
        master: master.name,
        expertise: master.expertise,
        teaching: principles.length > 0 ? principles[Math.floor(rng.next() * principles.length)] : 'No teaching available.',
        practice: practices[Math.floor(rng.next() * practices.length)],
        module,
      };
    } catch (error) {
      console.error('WisdomService: Failed to get master teaching', error);
      return null;
    }
  }

  /**
   * Get daily insight for the day
   */
  private async getDailyInsightForDate(focusModules: string[] = [], rng: SeededRandom): Promise<string> {
    try {
      let allInsights: string[] = [];

      for (const module of focusModules) {
        const moduleData = await this.loadMastersModule(module);
        if (moduleData && moduleData.daily_insights) {
          allInsights = allInsights.concat(moduleData.daily_insights);
        }
      }

      if (allInsights.length > 0) {
        return allInsights[Math.floor(rng.next() * allInsights.length)];
      }

      return 'Show up. Do the work. Repeat.';
    } catch (error) {
      console.error('WisdomService: Failed to get daily insight', error);
      return 'Show up. Do the work. Repeat.';
    }
  }

  /**
   * Get skill challenge for the day
   */
  private async getSkillChallengeForDate(focusModules: string[] = [], rng: SeededRandom): Promise<SkillChallenge> {
    try {
      if (focusModules.length === 0) {
        return {
          module: 'productivity',
          module_name: 'Productivity & Systems',
          challenge: 'Complete your #1 priority before noon.',
        };
      }

      const module = focusModules[Math.floor(rng.next() * focusModules.length)];
      const moduleData = await this.loadMastersModule(module);

      if (moduleData && moduleData.skill_challenges && moduleData.skill_challenges.length > 0) {
        const challenge = moduleData.skill_challenges[Math.floor(rng.next() * moduleData.skill_challenges.length)];
        return {
          module,
          module_name: this.getModuleName(module),
          challenge,
        };
      }

      return {
        module: 'productivity',
        module_name: 'Productivity & Systems',
        challenge: 'Complete your #1 priority before noon.',
      };
    } catch (error) {
      console.error('WisdomService: Failed to get skill challenge', error);
      return {
        module: 'productivity',
        module_name: 'Productivity & Systems',
        challenge: 'Complete your #1 priority before noon.',
      };
    }
  }

  /**
   * Generate daily wisdom content (legacy method, use getDailyWisdom instead)
   */
  async generateDailyWisdom(date: string, module: string, focusModules: string[] = []): Promise<DailyWisdom | null> {
    return this.getDailyWisdom(focusModules.length > 0 ? focusModules : [module], date);
  }

  /**
   * Get daily insights for a module
   */
  async getDailyInsights(module: string, count: number = 5): Promise<string[]> {
    try {
      const mastersModule = await this.loadMastersModule(module);
      if (!mastersModule) {
        return [];
      }

      const insights = mastersModule.daily_insights || [];
      const shuffled = this.shuffleArray([...insights]);
      return shuffled.slice(0, Math.min(count, shuffled.length));
    } catch (error) {
      console.error(`WisdomService: Failed to get daily insights for ${module}`, error);
      return [];
    }
  }

  /**
   * Get skill challenges for a module
   */
  async getSkillChallenges(module: string, count: number = 3): Promise<string[]> {
    try {
      const mastersModule = await this.loadMastersModule(module);
      if (!mastersModule) {
        return [];
      }

      const challenges = mastersModule.skill_challenges || [];
      const shuffled = this.shuffleArray([...challenges]);
      return shuffled.slice(0, Math.min(count, shuffled.length));
    } catch (error) {
      console.error(`WisdomService: Failed to get skill challenges for ${module}`, error);
      return [];
    }
  }

  /**
   * Get all worked examples from a module
   */
  async getWorkedExamples(module: string): Promise<WorkedExample[]> {
    try {
      const masters = await this.getMasters(module);
      const examples: WorkedExample[] = [];

      for (const master of masters) {
        examples.push(...(master.worked_examples || []));
      }

      return examples;
    } catch (error) {
      console.error(`WisdomService: Failed to get worked examples for ${module}`, error);
      return [];
    }
  }

  /**
   * Generate a power question based on master and module
   */
  private generatePowerQuestion(master: Master, module: string): string {
    const questions: Record<string, string[]> = {
      money: [
        'How can I create value that compounds?',
        'What leverage am I not using?',
        'If I had to triple my income in 90 days, what would I do?',
        'What specific knowledge could I monetize?',
      ],
      sales: [
        'What objection am I afraid to hear?',
        'How can I add more value to my prospect today?',
        'What one skill would 10x my closing rate?',
      ],
      finance: [
        'Where is money leaking from my finances?',
        'What investment decision would 10x my wealth?',
        'Am I spending on what matters?',
      ],
      dating: [
        'How can I be more genuine in my connections?',
        'What confidence block is holding me back?',
        'Who do I need to become to attract who I want?',
      ],
      mindset: [
        'What belief is limiting me?',
        'How can I reframe this challenge?',
        'What would the best version of me do?',
      ],
      productivity: [
        'What one thing would change everything?',
        'Where am I wasting focus?',
        'What system would 10x my output?',
      ],
      business: [
        'What problem can I solve at scale?',
        'How can I build something that works without me?',
        'What would the next level look like?',
      ],
      lifestyle: [
        'What habit would compound most?',
        'Where am I overcomplicating things?',
        'What would my ideal day look like?',
      ],
    };

    const moduleQuestions = questions[module] || ['How can I improve today?'];
    return moduleQuestions[Math.floor(Math.random() * moduleQuestions.length)];
  }

  /**
   * Generate a mindset shift based on master
   */
  private generateMindsetShift(master: Master, module: string): string {
    const shifts: Record<string, string[]> = {
      money: [
        'From "How much can I earn?" to "How much value can I create?"',
        'From "Trading time for money" to "Building assets that work for me"',
        'From "Earning more" to "Earning smarter"',
      ],
      sales: [
        'From "Making the sale" to "Solving their problem"',
        'From "Convincing people" to "Connecting with people"',
        'From "What I have to sell" to "What they need to buy"',
      ],
      finance: [
        'From "Making money" to "Keeping money"',
        'From "Budgeting constraints" to "Investment opportunities"',
        'From "Saving pennies" to "Building wealth systems"',
      ],
      dating: [
        'From "Finding someone" to "Being someone worth finding"',
        'From "Playing it safe" to "Being authentic"',
        'From "Chasing" to "Attracting"',
      ],
      mindset: [
        'From "I have to" to "I get to"',
        'From "What can go wrong?" to "What can go right?"',
        'From "Fixed identity" to "Growth mindset"',
      ],
      productivity: [
        'From "Busy" to "Focused"',
        'From "More hours" to "Better systems"',
        'From "Doing it all" to "Doing what matters"',
      ],
      business: [
        'From "Building a job" to "Building a business"',
        'From "Me" to "Systems and team"',
        'From "Survival" to "Scale"',
      ],
      lifestyle: [
        'From "Busy is productive" to "Focused is productive"',
        'From "More options" to "Clear priorities"',
        'From "Default life" to "Designed life"',
      ],
    };

    const moduleShifts = shifts[module] || ['From reactive to proactive'];
    return moduleShifts[Math.floor(Math.random() * moduleShifts.length)];
  }

  /**
   * Get power question for the day
   */
  private getPowerQuestionForDate(rng: SeededRandom): string {
    const dayNum = Math.floor(rng.next() * 1000000) % this.powerQuestions.length;
    return this.powerQuestions[dayNum];
  }

  /**
   * Get mindset shift for the day
   */
  private getMindsetShiftForDate(rng: SeededRandom): MindsetShift {
    const index = Math.floor(rng.next() * this.mindsetShifts.length);
    return this.mindsetShifts[index];
  }

  /**
   * Create a date-seeded random number generator
   * Same seed for same date means same "random" values all day
   */
  private getSeededRandom(date: string): SeededRandom {
    // Convert date to seed: take YYYY-MM-DD and convert to number
    const dateParts = date.split('-');
    let seed = parseInt(`${dateParts[0]}${dateParts[1]}${dateParts[2]}`);

    return {
      next: () => {
        seed = (seed * 9301 + 49297) % 233280;
        return seed / 233280;
      },
    };
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

  /**
   * Get module display name
   */
  private getModuleName(module: string): string {
    const names: Record<string, string> = {
      money: 'Money & Wealth',
      sales: 'Sales & Persuasion',
      finance: 'Personal Finance',
      dating: 'Dating & Social',
      mindset: 'Mindset & Wisdom',
      health: 'Health & Fitness',
      lifestyle: 'Lifestyle Design',
      business: 'Business & Career',
      productivity: 'Productivity & Systems',
      emotional_intelligence: 'Emotional Intelligence',
      critical_thinking: 'Critical Thinking',
      communication: 'Communication & Influence',
    };
    return names[module] || module.charAt(0).toUpperCase() + module.slice(1);
  }

  /**
   * Utility to shuffle array
   */
  private shuffleArray<T>(array: T[]): T[] {
    const shuffled = [...array];
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
  }
}

export default new WisdomService();
