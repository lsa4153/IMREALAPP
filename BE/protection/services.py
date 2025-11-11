import requests
import time
from django.conf import settings
from media_files.models import SystemLog


class ProtectionService:
    """콘텐츠 보호 서비스 (FastAPI 연동)"""
    
    def __init__(self):
        self.fastapi_url = settings.FASTAPI_URL
        self.timeout = 600  # 10분
    
    def protect_images(self, file_identifiers, job_type='both'):
        """
        이미지 보호 처리
        
        Args:
            file_identifiers: 파일 식별자 리스트 (S3 키 또는 로컬 경로)
            job_type: 보호 방식
        
        Returns:
            dict: 보호 처리 결과
        """
        
        start_time = time.time()
        
        # 🔧 AI 서버 연결 확인
        if not self.check_health():
            print("⚠️ AI 서버 없음 - Mock 데이터 반환")
            return self._get_mock_protection_response(
                file_identifiers,
                start_time,
                'image'
            )
        
        # 실제 AI 서버 호출
        try:
            # ✅ S3 정보 또는 로컬 경로를 JSON으로 전달
            response = requests.post(
                f"{self.fastapi_url}/api/protect/images",
                json={
                    'files': file_identifiers,
                    'job_type': job_type
                },
                timeout=self.timeout
            )
            
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
    
    def protect_video(self, file_identifier, job_type='both'):
        """
        영상 보호 처리
        
        Args:
            file_identifier: 파일 식별자 (S3 키 또는 로컬 경로)
            job_type: 보호 방식
        
        Returns:
            dict: 보호 처리 결과
        """
        
        start_time = time.time()
        
        # 🔧 AI 서버 연결 확인
        if not self.check_health():
            print("⚠️ AI 서버 없음 - Mock 데이터 반환")
            return self._get_mock_protection_response(
                [file_identifier],
                start_time,
                'video'
            )
        
        # 실제 AI 서버 호출
        try:
            # ✅ S3 정보 또는 로컬 경로를 JSON으로 전달
            response = requests.post(
                f"{self.fastapi_url}/api/protect/video",
                json={
                    'file': file_identifier,
                    'job_type': job_type
                },
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
    
    def _get_mock_protection_response(self, file_identifiers, start_time, file_type):
        """
        🔧 Mock 보호 처리 응답 (AI 서버 없을 때)
        """
        from datetime import datetime
        
        processing_time = int((time.time() - start_time) * 1000)
        
        if file_type == 'image':
            protected_files = []
            for i, identifier in enumerate(file_identifiers):
                # ✅ S3 또는 로컬 경로에서 파일명 추출
                if identifier.get('type') == 's3':
                    original_name = identifier['s3_key'].split('/')[-1]
                else:
                    original_name = identifier['path'].split('/')[-1]
                
                name_without_ext = '.'.join(original_name.split('.')[:-1])
                ext = original_name.split('.')[-1]
                timestamp = datetime.now().strftime('%Y%m%d')
                
                protected_name = f"{name_without_ext}_protected_{timestamp}.{ext}"
                
                protected_files.append({
                    'original_path': original_name,
                    'protected_path': protected_name,
                    'file_name': protected_name,
                    'file_size': 1024 * 1024
                })
            
            return {
                'success': True,
                'protected_files': protected_files,
                'processing_time': processing_time
            }
        
        else:  # video
            identifier = file_identifiers[0]
            
            if identifier.get('type') == 's3':
                original_name = identifier['s3_key'].split('/')[-1]
            else:
                original_name = identifier['path'].split('/')[-1]
            
            name_without_ext = '.'.join(original_name.split('.')[:-1])
            ext = original_name.split('.')[-1]
            timestamp = datetime.now().strftime('%Y%m%d')
            
            protected_name = f"{name_without_ext}_protected_{timestamp}.{ext}"
            
            return {
                'success': True,
                'protected_file': {
                    'original_path': original_name,
                    'protected_path': protected_name,
                    'file_name': protected_name,
                    'file_size': 50 * 1024 * 1024
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