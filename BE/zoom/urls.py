from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response

app_name = 'zoom'

# 임시 뷰 (실제 구현 필요)
class ZoomSessionListView(APIView):
    def get(self, request):
        return Response({"message": "Zoom 세션 목록"})
    
    def post(self, request):
        return Response({"message": "Zoom 세션 시작"})

urlpatterns = [
    path('sessions/', ZoomSessionListView.as_view(), name='session_list'),
]