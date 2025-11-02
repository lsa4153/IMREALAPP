import React, {useState, useEffect} from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  TextInput,
  ActivityIndicator,
} from 'react-native';
import {SafeAreaView} from 'react-native-safe-area-context';
import Icon from 'react-native-vector-icons/Feather';
import {api} from '../api/apiClient';
import BottomNav from '../components/BottomNav';

export default function NewsScreen() {
  const [searchQuery, setSearchQuery] = useState('');
  const [news, setNews] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchNews();
  }, []);

  const fetchNews = async () => {
    setLoading(true);
    try {
      const articles = await api.news.getLatest();
      setNews(articles);
    } catch (error) {
      console.error('Failed to fetch news:', error);
      setNews([]);
    }
    setLoading(false);
  };

  const filteredNews = news.filter(
    article =>
      article.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      article.summary.toLowerCase().includes(searchQuery.toLowerCase()),
  );

  return (
    <SafeAreaView style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>딥페이크 알아보기</Text>
        <Text style={styles.headerSubtitle}>
          딥페이크 관련 최신 뉴스와 정보를 확인하세요
        </Text>

        <View style={styles.searchContainer}>
          <Icon
            name="search"
            size={20}
            color="#9ca3af"
            style={styles.searchIcon}
          />
          <TextInput
            style={styles.searchInput}
            placeholder="검색"
            placeholderTextColor="#9ca3af"
            value={searchQuery}
            onChangeText={setSearchQuery}
          />
        </View>
      </View>

      <ScrollView style={styles.content} contentContainerStyle={{paddingBottom: 80}}>
        <View style={styles.newsHeader}>
          <Text style={styles.newsHeaderTitle}>최신 뉴스</Text>
          <TouchableOpacity onPress={fetchNews}>
            <Text style={styles.viewAllButton}>View All</Text>
          </TouchableOpacity>
        </View>

        {loading ? (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="large" color="#0ea5e9" />
          </View>
        ) : filteredNews.length === 0 ? (
          <View style={styles.emptyCard}>
            <Text style={styles.emptyText}>검색 결과가 없습니다</Text>
          </View>
        ) : (
          filteredNews.map((article, index) => (
            <TouchableOpacity
              key={article.id}
              style={styles.newsCard}
              activeOpacity={0.7}>
              <View style={styles.newsCardHeader}>
                <Text style={styles.newsTitle} numberOfLines={2}>
                  {article.title}
                </Text>
                <Icon name="external-link" size={16} color="#9ca3af" />
              </View>
              <Text style={styles.newsSummary} numberOfLines={3}>
                {article.summary}
              </Text>
              <View style={styles.newsFooter}>
                <Text style={styles.newsDate}>{article.date}</Text>
                {article.category && (
                  <View style={styles.categoryBadge}>
                    <Text style={styles.categoryText}>{article.category}</Text>
                  </View>
                )}
              </View>
            </TouchableOpacity>
          ))
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
    backgroundColor: '#0ea5e9',
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
    color: '#cffafe',
    lineHeight: 20,
    marginBottom: 24,
  },
  searchContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    borderRadius: 12,
    paddingHorizontal: 16,
    paddingVertical: 12,
  },
  searchIcon: {
    marginRight: 12,
  },
  searchInput: {
    flex: 1,
    fontSize: 16,
    color: '#111827',
  },
  content: {
    flex: 1,
    paddingHorizontal: 24,
    marginTop: -16,
  },
  newsHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: 16,
    marginBottom: 16,
  },
  newsHeaderTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#111827',
  },
  viewAllButton: {
    fontSize: 14,
    color: '#0ea5e9',
    fontWeight: '600',
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
  },
  emptyText: {
    fontSize: 14,
    color: '#6b7280',
  },
  newsCard: {
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 20,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: {width: 0, height: 2},
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
  },
  newsCardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 12,
  },
  newsTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#111827',
    flex: 1,
    marginRight: 12,
    lineHeight: 22,
  },
  newsSummary: {
    fontSize: 14,
    color: '#6b7280',
    lineHeight: 20,
    marginBottom: 12,
  },
  newsFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  newsDate: {
    fontSize: 12,
    color: '#9ca3af',
  },
  categoryBadge: {
    backgroundColor: '#dbeafe',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
  },
  categoryText: {
    fontSize: 12,
    color: '#1e40af',
    fontWeight: '600',
  },
});