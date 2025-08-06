from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Avg
from .models import ResourceType, ResourceAllocation, StaffSchedule, CapacityPlanning


@login_required
def planning_dashboard(request):
    """Planning dashboard view"""
    context = {
        'total_resources': ResourceType.objects.filter(is_active=True).count(),
        'active_allocations': ResourceAllocation.objects.filter(status='allocated').count(),
        'staff_schedules': StaffSchedule.objects.filter(status='scheduled').count(),
        'capacity_plans': CapacityPlanning.objects.count(),
        'recent_allocations': ResourceAllocation.objects.order_by('-created_at')[:5],
        'resource_by_category': ResourceType.objects.values('category').annotate(count=Count('id')),
        'utilization_avg': CapacityPlanning.objects.aggregate(avg_util=Avg('utilization_rate'))['avg_util'] or 0
    }
    return render(request, 'planning/dashboard.html', context)


@login_required
def resource_allocation(request):
    """Resource allocation view"""
    allocations = ResourceAllocation.objects.all().order_by('-created_at')
    return render(request, 'planning/resource_allocation.html', {'allocations': allocations})


@login_required
def staff_scheduling(request):
    """Staff scheduling view"""
    schedules = StaffSchedule.objects.all().order_by('-start_datetime')
    return render(request, 'planning/staff_scheduling.html', {'schedules': schedules})


@login_required
def capacity_planning(request):
    """Capacity planning view"""
    capacity_plans = CapacityPlanning.objects.all().order_by('-created_at')
    return render(request, 'planning/capacity_planning.html', {'capacity_plans': capacity_plans}) 