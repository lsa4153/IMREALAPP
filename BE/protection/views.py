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
        
        file_service = FileService(request.user)
        
        media_files = []
        file_identifiers = []
        
        try:
            for file in uploaded_files:
                media_file = file_service.upload_file(
                    uploaded_file=file,
                    file_type='image',
                    purpose='protection',
                    is_temporary=False,
                    use_s3=settings.USE_S3_FOR_PROTECTION  # ✅ 환경 변수로 제어
                )
                media_files.append(media_file)
                
                # ✅ S3 키 또는 로컬 경로 전달
                if media_file.storage_type == 's3':
                    # AI 서버에 S3 키 전달
                    file_identifiers.append({
                        'type': 's3',
                        's3_bucket': media_file.s3_bucket,
                        's3_key': media_file.s3_key
                    })
                else:
                    # 로컬 경로 전달
                    file_identifiers.append({
                        'type': 'local',
                        'path': os.path.join(settings.MEDIA_ROOT, media_file.file_path)
                    })
            
            original_files_data = [
                {
                    'file_id': mf.file_id,
                    'file_name': mf.original_name,
                    'file_size': mf.file_size,
                    'file_path': mf.file_path,
                    'mime_type': mf.mime_type,
                    'storage_type': mf.storage_type
                }
                for mf in media_files
            ]
            
            job = ProtectionJob.objects.create(
                user=request.user,
                job_type=job_type,
                original_files=original_files_data,
                job_status='pending',
                progress_percentage=0.0
            )
            
            # ✅ AI 서버에 파일 정보 전달
            protection_service = ProtectionService()
            result = protection_service.protect_images(file_identifiers, job_type)
            
            if not result['success']:
                job.job_status = 'failed'
                job.error_message = result.get('error', '알 수 없는 오류')
                job.save()
                
                return Response(
                    {'error': result['error']},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
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
        
        file_service = FileService(request.user)
        
        try:
            media_file = file_service.upload_file(
                uploaded_file=video,
                file_type='video',
                purpose='protection',
                is_temporary=False,
                use_s3=True  # ✅ S3에 저장
            )
            
            # ✅ S3 키 또는 로컬 경로 전달
            if media_file.storage_type == 's3':
                file_identifier = {
                    'type': 's3',
                    's3_bucket': media_file.s3_bucket,
                    's3_key': media_file.s3_key
                }
            else:
                file_identifier = {
                    'type': 'local',
                    'path': os.path.join(settings.MEDIA_ROOT, media_file.file_path)
                }
            
            original_files_data = [{
                'file_id': media_file.file_id,
                'file_name': media_file.original_name,
                'file_size': media_file.file_size,
                'file_path': media_file.file_path,
                'mime_type': media_file.mime_type,
                'storage_type': media_file.storage_type
            }]
            
            job = ProtectionJob.objects.create(
                user=request.user,
                job_type=job_type,
                original_files=original_files_data,
                job_status='pending',
                progress_percentage=0.0
            )
            
            protection_service = ProtectionService()
            result = protection_service.protect_video(file_identifier, job_type)
            
            if not result['success']:
                job.job_status = 'failed'
                job.error_message = result.get('error', '알 수 없는 오류')
                job.save()
                
                return Response(
                    {'error': result['error']},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
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