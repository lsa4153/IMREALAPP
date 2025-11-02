
# detection/admin.py
from django.contrib import admin
from .models import AnalysisRecord, FaceDetectionResult


@admin.register(AnalysisRecord)
class AnalysisRecordAdmin(admin.ModelAdmin):
    """분석 기록 관리자"""
    
    list_display = [
        'record_id',
        'user',
        'analysis_type',
        'file_name',
        'analysis_result',
        'confidence_score',
        'created_at'
    ]
    list_filter = ['analysis_type', 'analysis_result', 'created_at']
    search_fields = ['user__email', 'file_name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(FaceDetectionResult)
class FaceDetectionResultAdmin(admin.ModelAdmin):
    """얼굴 인식 결과 관리자"""
    
    list_display = [
        'detection_id',
        'record',
        'face_count',
        'detected_at'
    ]
    list_filter = ['detected_at']
    search_fields = ['record__file_name']
    readonly_fields = ['detected_at']
    ordering = ['-detected_at']