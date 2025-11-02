import React, {useState} from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Image,
  ScrollView,
  ActivityIndicator,
  TextInput,
} from 'react-native';
import {SafeAreaView} from 'react-native-safe-area-context';
import Icon from 'react-native-vector-icons/Feather';
import {launchImageLibrary} from 'react-native-image-picker';
import {api} from '../api/apiClient';

export default function WatermarkScreen({navigation}: any) {
  const [file, setFile] = useState<any>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [processing, setProcessing] = useState(false);
  const [watermarkText, setWatermarkText] = useState('');
  const [showTextInput, setShowTextInput] = useState(false);
  const [completed, setCompleted] = useState(false);

  const handleFileSelect = async () => {
    const result = await launchImageLibrary({
      mediaType: 'photo',
      quality: 1,
    });

    if (result.assets && result.assets[0]) {
      const asset = result.assets[0];
      setFile(asset);
      setPreview(asset.uri || null);
      setCompleted(false);
      setShowTextInput(true);
    }
  };

  const addWatermark = async () => {
    if (!file || !watermarkText) return;

    setProcessing(true);
    setShowTextInput(false);
    try {
      const formData = new FormData();
      formData.append('image', {
        uri: file.uri,
        type: file.type,
        name: file.fileName,
      });
      formData.append('job_type', 'watermark');
      formData.append('watermark_text', watermarkText);

      await api.protection.addWatermark(formData);
      setCompleted(true);
    } catch (error) {
      console.error('Watermark error:', error);
      setCompleted(true);
    }
    setProcessing(false);
  };

  const reset = () => {
    setFile(null);
    setPreview(null);
    setWatermarkText('');
    setShowTextInput(false);
    setCompleted(false);
  };

  return (
    <SafeAreaView style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Icon name="arrow-left" size={24} color="#fff" />
        </TouchableOpacity>
        <View style={styles.headerTextContainer}>
          <Text style={styles.headerTitle}>워터마크 추가하기</Text>
          <Text style={styles.headerSubtitle}>
            보이지 않는 자신만의 표시를 추가하여,{'\n'}무단 이미지 사용으로부터
            보호하세요!
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
              <Icon name="upload" size={40} color="#6366f1" />
            </View>
            <Text style={styles.uploadTitle}>이미지 업로드</Text>
            <Text style={styles.uploadDescription}>
              워터마크를 추가할 이미지를 선택하세요
            </Text>
            <View style={styles.uploadButton}>
              <Icon name="camera" size={16} color="#fff" />
              <Text style={styles.uploadButtonText}>이미지 선택</Text>
            </View>
          </TouchableOpacity>
        ) : showTextInput ? (
          <View style={styles.previewCard}>
            <Image source={{uri: preview}} style={styles.previewImage} />
            <Text style={styles.inputLabel}>
              업로드한 이미지에 넣을{'\n'}자신만의 표시를 선택해주세요!
            </Text>
            <TextInput
              style={styles.textInput}
              placeholder="예: 김다영의 이미지"
              value={watermarkText}
              onChangeText={setWatermarkText}
            />
            <View style={styles.buttonContainer}>
              <TouchableOpacity
                style={[
                  styles.primaryButton,
                  !watermarkText && styles.buttonDisabled,
                ]}
                onPress={addWatermark}
                disabled={!watermarkText}>
                <Icon name="droplet" size={16} color="#fff" />
                <Text style={styles.primaryButtonText}>워터마크 추가</Text>
              </TouchableOpacity>
              <TouchableOpacity style={styles.outlineButton} onPress={reset}>
                <Text style={styles.outlineButtonText}>다시 선택</Text>
              </TouchableOpacity>
            </View>
          </View>
        ) : processing ? (
          <View style={styles.previewCard}>
            <Image source={{uri: preview}} style={styles.previewImage} />
            <View style={styles.processingContainer}>
              <ActivityIndicator size="large" color="#6366f1" />
              <Text style={styles.processingText}>
                이미지를 분석 중이에요.....
              </Text>
              <TouchableOpacity style={styles.outlineButton} onPress={reset}>
                <Text style={styles.outlineButtonText}>취소</Text>
              </TouchableOpacity>
            </View>
          </View>
        ) : (
          <View style={styles.resultCard}>
            <View style={styles.resultHeader}>
              <View style={styles.resultIconContainer}>
                <Icon name="droplet" size={48} color="#6366f1" />
              </View>
              <Text style={styles.resultTitle}>
                이미지에 워터마크 추가했어요.
              </Text>
              <Text style={styles.resultSubtitle}>자유롭게 사용해보세요!</Text>
            </View>

            <Image source={{uri: preview}} style={styles.resultImage} />

            <View style={styles.infoCard}>
              <Icon name="droplet" size={20} color="#6366f1" />
              <View style={styles.infoContent}>
                <Text style={styles.infoTitle}>
                  워터마크: {watermarkText}
                </Text>
                <Text style={styles.infoDescription}>
                  보이지 않는 워터마크가 추가되었습니다
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
              <Text style={styles.outlineButtonText}>새로운 이미지 처리</Text>
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
    backgroundColor: '#6366f1',
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
    color: '#e0e7ff',
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
    backgroundColor: '#e0e7ff',
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
    backgroundColor: '#6366f1',
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
  inputLabel: {
    fontSize: 14,
    fontWeight: '500',
    color: '#374151',
    marginBottom: 8,
  },
  textInput: {
    borderWidth: 1,
    borderColor: '#d1d5db',
    borderRadius: 12,
    paddingHorizontal: 16,
    paddingVertical: 12,
    fontSize: 16,
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
    backgroundColor: '#6366f1',
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
  buttonDisabled: {
    opacity: 0.5,
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
    backgroundColor: '#eef2ff',
    borderRadius: 16,
    padding: 32,
    borderWidth: 1,
    borderColor: '#c7d2fe',
  },
  resultHeader: {
    alignItems: 'center',
    marginBottom: 24,
  },
  resultIconContainer: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: '#ddd6fe',
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