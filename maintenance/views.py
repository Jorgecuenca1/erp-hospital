from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q, Sum, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from .models import MedicalEquipment, MaintenanceSchedule, MaintenanceRecord, MaintenanceAlert


@login_required
def maintenance_dashboard(request):
    """Maintenance dashboard view"""
    today = timezone.now().date()
    
    context = {
        'total_equipment': MedicalEquipment.objects.count(),
        'operational_equipment': MedicalEquipment.objects.filter(status='operational').count(),
        'maintenance_equipment': MedicalEquipment.objects.filter(status='maintenance').count(),
        'repair_equipment': MedicalEquipment.objects.filter(status='repair').count(),
        'due_maintenance': MaintenanceSchedule.objects.filter(next_maintenance__lte=today).count(),
        'overdue_maintenance': MaintenanceSchedule.objects.filter(next_maintenance__lt=today).count(),
        'recent_maintenance': MaintenanceRecord.objects.order_by('-maintenance_date')[:5],
        'alerts': MaintenanceAlert.objects.filter(is_read=False).order_by('-created_at')[:5],
        'equipment_by_status': MedicalEquipment.objects.values('status').annotate(count=Count('id')),
        'maintenance_by_type': MaintenanceRecord.objects.values('maintenance_type').annotate(count=Count('id'))[:5],
        'avg_downtime': MaintenanceRecord.objects.aggregate(avg_downtime=Avg('downtime_hours'))['avg_downtime'] or 0,
        'total_maintenance_cost': MaintenanceRecord.objects.aggregate(total_cost=Sum('cost'))['total_cost'] or 0
    }
    return render(request, 'maintenance/dashboard.html', context)


@login_required
def equipment_list(request):
    """List all medical equipment"""
    equipment = MedicalEquipment.objects.all().order_by('-created_at')
    return render(request, 'maintenance/equipment_list.html', {'equipment': equipment})


@login_required
def maintenance_schedule(request):
    """Maintenance schedule view"""
    schedules = MaintenanceSchedule.objects.all().order_by('next_maintenance')
    return render(request, 'maintenance/maintenance_schedule.html', {'schedules': schedules})


@login_required
def maintenance_records(request):
    """Maintenance records view"""
    records = MaintenanceRecord.objects.all().order_by('-maintenance_date')
    return render(request, 'maintenance/maintenance_records.html', {'records': records})


@login_required
def maintenance_alerts(request):
    """Maintenance alerts view"""
    alerts = MaintenanceAlert.objects.all().order_by('-created_at')
    return render(request, 'maintenance/maintenance_alerts.html', {'alerts': alerts})


@login_required
def equipment_detail(request, equipment_id):
    """Equipment detail view"""
    equipment = get_object_or_404(MedicalEquipment, id=equipment_id)
    maintenance_history = MaintenanceRecord.objects.filter(equipment=equipment).order_by('-maintenance_date')
    upcoming_maintenance = MaintenanceSchedule.objects.filter(equipment=equipment).order_by('next_maintenance')
    
    context = {
        'equipment': equipment,
        'maintenance_history': maintenance_history,
        'upcoming_maintenance': upcoming_maintenance
    }
    return render(request, 'maintenance/equipment_detail.html', context) 