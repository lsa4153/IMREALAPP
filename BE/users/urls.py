from django.urls import path
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserLogoutView,
    UserProfileView,
    UserPermissionView,
    AppSettingView,
    UserDeleteView
)

app_name = 'users'

urlpatterns = [
    # 인증
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    
    # 프로필
    path('profile/', UserProfileView.as_view(), name='profile'),
    
    # 설정
    path('permissions/', UserPermissionView.as_view(), name='permissions'),
    path('settings/', AppSettingView.as_view(), name='settings'),
    
    # 회원 탈퇴
    path('delete/', UserDeleteView.as_view(), name='delete'),
]