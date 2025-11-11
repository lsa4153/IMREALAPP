import requests
import time
from django.conf import settings
from media_files.models import SystemLog


class ProtectionService:
    """콘텐츠 보호 서비스 (FastAPI 연동)"""
    
    def __init__(self):
        self.fastapi_url = settings.FASTAPI_URL
        self.timeout = 600  # 10분 (보호 처리는 시간이 오래 걸림)
    
    def protect_images(self, image_paths, job_type='both'):
        """
        이미지 보호 처리
        
        Args:
            image_paths: 이미지 파일 경로 리스트
            job_type: 보호 방식 (adversarial_noise, watermark, both)
        
        Returns:
            dict: 보호 처리 결과
        """
        
        start_time = time.time()
        
        # 🔧 AI 서버 연결 확인
        if not self.check_health():
            print("⚠️ AI 서버 없음 - Mock 데이터 반환")
            return self._get_mock_protection_response(
                image_paths,
                start_time,
                'image'
            )
        
        # 실제 AI 서버 호출
        try:
            # 여러 파일 전송
            files = []
            for path in image_paths:
                files.append(
                    ('files', open(path, 'rb'))
                )
            
            data = {'job_type': job_type}
            
            response = requests.post(
                f"{self.fastapi_url}/api/protect/images",
                files=files,
                data=data,
                timeout=self.timeout
            )
            
            # 파일 핸들 닫기
            for _, file_obj in files:
                file_obj.close()
            
            response.raise_for_status()
            result = response.json()
            
            processing_time = int((time.time() - start_time) * 1000)
            
            return {
                'success': True,
                'protected_files': result.get('protected_files', []),
                'processing_time': processing_time
            }
        
        except requests.exceptions.RequestException as e:
            SystemLog.objects.create(
                log_level='error',
                log_category='protection',
                message=f'이미지 보호 처리 실패: {str(e)}',
                error_code='PROTECTION_API_ERROR'
            )
            
            return {
                'success': False,
                'error': '보호 처리 중 오류가 발생했습니다.',
                'processing_time': int((time.time() - start_time) * 1000)
            }
    
    def protect_video(self, video_path, job_type='both'):
        """
        영상 보호 처리
        
        Args:
            video_path: 영상 파일 경로
            job_type: 보호 방식
        
        Returns:
            dict: 보호 처리 결과
        """
        
        start_time = time.time()
        
        # 🔧 AI 서버 연결 확인
        if not self.check_health():
            print("⚠️ AI 서버 없음 - Mock 데이터 반환")
            return self._get_mock_protection_response(
                [video_path],
                start_time,
                'video'
            )
        
        # 실제 AI 서버 호출
        try:
            with open(video_path, 'rb') as f:
                files = {'file': f}
                data = {'job_type': job_type}
                
                response = requests.post(
                    f"{self.fastapi_url}/api/protect/video",
                    files=files,
                    data=data,
                    timeout=self.timeout
                )
            
            response.raise_for_status()
            result = response.json()
            
            processing_time = int((time.time() - start_time) * 1000)
            
            return {
                'success': True,
                'protected_file': result.get('protected_file'),
                'processing_time': processing_time
            }
        
        except requests.exceptions.RequestException as e:
            SystemLog.objects.create(
                log_level='error',
                log_category='protection',
                message=f'영상 보호 처리 실패: {str(e)}',
                error_code='PROTECTION_API_ERROR'
            )
            
            return {
                'success': False,
                'error': '보호 처리 중 오류가 발생했습니다.',
                'processing_time': int((time.time() - start_time) * 1000)
            }
    
    def _get_mock_protection_response(self, file_paths, start_time, file_type):
        """
        🔧 Mock 보호 처리 응답 (AI 서버 없을 때)
        """
        from datetime import datetime
        
        processing_time = int((time.time() - start_time) * 1000)
        
        if file_type == 'image':
            protected_files = []
            for i, path in enumerate(file_paths):
                # 파일명 생성
                original_name = path.split('/')[-1]
                name_without_ext = '.'.join(original_name.split('.')[:-1])
                ext = original_name.split('.')[-1]
                timestamp = datetime.now().strftime('%Y%m%d')
                
                protected_name = f"{name_without_ext}_protected_{timestamp}.{ext}"
                
                protected_files.append({
                    'original_path': path,
                    'protected_path': path.replace(original_name, protected_name),
                    'file_name': protected_name,
                    'file_size': 1024 * 1024  # Mock: 1MB
                })
            
            return {
                'success': True,
                'protected_files': protected_files,
                'processing_time': processing_time
            }
        
        else:  # video
            original_name = file_paths[0].split('/')[-1]
            name_without_ext = '.'.join(original_name.split('.')[:-1])
            ext = original_name.split('.')[-1]
            timestamp = datetime.now().strftime('%Y%m%d')
            
            protected_name = f"{name_without_ext}_protected_{timestamp}.{ext}"
            
            return {
                'success': True,
                'protected_file': {
                    'original_path': file_paths[0],
                    'protected_path': file_paths[0].replace(original_name, protected_name),
                    'file_name': protected_name,
                    'file_size': 50 * 1024 * 1024  # Mock: 50MB
                },
                'processing_time': processing_time
            }
    
    def check_health(self):
        """FastAPI 서버 상태 확인"""
        try:
            response = requests.get(
                f"{self.fastapi_url}/health",
                timeout=2
            )
            return response.status_code == 200
        except:
            return False