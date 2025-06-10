from django.shortcuts import render
from rest_framework import viewsets, filters, permissions, status
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
from rest_framework.pagination import PageNumberPagination
import logging

class ImmigrationRecordViewSet(viewsets.ModelViewSet):
    """
    API endpoints để quản lý bản ghi xuất nhập cảnh
    

    """
    queryset = ImmigrationRecord.objects.all().order_by('-date_of_entry_exit')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['entry_type', 'purpose', 'status', 'nationality']
    search_fields = ['full_name', 'passport_number', 'visa_number', 'flight_number']
    ordering_fields = ['date_of_entry_exit', 'full_name', 'status']
    http_method_names = ['post']  # Chỉ cho phép phương thức POST
    
    def get_serializer_class(self):
        if self.action == 'list_records':
            return ImmigrationRecordListSerializer
        elif self.action in ['create', 'update_record', 'partial_update_record']:
            return ImmigrationRecordCreateSerializer
        return ImmigrationRecordDetailSerializer

    @swagger_auto_schema(
        operation_summary="Lấy danh sách bản ghi xuất nhập cảnh",
        operation_description="Trả về danh sách tất cả bản ghi xuất nhập cảnh với phân trang",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'page': openapi.Schema(type=openapi.TYPE_INTEGER, description="Số trang"),
                'search': openapi.Schema(type=openapi.TYPE_STRING, description="Tìm kiếm theo tên, số hộ chiếu, chuyến bay..."),
                'filters': openapi.Schema(type=openapi.TYPE_OBJECT, description="Các điều kiện lọc")
            }
        )
    )
    @action(detail=False, methods=['post'])
    def list_records(self, request):
        """Danh sách tất cả bản ghi xuất nhập cảnh"""
        logger = logging.getLogger(__name__)
        
        # Log request data
        logger.info(f"Received request data: {request.data}")
        
        # Lấy tham số từ request.data
        page = request.data.get('page', 1)
        search = request.data.get('search', '')
        filters = request.data.get('filters', {})
        
        logger.info(f"Processing request - Page: {page}, Search: {search}, Filters: {filters}")
        
        # Áp dụng bộ lọc
        queryset = self.get_queryset()
        logger.info(f"Initial queryset count: {queryset.count()}")
        
        # Áp dụng tìm kiếm nếu có
        if search:
            queryset = self.filter_queryset(queryset)
            logger.info(f"After search filter, queryset count: {queryset.count()}")
        
        # Áp dụng các bộ lọc bổ sung
        for field, value in filters.items():
            if field in self.filterset_fields:
                queryset = queryset.filter(**{field: value})
        
        logger.info(f"Final queryset count before pagination: {queryset.count()}")
        
        # Tạo paginator với kích thước trang cố định
        class CustomPagination(PageNumberPagination):
            page_size = 5
            page_query_param = 'page'
            
            def get_page_number(self, request, paginator):
                # Lấy số trang từ request.data thay vì query_params
                page_number = request.data.get(self.page_query_param, 1)
                try:
                    page_number = int(page_number)
                except (TypeError, ValueError):
                    page_number = 1
                return page_number
        
        try:
            # Thực hiện phân trang
            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset(queryset, request)
            logger.info(f"Paginated queryset size: {len(paginated_queryset) if paginated_queryset else 0}")
            
            # Serialize dữ liệu
            serializer = self.get_serializer(paginated_queryset, many=True)
            
            # Trả về response với thông tin phân trang
            response = paginator.get_paginated_response(serializer.data)
            logger.info(f"Response data count: {len(response.data['results'])}")
            return response
            
        except Exception as e:
            logger.error(f"Error during pagination: {str(e)}")
            return Response(
                {"error": "Lỗi khi phân trang dữ liệu"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        operation_summary="Xem chi tiết bản ghi xuất nhập cảnh",
        operation_description="Trả về thông tin chi tiết của một bản ghi xuất nhập cảnh",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID của bản ghi cần xem")
            },
            required=['id']
        )
    )
    @action(detail=False, methods=['post'])
    def get_record(self, request):
        """Chi tiết một bản ghi xuất nhập cảnh"""
        try:
            record = self.get_queryset().get(id=request.data.get('id'))
            serializer = self.get_serializer(record)
            return Response(serializer.data)
        except ImmigrationRecord.DoesNotExist:
            return Response(
                {"error": "Không tìm thấy bản ghi"},
                status=status.HTTP_404_NOT_FOUND
            )

    @swagger_auto_schema(
        operation_summary="Cập nhật bản ghi xuất nhập cảnh",
        operation_description="Cập nhật thông tin của một bản ghi xuất nhập cảnh",
        request_body=ImmigrationRecordCreateSerializer
    )
    @action(detail=False, methods=['post'])
    def update_record(self, request):
        """Cập nhật thông tin bản ghi xuất nhập cảnh"""
        try:
            record = self.get_queryset().get(id=request.data.get('id'))
            serializer = self.get_serializer(record, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except ImmigrationRecord.DoesNotExist:
            return Response(
                {"error": "Không tìm thấy bản ghi"},
                status=status.HTTP_404_NOT_FOUND
            )

    @swagger_auto_schema(
        operation_summary="Xóa bản ghi xuất nhập cảnh",
        operation_description="Xóa một bản ghi xuất nhập cảnh theo ID",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID của bản ghi cần xóa")
            },
            required=['id']
        )
    )
    @action(detail=False, methods=['post'])
    def delete_record(self, request):
        """Xóa bản ghi xuất nhập cảnh"""
        try:
            record = self.get_queryset().get(id=request.data.get('id'))
            record.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ImmigrationRecord.DoesNotExist:
            return Response(
                {"error": "Không tìm thấy bản ghi"},
                status=status.HTTP_404_NOT_FOUND
            )

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
    @action(detail=False, methods=['post'])
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
