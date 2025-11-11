from django.contrib import admin
from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """신고 관리자"""
    
    list_display = [
        'report_id',
        'user',
        'report_type',
        'report_agency',
        'report_reference_number',
        'report_status',
        'submitted_at'
    ]
    list_filter = [
        'report_type',
        'report_agency',
        'report_status',
        'damage_level',
        'submitted_at'
    ]
    search_fields = [
        'user__email',
        'report_reference_number',
        'description'
    ]
    readonly_fields = [
        'report_id',
        'submitted_at',
        'created_at',
        'updated_at'
    ]
    ordering = ['-submitted_at']
    
    fieldsets = (
        ('기본 정보', {
            'fields': (
                'report_id',
                'user',
                'record',
                'report_type',
                'discovery_source',
                'damage_level'
            )
        }),
        ('신고 내용', {
            'fields': (
                'description',
                'evidence_files'
            )
        }),
        ('처리 정보', {
            'fields': (
                'report_agency',
                'report_reference_number',
                'report_status'
            )
        }),
        ('타임스탬프', {
            'fields': (
                'submitted_at',
                'created_at',
                'updated_at'
            )
        }),
    )