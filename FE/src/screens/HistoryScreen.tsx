import React, {useState, useEffect} from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Image,
  ActivityIndicator,
} from 'react-native';
import {SafeAreaView} from 'react-native-safe-area-context';
import Icon from 'react-native-vector-icons/Feather';
import {api} from '../api/apiClient';
import BottomNav from '../components/BottomNav';

export default function HistoryScreen() {
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    setLoading(true);
    try {
      const data = await api.detection.getRecords();
      setHistory(data);
    } catch (error) {
      console.error('Failed to load history:', error);
      setHistory([]);
    }
    setLoading(false);
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('ko-KR', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <SafeAreaView style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>내 탐지 기록</Text>
        <Text style={styles.headerSubtitle}>
          지금까지 분석한 이미지 기록을 확인하세요
        </Text>
      </View>

      <ScrollView style={styles.content} contentContainerStyle={{paddingBottom: 80}}>
        {loading ? (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="large" color="#7c3aed" />
          </View>
        ) : history.length === 0 ? (
          <View style={styles.emptyCard}>
            <Icon name="clock" size={64} color="#d1d5db" />
            <Text style={styles.emptyTitle}>아직 탐지 기록이 없어요</Text>
            <Text style={styles.emptyDescription}>
              이미지를 분석하면 여기에 기록이 나타납니다
            </Text>
          </View>
        ) : (
          history.map((item, index) => {
            const isFake =
              item.analysis_result === 'deepfake' ||
              item.analysis_result === 'suspicious';
            return (
              <View
                key={item.record_id || index}
                style={[
                  styles.historyCard,
                  isFake ? styles.historyCardDanger : styles.historyCardSafe,
                ]}>
                <View style={styles.historyContent}>
                  {item.original_path && (
                    <Image
                      source={{uri: item.original_path}}
                      style={styles.historyImage}
                    />
                  )}
                  <View style={styles.historyInfo}>
                    <View style={styles.historyHeader}>
                      <Text style={styles.historyFileName} numberOfLines={1}>
                        {item.file_name || '이미지 분석'}
                      </Text>
                      <Icon
                        name={isFake ? 'x-circle' : 'check-circle'}
                        size={20}
                        color={isFake ? '#dc2626' : '#16a34a'}
                      />
                    </View>
                    <Text
                      style={[
                        styles.historyResult,
                        isFake ? styles.resultDanger : styles.resultSafe,
                      ]}>
                      {isFake ? '수상한 이미지' : '안전한 이미지'}
                    </Text>
                    <View style={styles.historyFooter}>
                      <Text style={styles.historyDate}>
                        {formatDate(item.created_at)}
                      </Text>
                      {item.confidence_score && (
                        <Text style={styles.historyConfidence}>
                          신뢰도 {Math.round(item.confidence_score)}%
                        </Text>
                      )}
                    </View>
                  </View>
                </View>
              </View>
            );
          })
        )}
      </ScrollView>

      <BottomNav />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f9fafb',
  },
  header: {
    backgroundColor: '#7c3aed',
    paddingHorizontal: 24,
    paddingTop: 24,
    paddingBottom: 32,
    borderBottomLeftRadius: 32,
    borderBottomRightRadius: 32,
  },
  headerTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 8,
  },
  headerSubtitle: {
    fontSize: 14,
    color: '#e9d5ff',
    lineHeight: 20,
  },
  content: {
    flex: 1,
    paddingHorizontal: 24,
    marginTop: -16,
  },
  loadingContainer: {
    paddingVertical: 48,
    alignItems: 'center',
  },
  emptyCard: {
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 48,
    alignItems: 'center',
    marginTop: 16,
  },
  emptyTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#111827',
    marginTop: 16,
    marginBottom: 8,
  },
  emptyDescription: {
    fontSize: 14,
    color: '#6b7280',
    textAlign: 'center',
  },
  historyCard: {
    borderRadius: 16,
    padding: 16,
    marginTop: 16,
    borderWidth: 1,
  },
  historyCardDanger: {
    backgroundColor: '#fee2e2',
    borderColor: '#fca5a5',
  },
  historyCardSafe: {
    backgroundColor: '#dcfce7',
    borderColor: '#86efac',
  },
  historyContent: {
    flexDirection: 'row',
    gap: 16,
  },
  historyImage: {
    width: 80,
    height: 80,
    borderRadius: 12,
  },
  historyInfo: {
    flex: 1,
  },
  historyHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 8,
  },
  historyFileName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#111827',
    flex: 1,
    marginRight: 8,
  },
  historyResult: {
    fontSize: 14,
    fontWeight: '600',
    marginBottom: 8,
  },
  resultDanger: {
    color: '#b91c1c',
  },
  resultSafe: {
    color: '#15803d',
  },
  historyFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  historyDate: {
    fontSize: 12,
    color: '#6b7280',
  },
  historyConfidence: {
    fontSize: 12,
    color: '#6b7280',
    fontWeight: '600',
  },
});