import requests
import time
from django.conf import settings
from media_files.models import SystemLog


class AIModelService:
    """AI 모델 서비스 (FastAPI 연동)"""
    
    def __init__(self):
        self.fastapi_url = settings.FASTAPI_URL
        self.timeout = settings.AI_REQUEST_TIMEOUT
    
    def analyze_image(self, image_path):
        """
        이미지 딥페이크 분석
        
        Args:
            image_path: 이미지 파일의 절대 경로
        """
        
        start_time = time.time()
        
        # 🔧 AI 서버 연결 확인
        if not self.check_health():
            print("⚠️ AI 서버 없음 - Mock 데이터 반환")
            return self._get_mock_image_response(start_time)
        
        # 실제 AI 서버 호출
        try:
            with open(image_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(
                    f"{self.fastapi_url}/api/analyze/image",
                    files=files,
                    timeout=self.timeout
                )
            
            response.raise_for_status()
            result = response.json()
            
            processing_time = int((time.time() - start_time) * 1000)
            
            return {
                'success': True,
                'is_deepfake': result.get('is_deepfake', False),
                'confidence_score': result.get('confidence', 0.0),
                'analysis_result': self._get_analysis_result(
                    result.get('is_deepfake', False),
                    result.get('confidence', 0.0)
                ),
                'face_count': result.get('face_count', 0),
                'face_coordinates': result.get('face_coordinates', []),
                'face_quality_scores': result.get('face_quality_scores', []),
                'ai_model_version': result.get('model_version', 'v1.0'),
                'processing_time': processing_time
            }
        
        except requests.exceptions.RequestException as e:
            SystemLog.objects.create(
                log_level='error',
                log_category='detection',
                message=f'AI 모델 분석 실패: {str(e)}',
                error_code='AI_API_ERROR'
            )
            
            return {
                'success': False,
                'error': 'AI 분석 중 오류가 발생했습니다. 다시 시도해주세요.',
                'processing_time': int((time.time() - start_time) * 1000)
            }
    
    def analyze_video(self, video_path):
        """
        영상 딥페이크 분석
        
        Args:
            video_path: 영상 파일의 절대 경로
        """
        
        start_time = time.time()
        
        # 🔧 AI 서버 연결 확인
        if not self.check_health():
            print("⚠️ AI 서버 없음 - Mock 데이터 반환")
            return self._get_mock_video_response(start_time)
        
        # 실제 AI 서버 호출
        try:
            with open(video_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(
                    f"{self.fastapi_url}/api/analyze/video",
                    files=files,
                    timeout=self.timeout
                )
            
            response.raise_for_status()
            result = response.json()
            
            processing_time = int((time.time() - start_time) * 1000)
            
            return {
                'success': True,
                'is_deepfake': result.get('is_deepfake', False),
                'confidence_score': result.get('confidence', 0.0),
                'analysis_result': self._get_analysis_result(
                    result.get('is_deepfake', False),
                    result.get('confidence', 0.0)
                ),
                'frame_count': result.get('frame_count', 0),
                'suspicious_frames': result.get('suspicious_frames', []),
                'ai_model_version': result.get('model_version', 'v1.0'),
                'processing_time': processing_time
            }
        
        except requests.exceptions.RequestException as e:
            SystemLog.objects.create(
                log_level='error',
                log_category='detection',
                message=f'영상 AI 분석 실패: {str(e)}',
                error_code='AI_API_ERROR'
            )
            
            return {
                'success': False,
                'error': 'AI 분석 중 오류가 발생했습니다. 다시 시도해주세요.',
                'processing_time': int((time.time() - start_time) * 1000)
            }
    
    def _get_mock_image_response(self, start_time):
        """
        🔧 Mock 이미지 분석 응답 (AI 서버 없을 때)
        """
        import random
        
        processing_time = int((time.time() - start_time) * 1000)
        
        # 랜덤으로 결과 생성 (테스트용)
        is_deepfake = random.choice([True, False, False, False])  # 25% 확률로 딥페이크
        confidence = random.uniform(75.0, 99.0)
        
        return {
            'success': True,
            'is_deepfake': is_deepfake,
            'confidence_score': round(confidence, 2),
            'analysis_result': self._get_analysis_result(is_deepfake, confidence),
            'face_count': random.randint(1, 3),
            'face_coordinates': [
                {
                    'x': random.randint(50, 200),
                    'y': random.randint(50, 200),
                    'width': random.randint(150, 300),
                    'height': random.randint(150, 300)
                }
            ],
            'face_quality_scores': [
                {'face_id': 1, 'quality': round(random.uniform(0.8, 0.99), 2)}
            ],
            'ai_model_version': 'v1.0-mock',
            'processing_time': processing_time
        }
    
    def _get_mock_video_response(self, start_time):
        """
        🔧 Mock 영상 분석 응답 (AI 서버 없을 때)
        """
        import random
        
        processing_time = int((time.time() - start_time) * 1000)
        
        is_deepfake = random.choice([True, False, False, False])
        confidence = random.uniform(75.0, 99.0)
        frame_count = random.randint(100, 500)
        
        return {
            'success': True,
            'is_deepfake': is_deepfake,
            'confidence_score': round(confidence, 2),
            'analysis_result': self._get_analysis_result(is_deepfake, confidence),
            'frame_count': frame_count,
            'suspicious_frames': [
                random.randint(1, frame_count) for _ in range(3)
            ] if is_deepfake else [],
            'ai_model_version': 'v1.0-mock',
            'processing_time': processing_time
        }
    
    def _get_analysis_result(self, is_deepfake, confidence):
        """분석 결과 결정"""
        if is_deepfake:
            if confidence >= 0.8:
                return 'deepfake'
            else:
                return 'suspicious'
        else:
            return 'safe'
    
    def check_health(self):
        """FastAPI 서버 상태 확인"""
        try:
            response = requests.get(
                f"{self.fastapi_url}/health",
                timeout=2  # 빠른 타임아웃
            )
            return response.status_code == 200
        except:
            return False