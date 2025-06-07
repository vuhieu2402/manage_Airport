from django.db import models
from django.utils import timezone

class ImmigrationRecord(models.Model):
    """Bản ghi xuất nhập cảnh"""
    ENTRY_TYPE_CHOICES = [
        ('ENTRY', 'Nhập cảnh'),
        ('EXIT', 'Xuất cảnh')
    ]
    
    PURPOSE_CHOICES = [
        ('TOURISM', 'Du lịch'),
        ('BUSINESS', 'Công việc'),
        ('STUDY', 'Học tập'),
        ('VISIT', 'Thăm thân'),
        ('DIPLOMATIC', 'Ngoại giao'),
        ('OTHER', 'Khác')
    ]
    
    STATUS_CHOICES = [
        ('APPROVED', 'Đã duyệt'),
        ('REJECTED', 'Từ chối'),
        ('PENDING', 'Đang xử lý')
    ]
    
    # Thông tin cơ bản
    full_name = models.CharField(max_length=100, verbose_name="Họ và tên")
    date_of_birth = models.DateField(verbose_name="Ngày sinh")
    gender = models.CharField(
        max_length=1,
        choices=[('M', 'Nam'), ('F', 'Nữ'), ('O', 'Khác')],
        verbose_name="Giới tính"
    )
    nationality = models.CharField(max_length=100, verbose_name="Quốc tịch")
    passport_number = models.CharField(max_length=20, verbose_name="Số hộ chiếu")
    passport_expiry_date = models.DateField(verbose_name="Ngày hết hạn hộ chiếu")
    
    # Thông tin xuất/nhập cảnh
    entry_type = models.CharField(
        max_length=5, 
        choices=ENTRY_TYPE_CHOICES,
        verbose_name="Loại cửa khẩu"
    )
    purpose = models.CharField(
        max_length=10,
        choices=PURPOSE_CHOICES,
        verbose_name="Mục đích"
    )
    purpose_detail = models.TextField(blank=True, null=True, verbose_name="Chi tiết mục đích")
    
    # Thông tin chuyến bay
    flight_number = models.CharField(max_length=20, verbose_name="Số hiệu chuyến bay")
    airline = models.CharField(max_length=100, verbose_name="Hãng hàng không")
    
    # Thông tin thời gian
    date_of_entry_exit = models.DateTimeField(verbose_name="Thời gian xuất/nhập cảnh")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Thời gian tạo bản ghi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Thời gian cập nhật")
    
    # Thông tin xử lý
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING',
        verbose_name="Trạng thái"
    )

    
    # Thông tin bổ sung
    visa_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Số thị thực")
    address_in_country = models.TextField(blank=True, null=True, verbose_name="Địa chỉ lưu trú")
    contact_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Số điện thoại liên hệ")
    
    def __str__(self):
        action = "Nhập cảnh" if self.entry_type == 'ENTRY' else "Xuất cảnh"
        return f"{action} - {self.full_name} - {self.passport_number}"
    
    class Meta:
        verbose_name = "Bản ghi xuất nhập cảnh"
        verbose_name_plural = "Bản ghi xuất nhập cảnh"
        ordering = ['-date_of_entry_exit']


