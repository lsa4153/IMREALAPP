import React, {useState, useEffect} from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  Dimensions,
} from 'react-native';
import {SafeAreaView} from 'react-native-safe-area-context';
import Icon from 'react-native-vector-icons/Feather';
import {api} from '../api/apiClient';
import BottomNav from '../components/BottomNav';

const {width} = Dimensions.get('window');

export default function HomeScreen({navigation}: any) {
  const [user, setUser] = useState<any>(null);
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    loadUser();
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const loadUser = async () => {
    try {
      const userData = await api.users.getProfile();
      setUser(userData);
    } catch (error) {
      console.log('User not logged in');
    }
  };

  const features = [
    {
      title: 'Deepfake 탐지',
      description: '이미지로부터\n탐지',
      icon: 'search',
      gradient: ['#a855f7', '#6366f1'],
      screen: 'Detect',
    },
    {
      title: '이미지 보호',
      description: 'AI로부터\n정보 보호',
      icon: 'shield',
      gradient: ['#3b82f6', '#06b6d4'],
      screen: 'Protect',
    },
    {
      title: '워터마크 추가하기',
      description: '보이지 않는\n워터마크',
      icon: 'droplet',
      gradient: ['#6366f1', '#a855f7'],
      screen: 'Watermark',
    },
    {
      title: '딥페이크 알아보기',
      description: '딥페이크\n최신 뉴스',
      icon: 'file-text',
      gradient: ['#06b6d4', '#3b82f6'],
      screen: 'News',
    },
  ];

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString('ko-KR', {
      hour: '2-digit',
      minute: '2-digit',
      hour12: false,
    });
  };

  return (
    <SafeAreaView style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <View style={styles.headerContent}>
          <View>
            <Text style={styles.welcomeText}>Welcome Home,</Text>
            <Text style={styles.nameText}>
              {user?.nickname || 'Guest'} 님
            </Text>
          </View>
          <View>
            <Text style={styles.timeText}>{formatTime(currentTime)}</Text>
          </View>
        </View>
        <Text style={styles.titleText}>
          딥페이크로부터{'\n'}보호하세요
        </Text>
      </View>

      <ScrollView style={styles.content} contentContainerStyle={{paddingBottom: 80}}>
        {/* Feature Cards */}
        <View style={styles.gridContainer}>
          {features.map((feature, index) => (
            <TouchableOpacity
              key={index}
              style={styles.card}
              onPress={() => navigation.navigate(feature.screen)}
              activeOpacity={0.7}>
              <View
                style={[
                  styles.iconContainer,
                  {backgroundColor: feature.gradient[0]},
                ]}>
                <Icon name={feature.icon} size={24} color="#fff" />
              </View>
              <Text style={styles.cardTitle}>{feature.title}</Text>
              <Text style={styles.cardDescription}>{feature.description}</Text>
            </TouchableOpacity>
          ))}
        </View>

        {/* Info Card */}
        <View style={styles.infoCard}>
          <View style={styles.infoIconContainer}>
            <Icon name="alert-circle" size={20} color="#d97706" />
          </View>
          <View style={styles.infoContent}>
            <Text style={styles.infoTitle}>딥페이크란?</Text>
            <Text style={styles.infoDescription}>
              인공지능을 이용해 사람의 얼굴이나 목소리를 조작한 가짜 콘텐츠입니다.
              IMReal로 여러분의 이미지를 보호하세요.
            </Text>
          </View>
        </View>
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
  headerContent: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 24,
  },
  welcomeText: {
    fontSize: 14,
    color: '#e9d5ff',
  },
  nameText: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
    marginTop: 4,
  },
  timeText: {
    fontSize: 32,
    fontWeight: '300',
    color: '#fff',
  },
  titleText: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#fff',
    lineHeight: 36,
  },
  content: {
    flex: 1,
    paddingHorizontal: 24,
    marginTop: -16,
  },
  gridContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    marginBottom: 24,
  },
  card: {
    width: (width - 64) / 2,
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
  iconContainer: {
    width: 48,
    height: 48,
    borderRadius: 16,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 16,
  },
  cardTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#111827',
    marginBottom: 8,
  },
  cardDescription: {
    fontSize: 14,
    color: '#6b7280',
    lineHeight: 20,
  },
  infoCard: {
    backgroundColor: '#fef3c7',
    borderRadius: 16,
    padding: 16,
    flexDirection: 'row',
    borderWidth: 1,
    borderColor: '#fcd34d',
    marginBottom: 24,
  },
  infoIconContainer: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: '#fde68a',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  infoContent: {
    flex: 1,
  },
  infoTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#111827',
    marginBottom: 4,
  },
  infoDescription: {
    fontSize: 14,
    color: '#4b5563',
    lineHeight: 20,
  },
});