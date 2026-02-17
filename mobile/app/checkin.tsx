import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  TextInput,
  SafeAreaView,
  ActivityIndicator,
  Modal,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { useTodayCheckin, useMorningCheckin, useEveningCheckin } from '@/hooks/useCheckin';
import { COLORS, SPACING, TYPOGRAPHY, BORDER_RADIUS, SHADOWS } from '@/constants/theme';

export default function CheckinScreen() {
  const { checkin, loading: checkinLoading, refreshCheckin } = useTodayCheckin();
  const { isComplete: morningComplete, saveMorningCheckin } = useMorningCheckin();
  const { isComplete: eveningComplete, saveEveningCheckin } = useEveningCheckin();

  const [showMorningModal, setShowMorningModal] = useState(false);
  const [showEveningModal, setShowEveningModal] = useState(false);

  // Morning Checkin State
  const [sleepQuality, setSleepQuality] = useState(5);
  const [energyLevel, setEnergyLevel] = useState(5);
  const [priorities, setPriorities] = useState<string[]>(['', '', '']);
  const [winDefinition, setWinDefinition] = useState('');

  // Evening Reflection State
  const [wins, setWins] = useState<string[]>(['']);
  const [challenges, setChallenges] = useState<string[]>(['']);
  const [deepWorkHours, setDeepWorkHours] = useState(0);
  const [dayScore, setDayScore] = useState(5);
  const [savingMorning, setSavingMorning] = useState(false);
  const [savingEvening, setSavingEvening] = useState(false);

  useEffect(() => {
    if (checkin?.morning) {
      setSleepQuality(checkin.morning.sleep_quality);
      setEnergyLevel(checkin.morning.energy_level);
      setPriorities(checkin.morning.top_3_priorities);
      setWinDefinition(checkin.morning.win_definition);
    }

    if (checkin?.evening) {
      setWins(checkin.evening.wins);
      setChallenges(checkin.evening.challenges_lessons);
      setDeepWorkHours(checkin.evening.deep_work_hours);
      setDayScore(checkin.evening.day_score);
    }
  }, [checkin]);

  const handleSaveMorning = async () => {
    try {
      setSavingMorning(true);
      await saveMorningCheckin(sleepQuality, energyLevel, priorities.filter(p => p.length > 0), winDefinition);
      await refreshCheckin();
      setShowMorningModal(false);
    } catch (error) {
      alert('Failed to save morning checkin');
      console.error('Failed to save morning checkin:', error);
    } finally {
      setSavingMorning(false);
    }
  };

  const handleSaveEvening = async () => {
    try {
      setSavingEvening(true);
      await saveEveningCheckin(
        wins.filter(w => w.length > 0),
        challenges.filter(c => c.length > 0),
        deepWorkHours,
        [],
        dayScore
      );
      await refreshCheckin();
      setShowEveningModal(false);
    } catch (error) {
      alert('Failed to save evening reflection');
      console.error('Failed to save evening reflection:', error);
    } finally {
      setSavingEvening(false);
    }
  };

  if (checkinLoading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={COLORS.info} />
      </View>
    );
  }

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView style={styles.container} showsVerticalScrollIndicator={false}>
        {/* Morning Checkin Card */}
        <TouchableOpacity
          style={[
            styles.checkinCard,
            morningComplete && styles.completedCard,
            { borderLeftColor: COLORS.info },
          ]}
          onPress={() => setShowMorningModal(true)}
        >
          <View style={styles.cardHeader}>
            <Text style={styles.cardTitle}>🌅 Morning Check-in</Text>
            {morningComplete && <Text style={styles.completeBadge}>✓ Complete</Text>}
          </View>
          {checkin?.morning ? (
            <View style={styles.cardContent}>
              <Text style={styles.fieldLabel}>Sleep Quality: {checkin.morning.sleep_quality}/10</Text>
              <Text style={styles.fieldLabel}>Energy Level: {checkin.morning.energy_level}/10</Text>
              <Text style={styles.fieldLabel}>Win Definition: {checkin.morning.win_definition}</Text>
            </View>
          ) : (
            <Text style={styles.emptyText}>Tap to complete your morning check-in</Text>
          )}
        </TouchableOpacity>

        {/* Evening Reflection Card */}
        <TouchableOpacity
          style={[
            styles.checkinCard,
            eveningComplete && styles.completedCard,
            { borderLeftColor: COLORS.warning },
            { marginTop: SPACING.lg },
          ]}
          onPress={() => setShowEveningModal(true)}
        >
          <View style={styles.cardHeader}>
            <Text style={styles.cardTitle}>🌙 Evening Reflection</Text>
            {eveningComplete && <Text style={styles.completeBadge}>✓ Complete</Text>}
          </View>
          {checkin?.evening ? (
            <View style={styles.cardContent}>
              <Text style={styles.fieldLabel}>Day Score: {checkin.evening.day_score}/10</Text>
              <Text style={styles.fieldLabel}>Deep Work: {checkin.evening.deep_work_hours}h</Text>
              <Text style={styles.fieldLabel}>Wins: {checkin.evening.wins.length}</Text>
            </View>
          ) : (
            <Text style={styles.emptyText}>Tap to complete your evening reflection</Text>
          )}
        </TouchableOpacity>

        <View style={{ height: SPACING.xl }} />
      </ScrollView>

      {/* Morning Checkin Modal */}
      <Modal
        visible={showMorningModal}
        animationType="slide"
        onRequestClose={() => setShowMorningModal(false)}
      >
        <SafeAreaView style={styles.modalSafeArea}>
          <KeyboardAvoidingView
            behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
            style={styles.keyboardAvoid}
          >
            <ScrollView style={styles.modalContainer} showsVerticalScrollIndicator={false}>
              <View style={styles.modalHeader}>
                <TouchableOpacity onPress={() => setShowMorningModal(false)}>
                  <Text style={styles.closeButton}>✕</Text>
                </TouchableOpacity>
                <Text style={styles.modalTitle}>Morning Check-in</Text>
                <View style={{ width: 40 }} />
              </View>

              {/* Sleep Quality */}
              <View style={styles.section}>
                <Text style={styles.label}>How well did you sleep?</Text>
                <View style={styles.sliderContainer}>
                  {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(value => (
                    <TouchableOpacity
                      key={value}
                      style={[
                        styles.sliderButton,
                        sleepQuality === value && styles.sliderButtonActive,
                      ]}
                      onPress={() => setSleepQuality(value)}
                    >
                      <Text
                        style={[
                          styles.sliderButtonText,
                          sleepQuality === value && styles.sliderButtonTextActive,
                        ]}
                      >
                        {value}
                      </Text>
                    </TouchableOpacity>
                  ))}
                </View>
              </View>

              {/* Energy Level */}
              <View style={styles.section}>
                <Text style={styles.label}>What's your energy level?</Text>
                <View style={styles.sliderContainer}>
                  {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(value => (
                    <TouchableOpacity
                      key={value}
                      style={[
                        styles.sliderButton,
                        energyLevel === value && styles.sliderButtonActive,
                      ]}
                      onPress={() => setEnergyLevel(value)}
                    >
                      <Text
                        style={[
                          styles.sliderButtonText,
                          energyLevel === value && styles.sliderButtonTextActive,
                        ]}
                      >
                        {value}
                      </Text>
                    </TouchableOpacity>
                  ))}
                </View>
              </View>

              {/* Top 3 Priorities */}
              <View style={styles.section}>
                <Text style={styles.label}>Top 3 Priorities for Today</Text>
                {priorities.map((priority, index) => (
                  <TextInput
                    key={index}
                    style={styles.textInput}
                    placeholder={`Priority ${index + 1}`}
                    placeholderTextColor={COLORS.textTertiary}
                    value={priority}
                    onChangeText={text => {
                      const newPriorities = [...priorities];
                      newPriorities[index] = text;
                      setPriorities(newPriorities);
                    }}
                  />
                ))}
              </View>

              {/* Win Definition */}
              <View style={styles.section}>
                <Text style={styles.label}>What defines a WIN for today?</Text>
                <TextInput
                  style={[styles.textInput, styles.multilineInput]}
                  placeholder="Define your win..."
                  placeholderTextColor={COLORS.textTertiary}
                  value={winDefinition}
                  onChangeText={setWinDefinition}
                  multiline
                  numberOfLines={3}
                />
              </View>

              {/* Save Button */}
              <TouchableOpacity
                style={styles.saveButton}
                onPress={handleSaveMorning}
                disabled={savingMorning}
              >
                {savingMorning ? (
                  <ActivityIndicator color={COLORS.white} />
                ) : (
                  <Text style={styles.saveButtonText}>Save Check-in</Text>
                )}
              </TouchableOpacity>

              <View style={{ height: SPACING.xl }} />
            </ScrollView>
          </KeyboardAvoidingView>
        </SafeAreaView>
      </Modal>

      {/* Evening Reflection Modal */}
      <Modal
        visible={showEveningModal}
        animationType="slide"
        onRequestClose={() => setShowEveningModal(false)}
      >
        <SafeAreaView style={styles.modalSafeArea}>
          <KeyboardAvoidingView
            behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
            style={styles.keyboardAvoid}
          >
            <ScrollView style={styles.modalContainer} showsVerticalScrollIndicator={false}>
              <View style={styles.modalHeader}>
                <TouchableOpacity onPress={() => setShowEveningModal(false)}>
                  <Text style={styles.closeButton}>✕</Text>
                </TouchableOpacity>
                <Text style={styles.modalTitle}>Evening Reflection</Text>
                <View style={{ width: 40 }} />
              </View>

              {/* Day Score */}
              <View style={styles.section}>
                <Text style={styles.label}>How would you rate today? (1-10)</Text>
                <View style={styles.sliderContainer}>
                  {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(value => (
                    <TouchableOpacity
                      key={value}
                      style={[
                        styles.sliderButton,
                        dayScore === value && styles.sliderButtonActive,
                      ]}
                      onPress={() => setDayScore(value)}
                    >
                      <Text
                        style={[
                          styles.sliderButtonText,
                          dayScore === value && styles.sliderButtonTextActive,
                        ]}
                      >
                        {value}
                      </Text>
                    </TouchableOpacity>
                  ))}
                </View>
              </View>

              {/* Deep Work Hours */}
              <View style={styles.section}>
                <Text style={styles.label}>Deep Work Hours (0-12)</Text>
                <TextInput
                  style={styles.numberInput}
                  placeholder="Hours"
                  placeholderTextColor={COLORS.textTertiary}
                  keyboardType="decimal-pad"
                  value={deepWorkHours.toString()}
                  onChangeText={text => setDeepWorkHours(parseFloat(text) || 0)}
                />
              </View>

              {/* Wins */}
              <View style={styles.section}>
                <Text style={styles.label}>What are your WINS? 🏆</Text>
                {wins.map((win, index) => (
                  <TextInput
                    key={index}
                    style={[styles.textInput, styles.multilineInput]}
                    placeholder={`Win ${index + 1}`}
                    placeholderTextColor={COLORS.textTertiary}
                    value={win}
                    onChangeText={text => {
                      const newWins = [...wins];
                      newWins[index] = text;
                      setWins(newWins);
                    }}
                    multiline
                    numberOfLines={2}
                  />
                ))}
                <TouchableOpacity
                  style={styles.addButton}
                  onPress={() => setWins([...wins, ''])}
                >
                  <Text style={styles.addButtonText}>+ Add another win</Text>
                </TouchableOpacity>
              </View>

              {/* Challenges/Lessons */}
              <View style={styles.section}>
                <Text style={styles.label}>Challenges & Lessons Learned 📚</Text>
                {challenges.map((challenge, index) => (
                  <TextInput
                    key={index}
                    style={[styles.textInput, styles.multilineInput]}
                    placeholder={`Challenge ${index + 1}`}
                    placeholderTextColor={COLORS.textTertiary}
                    value={challenge}
                    onChangeText={text => {
                      const newChallenges = [...challenges];
                      newChallenges[index] = text;
                      setChallenges(newChallenges);
                    }}
                    multiline
                    numberOfLines={2}
                  />
                ))}
                <TouchableOpacity
                  style={styles.addButton}
                  onPress={() => setChallenges([...challenges, ''])}
                >
                  <Text style={styles.addButtonText}>+ Add another challenge</Text>
                </TouchableOpacity>
              </View>

              {/* Save Button */}
              <TouchableOpacity
                style={styles.saveButton}
                onPress={handleSaveEvening}
                disabled={savingEvening}
              >
                {savingEvening ? (
                  <ActivityIndicator color={COLORS.white} />
                ) : (
                  <Text style={styles.saveButtonText}>Save Reflection</Text>
                )}
              </TouchableOpacity>

              <View style={{ height: SPACING.xl }} />
            </ScrollView>
          </KeyboardAvoidingView>
        </SafeAreaView>
      </Modal>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
    paddingHorizontal: SPACING.lg,
    paddingTop: SPACING.lg,
  },
  loadingContainer: {
    flex: 1,
    backgroundColor: COLORS.background,
    justifyContent: 'center',
    alignItems: 'center',
  },
  checkinCard: {
    backgroundColor: COLORS.surface,
    borderRadius: BORDER_RADIUS.lg,
    borderLeftWidth: 4,
    paddingHorizontal: SPACING.lg,
    paddingVertical: SPACING.lg,
    ...SHADOWS.md,
  },
  completedCard: {
    opacity: 0.8,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.md,
  },
  cardTitle: {
    ...TYPOGRAPHY.h3,
    color: COLORS.text,
  },
  completeBadge: {
    ...TYPOGRAPHY.caption,
    color: COLORS.success,
    fontWeight: '700',
  },
  cardContent: {
    gap: SPACING.sm,
  },
  fieldLabel: {
    ...TYPOGRAPHY.body,
    color: COLORS.textSecondary,
  },
  emptyText: {
    ...TYPOGRAPHY.body,
    color: COLORS.textTertiary,
    fontStyle: 'italic',
  },
  // Modal Styles
  modalSafeArea: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  keyboardAvoid: {
    flex: 1,
  },
  modalContainer: {
    flex: 1,
    paddingHorizontal: SPACING.lg,
    paddingTop: SPACING.lg,
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.xl,
  },
  closeButton: {
    fontSize: 24,
    color: COLORS.textSecondary,
    fontWeight: '600',
  },
  modalTitle: {
    ...TYPOGRAPHY.h2,
    color: COLORS.text,
  },
  section: {
    marginBottom: SPACING.xl,
  },
  label: {
    ...TYPOGRAPHY.bodyBold,
    color: COLORS.text,
    marginBottom: SPACING.md,
  },
  sliderContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    gap: SPACING.xs,
    flexWrap: 'wrap',
  },
  sliderButton: {
    width: '9%',
    aspectRatio: 1,
    borderRadius: BORDER_RADIUS.md,
    backgroundColor: COLORS.surfaceLight,
    justifyContent: 'center',
    alignItems: 'center',
  },
  sliderButtonActive: {
    backgroundColor: COLORS.info,
  },
  sliderButtonText: {
    ...TYPOGRAPHY.caption,
    color: COLORS.textSecondary,
    fontWeight: '600',
  },
  sliderButtonTextActive: {
    color: COLORS.white,
  },
  textInput: {
    backgroundColor: COLORS.surface,
    borderRadius: BORDER_RADIUS.md,
    borderWidth: 1,
    borderColor: COLORS.surfaceLight,
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.md,
    color: COLORS.text,
    marginBottom: SPACING.md,
    ...TYPOGRAPHY.body,
  },
  multilineInput: {
    minHeight: 80,
    textAlignVertical: 'top',
  },
  numberInput: {
    backgroundColor: COLORS.surface,
    borderRadius: BORDER_RADIUS.md,
    borderWidth: 1,
    borderColor: COLORS.surfaceLight,
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.md,
    color: COLORS.text,
    ...TYPOGRAPHY.body,
  },
  addButton: {
    paddingVertical: SPACING.md,
    alignItems: 'center',
    marginTop: SPACING.sm,
  },
  addButtonText: {
    ...TYPOGRAPHY.subtitle,
    color: COLORS.info,
    fontWeight: '600',
  },
  saveButton: {
    backgroundColor: COLORS.info,
    borderRadius: BORDER_RADIUS.lg,
    paddingVertical: SPACING.lg,
    alignItems: 'center',
    marginBottom: SPACING.lg,
  },
  saveButtonText: {
    ...TYPOGRAPHY.bodyBold,
    color: COLORS.white,
  },
});
