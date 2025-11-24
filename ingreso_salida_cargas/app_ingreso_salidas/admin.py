from django.contrib import admin
from .models import Vehicle, AccessRecord


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('plate', 'type', 'owner', 'status', 'capacity_kg', 'tech_review_due')
    list_filter = ('status', 'type')
    search_fields = ('plate', 'owner')
    ordering = ('-created_at',)


@admin.register(AccessRecord)
class AccessRecordAdmin(admin.ModelAdmin):
    list_display = (
        'vehicle', 'driver_name', 'driver_rut', 
        'state', 'gate_in_at', 'gate_out_at', 'created_by'
    )
    list_filter = ('state', 'gate_in_at')
    search_fields = ('vehicle__plate', 'driver_name', 'driver_rut')
    readonly_fields = ('gate_in_at', 'created_by')
    ordering = ('-gate_in_at',)
