from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
import os

from .models import Report
from .serializers import (
    ReportSerializer,
    ReportListSerializer,
    ReportSubmitSerializer
)
from detection.models import AnalysisRecord
from media_files.services import FileService


class ReportSubmitView(APIView):
    """신고 접수 API"""
    
    def post(self, request):
        serializer = ReportSubmitSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        record_id = serializer.validated_data['record_id']
        evidence_files = serializer.validated_data.get('evidence_files', [])
        
        # 분석 기록 확인
        try:
            record = AnalysisRecord.objects.get(
                record_id=record_id,
                user=request.user
            )
        except AnalysisRecord.DoesNotExist:
            return Response(
                {'error': '분석 기록을 찾을 수 없습니다.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # ✅ FileService 사용
        file_service = FileService(request.user)
        
        media_files = []
        evidence_data = []
        
        try:
            # 증거 파일 업로드
            for file in evidence_files:
                # ✅ 파일 확장자에 따라 타입 자동 판별
                ext = file.name.split('.')[-1].lower()
                
                if ext in ['jpg', 'jpeg', 'png', 'webp', 'gif']:
                    file_type = 'image'
                elif ext in ['mp4', 'mov', 'avi']:
                    file_type = 'video'
                else:
                    file_type = 'document'
                
                media_file = file_service.upload_file(
                    uploaded_file=file,
                    file_type=file_type,  # ✅ 동적으로 결정
                    purpose='report',
                    is_temporary=False,
                    use_s3=False # s3 준비 되면 true로 바꾸기
                )
                media_files.append(media_file)
                
                evidence_data.append({
                    'file_id': media_file.file_id,
                    'file_name': media_file.original_name,
                    'file_path': media_file.file_path,
                    'file_type': media_file.mime_type,
                    'file_size': media_file.file_size
                })
            
            # Report 생성
            report = Report.objects.create(
                user=request.user,
                record=record,
                report_type=serializer.validated_data['report_type'],
                discovery_source=serializer.validated_data['discovery_source'],
                damage_level=serializer.validated_data['damage_level'],
                description=serializer.validated_data['description'],
                report_agency=serializer.validated_data['report_agency'],
                evidence_files=evidence_data if evidence_data else None,
                report_status='submitted'
            )
            
            # ✅ 관계 연결
            for media_file in media_files:
                media_file.related_model = 'Report'
                media_file.related_record_id = report.report_id
                media_file.save()
            
            return Response(
                ReportSerializer(report).data,
                status=status.HTTP_201_CREATED
            )
        
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class ReportListView(generics.ListAPIView):
    """신고 목록 조회 API"""
    
    serializer_class = ReportListSerializer
    
    def get_queryset(self):
        queryset = Report.objects.filter(user=self.request.user)
        
        # 필터링
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(report_status=status_filter)
        
        agency_filter = self.request.query_params.get('agency', None)
        if agency_filter:
            queryset = queryset.filter(report_agency=agency_filter)
        
        return queryset


class ReportDetailView(generics.RetrieveAPIView):
    """신고 상세 조회 API"""
    
    serializer_class = ReportSerializer
    
    def get_queryset(self):
        return Report.objects.filter(user=self.request.user)


class ReportUpdateStatusView(APIView):
    """신고 상태 업데이트 API (관리자용)"""
    
    def patch(self, request, pk):
        try:
            report = Report.objects.get(report_id=pk)
        except Report.DoesNotExist:
            return Response(
                {'error': '신고를 찾을 수 없습니다.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # 상태 업데이트
        new_status = request.data.get('report_status')
        if new_status and new_status in dict(Report.STATUS_CHOICES):
            report.report_status = new_status
        
        # 접수번호 업데이트
        reference_number = request.data.get('report_reference_number')
        if reference_number:
            report.report_reference_number = reference_number
        
        report.save()
        
        return Response(
            ReportSerializer(report).data,
            status=status.HTTP_200_OK
        )