import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { COLORS, SPACING, TYPOGRAPHY, BORDER_RADIUS, SHADOWS } from '@/constants/theme';

interface StatItem {
  label: string;
  value: string | number;
  color?: string;
  icon?: string;
}

interface StatsBarProps {
  stats: StatItem[];
  variant?: 'horizontal' | 'grid';
  columns?: number;
}

export const StatsBar: React.FC<StatsBarProps> = ({
  stats,
  variant = 'horizontal',
  columns = 2,
}) => {
  if (variant === 'grid') {
    return (
      <View
        style={[
          styles.gridContainer,
          { flexWrap: 'wrap', justifyContent: 'space-between' },
        ]}
      >
        {stats.map((stat, index) => (
          <View
            key={index}
            style={[
              styles.gridItem,
              { width: `${100 / columns - 2}%` },
            ]}
          >
            <View style={styles.gridContent}>
              {stat.icon && <Text style={styles.icon}>{stat.icon}</Text>}
              <Text style={styles.label}>{stat.label}</Text>
              <Text
                style={[
                  styles.value,
                  stat.color && { color: stat.color },
                ]}
              >
                {stat.value}
              </Text>
            </View>
          </View>
        ))}
      </View>
    );
  }

  return (
    <View style={styles.horizontalContainer}>
      {stats.map((stat, index) => (
        <React.Fragment key={index}>
          <View style={styles.horizontalItem}>
            <Text style={styles.label}>{stat.label}</Text>
            <Text
              style={[
                styles.value,
                stat.color && { color: stat.color },
              ]}
            >
              {stat.icon && `${stat.icon} `}
              {stat.value}
            </Text>
          </View>
          {index < stats.length - 1 && <View style={styles.divider} />}
        </React.Fragment>
      ))}
    </View>
  );
};

const styles = StyleSheet.create({
  horizontalContainer: {
    flexDirection: 'row',
    backgroundColor: COLORS.surface,
    borderRadius: BORDER_RADIUS.lg,
    paddingHorizontal: SPACING.lg,
    paddingVertical: SPACING.lg,
    ...SHADOWS.sm,
  },
  horizontalItem: {
    flex: 1,
    alignItems: 'center',
  },
  gridContainer: {
    display: 'flex',
  },
  gridItem: {
    marginBottom: SPACING.md,
  },
  gridContent: {
    backgroundColor: COLORS.surface,
    borderRadius: BORDER_RADIUS.lg,
    paddingVertical: SPACING.lg,
    paddingHorizontal: SPACING.md,
    alignItems: 'center',
    ...SHADOWS.sm,
  },
  icon: {
    fontSize: 24,
    marginBottom: SPACING.sm,
  },
  label: {
    ...TYPOGRAPHY.caption,
    color: COLORS.textSecondary,
    marginBottom: SPACING.xs,
  },
  value: {
    ...TYPOGRAPHY.h3,
    color: COLORS.text,
  },
  divider: {
    width: 1,
    height: 40,
    backgroundColor: COLORS.surfaceLight,
    marginHorizontal: SPACING.md,
  },
});
