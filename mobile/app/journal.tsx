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
  Alert,
} from 'react-native';
import { StorageService } from '@/services';
import { JournalEntry } from '@/types';
import { COLORS, SPACING, TYPOGRAPHY, BORDER_RADIUS, SHADOWS } from '@/constants/theme';
import { v4 as uuidv4 } from 'uuid';

export default function JournalScreen() {
  const [entries, setEntries] = useState<JournalEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [showNewModal, setShowNewModal] = useState(false);
  const [selectedEntry, setSelectedEntry] = useState<JournalEntry | null>(null);
  const [showViewModal, setShowViewModal] = useState(false);

  // New entry state
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [mood, setMood] = useState(5);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    loadEntries();
  }, []);

  const loadEntries = async () => {
    try {
      setLoading(true);
      const journalEntries = await StorageService.getJournalEntries();
      setEntries(journalEntries.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()));
    } catch (error) {
      console.error('Failed to load journal entries:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveEntry = async () => {
    if (!title.trim() || !content.trim()) {
      Alert.alert('Error', 'Please fill in both title and content');
      return;
    }

    try {
      setSaving(true);
      const newEntry: JournalEntry = {
        id: uuidv4(),
        date: new Date().toISOString().split('T')[0],
        timestamp: new Date().toISOString(),
        title,
        content,
        tags: [],
        mood,
      };

      await StorageService.addJournalEntry(newEntry);
      setTitle('');
      setContent('');
      setMood(5);
      setShowNewModal(false);
      await loadEntries();
    } catch (error) {
      Alert.alert('Error', 'Failed to save journal entry');
      console.error('Failed to save entry:', error);
    } finally {
      setSaving(false);
    }
  };

  const handleDeleteEntry = async (id: string) => {
    Alert.alert('Delete Entry?', 'This action cannot be undone.', [
      { text: 'Cancel', style: 'cancel' },
      {
        text: 'Delete',
        onPress: async () => {
          try {
            await StorageService.deleteJournalEntry(id);
            await loadEntries();
            setShowViewModal(false);
          } catch (error) {
            Alert.alert('Error', 'Failed to delete entry');
            console.error('Failed to delete entry:', error);
          }
        },
        style: 'destructive',
      },
    ]);
  };

  const getMoodEmoji = (mood: number): string => {
    if (mood <= 2) return '😢';
    if (mood <= 4) return '😞';
    if (mood <= 6) return '😐';
    if (mood <= 8) return '🙂';
    return '😊';
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color={COLORS.info} />
      </View>
    );
  }

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView style={styles.container} showsVerticalScrollIndicator={false}>
        {entries.length === 0 ? (
          <View style={styles.emptyContainer}>
            <Text style={styles.emptyIcon}>📔</Text>
            <Text style={styles.emptyTitle}>No Journal Entries Yet</Text>
            <Text style={styles.emptyText}>Start writing to track your thoughts and progress</Text>
          </View>
        ) : (
          <View style={styles.entriesList}>
            {entries.map(entry => (
              <TouchableOpacity
                key={entry.id}
                style={styles.entryCard}
                onPress={() => {
                  setSelectedEntry(entry);
                  setShowViewModal(true);
                }}
              >
                <View style={styles.entryHeader}>
                  <View style={styles.entryMeta}>
                    <Text style={styles.entryMood}>{getMoodEmoji(entry.mood)}</Text>
                    <View style={styles.entryInfo}>
                      <Text style={styles.entryTitle}>{entry.title}</Text>
                      <Text style={styles.entryDate}>
                        {new Date(entry.timestamp).toLocaleDateString('en-US', {
                          month: 'short',
                          day: 'numeric',
                          year: 'numeric',
                        })}
                      </Text>
                    </View>
                  </View>
                  <Text style={styles.moodNumber}>{entry.mood}/10</Text>
                </View>
                <Text style={styles.entryPreview} numberOfLines={2}>
                  {entry.content}
                </Text>
              </TouchableOpacity>
            ))}
          </View>
        )}

        <View style={{ height: SPACING.xl }} />
      </ScrollView>

      {/* New Entry Button */}
      <TouchableOpacity
        style={styles.fab}
        onPress={() => setShowNewModal(true)}
      >
        <Text style={styles.fabText}>+</Text>
      </TouchableOpacity>

      {/* New Entry Modal */}
      <Modal
        visible={showNewModal}
        animationType="slide"
        onRequestClose={() => setShowNewModal(false)}
      >
        <SafeAreaView style={styles.modalSafeArea}>
          <KeyboardAvoidingView
            behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
            style={styles.keyboardAvoid}
          >
            <ScrollView style={styles.modalContainer} showsVerticalScrollIndicator={false}>
              <View style={styles.modalHeader}>
                <TouchableOpacity onPress={() => setShowNewModal(false)}>
                  <Text style={styles.closeButton}>✕</Text>
                </TouchableOpacity>
                <Text style={styles.modalTitle}>New Journal Entry</Text>
                <View style={{ width: 40 }} />
              </View>

              {/* Title */}
              <View style={styles.section}>
                <Text style={styles.label}>Title</Text>
                <TextInput
                  style={styles.textInput}
                  placeholder="Entry title..."
                  placeholderTextColor={COLORS.textTertiary}
                  value={title}
                  onChangeText={setTitle}
                />
              </View>

              {/* Mood */}
              <View style={styles.section}>
                <Text style={styles.label}>How are you feeling? {getMoodEmoji(mood)}</Text>
                <View style={styles.sliderContainer}>
                  {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(value => (
                    <TouchableOpacity
                      key={value}
                      style={[
                        styles.sliderButton,
                        mood === value && styles.sliderButtonActive,
                      ]}
                      onPress={() => setMood(value)}
                    >
                      <Text
                        style={[
                          styles.sliderButtonText,
                          mood === value && styles.sliderButtonTextActive,
                        ]}
                      >
                        {value}
                      </Text>
                    </TouchableOpacity>
                  ))}
                </View>
              </View>

              {/* Content */}
              <View style={styles.section}>
                <Text style={styles.label}>Your Thoughts</Text>
                <TextInput
                  style={[styles.textInput, styles.multilineInput]}
                  placeholder="Write your thoughts here..."
                  placeholderTextColor={COLORS.textTertiary}
                  value={content}
                  onChangeText={setContent}
                  multiline
                  numberOfLines={10}
                />
              </View>

              {/* Save Button */}
              <TouchableOpacity
                style={styles.saveButton}
                onPress={handleSaveEntry}
                disabled={saving}
              >
                {saving ? (
                  <ActivityIndicator color={COLORS.white} />
                ) : (
                  <Text style={styles.saveButtonText}>Save Entry</Text>
                )}
              </TouchableOpacity>

              <View style={{ height: SPACING.xl }} />
            </ScrollView>
          </KeyboardAvoidingView>
        </SafeAreaView>
      </Modal>

      {/* View Entry Modal */}
      <Modal
        visible={showViewModal}
        animationType="slide"
        onRequestClose={() => setShowViewModal(false)}
      >
        <SafeAreaView style={styles.modalSafeArea}>
          <ScrollView style={styles.modalContainer} showsVerticalScrollIndicator={false}>
            {selectedEntry && (
              <>
                <View style={styles.modalHeader}>
                  <TouchableOpacity onPress={() => setShowViewModal(false)}>
                    <Text style={styles.closeButton}>✕</Text>
                  </TouchableOpacity>
                  <Text style={styles.modalTitle}>Journal Entry</Text>
                  <TouchableOpacity onPress={() => handleDeleteEntry(selectedEntry.id)}>
                    <Text style={styles.deleteButton}>🗑️</Text>
                  </TouchableOpacity>
                </View>

                <View style={styles.section}>
                  <Text style={styles.viewTitle}>{selectedEntry.title}</Text>
                  <View style={styles.viewMeta}>
                    <Text style={styles.viewMood}>{getMoodEmoji(selectedEntry.mood)} {selectedEntry.mood}/10</Text>
                    <Text style={styles.viewDate}>
                      {new Date(selectedEntry.timestamp).toLocaleDateString('en-US', {
                        weekday: 'long',
                        month: 'long',
                        day: 'numeric',
                        year: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit',
                      })}
                    </Text>
                  </View>
                  <Text style={styles.viewContent}>{selectedEntry.content}</Text>
                </View>
              </>
            )}
          </ScrollView>
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
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: SPACING.xxl,
  },
  emptyIcon: {
    fontSize: 64,
    marginBottom: SPACING.lg,
  },
  emptyTitle: {
    ...TYPOGRAPHY.h2,
    color: COLORS.text,
    marginBottom: SPACING.md,
    textAlign: 'center',
  },
  emptyText: {
    ...TYPOGRAPHY.body,
    color: COLORS.textSecondary,
    textAlign: 'center',
  },
  entriesList: {
    gap: SPACING.md,
  },
  entryCard: {
    backgroundColor: COLORS.surface,
    borderRadius: BORDER_RADIUS.lg,
    paddingHorizontal: SPACING.lg,
    paddingVertical: SPACING.lg,
    ...SHADOWS.sm,
  },
  entryHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: SPACING.md,
  },
  entryMeta: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
    gap: SPACING.md,
  },
  entryMood: {
    fontSize: 28,
  },
  entryInfo: {
    flex: 1,
  },
  entryTitle: {
    ...TYPOGRAPHY.bodyBold,
    color: COLORS.text,
    marginBottom: SPACING.xs,
  },
  entryDate: {
    ...TYPOGRAPHY.caption,
    color: COLORS.textSecondary,
  },
  moodNumber: {
    ...TYPOGRAPHY.bodyBold,
    color: COLORS.info,
  },
  entryPreview: {
    ...TYPOGRAPHY.body,
    color: COLORS.textSecondary,
    lineHeight: 20,
  },
  fab: {
    position: 'absolute',
    bottom: SPACING.xl,
    right: SPACING.xl,
    width: 60,
    height: 60,
    borderRadius: BORDER_RADIUS.full,
    backgroundColor: COLORS.info,
    justifyContent: 'center',
    alignItems: 'center',
    ...SHADOWS.lg,
  },
  fabText: {
    fontSize: 32,
    color: COLORS.white,
    fontWeight: '300',
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
  deleteButton: {
    fontSize: 20,
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
  textInput: {
    backgroundColor: COLORS.surface,
    borderRadius: BORDER_RADIUS.md,
    borderWidth: 1,
    borderColor: COLORS.surfaceLight,
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.md,
    color: COLORS.text,
    ...TYPOGRAPHY.body,
  },
  multilineInput: {
    minHeight: 150,
    textAlignVertical: 'top',
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
  viewTitle: {
    ...TYPOGRAPHY.h2,
    color: COLORS.text,
    marginBottom: SPACING.md,
  },
  viewMeta: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: SPACING.lg,
    marginBottom: SPACING.xl,
    paddingBottom: SPACING.lg,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.surfaceLight,
  },
  viewMood: {
    ...TYPOGRAPHY.bodyBold,
    color: COLORS.info,
  },
  viewDate: {
    ...TYPOGRAPHY.body,
    color: COLORS.textSecondary,
  },
  viewContent: {
    ...TYPOGRAPHY.body,
    color: COLORS.text,
    lineHeight: 24,
  },
});
