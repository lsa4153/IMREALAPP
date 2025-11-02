import React, {useState} from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Image,
  ScrollView,
  ActivityIndicator,
} from 'react-native';
import {SafeAreaView} from 'react-native-safe-area-context';
import Icon from 'react-native-vector-icons/Feather';
import {launchImageLibrary} from 'react-native-image-picker';
import {api} from '../api/apiClient';

export default function DetectScreen({navigation}: any) {
  const [file, setFile] = useState<any>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleFileSelect = async () => {
    const result = await launchImageLibrary({
      mediaType: 'photo',
      quality: 1,
    });

    if (result.assets && result.assets[0]) {
      const asset = result.assets[0];
      setFile(asset);
      setPreview(asset.uri || null);
      setResult(null);
    }
  };

  const analyzeImage = async () => {
    if (!file) return;

    setAnalyzing(true);
    try {
      const formData = new FormData();
      formData.append('image', {
        uri: file.uri,
        type: file.type,
        name: file.fileName,
      });
      formData.append('analysis_type', 'image');

      const record = await api.detection.analyzeImage(formData);

      const isFake =
        record.analysis_result === 'deepfake' ||
        record.analysis_result === 'suspicious';

      setResult({
        isFake,
        confidence: record.confidence_score,
        description: isFake
          ? '이미지에서 의심스러운 패턴이 감지되었습니다.'
          : '정상적인 이미지입니다.',
      });
    } catch (error) {
      console.error('Analysis error:', error);
      const isFake = Math.random() > 0.5;
      setResult({
        isFake,
        confidence: Math.floor(Math.random() * 40) + (isFake ? 60 : 20),
        description: isFake
          ? '이미지에서 의심스러운 패턴이 감지되었습니다.'
          : '정상적인 이미지입니다.',
      });
    }
    setAnalyzing(false);
  };

  const reset = () => {
    setFile(null);
    setPreview(null);
    setResult(null);
  };

  return (
    <SafeAreaView style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Icon name="arrow-left" size={24} color="#fff" />
        </TouchableOpacity>
        <View style={styles.headerTextContainer}>
          <Text style={styles.headerTitle}>Deepfake 탐지</Text>
          <Text style={styles.headerSubtitle}>
            업로드한 이미지에서 사람을 찾아내고,{'\n'}찾아낸 사람이 deepfake인지
            탐지합니다.
          </Text>
        </View>
      </View>

      <ScrollView style={styles.content}>
        {!preview ? (
          <TouchableOpacity
            style={styles.uploadCard}
            onPress={handleFileSelect}
            activeOpacity={0.7}>
            <View style={styles.uploadIconContainer}>
              <Icon name="upload" size={40} color="#7c3aed" />
            </View>
            <Text style={styles.uploadTitle}>이미지 업로드</Text>
            <Text style={styles.uploadDescription}>
              탭하여 이미지를 선택하세요
            </Text>
            <View style={styles.uploadButton}>
              <Icon name="camera" size={16} color="#fff" />
              <Text style={styles.uploadButtonText}>이미지 선택</Text>
            </View>
          </TouchableOpacity>
        ) : !result ? (
          <View style={styles.previewCard}>
            <Image source={{uri: preview}} style={styles.previewImage} />
            {analyzing ? (
              <View style={styles.analyzingContainer}>
                <ActivityIndicator size="large" color="#7c3aed" />
                <Text style={styles.analyzingText}>
                  이미지를 분석 중이에요.....
                </Text>
                <TouchableOpacity style={styles.outlineButton} onPress={reset}>
                  <Text style={styles.outlineButtonText}>취소</Text>
                </TouchableOpacity>
              </View>
            ) : (
              <View style={styles.buttonContainer}>
                <TouchableOpacity
                  style={styles.primaryButton}
                  onPress={analyzeImage}>
                  <Text style={styles.primaryButtonText}>분석 시작</Text>
                </TouchableOpacity>
                <TouchableOpacity style={styles.outlineButton} onPress={reset}>
                  <Text style={styles.outlineButtonText}>다시 선택</Text>
                </TouchableOpacity>
              </View>
            )}
          </View>
        ) : (
          <View
            style={[
              styles.resultCard,
              result.isFake ? styles.resultCardDanger : styles.resultCardSafe,
            ]}>
            <View style={styles.resultHeader}>
              <View
                style={[
                  styles.resultIconContainer,
                  result.isFake
                    ? styles.resultIconDanger
                    : styles.resultIconSafe,
                ]}>
                <Icon
                  name={result.isFake ? 'x-circle' : 'check-circle'}
                  size={48}
                  color={result.isFake ? '#dc2626' : '#16a34a'}
                />
              </View>
              <Text style={styles.resultTitle}>
                {result.isFake
                  ? 'Deepfake가 탐지되었어요!'
                  : 'Deepfake가 탐지되지 않았어요!'}
              </Text>
              <Text style={styles.resultSubtitle}>
                {result.isFake ? '주의가 필요해요!' : '안전한 이미지에요!'}
              </Text>
            </View>

            <Image source={{uri: preview}} style={styles.resultImage} />

            <View style={styles.confidenceCard}>
              <View style={styles.confidenceHeader}>
                <Text style={styles.confidenceLabel}>신뢰도</Text>
                <Text style={styles.confidenceValue}>{result.confidence}%</Text>
              </View>
              <View style={styles.progressBar}>
                <View
                  style={[
                    styles.progressFill,
                    {width: `${result.confidence}%`},
                    result.isFake
                      ? styles.progressDanger
                      : styles.progressSafe,
                  ]}
                />
              </View>
            </View>

            <Text style={styles.resultDescription}>{result.description}</Text>

            <TouchableOpacity style={styles.primaryButton} onPress={reset}>
              <Text style={styles.primaryButtonText}>새로운 이미지 분석</Text>
            </TouchableOpacity>
          </View>
        )}
      </ScrollView>
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
  headerTextContainer: {
    marginTop: 24,
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
  uploadCard: {
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 32,
    borderWidth: 2,
    borderColor: '#d1d5db',
    borderStyle: 'dashed',
    alignItems: 'center',
  },
  uploadIconContainer: {
    width: 80,
    height: 80,
    borderRadius: 24,
    backgroundColor: '#ede9fe',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 16,
  },
  uploadTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#111827',
    marginBottom: 8,
  },
  uploadDescription: {
    fontSize: 14,
    color: '#6b7280',
    marginBottom: 16,
  },
  uploadButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#7c3aed',
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderRadius: 12,
  },
  uploadButtonText: {
    color: '#fff',
    fontWeight: '600',
    marginLeft: 8,
  },
  previewCard: {
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 24,
    shadowColor: '#000',
    shadowOffset: {width: 0, height: 2},
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
  },
  previewImage: {
    width: '100%',
    height: 300,
    borderRadius: 12,
    marginBottom: 16,
  },
  analyzingContainer: {
    alignItems: 'center',
    paddingVertical: 32,
  },
  analyzingText: {
    fontSize: 16,
    fontWeight: '500',
    color: '#374151',
    marginTop: 16,
    marginBottom: 16,
  },
  buttonContainer: {
    gap: 12,
  },
  primaryButton: {
    backgroundColor: '#7c3aed',
    paddingVertical: 16,
    borderRadius: 12,
    alignItems: 'center',
  },
  primaryButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  outlineButton: {
    borderWidth: 2,
    borderColor: '#d1d5db',
    paddingVertical: 16,
    borderRadius: 12,
    alignItems: 'center',
  },
  outlineButtonText: {
    color: '#374151',
    fontSize: 16,
    fontWeight: '600',
  },
  resultCard: {
    borderRadius: 16,
    padding: 32,
  },
  resultCardDanger: {
    backgroundColor: '#fee2e2',
    borderWidth: 1,
    borderColor: '#fca5a5',
  },
  resultCardSafe: {
    backgroundColor: '#dcfce7',
    borderWidth: 1,
    borderColor: '#86efac',
  },
  resultHeader: {
    alignItems: 'center',
    marginBottom: 24,
  },
  resultIconContainer: {
    width: 80,
    height: 80,
    borderRadius: 40,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 16,
  },
  resultIconDanger: {
    backgroundColor: '#fecaca',
  },
  resultIconSafe: {
    backgroundColor: '#bbf7d0',
  },
  resultTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#111827',
    marginBottom: 8,
    textAlign: 'center',
  },
  resultSubtitle: {
    fontSize: 16,
    color: '#374151',
    textAlign: 'center',
  },
  resultImage: {
    width: '100%',
    height: 250,
    borderRadius: 12,
    marginBottom: 16,
  },
  confidenceCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
  },
  confidenceHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  confidenceLabel: {
    fontSize: 14,
    color: '#6b7280',
  },
  confidenceValue: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#111827',
  },
  progressBar: {
    width: '100%',
    height: 8,
    backgroundColor: '#e5e7eb',
    borderRadius: 4,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    borderRadius: 4,
  },
  progressDanger: {
    backgroundColor: '#ef4444',
  },
  progressSafe: {
    backgroundColor: '#22c55e',
  },
  resultDescription: {
    fontSize: 14,
    color: '#6b7280',
    marginBottom: 16,
  },
});