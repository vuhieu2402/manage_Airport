from django.urls import path
from .views import ImmigrationRecordViewSet

urlpatterns = [
    # List records
    path('api/list/', ImmigrationRecordViewSet.as_view({'post': 'list_records'})),
    
    # Get single record
    path('api/detail/', ImmigrationRecordViewSet.as_view({'post': 'get_record'})),
    
    # Create record
    path('api/create/', ImmigrationRecordViewSet.as_view({'post': 'create'})),
    
    # Update record
    path('api/update/', ImmigrationRecordViewSet.as_view({'post': 'update_record'})),
    
    # Delete record
    path('api/delete/', ImmigrationRecordViewSet.as_view({'post': 'delete_record'})),
    
    # Statistics
    path('api/statistics/', ImmigrationRecordViewSet.as_view({'post': 'statistics'})),
]
