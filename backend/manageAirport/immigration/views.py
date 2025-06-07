from django.shortcuts import render
from rest_framework import viewsets, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import ImmigrationRecord
from .serializers import (
    ImmigrationRecordListSerializer,
    ImmigrationRecordDetailSerializer,
    ImmigrationRecordCreateSerializer
)

class ImmigrationRecordViewSet(viewsets.ModelViewSet):
    """
    API endpoints để quản lý bản ghi xuất nhập cảnh
    
    Cung cấp CRUD đầy đủ (Create, Read, Update, Delete) cho bản ghi xuất nhập cảnh sân bay
    """
    queryset = ImmigrationRecord.objects.all().order_by('-date_of_entry_exit')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['entry_type', 'purpose', 'status', 'nationality']
    search_fields = ['full_name', 'passport_number', 'visa_number', 'flight_number']
    ordering_fields = ['date_of_entry_exit', 'full_name', 'status']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ImmigrationRecordListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ImmigrationRecordCreateSerializer
        return ImmigrationRecordDetailSerializer
    
    @swagger_auto_schema(
        operation_summary="Tạo bản ghi xuất nhập cảnh mới",
        operation_description="Tạo một bản ghi mới với thông tin xuất nhập cảnh"
    )
    def create(self, request, *args, **kwargs):
        """Tạo bản ghi xuất nhập cảnh mới"""
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Danh sách bản ghi xuất nhập cảnh",
        operation_description="Trả về danh sách tất cả bản ghi xuất nhập cảnh với phân trang",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, description="Số trang", type=openapi.TYPE_INTEGER),
            openapi.Parameter('search', openapi.IN_QUERY, description="Tìm kiếm theo tên, số hộ chiếu, chuyến bay...", type=openapi.TYPE_STRING),
        ]
    )
    def list(self, request, *args, **kwargs):
        """Danh sách tất cả bản ghi xuất nhập cảnh"""
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Chi tiết bản ghi xuất nhập cảnh",
        operation_description="Trả về thông tin chi tiết của một bản ghi xuất nhập cảnh"
    )
    def retrieve(self, request, *args, **kwargs):
        """Chi tiết một bản ghi xuất nhập cảnh"""
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Cập nhật bản ghi xuất nhập cảnh",
        operation_description="Cập nhật thông tin của một bản ghi xuất nhập cảnh"
    )
    def update(self, request, *args, **kwargs):
        """Cập nhật thông tin bản ghi xuất nhập cảnh"""
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Cập nhật một phần bản ghi",
        operation_description="Cập nhật một phần thông tin của bản ghi xuất nhập cảnh"
    )
    def partial_update(self, request, *args, **kwargs):
        """Cập nhật một phần thông tin bản ghi xuất nhập cảnh"""
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Xóa bản ghi xuất nhập cảnh",
        operation_description="Xóa một bản ghi xuất nhập cảnh theo ID"
    )
    def destroy(self, request, *args, **kwargs):
        """Xóa bản ghi xuất nhập cảnh"""
        return super().destroy(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Thống kê xuất nhập cảnh",
        operation_description="Trả về các thống kê về bản ghi xuất nhập cảnh",
        responses={
            200: openapi.Response(
                description="Thống kê thành công",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'total': openapi.Schema(type=openapi.TYPE_INTEGER, description="Tổng số bản ghi"),
                        'by_entry_type': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'entry': openapi.Schema(type=openapi.TYPE_INTEGER, description="Số bản ghi nhập cảnh"),
                                'exit': openapi.Schema(type=openapi.TYPE_INTEGER, description="Số bản ghi xuất cảnh")
                            }
                        ),
                        'by_purpose': openapi.Schema(type=openapi.TYPE_OBJECT, description="Thống kê theo mục đích"),
                        'by_status': openapi.Schema(type=openapi.TYPE_OBJECT, description="Thống kê theo trạng thái")
                    }
                )
            )
        }
    )
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Thống kê số lượng xuất nhập cảnh"""
        total_records = ImmigrationRecord.objects.count()
        entry_count = ImmigrationRecord.objects.filter(entry_type='ENTRY').count()
        exit_count = ImmigrationRecord.objects.filter(entry_type='EXIT').count()
        
        by_purpose = {}
        for purpose_code, purpose_name in ImmigrationRecord.PURPOSE_CHOICES:
            by_purpose[purpose_code] = ImmigrationRecord.objects.filter(purpose=purpose_code).count()
        
        by_status = {}
        for status_code, status_name in ImmigrationRecord.STATUS_CHOICES:
            by_status[status_code] = ImmigrationRecord.objects.filter(status=status_code).count()
        
        return Response({
            'total': total_records,
            'by_entry_type': {
                'entry': entry_count,
                'exit': exit_count
            },
            'by_purpose': by_purpose,
            'by_status': by_status
        })
