from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ImmigrationRecordViewSet

router = DefaultRouter()
router.register('records', ImmigrationRecordViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
