from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from datetime import date, timedelta
from .models import Vehicle, AccessRecord
from .forms import VehicleForm, AccessRecordForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido {user.username}')
            return redirect('dashboard')
        else:
            messages.error(request, 'Credenciales inválidas')
    
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'Sesión cerrada exitosamente')
    return redirect('login')


@login_required
def dashboard(request):
    today = date.today()
    
    context = {
        'total_vehicles': Vehicle.objects.count(),
        'active_vehicles': Vehicle.objects.filter(status='active').count(),
        'in_plant': AccessRecord.objects.filter(state='en_planta', gate_out_at__isnull=True).count(),
        'today_records': AccessRecord.objects.filter(gate_in_at__date=today).count(),
        'recent_records': AccessRecord.objects.select_related('vehicle').order_by('-gate_in_at')[:5],
        'expiring_vehicles': Vehicle.objects.filter(
            tech_review_due__lte=today + timedelta(days=30),
            tech_review_due__gte=today
        ).order_by('tech_review_due')[:5]
    }
    return render(request, 'dashboard.html', context)


@login_required
def vehicle_list(request):
    vehicles = Vehicle.objects.all().order_by('-created_at')
    today = date.today()
    next_month = today + timedelta(days=30)
    
    context = {
        'vehicles': vehicles,
        'today': today,
        'next_month': next_month
    }
    return render(request, 'vehicle_list.html', context)


@login_required
def vehicle_create(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehículo creado exitosamente')
            return redirect('vehicle_list')
    else:
        form = VehicleForm()
    
    return render(request, 'vehicle_form.html', {'form': form})


@login_required
def vehicle_update(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehículo actualizado exitosamente')
            return redirect('vehicle_list')
    else:
        form = VehicleForm(instance=vehicle)
    
    return render(request, 'vehicle_form.html', {'form': form})


@login_required
def vehicle_delete(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    vehicle.delete()
    messages.success(request, 'Vehículo eliminado exitosamente')
    return redirect('vehicle_list')


@login_required
def access_list(request):
    records = AccessRecord.objects.select_related('vehicle').all()
    
    state = request.GET.get('state')
    if state:
        records = records.filter(state=state)
    
    date_from = request.GET.get('date_from')
    if date_from:
        records = records.filter(gate_in_at__date__gte=date_from)
    
    date_to = request.GET.get('date_to')
    if date_to:
        records = records.filter(gate_in_at__date__lte=date_to)
    
    records = records.order_by('-gate_in_at')
    
    return render(request, 'access_list.html', {'records': records})


@login_required
def access_create(request):
    if request.method == 'POST':
        form = AccessRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.created_by = request.user
            record.save()
            messages.success(request, 'Registro de acceso creado exitosamente')
            return redirect('access_list')
    else:
        form = AccessRecordForm()
    
    vehicles = Vehicle.objects.filter(status='active').order_by('plate')
    return render(request, 'access_form.html', {'form': form, 'vehicles': vehicles})


@login_required
def access_exit(request, pk):
    record = get_object_or_404(AccessRecord, pk=pk)
    
    if record.gate_out_at:
        messages.warning(request, 'Este registro ya tiene salida registrada')
    else:
        record.gate_out_at = timezone.now()
        record.state = 'salida'
        record.save()
        messages.success(request, f'Salida registrada para {record.vehicle.plate}')
    
    return redirect('access_list')
