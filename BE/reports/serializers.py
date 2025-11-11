from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    """신고 Serializer"""
    
    report_type_display = serializers.CharField(
        source='get_report_type_display',
        read_only=True
    )
    discovery_source_display = serializers.CharField(
        source='get_discovery_source_display',
        read_only=True
    )
    damage_level_display = serializers.CharField(
        source='get_damage_level_display',
        read_only=True
    )
    report_agency_display = serializers.CharField(
        source='get_report_agency_display',
        read_only=True
    )
    report_status_display = serializers.CharField(
        source='get_report_status_display',
        read_only=True
    )
    
    class Meta:
        model = Report
        fields = [
            'report_id',
            'user',
            'record',
            'report_type',
            'report_type_display',
            'discovery_source',
            'discovery_source_display',
            'damage_level',
            'damage_level_display',
            'description',
            'evidence_files',
            'report_agency',
            'report_agency_display',
            'report_reference_number',
            'report_status',
            'report_status_display',
            'submitted_at',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'report_id',
            'user',
            'report_reference_number',
            'report_status',
            'submitted_at',
            'created_at',
            'updated_at',
        ]


class ReportSubmitSerializer(serializers.Serializer):
    """신고 접수 Serializer"""
    
    record_id = serializers.IntegerField(help_text="분석 기록 ID")
    report_type = serializers.ChoiceField(
        choices=Report.REPORT_TYPE_CHOICES,
        help_text="신고 유형"
    )
    discovery_source = serializers.ChoiceField(
        choices=Report.DISCOVERY_SOURCE_CHOICES,
        help_text="발견 경로"
    )
    damage_level = serializers.ChoiceField(
        choices=Report.DAMAGE_LEVEL_CHOICES,
        help_text="피해 정도"
    )
    description = serializers.CharField(
        style={'base_template': 'textarea.html'},
        help_text="상세 설명"
    )
    report_agency = serializers.ChoiceField(
        choices=Report.REPORT_AGENCY_CHOICES,
        help_text="신고 기관"
    )
    evidence_files = serializers.ListField(
        child=serializers.FileField(),
        required=False,
        allow_empty=True,
        help_text="증거 파일 (선택)"
    )
    

class ReportListSerializer(serializers.ModelSerializer):
    """신고 목록 Serializer (간단한 정보만)"""
    
    report_type_display = serializers.CharField(
        source='get_report_type_display',
        read_only=True
    )
    report_agency_display = serializers.CharField(
        source='get_report_agency_display',
        read_only=True
    )
    report_status_display = serializers.CharField(
        source='get_report_status_display',
        read_only=True
    )
    
    class Meta:
        model = Report
        fields = [
            'report_id',
            'report_type',
            'report_type_display',
            'report_agency',
            'report_agency_display',
            'report_reference_number',
            'report_status',
            'report_status_display',
            'submitted_at',
        ]
        read_only_fields = fields