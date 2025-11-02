from django.db import models
from django.conf import settings


class ProtectionJob(models.Model):
    """콘텐츠 보호 작업"""
    
    JOB_TYPE_CHOICES = [
        ('adversarial_noise', 'Adversarial Noise 추가'),
        ('watermark', '워터마크 삽입'),
        ('both', '노이즈 + 워터마크'),
    ]
    
    STATUS_CHOICES = [
        ('pending', '대기 중'),
        ('processing', '처리 중'),
        ('completed', '완료'),
        ('failed', '실패'),
    ]
    
    job_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='protection_jobs',
        verbose_name='사용자'
    )
    job_type = models.CharField(
        max_length=50,
        choices=JOB_TYPE_CHOICES,
        verbose_name='작업 유형'
    )
    original_files = models.JSONField(
        verbose_name='원본 파일 목록',
        help_text='[{"file_name": "image1.jpg", "file_path": "/path/to/file", "file_size": 1024}]'
    )
    protected_files = models.JSONField(
        null=True,
        blank=True,
        verbose_name='보호된 파일 목록',
        help_text='[{"file_name": "image1_protected.jpg", "file_path": "/path/to/file", "file_size": 1024}]'
    )
    job_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='작업 상태'
    )
    progress_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        verbose_name='진행률(%)'
    )
    processing_started_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='처리 시작 시간'
    )
    processing_completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='처리 완료 시간'
    )
    error_message = models.TextField(
        null=True,
        blank=True,
        verbose_name='오류 메시지'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일시')
    
    class Meta:
        db_table = 'protection_jobs'
        verbose_name = '보호 작업'
        verbose_name_plural = '보호 작업 목록'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['job_status']),
        ]
    
    def __str__(self):
        return f"{self.get_job_type_display()} - {self.get_job_status_display()}"
    
    @property
    def processing_duration(self):
        """처리 소요 시간 계산"""
        if self.processing_started_at and self.processing_completed_at:
            return (self.processing_completed_at - self.processing_started_at).total_seconds()
        return None
    
    @property
    def file_count(self):
        """파일 개수"""
        return len(self.original_files) if self.original_files else 0