// User Profile Types
export interface UserProfile {
  name: string;
  created_at: string;
  updated_at: string;
  top_goals: string[];
  daily_time_available_minutes: number;
  coaching_style: 'direct' | 'supportive' | 'balanced';
  constraints: string[];
  module_levels: ModuleLevels;
  focus_modules: string[];
  goals_90_day: Record<string, NinetyDayGoal>;
}

export interface ModuleLevels {
  money: number;
  sales: number;
  finance: number;
  dating: number;
  mindset: number;
  health: number;
  lifestyle: number;
  business: number;
  productivity: number;
  emotional_intelligence: number;
  critical_thinking: number;
  communication: number;
}

export interface NinetyDayGoal {
  goal: string;
  target_level: number;
  start_level: number;
  created_at: string;
}

// Habit Types
export interface Habit {
  id: string;
  name: string;
  module: string;
  frequency: 'daily' | 'weekly' | 'custom';
  created_at: string;
  current_streak: number;
  best_streak: number;
  total_completions: number;
}

export interface HabitCompletion {
  habit_id: string;
  completed_at: string;
  date: string;
  notes?: string;
}

export interface HabitsData {
  habits: Habit[];
  completions: {
    [date: string]: string[]; // date -> array of habit IDs
  };
}

// Daily Check-in Types
export interface DailyCheckin {
  date: string;
  morning: MorningCheckin;
  evening: EveningCheckin;
}

export interface MorningCheckin {
  sleep_hours?: number; // web uses this
  sleep_quality: number; // 1-10
  energy_level: number; // 1-10
  top_3_priorities: string[];
  win_definition: string;
  timestamp: string;
  time?: string; // compatibility with web format
}

export interface EveningCheckin {
  wins: string[];
  challenges_lessons: string[];
  deep_work_hours: number;
  habits_completed: string[]; // habit IDs
  day_score: number; // 1-10
  timestamp: string;
  time?: string; // compatibility with web format
  challenges?: string[]; // compatibility with web format
  lessons?: string[]; // compatibility with web format
  improvement_for_tomorrow?: string; // compatibility
  main_win_achieved?: boolean; // compatibility
}

export interface AMCheckin {
  time: string;
  sleep_hours: number;
  sleep_quality: number;
  energy_level: number;
  top_3_priorities: string[];
  win_definition: string;
}

export interface PMReflection {
  time: string;
  wins: string[];
  challenges: string[];
  lessons: string[];
  improvement_for_tomorrow: string;
  day_score: number;
  main_win_achieved?: boolean;
}

export interface PlannedAction {
  module: string;
  module_name: string;
  text: string;
  time: number;
  difficulty: number;
  completed?: boolean;
}

export interface Metrics {
  deep_work_hours: number;
  workouts: number;
  sales_calls: number;
  social_interactions: number;
  steps: number;
  water_liters: number;
}

export interface DailyLog {
  date: string;
  created_at: string;
  updated_at: string;
  am_checkin: AMCheckin | null;
  planned_actions: PlannedAction[];
  completed_actions: PlannedAction[];
  pm_reflection: PMReflection | null;
  metrics: Metrics;
  habits: {
    [habitId: string]: boolean;
  };
  notes: string;
}

// Wisdom/Master Types
export interface Master {
  name: string;
  expertise: string;
  key_principles: string[];
  daily_practices: string[];
  worked_examples: WorkedExample[];
  scripts_templates: ScriptTemplate[];
  resources: MasterResources;
}

export interface WorkedExample {
  title: string;
  scenario: string;
  framework_applied: string;
  step_by_step: string[];
  outcome: string;
}

export interface ScriptTemplate {
  title: string;
  context: string;
  template: string;
  example_filled: string;
}

export interface MasterResources {
  books: BookResource[];
  podcasts: PodcastResource[];
}

export interface BookResource {
  title: string;
  author: string;
  key_takeaway: string;
}

export interface PodcastResource {
  title: string;
  episode?: string;
  key_takeaway: string;
}

export interface MastersModule {
  module: string;
  level_definitions: Record<string, LevelDefinition>;
  progressive_exercises: Record<string, Exercise[]>;
  cross_module_connections: CrossModuleConnection[];
  masters: Master[];
  daily_insights: string[];
  skill_challenges: string[];
}

export interface LevelDefinition {
  name: string;
  description: string;
  capabilities: string[];
  milestone: string;
}

export interface Exercise {
  title: string;
  difficulty: number;
  time_minutes: number;
  instructions: string;
  success_criteria: string;
}

export interface CrossModuleConnection {
  connected_module: string;
  insight: string;
  combined_exercise: string;
}

// Stats/Progress Types
export interface ProgressStats {
  date: string;
  day_streak: number;
  deep_work_hours: number;
  habit_completion_percentage: number;
  average_day_score: number;
  module_scores: Record<string, number>;
  habit_streaks: Record<string, number>;
}

// Wisdom Daily Content
export interface DailyWisdom {
  date: string;
  master_name?: string;
  module?: string;
  teaching?: string;
  master_teaching: MasterTeaching;
  daily_insight: string;
  skill_challenge: SkillChallenge;
  power_question: string;
  mindset_shift: MindsetShift;
  worked_example?: WorkedExample;
  insight?: string;
}

export interface MasterTeaching {
  master: string;
  expertise: string;
  teaching: string;
  practice: string;
  module: string;
}

export interface SkillChallenge {
  module: string;
  module_name: string;
  challenge: string;
}

export interface MindsetShift {
  from: string;
  to: string;
  why: string;
}

export interface TodaysCheckin {
  date: string;
  hasAMCheckin: boolean;
  hasPMReflection: boolean;
  morningCheckin?: AMCheckin;
  eveningReflection?: PMReflection;
}

// Journal Entry Types
export interface JournalEntry {
  id: string;
  date: string;
  timestamp: string;
  title: string;
  content: string;
  module?: string;
  tags: string[];
  mood: number; // 1-10
}

// Storage Types
export interface StorageData {
  userProfile: UserProfile;
  habits: Habit[];
  habitCompletions: HabitCompletion[];
  checkins: DailyCheckin[];
  stats: ProgressStats[];
  journalEntries: JournalEntry[];
}

// API Response Types
export interface ApiResponse<T> {
  success: boolean;
  data: T;
  error?: string;
}

export interface ApiError {
  code: string;
  message: string;
  details?: unknown;
}
