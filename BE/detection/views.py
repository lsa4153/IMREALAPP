from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Q
from django.conf import settings
import os

from .models import AnalysisRecord, FaceDetectionResult
from .serializers import (
    AnalysisRecordSerializer,
    AnalysisRecordListSerializer,
    ImageAnalysisRequestSerializer,
    VideoAnalysisRequestSerializer,
    AnalysisStatisticsSerializer
)
from .services import AIModelService
from media_files.services import FileService


class ImageAnalysisView(APIView):
    """이미지 딥페이크 분석 API"""
    
    def post(self, request):
        serializer = ImageAnalysisRequestSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        image = serializer.validated_data['image']
        analysis_type = serializer.validated_data['analysis_type']
        
        # ✅ FileService 사용
        file_service = FileService(request.user)
        
        try:
            # ✅ 통합 파일 업로드
            media_file = file_service.upload_file(
                uploaded_file=image,
                file_type='image',
                purpose='detection',
                is_temporary=True,  # 분석 후 삭제
                use_s3=False
            )
            
            # AI 분석
            ai_service = AIModelService()
            full_path = os.path.join(settings.MEDIA_ROOT, media_file.file_path)
            result = ai_service.analyze_image(full_path)
            
            if not result['success']:
                return Response(
                    {'error': result['error']},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # 분석 기록 저장
            record = AnalysisRecord.objects.create(
                user=request.user,
                analysis_type=analysis_type,
                file_name=media_file.original_name,
                file_size=media_file.file_size,
                file_format=media_file.file_format,
                original_path=media_file.file_path,
                analysis_result=result['analysis_result'],
                confidence_score=result['confidence_score'],
                processing_time=result['processing_time'],
                ai_model_version=result['ai_model_version']
            )
            
            # ✅ 관계 연결
            media_file.related_model = 'AnalysisRecord'
            media_file.related_record_id = record.record_id
            media_file.save()
            
            # 얼굴 인식 결과 저장
            if result.get('face_count', 0) > 0:
                FaceDetectionResult.objects.create(
                    record=record,
                    face_count=result['face_count'],
                    face_coordinates=result['face_coordinates'],
                    face_quality_scores=result['face_quality_scores']
                )
            
            return Response(
                AnalysisRecordSerializer(record).data,
                status=status.HTTP_201_CREATED
            )
        
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class VideoAnalysisView(APIView):
    """영상 딥페이크 분석 API"""
    
    def post(self, request):
        serializer = VideoAnalysisRequestSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        video = serializer.validated_data['video']
        
        # ✅ FileService 사용
        file_service = FileService(request.user)
        
        try:
            # ✅ 통합 파일 업로드
            media_file = file_service.upload_file(
                uploaded_file=video,
                file_type='video',
                purpose='detection',
                is_temporary=True,  # 분석 후 삭제
                use_s3=False
            )
            
            # AI 분석
            ai_service = AIModelService()
            full_path = os.path.join(settings.MEDIA_ROOT, media_file.file_path)
            result = ai_service.analyze_video(full_path)
            
            if not result['success']:
                return Response(
                    {'error': result['error']},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # 분석 기록 저장
            record = AnalysisRecord.objects.create(
                user=request.user,
                analysis_type='video',
                file_name=media_file.original_name,
                file_size=media_file.file_size,
                file_format=media_file.file_format,
                original_path=media_file.file_path,
                analysis_result=result['analysis_result'],
                confidence_score=result['confidence_score'],
                processing_time=result['processing_time'],
                ai_model_version=result['ai_model_version']
            )
            
            # ✅ 관계 연결
            media_file.related_model = 'AnalysisRecord'
            media_file.related_record_id = record.record_id
            media_file.save()
            
            return Response(
                AnalysisRecordSerializer(record).data,
                status=status.HTTP_201_CREATED
            )
        
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class AnalysisRecordListView(generics.ListAPIView):
    """분석 기록 목록 조회 API"""
    
    serializer_class = AnalysisRecordListSerializer
    
    def get_queryset(self):
        queryset = AnalysisRecord.objects.filter(user=self.request.user)
        
        # 필터링
        analysis_type = self.request.query_params.get('type', None)
        if analysis_type:
            queryset = queryset.filter(analysis_type=analysis_type)
        
        analysis_result = self.request.query_params.get('result', None)
        if analysis_result:
            queryset = queryset.filter(analysis_result=analysis_result)
        
        return queryset


class AnalysisRecordDetailView(generics.RetrieveDestroyAPIView):
    """분석 기록 상세 조회/삭제 API"""
    
    serializer_class = AnalysisRecordSerializer
    
    def get_queryset(self):
        return AnalysisRecord.objects.filter(user=self.request.user)
    
    def perform_destroy(self, instance):
        """
        분석 기록 삭제 시 관련 파일도 삭제
        """
        # 관련 미디어 파일 찾기
        from media_files.models import MediaFile
        
        media_files = MediaFile.objects.filter(
            related_model='AnalysisRecord',
            related_record_id=instance.record_id,
            is_deleted=False
        )
        
        # FileService로 파일 삭제
        file_service = FileService(self.request.user)
        for media_file in media_files:
            try:
                file_service.delete_file(media_file.file_id, hard_delete=True)
            except:
                pass
        
        # 분석 기록 삭제
        instance.delete()


class AnalysisStatisticsView(APIView):
    """분석 통계 API"""
    
    def get(self, request):
        # 사용자의 전체 분석 통계
        records = AnalysisRecord.objects.filter(user=request.user)
        
        stats = records.aggregate(
            total=Count('record_id'),
            safe=Count('record_id', filter=Q(analysis_result='safe')),
            suspicious=Count('record_id', filter=Q(analysis_result='suspicious')),
            deepfake=Count('record_id', filter=Q(analysis_result='deepfake'))
        )
        
        # 최근 5개 분석 기록
        recent = records[:5]
        
        data = {
            'total_analyses': stats['total'],
            'safe_count': stats['safe'],
            'suspicious_count': stats['suspicious'],
            'deepfake_count': stats['deepfake'],
            'recent_analyses': AnalysisRecordListSerializer(recent, many=True).data
        }
        
        serializer = AnalysisStatisticsSerializer(data)
        return Response(serializer.data)


class AIHealthCheckView(APIView):
    """AI 서버 상태 확인 API"""
    
    def get(self, request):
        ai_service = AIModelService()
        is_healthy = ai_service.check_health()
        
        return Response({
            'status': 'healthy' if is_healthy else 'unhealthy',
            'fastapi_url': ai_service.fastapi_url
        })