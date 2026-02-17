import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView, SafeAreaView } from 'react-native';
import { DailyWisdom } from '@/types';
import { COLORS, SPACING, TYPOGRAPHY, BORDER_RADIUS, SHADOWS } from '@/constants/theme';
import { MODULE_ICONS, MODULE_COLORS } from '@/constants/modules';

interface WisdomCardProps {
  wisdom: DailyWisdom | null;
  loading?: boolean;
  onRefresh?: () => void;
}

export const WisdomCard: React.FC<WisdomCardProps> = ({ wisdom, loading, onRefresh }) => {
  if (!wisdom) {
    return (
      <View style={styles.container}>
        <Text style={styles.emptyText}>Loading wisdom...</Text>
      </View>
    );
  }

  const moduleColor = MODULE_COLORS[wisdom.module as keyof typeof MODULE_COLORS] || COLORS.info;
  const moduleIcon = MODULE_ICONS[wisdom.module as keyof typeof MODULE_ICONS] || '🎯';

  return (
    <ScrollView style={styles.container} showsVerticalScrollIndicator={false}>
      <SafeAreaView>
        {/* Header */}
        <View style={[styles.header, { borderLeftColor: moduleColor }]}>
          <View style={styles.headerContent}>
            <Text style={styles.moduleLabel}>{moduleIcon} {wisdom.module.toUpperCase()}</Text>
            <Text style={styles.masterName}>{wisdom.master_name}</Text>
          </View>
          <TouchableOpacity
            style={[styles.refreshButton, { backgroundColor: moduleColor }]}
            onPress={onRefresh}
            disabled={loading}
          >
            <Text style={styles.refreshButtonText}>🔄</Text>
          </TouchableOpacity>
        </View>

        {/* Teaching */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Teaching</Text>
          <Text style={styles.sectionContent}>{wisdom.teaching}</Text>
        </View>

        {/* Insight */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Daily Insight</Text>
          <Text style={styles.sectionContent}>{wisdom.insight}</Text>
        </View>

        {/* Power Question */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Power Question</Text>
          <Text style={[styles.sectionContent, styles.question]}>{wisdom.power_question}</Text>
        </View>

        {/* Mindset Shift */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Mindset Shift</Text>
          <View style={[styles.mindsetBox, { borderLeftColor: moduleColor }]}>
            <Text style={styles.mindsetText}>{wisdom.mindset_shift}</Text>
          </View>
        </View>

        {/* Skill Challenge */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Today's Challenge</Text>
          <View style={[styles.challengeBox, { backgroundColor: moduleColor + '15' }]}>
            <Text style={styles.challengeText}>{wisdom.skill_challenge}</Text>
          </View>
        </View>

        {/* Worked Example */}
        {wisdom.worked_example && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Worked Example</Text>
            <View style={styles.exampleBox}>
              <Text style={styles.exampleTitle}>{wisdom.worked_example.title}</Text>
              <Text style={styles.exampleScenario}>{wisdom.worked_example.scenario}</Text>
              <Text style={styles.exampleFramework}>
                Framework: {wisdom.worked_example.framework_applied}
              </Text>
              <Text style={styles.exampleOutcome}>Outcome: {wisdom.worked_example.outcome}</Text>
            </View>
          </View>
        )}

        {/* Spacing */}
        <View style={{ height: SPACING.lg }} />
      </SafeAreaView>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
    paddingHorizontal: SPACING.lg,
    paddingTop: SPACING.lg,
  },
  emptyText: {
    ...TYPOGRAPHY.body,
    color: COLORS.textSecondary,
    textAlign: 'center',
    marginTop: SPACING.xl,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: SPACING.lg,
    paddingHorizontal: SPACING.lg,
    backgroundColor: COLORS.surface,
    borderRadius: BORDER_RADIUS.lg,
    borderLeftWidth: 4,
    marginBottom: SPACING.lg,
    ...SHADOWS.md,
  },
  headerContent: {
    flex: 1,
  },
  moduleLabel: {
    ...TYPOGRAPHY.caption,
    color: COLORS.textSecondary,
    marginBottom: SPACING.sm,
  },
  masterName: {
    ...TYPOGRAPHY.h3,
    color: COLORS.text,
  },
  refreshButton: {
    width: 44,
    height: 44,
    borderRadius: BORDER_RADIUS.full,
    justifyContent: 'center',
    alignItems: 'center',
  },
  refreshButtonText: {
    fontSize: 20,
  },
  section: {
    marginBottom: SPACING.xl,
  },
  sectionTitle: {
    ...TYPOGRAPHY.bodyBold,
    color: COLORS.text,
    marginBottom: SPACING.md,
  },
  sectionContent: {
    ...TYPOGRAPHY.body,
    color: COLORS.textSecondary,
    lineHeight: 22,
  },
  question: {
    fontStyle: 'italic',
    color: COLORS.info,
  },
  mindsetBox: {
    borderLeftWidth: 3,
    paddingLeft: SPACING.md,
    paddingRight: SPACING.md,
    paddingVertical: SPACING.md,
    backgroundColor: COLORS.surfaceLight,
    borderRadius: BORDER_RADIUS.md,
  },
  mindsetText: {
    ...TYPOGRAPHY.body,
    color: COLORS.text,
    fontStyle: 'italic',
  },
  challengeBox: {
    padding: SPACING.lg,
    borderRadius: BORDER_RADIUS.lg,
  },
  challengeText: {
    ...TYPOGRAPHY.body,
    color: COLORS.text,
    lineHeight: 22,
  },
  exampleBox: {
    backgroundColor: COLORS.surface,
    padding: SPACING.lg,
    borderRadius: BORDER_RADIUS.lg,
    borderLeftWidth: 3,
    borderLeftColor: COLORS.success,
  },
  exampleTitle: {
    ...TYPOGRAPHY.bodyBold,
    color: COLORS.text,
    marginBottom: SPACING.sm,
  },
  exampleScenario: {
    ...TYPOGRAPHY.body,
    color: COLORS.textSecondary,
    marginBottom: SPACING.md,
  },
  exampleFramework: {
    ...TYPOGRAPHY.caption,
    color: COLORS.info,
    marginBottom: SPACING.sm,
  },
  exampleOutcome: {
    ...TYPOGRAPHY.caption,
    color: COLORS.success,
  },
});
