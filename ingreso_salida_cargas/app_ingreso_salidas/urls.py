from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehicleViewSet, AccessRecordViewSet

router = DefaultRouter()
router.register(r'vehicles', VehicleViewSet, basename='vehicle')
router.register(r'access-records', AccessRecordViewSet, basename='accessrecord')

urlpatterns = [
    path('', include(router.urls)),
]
