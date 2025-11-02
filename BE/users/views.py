from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.utils import timezone
from .models import User, UserPermission, AppSetting
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserSerializer,
    UserProfileSerializer,
    UserPermissionSerializer,
    AppSettingSerializer
)


class UserRegistrationView(APIView):
    """사용자 회원가입 API"""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'message': '회원가입이 완료되었습니다.',
                'user': UserSerializer(user).data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """사용자 로그인 API"""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # 마지막 로그인 시간 업데이트
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
            
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'message': '로그인 성공',
                'user': UserSerializer(user).data,
                'token': token.key
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    """사용자 로그아웃 API"""
    
    def post(self, request):
        try:
            # 토큰 삭제
            request.user.auth_token.delete()
            return Response({
                'message': '로그아웃 되었습니다.'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': '로그아웃 처리 중 오류가 발생했습니다.'
            }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """사용자 프로필 조회/수정 API"""
    
    serializer_class = UserProfileSerializer
    
    def get_object(self):
        return self.request.user


class UserPermissionView(generics.RetrieveUpdateAPIView):
    """사용자 권한 설정 조회/수정 API"""
    
    serializer_class = UserPermissionSerializer
    
    def get_object(self):
        permission, created = UserPermission.objects.get_or_create(
            user=self.request.user
        )
        return permission


class AppSettingView(generics.RetrieveUpdateAPIView):
    """앱 설정 조회/수정 API"""
    
    serializer_class = AppSettingSerializer
    
    def get_object(self):
        setting, created = AppSetting.objects.get_or_create(
            user=self.request.user
        )
        return setting


class UserDeleteView(APIView):
    """회원 탈퇴 API"""
    
    def delete(self, request):
        user = request.user
        
        # 사용자 비활성화 (실제 삭제 대신)
        user.is_active = False
        user.save()
        
        # 토큰 삭제
        try:
            user.auth_token.delete()
        except:
            pass
        
        return Response({
            'message': '회원 탈퇴가 완료되었습니다.'
        }, status=status.HTTP_200_OK)