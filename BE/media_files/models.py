from django.db import models
from django.conf import settings


class SystemLog(models.Model):
    """시스템 로그"""
    
    LOG_LEVEL_CHOICES = [
        ('debug', 'DEBUG'),
        ('info', 'INFO'),
        ('warning', 'WARNING'),
        ('error', 'ERROR'),
        ('critical', 'CRITICAL'),
    ]
    
    LOG_CATEGORY_CHOICES = [
        ('auth', '인증'),
        ('api', 'API'),
        ('detection', '탐지'),
        ('protection', '보호'),
        ('report', '신고'),
        ('system', '시스템'),
        ('database', '데이터베이스'),
    ]
    
    log_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='system_logs',
        verbose_name='사용자'
    )
    log_level = models.CharField(
        max_length=20,
        choices=LOG_LEVEL_CHOICES,
        verbose_name='로그 레벨'
    )
    log_category = models.CharField(
        max_length=50,
        choices=LOG_CATEGORY_CHOICES,
        verbose_name='로그 카테고리'
    )
    message = models.TextField(verbose_name='메시지')
    error_code = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='오류 코드'
    )
    request_data = models.JSONField(
        null=True,
        blank=True,
        verbose_name='요청 데이터'
    )
    response_data = models.JSONField(
        null=True,
        blank=True,
        verbose_name='응답 데이터'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일시')
    
    class Meta:
        db_table = 'system_logs'
        verbose_name = '시스템 로그'
        verbose_name_plural = '시스템 로그 목록'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['log_level']),
            models.Index(fields=['log_category']),
            models.Index(fields=['user', '-created_at']),
        ]
    
    def __str__(self):
        return f"[{self.log_level.upper()}] {self.message[:50]}"