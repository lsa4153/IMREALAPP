from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
import os

from .models import ProtectionJob
from .serializers import (
    ProtectionJobSerializer,
    ProtectionJobListSerializer,
    ImageProtectionRequestSerializer,
    VideoProtectionRequestSerializer
)
from .services import ProtectionService
from media_files.services import FileService


class ImageProtectionView(APIView):
    """이미지 보호 API"""
    
    def post(self, request):
        serializer = ImageProtectionRequestSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        uploaded_files = serializer.validated_data['files']
        job_type = serializer.validated_data['job_type']
        
        # ✅ FileService 사용
        file_service = FileService(request.user)
        
        media_files = []
        file_paths = []
        
        try:
            # 각 파일 업로드
            for file in uploaded_files:
                media_file = file_service.upload_file(
                    uploaded_file=file,
                    file_type='image',
                    purpose='protection',
                    is_temporary=False,  # 영구 저장
                    use_s3=False
                )
                media_files.append(media_file)
                file_paths.append(
                    os.path.join(settings.MEDIA_ROOT, media_file.file_path)
                )
            
            # original_files JSONB 데이터 생성
            original_files_data = [
                {
                    'file_id': mf.file_id,
                    'file_name': mf.original_name,
                    'file_size': mf.file_size,
                    'file_path': mf.file_path,
                    'mime_type': mf.mime_type
                }
                for mf in media_files
            ]
            
            # ProtectionJob 생성
            job = ProtectionJob.objects.create(
                user=request.user,
                job_type=job_type,
                original_files=original_files_data,
                job_status='pending',
                progress_percentage=0.0
            )
            
            # 보호 처리 (Mock 또는 실제 AI 서버)
            protection_service = ProtectionService()
            result = protection_service.protect_images(file_paths, job_type)
            
            if not result['success']:
                job.job_status = 'failed'
                job.error_message = result.get('error', '알 수 없는 오류')
                job.save()
                
                return Response(
                    {'error': result['error']},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # 보호된 파일 정보 저장
            protected_files_data = []
            for protected_file_info in result['protected_files']:
                protected_files_data.append({
                    'file_name': protected_file_info['file_name'],
                    'file_path': protected_file_info['protected_path'],
                    'file_size': protected_file_info['file_size']
                })
            
            job.protected_files = protected_files_data
            job.job_status = 'completed'
            job.progress_percentage = 100.0
            job.save()
            
            return Response({
                'job_id': job.job_id,
                'status': 'completed',
                'protected_files': protected_files_data
            }, status=status.HTTP_201_CREATED)
        
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class VideoProtectionView(APIView):
    """영상 보호 API"""
    
    def post(self, request):
        serializer = VideoProtectionRequestSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        video = serializer.validated_data['file']
        job_type = serializer.validated_data['job_type']
        
        # ✅ FileService 사용
        file_service = FileService(request.user)
        
        try:
            # 파일 업로드
            media_file = file_service.upload_file(
                uploaded_file=video,
                file_type='video',
                purpose='protection',
                is_temporary=False,
                use_s3=False
            )
            
            file_path = os.path.join(settings.MEDIA_ROOT, media_file.file_path)
            
            # original_files JSONB 데이터
            original_files_data = [{
                'file_id': media_file.file_id,
                'file_name': media_file.original_name,
                'file_size': media_file.file_size,
                'file_path': media_file.file_path,
                'mime_type': media_file.mime_type
            }]
            
            # ProtectionJob 생성
            job = ProtectionJob.objects.create(
                user=request.user,
                job_type=job_type,
                original_files=original_files_data,
                job_status='pending',
                progress_percentage=0.0
            )
            
            # 보호 처리
            protection_service = ProtectionService()
            result = protection_service.protect_video(file_path, job_type)
            
            if not result['success']:
                job.job_status = 'failed'
                job.error_message = result.get('error', '알 수 없는 오류')
                job.save()
                
                return Response(
                    {'error': result['error']},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # 보호된 파일 정보 저장
            protected_file_info = result['protected_file']
            protected_files_data = [{
                'file_name': protected_file_info['file_name'],
                'file_path': protected_file_info['protected_path'],
                'file_size': protected_file_info['file_size']
            }]
            
            job.protected_files = protected_files_data
            job.job_status = 'completed'
            job.progress_percentage = 100.0
            job.save()
            
            return Response({
                'job_id': job.job_id,
                'status': 'completed',
                'protected_file': protected_files_data[0]
            }, status=status.HTTP_201_CREATED)
        
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class ProtectionJobListView(generics.ListAPIView):
    """보호 작업 목록 조회 API"""
    
    serializer_class = ProtectionJobListSerializer
    
    def get_queryset(self):
        return ProtectionJob.objects.filter(user=self.request.user)


class ProtectionJobDetailView(generics.RetrieveAPIView):
    """보호 작업 상세 조회 API"""
    
    serializer_class = ProtectionJobSerializer
    
    def get_queryset(self):
        return ProtectionJob.objects.filter(user=self.request.user)