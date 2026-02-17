import { ModuleLevels } from '@/types';
import { COLORS } from './theme';

export const MODULE_NAMES = [
  'money',
  'sales',
  'finance',
  'dating',
  'mindset',
  'health',
  'lifestyle',
  'business',
  'productivity',
  'emotional_intelligence',
  'critical_thinking',
  'communication',
] as const;

export const MODULE_DISPLAY_NAMES: Record<string, string> = {
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

export const MODULE_DESCRIPTIONS: Record<string, string> = {
  money: 'Building wealth, income streams, financial freedom',
  sales: 'Closing deals, negotiation, influence',
  finance: 'Budgeting, investing, debt management',
  dating: 'Relationships, social skills, confidence',
  mindset: 'Mental models, stoicism, resilience',
  health: 'Physical fitness, nutrition, recovery',
  lifestyle: 'Habits, environment, time management',
  business: 'Entrepreneurship, leadership, strategy',
  productivity: 'Deep work, focus, systems thinking',
  emotional_intelligence: 'EQ, regulation, empathy, relationships',
  critical_thinking: 'Mental models, biases, decision-making',
  communication: 'Speaking, listening, presence, persuasion',
};

export const MODULE_ICONS: Record<string, string> = {
  money: '💰',
  sales: '🤝',
  finance: '📊',
  dating: '💕',
  mindset: '🧠',
  health: '💪',
  lifestyle: '🎯',
  business: '📈',
  productivity: '⚡',
  emotional_intelligence: '❤️',
  critical_thinking: '🔍',
  communication: '🗣️',
};

export const MODULE_COLORS: Record<string, string> = {
  money: COLORS.module.money,
  sales: COLORS.module.sales,
  finance: COLORS.module.finance,
  dating: COLORS.module.dating,
  mindset: COLORS.module.mindset,
  health: COLORS.module.health,
  lifestyle: COLORS.module.lifestyle,
  business: COLORS.module.business,
  productivity: COLORS.module.productivity,
  emotional_intelligence: COLORS.module.emotional_intelligence,
  critical_thinking: COLORS.module.critical_thinking,
  communication: COLORS.module.communication,
};

export const DEFAULT_MODULE_LEVELS: ModuleLevels = {
  money: 1,
  sales: 1,
  finance: 1,
  dating: 1,
  mindset: 1,
  health: 1,
  lifestyle: 1,
  business: 1,
  productivity: 1,
  emotional_intelligence: 1,
  critical_thinking: 1,
  communication: 1,
};

export const FOCUS_MODULES = [
  'money',
  'sales',
  'finance',
  'productivity',
  'business',
];

export const DEFAULT_HABITS = [
  {
    id: 'morning_routine',
    name: 'Morning Routine (full)',
    module: 'productivity',
    target_time: '05:30',
  },
  {
    id: 'deep_work_90',
    name: 'Deep Work Block (90+ min)',
    module: 'productivity',
    target_time: '09:00',
  },
  {
    id: 'sales_outreach',
    name: 'Sales Outreach (10+ touches)',
    module: 'sales',
    target_time: '10:00',
  },
  {
    id: 'objection_practice',
    name: 'Objection Handling Practice',
    module: 'sales',
    target_time: '14:00',
  },
  {
    id: 'finance_review',
    name: 'Finance Check (spending/budget)',
    module: 'finance',
    target_time: '18:00',
  },
  {
    id: 'skill_learning',
    name: 'Skill Development (30+ min)',
    module: 'money',
    target_time: '11:00',
  },
  {
    id: 'journaling',
    name: 'Journaling (AM or PM)',
    module: 'mindset',
    target_time: '21:00',
  },
  {
    id: 'reading',
    name: 'Reading (20+ min)',
    module: 'mindset',
    target_time: '20:00',
  },
  {
    id: 'networking',
    name: 'Networking Action (1 message/call)',
    module: 'business',
    target_time: '15:00',
  },
  {
    id: 'social_interaction',
    name: 'New Social Interaction',
    module: 'dating',
    target_time: '18:00',
  },
  {
    id: 'inbox_zero',
    name: 'Inbox Zero',
    module: 'productivity',
    target_time: '17:00',
  },
  {
    id: 'no_phone_morning',
    name: 'No Phone First Hour',
    module: 'lifestyle',
    target_time: '05:30',
  },
];

export const LEVEL_DESCRIPTIONS: Record<number, string> = {
  1: 'Awareness',
  2: 'Foundation',
  3: 'Skill Builder',
  4: 'Value Creator',
  5: 'Leverage Seeker',
  6: 'System Builder',
  7: 'Equity Thinker',
  8: 'Architect',
  9: 'Freedom Builder',
  10: 'Master',
};

export const LEVEL_COLORS: Record<number, string> = {
  1: '#505050',
  2: '#626262',
  3: '#747474',
  4: '#868686',
  5: '#4dabf7',
  6: '#20c997',
  7: '#ffd700',
  8: '#ff922b',
  9: '#ff6b6b',
  10: '#ff69b4',
};
