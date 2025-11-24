from django import forms
from .models import Vehicle, AccessRecord


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['plate', 'type', 'owner', 'status', 'tech_review_due', 'capacity_kg']


class AccessRecordForm(forms.ModelForm):
    class Meta:
        model = AccessRecord
        fields = ['vehicle', 'driver_name', 'driver_rut', 'load_type', 'origin', 'destination']
