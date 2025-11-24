from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class Vehicle(models.Model):
    class VehicleType(models.TextChoices):
        TRUCK = 'truck', 'Camión'
        PICKUP = 'pickup', 'Camioneta'
        MACHINERY = 'machinery', 'Maquinaria'
    
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Activo'
        INACTIVE = 'inactive', 'Inactivo'
    
    plate = models.CharField(max_length=10, unique=True, verbose_name='Patente')
    type = models.CharField(max_length=20, choices=VehicleType.choices, verbose_name='Tipo')
    owner = models.CharField(max_length=120, blank=True, verbose_name='Propietario')
    status = models.CharField(
        max_length=12, 
        choices=Status.choices, 
        default=Status.ACTIVE,
        verbose_name='Estado'
    )
    tech_review_due = models.DateField(
        null=True, 
        blank=True,
        verbose_name='Vencimiento Revisión Técnica'
    )
    capacity_kg = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Capacidad (kg)'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado el')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Actualizado el')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Vehículo'
        verbose_name_plural = 'Vehículos'
        indexes = [
            models.Index(fields=['plate']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.plate} ({self.get_type_display()})"


class AccessRecord(models.Model):
    class State(models.TextChoices):
        EN_PLANTA = 'en_planta', 'En Planta'
        SALIDA = 'salida', 'Salida'
    
    vehicle = models.ForeignKey(
        Vehicle, 
        on_delete=models.PROTECT, 
        related_name='access_records',
        verbose_name='Vehículo'
    )
    driver_name = models.CharField(max_length=120, verbose_name='Nombre Conductor')
    driver_rut = models.CharField(max_length=12, verbose_name='RUT Conductor')
    load_type = models.CharField(max_length=30, verbose_name='Tipo de Carga')
    origin = models.CharField(max_length=120, verbose_name='Origen')
    destination = models.CharField(max_length=120, verbose_name='Destino')
    state = models.CharField(
        max_length=20, 
        choices=State.choices, 
        default=State.EN_PLANTA,
        verbose_name='Estado'
    )
    gate_in_at = models.DateTimeField(auto_now_add=True, verbose_name='Hora de Ingreso')
    gate_out_at = models.DateTimeField(
        null=True, 
        blank=True,
        verbose_name='Hora de Salida'
    )
    created_by = models.ForeignKey(
        'auth.User', 
        on_delete=models.PROTECT,
        verbose_name='Creado por'
    )

    class Meta:
        ordering = ['-gate_in_at']
        verbose_name = 'Registro de Acceso'
        verbose_name_plural = 'Registros de Acceso'
        indexes = [
            models.Index(fields=['vehicle', 'gate_in_at']),
            models.Index(fields=['state']),
            models.Index(fields=['-gate_in_at']),
        ]

    def clean(self):
        if self.gate_out_at and self.gate_out_at < self.gate_in_at:
            raise ValidationError({
                'gate_out_at': 'La hora de salida debe ser posterior a la hora de ingreso'
            })

    def __str__(self):
        return f"{self.vehicle.plate} - {self.driver_name} ({self.gate_in_at.strftime('%Y-%m-%d %H:%M')})"