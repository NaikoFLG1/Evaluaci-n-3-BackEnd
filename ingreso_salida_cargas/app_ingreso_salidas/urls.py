from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehicleViewSet, AccessRecordViewSet
from .views_web import (
    login_view, logout_view, dashboard,
    vehicle_list, vehicle_create, vehicle_update, vehicle_delete,
    access_list, access_create, access_exit
)

router = DefaultRouter()
router.register(r'vehicles', VehicleViewSet, basename='vehicle')
router.register(r'access-records', AccessRecordViewSet, basename='accessrecord')

urlpatterns = [
    path('', include(router.urls)),
]
