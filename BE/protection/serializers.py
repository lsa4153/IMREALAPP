from rest_framework import serializers
from .models import ProtectionJob


class ProtectionJobSerializer(serializers.ModelSerializer):
    """보호 작업 Serializer"""
    
    job_type_display = serializers.CharField(
        source='get_job_type_display',
        read_only=True
    )
    job_status_display = serializers.CharField(
        source='get_job_status_display',
        read_only=True
    )
    processing_duration = serializers.SerializerMethodField()
    
    class Meta:
        model = ProtectionJob
        fields = [
            'job_id',
            'user',
            'job_type',
            'job_type_display',
            'original_files',
            'protected_files',
            'job_status',
            'job_status_display',
            'progress_percentage',
            'processing_started_at',
            'processing_completed_at',
            'processing_duration',
            'error_message',
            'created_at',
        ]
        read_only_fields = [
            'job_id',
            'user',
            'protected_files',
            'job_status',
            'progress_percentage',
            'processing_started_at',
            'processing_completed_at',
            'error_message',
            'created_at',
        ]
    
    def get_processing_duration(self, obj):
        """처리 소요 시간 (초)"""
        return obj.processing_duration


class ImageProtectionRequestSerializer(serializers.Serializer):
    """이미지 보호 요청 Serializer"""
    
    files = serializers.ListField(
        child=serializers.ImageField(),
        max_length=10,  # 최대 10장
        min_length=1,
        help_text="보호할 이미지 파일 (최대 10장)"
    )
    job_type = serializers.ChoiceField(
        choices=['adversarial_noise', 'watermark', 'both'],
        default='both',
        help_text="보호 방식"
    )


class VideoProtectionRequestSerializer(serializers.Serializer):
    """영상 보호 요청 Serializer"""
    
    file = serializers.FileField(help_text="보호할 영상 파일")
    job_type = serializers.ChoiceField(
        choices=['adversarial_noise', 'watermark', 'both'],
        default='both',
        help_text="보호 방식"
    )
    
    def validate_file(self, value):
        """영상 파일 검증"""
        
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


class ProtectionJobListSerializer(serializers.ModelSerializer):
    """보호 작업 목록 Serializer (간단한 정보만)"""
    
    job_type_display = serializers.CharField(
        source='get_job_type_display',
        read_only=True
    )
    job_status_display = serializers.CharField(
        source='get_job_status_display',
        read_only=True
    )
    file_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = ProtectionJob
        fields = [
            'job_id',
            'job_type',
            'job_type_display',
            'job_status',
            'job_status_display',
            'file_count',
            'progress_percentage',
            'created_at',
        ]
        read_only_fields = fields