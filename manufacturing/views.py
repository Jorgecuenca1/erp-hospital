from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from .models import MedicalDevice, ProductionOrder, QualityCheck, BillOfMaterials


@login_required
def manufacturing_dashboard(request):
    """Manufacturing dashboard view"""
    context = {
        'total_devices': MedicalDevice.objects.count(),
        'active_orders': ProductionOrder.objects.filter(status='in_progress').count(),
        'completed_orders': ProductionOrder.objects.filter(status='completed').count(),
        'quality_checks': QualityCheck.objects.filter(result='pending').count(),
        'recent_orders': ProductionOrder.objects.order_by('-created_at')[:5],
        'device_types': MedicalDevice.objects.values('device_type').annotate(count=Count('id'))[:5],
        'quality_stats': {
            'passed': QualityCheck.objects.filter(result='passed').count(),
            'failed': QualityCheck.objects.filter(result='failed').count(),
            'pending': QualityCheck.objects.filter(result='pending').count(),
        }
    }
    return render(request, 'manufacturing/dashboard.html', context)


@login_required
def device_list(request):
    """List all medical devices"""
    devices = MedicalDevice.objects.all().order_by('-created_at')
    return render(request, 'manufacturing/device_list.html', {'devices': devices})


@login_required
def production_orders(request):
    """List all production orders"""
    orders = ProductionOrder.objects.all().order_by('-created_at')
    return render(request, 'manufacturing/production_orders.html', {'orders': orders})


@login_required
def quality_control(request):
    """Quality control dashboard"""
    quality_checks = QualityCheck.objects.all().order_by('-checked_at')
    return render(request, 'manufacturing/quality_control.html', {'quality_checks': quality_checks})


@login_required
def bill_of_materials(request):
    """Bill of materials management"""
    bom_items = BillOfMaterials.objects.all().order_by('device__name')
    return render(request, 'manufacturing/bill_of_materials.html', {'bom_items': bom_items}) 