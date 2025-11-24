"""
URL configuration for ingreso_salida_cargas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app_ingreso_salidas.views_health import DBHealthView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from app_ingreso_salidas.views_web import (
    login_view, logout_view, dashboard,
    vehicle_list, vehicle_create, vehicle_update, vehicle_delete,
    access_list, access_create, access_exit
)

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    
    # Web Frontend
    path('', dashboard, name='dashboard'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    # Vehículos Web
    path('vehicles/', vehicle_list, name='vehicle_list'),
    path('vehicles/create/', vehicle_create, name='vehicle_create'),
    path('vehicles/<int:pk>/update/', vehicle_update, name='vehicle_update'),
    path('vehicles/<int:pk>/delete/', vehicle_delete, name='vehicle_delete'),
    
    # Registros de Acceso Web
    path('access/', access_list, name='access_list'),
    path('access/create/', access_create, name='access_create'),
    path('access/<int:pk>/exit/', access_exit, name='access_exit'),
    
    # API REST
    path('api/health/db/', DBHealthView.as_view()),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('app_ingreso_salidas.urls')),
]
