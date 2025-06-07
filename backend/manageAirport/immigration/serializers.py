from rest_framework import serializers
from .models import ImmigrationRecord

class ImmigrationRecordListSerializer(serializers.ModelSerializer):
    """Serializer cho danh sách bản ghi xuất nhập cảnh (hiển thị ngắn gọn)"""
    
    class Meta:
        model = ImmigrationRecord
        fields = ('id', 'full_name', 'passport_number', 'nationality', 'entry_type', 
                 'purpose', 'flight_number', 'date_of_entry_exit', 'status')
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['entry_type_display'] = instance.get_entry_type_display()
        representation['purpose_display'] = instance.get_purpose_display()
        representation['status_display'] = instance.get_status_display()
        return representation

class ImmigrationRecordDetailSerializer(serializers.ModelSerializer):
    """Serializer chi tiết cho một bản ghi xuất nhập cảnh"""
    
    entry_type_display = serializers.SerializerMethodField()
    purpose_display = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    gender_display = serializers.SerializerMethodField()
    
    class Meta:
        model = ImmigrationRecord
        fields = '__all__'
        extra_fields = ['entry_type_display', 'purpose_display', 'status_display', 'gender_display']
    
    def get_entry_type_display(self, obj):
        return obj.get_entry_type_display()
    
    def get_purpose_display(self, obj):
        return obj.get_purpose_display()
    
    def get_status_display(self, obj):
        return obj.get_status_display()
        
    def get_gender_display(self, obj):
        return obj.get_gender_display()
    
class ImmigrationRecordCreateSerializer(serializers.ModelSerializer):
    """Serializer để tạo bản ghi xuất nhập cảnh mới"""
    
    class Meta:
        model = ImmigrationRecord
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def validate_passport_expiry_date(self, value):
        """Kiểm tra ngày hết hạn hộ chiếu phải lớn hơn ngày hiện tại"""
        from django.utils import timezone
        if value <= timezone.now().date():
            raise serializers.ValidationError("Hộ chiếu đã hết hạn")
        return value
    
    def validate(self, data):
        """Kiểm tra các trường dữ liệu liên quan"""
        if data.get('date_of_birth') and data.get('date_of_entry_exit'):
            if data['date_of_birth'].year > data['date_of_entry_exit'].year - 18 and data.get('purpose') == 'BUSINESS':
                raise serializers.ValidationError("Người dưới 18 tuổi không thể đi công tác")
        
        return data
