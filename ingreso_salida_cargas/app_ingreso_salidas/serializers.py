from rest_framework import serializers
from .models import Vehicle, AccessRecord
from .validators import validate_plate, validate_rut
from datetime import date


class VehicleSerializer(serializers.ModelSerializer):
    plate = serializers.CharField(validators=[validate_plate])

    class Meta:
        model = Vehicle
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def validate(self, attrs):
        status = attrs.get('status', getattr(self.instance, 'status', 'active'))
        due = attrs.get('tech_review_due', getattr(self.instance, 'tech_review_due', None))
        
        if status == 'active' and due and due < date.today():
            raise serializers.ValidationError({
                'tech_review_due': 'No se puede activar un vehículo con revisión técnica vencida'
            })
        
        return attrs


class AccessRecordSerializer(serializers.ModelSerializer):
    driver_rut = serializers.CharField(validators=[validate_rut])
    vehicle_plate = serializers.CharField(source='vehicle.plate', read_only=True)
    vehicle_type = serializers.CharField(source='vehicle.get_type_display', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = AccessRecord
        fields = '__all__'
        read_only_fields = ('gate_in_at', 'created_by')

    def validate(self, attrs):
        vehicle = attrs.get('vehicle', getattr(self.instance, 'vehicle', None))
        gate_out = attrs.get('gate_out_at')
        
        if vehicle and vehicle.status != 'active':
            raise serializers.ValidationError({
                'vehicle': 'No se puede registrar acceso con un vehículo inactivo'
            })
        
        if gate_out and self.instance and gate_out < self.instance.gate_in_at:
            raise serializers.ValidationError({
                'gate_out_at': 'La hora de salida debe ser posterior a la hora de ingreso'
            })
        
        return attrs


class AccessRecordCreateSerializer(serializers.ModelSerializer):
    driver_rut = serializers.CharField(validators=[validate_rut])

    class Meta:
        model = AccessRecord
        fields = ['vehicle', 'driver_name', 'driver_rut', 'load_type', 'origin', 'destination']

    def validate_vehicle(self, value):
        if value.status != 'active':
            raise serializers.ValidationError('No se puede registrar acceso con un vehículo inactivo')
        return value
