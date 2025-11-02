from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Q
from django.core.files.storage import default_storage
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
        
        # 파일 저장
        file_path = default_storage.save(
            f'uploads/images/{image.name}',
            image
        )
        full_path = default_storage.path(file_path)
        
        # AI 모델 분석
        ai_service = AIModelService()
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
            file_name=image.name,
            file_size=image.size,
            file_format=image.name.split('.')[-1].lower(),
            original_path=file_path,
            analysis_result=result['analysis_result'],
            confidence_score=result['confidence_score'],
            processing_time=result['processing_time'],
            ai_model_version=result['ai_model_version']
        )
        
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
        
        # 파일 저장
        file_path = default_storage.save(
            f'uploads/videos/{video.name}',
            video
        )
        full_path = default_storage.path(file_path)
        
        # AI 모델 분석
        ai_service = AIModelService()
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
            file_name=video.name,
            file_size=video.size,
            file_format=video.name.split('.')[-1].lower(),
            original_path=file_path,
            analysis_result=result['analysis_result'],
            confidence_score=result['confidence_score'],
            processing_time=result['processing_time'],
            ai_model_version=result['ai_model_version']
        )
        
        return Response(
            AnalysisRecordSerializer(record).data,
            status=status.HTTP_201_CREATED
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