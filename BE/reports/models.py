from django.db import models
from django.conf import settings


class Report(models.Model):
    """신고"""
    
    REPORT_TYPE_CHOICES = [
        ('deepfake_image', '딥페이크 이미지'),
        ('deepfake_video', '딥페이크 영상'),
        ('deepfake_audio', '딥페이크 음성'),
        ('fake_interview', '온라인 면접 딥페이크'),
    ]
    
    DISCOVERY_SOURCE_CHOICES = [
        ('sns', 'SNS'),
        ('messenger', '메신저'),
        ('website', '웹사이트'),
        ('email', '이메일'),
        ('video_conference', '화상회의'),
        ('other', '기타'),
    ]
    
    DAMAGE_LEVEL_CHOICES = [
        ('personal', '개인 피해'),
        ('group', '단체 피해'),
        ('social', '사회적 피해'),
    ]
    
    REPORT_AGENCY_CHOICES = [
        ('kisa', '한국인터넷진흥원(KISA)'),
        ('pipc', '개인정보보호위원회'),
        ('cyberbureau', '사이버수사대'),
        ('dscc', '디지털성범죄신고센터'),
        ('moel', '고용노동부'),
        ('company_hr', '기업 HR 부서'),
    ]
    
    STATUS_CHOICES = [
        ('submitted', '접수됨'),
        ('under_review', '검토 중'),
        ('in_progress', '처리 중'),
        ('completed', '완료'),
        ('rejected', '반려'),
    ]
    
    report_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports',
        verbose_name='사용자'
    )
    record = models.ForeignKey(
        'detection.AnalysisRecord',
        on_delete=models.CASCADE,
        related_name='reports',
        verbose_name='분석 기록'
    )
    report_type = models.CharField(
        max_length=50,
        choices=REPORT_TYPE_CHOICES,
        verbose_name='신고 유형'
    )
    discovery_source = models.CharField(
        max_length=50,
        choices=DISCOVERY_SOURCE_CHOICES,
        verbose_name='발견 경로'
    )
    damage_level = models.CharField(
        max_length=20,
        choices=DAMAGE_LEVEL_CHOICES,
        verbose_name='피해 정도'
    )
    description = models.TextField(verbose_name='상세 설명')
    evidence_files = models.JSONField(
        null=True,
        blank=True,
        verbose_name='증거 자료',
        help_text='[{"file_name": "screenshot.png", "file_url": "https://..."}]'
    )
    report_agency = models.CharField(
        max_length=50,
        choices=REPORT_AGENCY_CHOICES,
        verbose_name='신고 기관'
    )
    report_reference_number = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='신고 접수번호'
    )
    report_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='submitted',
        verbose_name='신고 상태'
    )
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name='제출일시')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일시')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일시')
    
    class Meta:
        db_table = 'reports'
        verbose_name = '신고'
        verbose_name_plural = '신고 목록'
        ordering = ['-submitted_at']
        indexes = [
            models.Index(fields=['user', '-submitted_at']),
            models.Index(fields=['report_status']),
            models.Index(fields=['report_agency']),
        ]
    
    def __str__(self):
        return f"{self.get_report_type_display()} - {self.report_reference_number or '접수 대기'}"