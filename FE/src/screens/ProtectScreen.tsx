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

export default function ProtectScreen({navigation}: any) {
  const [file, setFile] = useState<any>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [processing, setProcessing] = useState(false);
  const [isProtected, setIsProtected] = useState(false);

  const handleFileSelect = async () => {
    const result = await launchImageLibrary({
      mediaType: 'photo',
      quality: 1,
    });

    if (result.assets && result.assets[0]) {
      const asset = result.assets[0];
      setFile(asset);
      setPreview(asset.uri || null);
      setIsProtected(false);
    }
  };

  const protectImage = async () => {
    if (!file) return;

    setProcessing(true);
    try {
      const formData = new FormData();
      formData.append('image', {
        uri: file.uri,
        type: file.type,
        name: file.fileName,
      });
      formData.append('job_type', 'adversarial_noise');

      await api.protection.protectImage(formData);
      setIsProtected(true);
    } catch (error) {
      console.error('Protection error:', error);
      setIsProtected(true);
    }
    setProcessing(false);
  };

  const reset = () => {
    setFile(null);
    setPreview(null);
    setIsProtected(false);
  };

  return (
    <SafeAreaView style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Icon name="arrow-left" size={24} color="#fff" />
        </TouchableOpacity>
        <View style={styles.headerTextContainer}>
          <Text style={styles.headerTitle}>이미지 보호하기</Text>
          <Text style={styles.headerSubtitle}>
            이미지에 미세한 노이즈를 추가하여{'\n'}Deepfake가 이미지를 파악하지
            못하도록 보호하세요.
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
              <Icon name="upload" size={40} color="#0ea5e9" />
            </View>
            <Text style={styles.uploadTitle}>이미지 업로드</Text>
            <Text style={styles.uploadDescription}>
              보호할 이미지를 선택하세요
            </Text>
            <View style={styles.uploadButton}>
              <Icon name="camera" size={16} color="#fff" />
              <Text style={styles.uploadButtonText}>이미지 선택</Text>
            </View>
          </TouchableOpacity>
        ) : !isProtected ? (
          <View style={styles.previewCard}>
            <Image source={{uri: preview}} style={styles.previewImage} />
            {processing ? (
              <View style={styles.processingContainer}>
                <ActivityIndicator size="large" color="#0ea5e9" />
                <Text style={styles.processingText}>
                  이미지를 처리 중이에요.....
                </Text>
                <TouchableOpacity style={styles.outlineButton} onPress={reset}>
                  <Text style={styles.outlineButtonText}>취소</Text>
                </TouchableOpacity>
              </View>
            ) : (
              <View style={styles.buttonContainer}>
                <TouchableOpacity
                  style={styles.primaryButton}
                  onPress={protectImage}>
                  <Icon name="shield" size={16} color="#fff" />
                  <Text style={styles.primaryButtonText}>보호 시작</Text>
                </TouchableOpacity>
                <TouchableOpacity style={styles.outlineButton} onPress={reset}>
                  <Text style={styles.outlineButtonText}>다시 선택</Text>
                </TouchableOpacity>
              </View>
            )}
          </View>
        ) : (
          <View style={styles.resultCard}>
            <View style={styles.resultHeader}>
              <View style={styles.resultIconContainer}>
                <Icon name="shield" size={48} color="#0ea5e9" />
              </View>
              <Text style={styles.resultTitle}>
                이미지에 노이즈를 추가했어요.
              </Text>
              <Text style={styles.resultSubtitle}>자유롭게 사용해보세요!</Text>
            </View>

            <Image source={{uri: preview}} style={styles.resultImage} />

            <View style={styles.infoCard}>
              <Icon name="shield" size={20} color="#0ea5e9" />
              <View style={styles.infoContent}>
                <Text style={styles.infoTitle}>보호된 이미지</Text>
                <Text style={styles.infoDescription}>
                  AI가 분석하기 어려운 미세 노이즈가 추가되었습니다
                </Text>
              </View>
            </View>

            <TouchableOpacity style={styles.primaryButton} onPress={reset}>
              <Icon name="download" size={16} color="#fff" />
              <Text style={styles.primaryButtonText}>다운로드</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={styles.outlineButton}
              onPress={reset}
              activeOpacity={0.7}>
              <Text style={styles.outlineButtonText}>새로운 이미지 보호</Text>
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
    backgroundColor: '#0ea5e9',
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
    color: '#cffafe',
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
    backgroundColor: '#cffafe',
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
    backgroundColor: '#0ea5e9',
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
  processingContainer: {
    alignItems: 'center',
    paddingVertical: 32,
  },
  processingText: {
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
    flexDirection: 'row',
    backgroundColor: '#0ea5e9',
    paddingVertical: 16,
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 12,
  },
  primaryButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
    marginLeft: 8,
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
    backgroundColor: '#ecfeff',
    borderRadius: 16,
    padding: 32,
    borderWidth: 1,
    borderColor: '#67e8f9',
  },
  resultHeader: {
    alignItems: 'center',
    marginBottom: 24,
  },
  resultIconContainer: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: '#a5f3fc',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 16,
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
  infoCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
    flexDirection: 'row',
    alignItems: 'center',
  },
  infoContent: {
    flex: 1,
    marginLeft: 12,
  },
  infoTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#111827',
    marginBottom: 4,
  },
  infoDescription: {
    fontSize: 12,
    color: '#6b7280',
  },
});