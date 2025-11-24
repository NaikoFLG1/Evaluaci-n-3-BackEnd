from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

class Vehicle(models.Model):
    plate = models.CharField(max_length=10, unique=True)
    type = models.CharField(max_length=20)  # truck, pickup, machinery
    owner = models.CharField(max_length=120, blank=True)
    status = models.CharField(max_length=12, default='active')  # active/inactive
    tech_review_due = models.DateField(null=True, blank=True)
    capacity_kg = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.plate} ({self.type})"

class AccessRecord(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT, related_name='access_records')
    driver_name = models.CharField(max_length=120)
    driver_rut = models.CharField(max_length=12)
    load_type = models.CharField(max_length=30)  
    origin = models.CharField(max_length=120)
    destination = models.CharField(max_length=120)
    state = models.CharField(max_length=20, default='en_planta')
    gate_in_at = models.DateTimeField(auto_now_add=True)
    gate_out_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.PROTECT)

    def clean(self):
        if self.gate_out_at and self.gate_out_at < self.gate_in_at:
            raise ValidationError({'gate_out_at': 'Debe ser posterior a gate_in_at'})