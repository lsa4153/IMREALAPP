import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

// 백엔드 URL - IMREALApp/BE 사용
const USE_MOCK_API = true; // false로 변경하면 실제 BE 사용
const API_BASE_URL = 'http://127.0.0.1:8000'; // Django 백엔드 주소

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  async config => {
    const token = await AsyncStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  },
);

// Response interceptor
apiClient.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 401) {
      await AsyncStorage.removeItem('auth_token');
    }
    return Promise.reject(error);
  },
);

// Mock API
const mockDelay = (ms = 1000) =>
  new Promise<void>(resolve => setTimeout(resolve, ms));

const mockAPI = {
  users: {
    getProfile: async () => {
      await mockDelay(500);
      return {
        user_id: 1,
        nickname: '테스트유저',
        email: 'test@example.com',
      };
    },
  },
  detection: {
    analyzeImage: async (formData: any) => {
      await mockDelay(1500);
      const isFake = Math.random() > 0.5;
      const confidence = Math.floor(Math.random() * 40) + (isFake ? 60 : 20);

      const record = {
        record_id: Date.now(),
        analysis_type: 'image',
        analysis_result: isFake ? 'deepfake' : 'safe',
        confidence_score: confidence,
        created_at: new Date().toISOString(),
        file_name: 'test_image.jpg',
      };

      // 로컬 저장
      const history = await AsyncStorage.getItem('detection_history');
      const historyArray = history ? JSON.parse(history) : [];
      historyArray.unshift(record);
      await AsyncStorage.setItem('detection_history', JSON.stringify(historyArray));

      return record;
    },
    getRecords: async () => {
      await mockDelay(500);
      const history = await AsyncStorage.getItem('detection_history');
      return history ? JSON.parse(history) : [];
    },
  },
  protection: {
    protectImage: async (formData: any) => {
      await mockDelay(2000);
      return {
        job_id: Date.now(),
        job_type: 'adversarial_noise',
        job_status: 'completed',
      };
    },
    addWatermark: async (formData: any) => {
      await mockDelay(2000);
      return {
        job_id: Date.now(),
        job_type: 'watermark',
        job_status: 'completed',
      };
    },
  },
  news: {
    getLatest: async () => {
      await mockDelay(800);
      return [
        {
          id: 1,
          title: '딥페이크 기술, 2025년 급속 발전 예상',
          summary:
            'AI 기술의 발전으로 딥페이크 탐지가 더욱 중요해지고 있습니다. 전문가들은 새로운 보안 기술의 필요성을 강조하고 있습니다.',
          date: '2025.01.15',
          category: '기술',
        },
        {
          id: 2,
          title: '정부, 딥페이크 범죄 강력 대응 방침',
          summary:
            '최근 딥페이크를 이용한 범죄가 증가함에 따라 정부가 강력한 처벌 규정을 마련하고 있습니다.',
          date: '2025.01.12',
          category: '사회',
        },
        {
          id: 3,
          title: 'AI 기반 딥페이크 탐지 기술 개발',
          summary:
            '국내 연구팀이 99% 정확도의 딥페이크 탐지 알고리즘을 개발해 주목받고 있습니다.',
          date: '2025.01.10',
          category: '과학',
        },
      ];
    },
  },
};

// Real API (BE 연결용)
const realAPI = {
  users: {
    getProfile: async () => {
      const res = await apiClient.get('/api/users/profile/');
      return res.data;
    },
  },
  detection: {
    analyzeImage: async (formData: FormData) => {
      const res = await apiClient.post('/api/detection/image/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      return res.data;
    },
    getRecords: async () => {
      const res = await apiClient.get('/api/detection/records/');
      return res.data;
    },
  },
  protection: {
    protectImage: async (formData: FormData) => {
      const res = await apiClient.post('/api/protection/jobs/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      return res.data;
    },
    addWatermark: async (formData: FormData) => {
      const res = await apiClient.post('/api/protection/jobs/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      return res.data;
    },
  },
  news: {
    getLatest: async () => {
      const res = await apiClient.get('/api/news/');
      return res.data;
    },
  },
};

export const api = USE_MOCK_API ? mockAPI : realAPI;
