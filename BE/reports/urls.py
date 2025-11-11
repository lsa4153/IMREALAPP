from django.urls import path
from .views import (
    ReportSubmitView,
    ReportListView,
    ReportDetailView,
    ReportUpdateStatusView
)

app_name = 'reports'

urlpatterns = [
    # 신고 접수
    path('submit/', ReportSubmitView.as_view(), name='submit'),
    
    # 신고 조회
    path('', ReportListView.as_view(), name='list'),
    path('<int:pk>/', ReportDetailView.as_view(), name='detail'),
    
    # 신고 상태 업데이트 (관리자용)
    path('<int:pk>/status/', ReportUpdateStatusView.as_view(), name='update_status'),
]