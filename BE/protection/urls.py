from django.urls import path
from .views import (
    ImageProtectionView,
    VideoProtectionView,
    ProtectionJobListView,
    ProtectionJobDetailView
)

app_name = 'protection'

urlpatterns = [
    # 보호 처리
    path('images/', ImageProtectionView.as_view(), name='image_protection'),
    path('videos/', VideoProtectionView.as_view(), name='video_protection'),
    
    # 작업 조회
    path('jobs/', ProtectionJobListView.as_view(), name='job_list'),
    path('jobs/<int:pk>/', ProtectionJobDetailView.as_view(), name='job_detail'),
]