from django.contrib import admin
from .models import ImmigrationRecord

@admin.register(ImmigrationRecord)
class ImmigrationRecordAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'passport_number', 'nationality', 'entry_type', 
                   'purpose', 'flight_number', 'date_of_entry_exit', 'status')
    list_filter = ('entry_type', 'purpose', 'status', 'nationality', 'date_of_entry_exit')
    search_fields = ('full_name', 'passport_number', 'visa_number', 'flight_number')
    date_hierarchy = 'date_of_entry_exit'
    
    fieldsets = (
        ('Thông tin cá nhân', {
            'fields': ('full_name', 'date_of_birth', 'gender', 'nationality', 
                      'passport_number', 'passport_expiry_date')
        }),
        ('Thông tin xuất/nhập cảnh', {
            'fields': ('entry_type', 'purpose', 'purpose_detail', 'date_of_entry_exit')
        }),
        ('Thông tin chuyến bay', {
            'fields': ('flight_number', 'airline')
        }),
        ('Thông tin xử lý', {
            'fields': ('status',)
        }),
        ('Thông tin bổ sung', {
            'fields': ('visa_number', 'address_in_country', 'contact_phone'),
            'classes': ('collapse',)
        }),
    )
    
    list_per_page = 20  # Số bản ghi hiển thị trên mỗi trang
    
    def get_readonly_fields(self, request, obj=None):
        # Một số trường không thể sửa sau khi đã tạo
        if obj:  # Nếu đang chỉnh sửa bản ghi đã tồn tại
            return ('passport_number', 'date_of_birth', 'entry_type', 'date_of_entry_exit')
        return ()
