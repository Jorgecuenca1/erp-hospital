from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Sum, Count
from django.utils import timezone
from django.core.paginator import Paginator
from .models import (
    LabTestCategory, LabTest, LabEquipment, LabTestOrder, LabTestOrderItem,
    LabSample, LabResult, LabReport, LabQualityControl, LabWorkshift
)
from .forms import (
    LabTestOrderForm, LabSampleForm, LabResultForm, LabReportForm,
    LabQualityControlForm, LabWorkshiftForm
)


@login_required
def laboratory_dashboard(request):
    """Laboratory Dashboard with statistics and pending tasks"""
    today = timezone.now().date()
    
    # Statistics
    stats = {
        'pending_orders': LabTestOrder.objects.filter(status='PENDING').count(),
        'samples_collected': LabSample.objects.filter(collection_date__date=today).count(),
        'tests_completed': LabResult.objects.filter(test_date__date=today, status='FINAL').count(),
        'pending_reports': LabReport.objects.filter(status='DRAFT').count(),
        'active_equipment': LabEquipment.objects.filter(status='ACTIVE').count(),
        'maintenance_due': LabEquipment.objects.filter(
            next_maintenance_date__lte=today,
            status='ACTIVE'
        ).count(),
    }
    
    # Recent orders
    recent_orders = LabTestOrder.objects.select_related(
        'patient', 'ordered_by__user'
    ).order_by('-order_date')[:10]
    
    # Pending samples
    pending_samples = LabSample.objects.filter(
        status__in=['COLLECTED', 'RECEIVED']
    ).select_related('order__patient')[:10]
    
    # Critical results
    critical_results = LabResult.objects.filter(
        critical_flag=True,
        status='FINAL'
    ).select_related('order_item__test', 'sample__order__patient')[:10]
    
    context = {
        'stats': stats,
        'recent_orders': recent_orders,
        'pending_samples': pending_samples,
        'critical_results': critical_results,
    }
    
    return render(request, 'acs_hms_laboratory/dashboard.html', context)


@login_required
def lab_test_list(request):
    """List of available lab tests"""
    tests = LabTest.objects.filter(is_active=True).select_related('category')
    category_filter = request.GET.get('category')
    search = request.GET.get('search')
    
    if category_filter:
        tests = tests.filter(category_id=category_filter)
    
    if search:
        tests = tests.filter(
            Q(name__icontains=search) | 
            Q(code__icontains=search) |
            Q(description__icontains=search)
        )
    
    paginator = Paginator(tests, 20)
    page = request.GET.get('page')
    tests = paginator.get_page(page)
    
    categories = LabTestCategory.objects.filter(is_active=True)
    
    context = {
        'tests': tests,
        'categories': categories,
        'current_category': category_filter,
        'search': search,
    }
    
    return render(request, 'acs_hms_laboratory/test_list.html', context)


@login_required
def create_lab_order(request):
    """Create new lab test order"""
    if request.method == 'POST':
        form = LabTestOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.ordered_by = request.user.hms_profile
            order.save()
            
            # Create order items for selected tests
            tests = form.cleaned_data['tests']
            total_amount = 0
            
            for test in tests:
                order_item = LabTestOrderItem.objects.create(
                    order=order,
                    test=test,
                    quantity=1,
                    unit_price=test.price,
                    total_price=test.price
                )
                total_amount += test.price
            
            order.total_amount = total_amount
            order.save()
            
            messages.success(request, f'Lab order {order.order_number} created successfully!')
            return redirect('acs_hms_laboratory:order_detail', order_id=order.id)
    else:
        form = LabTestOrderForm()
    
    return render(request, 'acs_hms_laboratory/create_order.html', {'form': form})


@login_required
def lab_order_detail(request, order_id):
    """Lab order detail view"""
    order = get_object_or_404(LabTestOrder, id=order_id)
    order_items = order.test_items.select_related('test')
    samples = order.samples.all()
    
    context = {
        'order': order,
        'order_items': order_items,
        'samples': samples,
    }
    
    return render(request, 'acs_hms_laboratory/order_detail.html', context)


@login_required
def collect_sample(request, order_id):
    """Collect sample for lab order"""
    order = get_object_or_404(LabTestOrder, id=order_id)
    
    if request.method == 'POST':
        form = LabSampleForm(request.POST)
        if form.is_valid():
            sample = form.save(commit=False)
            sample.order = order
            sample.collected_by = request.user.hms_profile
            sample.save()
            
            order.status = 'SAMPLE_COLLECTED'
            order.sample_collected_date = timezone.now()
            order.collected_by = request.user.hms_profile
            order.save()
            
            messages.success(request, f'Sample {sample.sample_number} collected successfully!')
            return redirect('acs_hms_laboratory:order_detail', order_id=order.id)
    else:
        form = LabSampleForm()
    
    context = {
        'form': form,
        'order': order,
    }
    
    return render(request, 'acs_hms_laboratory/collect_sample.html', context)


@login_required
def lab_results_list(request):
    """List of lab results"""
    results = LabResult.objects.select_related(
        'order_item__test', 
        'sample__order__patient'
    ).order_by('-test_date')
    
    status_filter = request.GET.get('status')
    search = request.GET.get('search')
    
    if status_filter:
        results = results.filter(status=status_filter)
    
    if search:
        results = results.filter(
            Q(sample__order__patient__first_name__icontains=search) |
            Q(sample__order__patient__last_name__icontains=search) |
            Q(order_item__test__name__icontains=search) |
            Q(sample__sample_number__icontains=search)
        )
    
    paginator = Paginator(results, 20)
    page = request.GET.get('page')
    results = paginator.get_page(page)
    
    context = {
        'results': results,
        'status_filter': status_filter,
        'search': search,
    }
    
    return render(request, 'acs_hms_laboratory/results_list.html', context)


