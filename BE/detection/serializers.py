from rest_framework import serializers
from .models import AnalysisRecord, FaceDetectionResult


class FaceDetectionResultSerializer(serializers.ModelSerializer):
    """얼굴 인식 결과 Serializer"""
    
    class Meta:
        model = FaceDetectionResult
        fields = [
            'detection_id',
            'face_count',
            'face_coordinates',
            'face_quality_scores',
            'detected_at'
        ]
        read_only_fields = ['detection_id', 'detected_at']


class AnalysisRecordSerializer(serializers.ModelSerializer):
    """분석 기록 Serializer"""
    
    face_detections = FaceDetectionResultSerializer(many=True, read_only=True)
    analysis_type_display = serializers.CharField(
        source='get_analysis_type_display',
        read_only=True
    )
    analysis_result_display = serializers.CharField(
        source='get_analysis_result_display',
        read_only=True
    )
    
    class Meta:
        model = AnalysisRecord
        fields = [
            'record_id',
            'user',
            'analysis_type',
            'analysis_type_display',
            'file_name',
            'file_size',
            'file_format',
            'original_path',
            'processed_path',
            'analysis_result',
            'analysis_result_display',
            'confidence_score',
            'processing_time',
            'ai_model_version',
            'face_detections',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'record_id',
            'user',
            'created_at',
            'updated_at'
        ]


class ImageAnalysisRequestSerializer(serializers.Serializer):
    """이미지 분석 요청 Serializer"""
    
    image = serializers.ImageField(required=True)
    analysis_type = serializers.ChoiceField(
        choices=['image', 'screenshot'],
        default='image'
    )


class VideoAnalysisRequestSerializer(serializers.Serializer):
    """영상 분석 요청 Serializer"""
    
    video = serializers.FileField(required=True)
    
    def validate_video(self, value):
        # 파일 확장자 검증
        ext = value.name.split('.')[-1].lower()
        if ext not in ['mp4', 'mov', 'avi']:
            raise serializers.ValidationError(
                "MP4, MOV, AVI 파일만 업로드 가능합니다."
            )
        
        # 파일 크기 검증 (500MB)
        if value.size > 500 * 1024 * 1024:
            raise serializers.ValidationError(
                "파일 크기는 500MB 이하여야 합니다."
            )
        
        return value


class AnalysisRecordListSerializer(serializers.ModelSerializer):
    """분석 기록 목록 Serializer (간단한 정보만)"""
    
    analysis_type_display = serializers.CharField(
        source='get_analysis_type_display',
        read_only=True
    )
    analysis_result_display = serializers.CharField(
        source='get_analysis_result_display',
        read_only=True
    )
    
    class Meta:
        model = AnalysisRecord
        fields = [
            'record_id',
            'analysis_type',
            'analysis_type_display',
            'file_name',
            'analysis_result',
            'analysis_result_display',
            'confidence_score',
            'created_at'
        ]
        read_only_fields = fields


class AnalysisStatisticsSerializer(serializers.Serializer):
    """분석 통계 Serializer"""
    
    total_analyses = serializers.IntegerField()
    safe_count = serializers.IntegerField()
    suspicious_count = serializers.IntegerField()
    deepfake_count = serializers.IntegerField()
    recent_analyses = AnalysisRecordListSerializer(many=True)