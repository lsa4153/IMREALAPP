from django.contrib import admin
from .models import ProtectionJob


@admin.register(ProtectionJob)
class ProtectionJobAdmin(admin.ModelAdmin):
    """보호 작업 관리자"""
    
    list_display = [
        'job_id',
        'user',
        'job_type',
        'job_status',
        'file_count',
        'progress_percentage',
        'created_at'
    ]
    list_filter = ['job_type', 'job_status', 'created_at']
    search_fields = ['user__email']
    readonly_fields = [
        'job_id',
        'created_at',
        'processing_started_at',
        'processing_completed_at'
    ]
    ordering = ['-created_at']