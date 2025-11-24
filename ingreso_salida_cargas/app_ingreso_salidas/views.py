from rest_framework import viewsets, status, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Vehicle, AccessRecord
from .serializers import VehicleSerializer, AccessRecordSerializer, AccessRecordCreateSerializer


class IsAdminOrReadCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'POST']:
            return True
        return request.user.is_staff


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all().order_by('-created_at')
    serializer_class = VehicleSerializer
    permission_classes = [IsAdminOrReadCreate]
    filter_backends = [filters.SearchFilter]
    search_fields = ['plate', 'status']
    
    def get_queryset(self):
        queryset = Vehicle.objects.all()
        
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        type_filter = self.request.query_params.get('type')
        if type_filter:
            queryset = queryset.filter(type=type_filter)
        
        return queryset

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        vehicle = self.get_object()
        vehicle.status = 'active'
        vehicle.save()
        return Response(self.get_serializer(vehicle).data)

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        vehicle = self.get_object()
        vehicle.status = 'inactive'
        vehicle.save()
        return Response(self.get_serializer(vehicle).data)


class AccessRecordViewSet(viewsets.ModelViewSet):
    queryset = AccessRecord.objects.select_related('vehicle', 'created_by').all().order_by('-gate_in_at')
    permission_classes = [IsAdminOrReadCreate]
    filter_backends = [filters.SearchFilter]
    search_fields = ['vehicle__plate', 'state', 'destination', 'origin']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return AccessRecordCreateSerializer
        return AccessRecordSerializer
    
    def get_queryset(self):
        queryset = AccessRecord.objects.select_related('vehicle', 'created_by').all()
        
        state_filter = self.request.query_params.get('state')
        if state_filter:
            queryset = queryset.filter(state=state_filter)
        
        vehicle_id = self.request.query_params.get('vehicle')
        if vehicle_id:
            queryset = queryset.filter(vehicle_id=vehicle_id)
        
        date_from = self.request.query_params.get('date_from')
        if date_from:
            queryset = queryset.filter(gate_in_at__gte=date_from)
        
        date_to = self.request.query_params.get('date_to')
        if date_to:
            queryset = queryset.filter(gate_in_at__lte=date_to)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def register_exit(self, request, pk=None):
        record = self.get_object()
        
        if record.gate_out_at:
            return Response(
                {'error': 'Este registro ya tiene salida registrada'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        record.gate_out_at = timezone.now()
        record.state = 'salida'
        record.save()
        
        return Response(self.get_serializer(record).data)

    @action(detail=False, methods=['get'])
    def vehicles_in_plant(self, request):
        records = self.get_queryset().filter(state='en_planta', gate_out_at__isnull=True)
        return Response(self.get_serializer(records, many=True).data)
