export const COLORS = {
  // Primary dark mode theme
  background: '#0a0a0a',
  surface: '#1a1a1a',
  surfaceLight: '#2d2d2d',
  text: '#ffffff',
  textSecondary: '#b3b3b3',
  textTertiary: '#808080',

  // Accent colors by module
  module: {
    money: '#ffd700',
    sales: '#ff6b6b',
    finance: '#4dabf7',
    dating: '#ff69b4',
    mindset: '#9775fa',
    health: '#51cf66',
    lifestyle: '#20c997',
    business: '#ff922b',
    productivity: '#748ffc',
    emotional_intelligence: '#ff8787',
    critical_thinking: '#a8e6cf',
    communication: '#ffd3b6',
  },

  // Semantic colors
  success: '#51cf66',
  warning: '#ffd43b',
  error: '#ff6b6b',
  info: '#4dabf7',

  // Grayscale
  black: '#000000',
  white: '#ffffff',
  gray50: '#f8f9fa',
  gray100: '#e9ecef',
  gray200: '#dee2e6',
  gray300: '#ced4da',
  gray400: '#adb5bd',
  gray500: '#868e96',
  gray600: '#495057',
  gray700: '#343a40',
  gray800: '#212529',
  gray900: '#0d0f12',

  // Overlay
  overlay: 'rgba(0, 0, 0, 0.7)',
  overlayLight: 'rgba(255, 255, 255, 0.1)',
};

export const SPACING = {
  xs: 4,
  sm: 8,
  md: 12,
  lg: 16,
  xl: 24,
  xxl: 32,
  xxxl: 48,
};

export const TYPOGRAPHY = {
  display: {
    fontSize: 36,
    fontWeight: '700' as const,
    lineHeight: 42,
  },
  h1: {
    fontSize: 28,
    fontWeight: '700' as const,
    lineHeight: 34,
  },
  h2: {
    fontSize: 24,
    fontWeight: '700' as const,
    lineHeight: 30,
  },
  h3: {
    fontSize: 20,
    fontWeight: '600' as const,
    lineHeight: 26,
  },
  body: {
    fontSize: 16,
    fontWeight: '400' as const,
    lineHeight: 22,
  },
  bodyBold: {
    fontSize: 16,
    fontWeight: '600' as const,
    lineHeight: 22,
  },
  subtitle: {
    fontSize: 14,
    fontWeight: '500' as const,
    lineHeight: 20,
  },
  caption: {
    fontSize: 12,
    fontWeight: '400' as const,
    lineHeight: 16,
  },
  captionBold: {
    fontSize: 12,
    fontWeight: '600' as const,
    lineHeight: 16,
  },
  overline: {
    fontSize: 11,
    fontWeight: '700' as const,
    lineHeight: 16,
    textTransform: 'uppercase' as const,
  },
};

export const BORDER_RADIUS = {
  none: 0,
  sm: 4,
  md: 8,
  lg: 12,
  xl: 16,
  full: 999,
};

export const SHADOWS = {
  none: {
    shadowColor: 'transparent',
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0,
    shadowRadius: 0,
    elevation: 0,
  },
  sm: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.18,
    shadowRadius: 1.0,
    elevation: 1,
  },
  md: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  lg: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 4.65,
    elevation: 8,
  },
};

export const theme = {
  colors: COLORS,
  spacing: SPACING,
  typography: TYPOGRAPHY,
  borderRadius: BORDER_RADIUS,
  shadows: SHADOWS,
};

export type Theme = typeof theme;
