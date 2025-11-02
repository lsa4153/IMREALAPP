from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response

app_name = 'reports'

class ReportListView(APIView):
    def get(self, request):
        return Response({"message": "신고 목록"})
    
    def post(self, request):
        return Response({"message": "신고 접수"})

urlpatterns = [
    path('', ReportListView.as_view(), name='report_list'),
]