from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response

app_name = 'protection'

class ProtectionJobView(APIView):
    def get(self, request):
        return Response({"message": "보호 작업 목록"})
    
    def post(self, request):
        return Response({"message": "보호 작업 시작"})

urlpatterns = [
    path('jobs/', ProtectionJobView.as_view(), name='job_list'),
]