@login_required
def enter_result(request, order_item_id):
    """Enter test result"""
    order_item = get_object_or_404(LabTestOrderItem, id=order_item_id)
    sample = order_item.order.samples.first()
    
    try:
        result = LabResult.objects.get(order_item=order_item)
    except LabResult.DoesNotExist:
        result = None
    
    if request.method == 'POST':
        form = LabResultForm(request.POST, instance=result)
        if form.is_valid():
            result = form.save(commit=False)
            result.order_item = order_item
            result.sample = sample
            result.tested_by = request.user.hms_profile
            result.test_date = timezone.now()
            result.save()
            
            # Update order item status
            order_item.status = 'COMPLETED'
            order_item.save()
            
            messages.success(request, 'Test result entered successfully!')
            return redirect('acs_hms_laboratory:results_list')
    else:
        form = LabResultForm(instance=result)
    
    context = {
        'form': form,
        'order_item': order_item,
        'sample': sample,
        'result': result,
    }
    
    return render(request, 'acs_hms_laboratory/enter_result.html', context)


@login_required
def generate_report(request, order_id):
    """Generate lab report"""
    order = get_object_or_404(LabTestOrder, id=order_id)
    
    try:
        report = LabReport.objects.get(order=order)
    except LabReport.DoesNotExist:
        report = None
    
    if request.method == 'POST':
        form = LabReportForm(request.POST, instance=report)
        if form.is_valid():
            report = form.save(commit=False)
            report.order = order
            report.generated_by = request.user.hms_profile
            report.save()
            
            messages.success(request, f'Report {report.report_number} generated successfully!')
            return redirect('acs_hms_laboratory:report_detail', report_id=report.id)
    else:
        form = LabReportForm(instance=report)
    
    # Get all results for this order
    results = LabResult.objects.filter(
        order_item__order=order,
        status='FINAL'
    ).select_related('order_item__test')
    
    context = {
        'form': form,
        'order': order,
        'results': results,
        'report': report,
    }
    
    return render(request, 'acs_hms_laboratory/generate_report.html', context)


@login_required
def report_detail(request, report_id):
    """Lab report detail view"""
    report = get_object_or_404(LabReport, id=report_id)
    results = LabResult.objects.filter(
        order_item__order=report.order,
        status='FINAL'
    ).select_related('order_item__test')
    
    context = {
        'report': report,
        'results': results,
    }
    
    return render(request, 'acs_hms_laboratory/report_detail.html', context)


@login_required
def equipment_list(request):
    """List of lab equipment"""
    equipment = LabEquipment.objects.select_related('department')
    
    status_filter = request.GET.get('status')
    search = request.GET.get('search')
    
    if status_filter:
        equipment = equipment.filter(status=status_filter)
    
    if search:
        equipment = equipment.filter(
            Q(name__icontains=search) |
            Q(model__icontains=search) |
            Q(serial_number__icontains=search)
        )
    
    paginator = Paginator(equipment, 20)
    page = request.GET.get('page')
    equipment = paginator.get_page(page)
    
    context = {
        'equipment': equipment,
        'status_filter': status_filter,
        'search': search,
    }
    
    return render(request, 'acs_hms_laboratory/equipment_list.html', context)


@login_required
def quality_control_list(request):
    """List of quality control records"""
    qc_records = LabQualityControl.objects.select_related(
        'equipment', 'performed_by__user'
    ).order_by('-qc_date')
    
    paginator = Paginator(qc_records, 20)
    page = request.GET.get('page')
    qc_records = paginator.get_page(page)
    
    context = {
        'qc_records': qc_records,
    }
    
    return render(request, 'acs_hms_laboratory/quality_control_list.html', context)


@login_required
def create_quality_control(request):
    """Create quality control record"""
    if request.method == 'POST':
        form = LabQualityControlForm(request.POST)
        if form.is_valid():
            qc = form.save(commit=False)
            qc.performed_by = request.user.hms_profile
            qc.save()
            
            messages.success(request, 'Quality control record created successfully!')
            return redirect('acs_hms_laboratory:quality_control_list')
    else:
        form = LabQualityControlForm()
    
    return render(request, 'acs_hms_laboratory/create_quality_control.html', {'form': form})


@login_required
def workshift_list(request):
    """List of work shifts"""
    shifts = LabWorkshift.objects.select_related(
        'supervisor__user'
    ).order_by('-shift_date')
    
    paginator = Paginator(shifts, 20)
    page = request.GET.get('page')
    shifts = paginator.get_page(page)
    
    context = {
        'shifts': shifts,
    }
    
    return render(request, 'acs_hms_laboratory/workshift_list.html', context)


@login_required
def create_workshift(request):
    """Create work shift"""
    if request.method == 'POST':
        form = LabWorkshiftForm(request.POST)
        if form.is_valid():
            shift = form.save()
            
            messages.success(request, 'Work shift created successfully!')
            return redirect('acs_hms_laboratory:workshift_list')
    else:
        form = LabWorkshiftForm()
    
    return render(request, 'acs_hms_laboratory/create_workshift.html', {'form': form})


@login_required
def get_test_price(request, test_id):
    """AJAX endpoint to get test price"""
    try:
        test = LabTest.objects.get(id=test_id)
        return JsonResponse({
            'price': float(test.price),
            'name': test.name,
            'code': test.code
        })
    except LabTest.DoesNotExist:
        return JsonResponse({'error': 'Test not found'}, status=404) 