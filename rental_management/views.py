from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Avg
from .models import RentalEquipment, RentalAgreement, RentalPayment, RentalInspection


@login_required
def rental_dashboard(request):
    """Rental management dashboard"""
    context = {
        'total_equipment': RentalEquipment.objects.count(),
        'available_equipment': RentalEquipment.objects.filter(availability_status='available').count(),
        'active_rentals': RentalAgreement.objects.filter(status='active').count(),
        'total_revenue': RentalPayment.objects.aggregate(total=Sum('amount'))['total'] or 0,
        'recent_agreements': RentalAgreement.objects.order_by('-created_at')[:5],
        'equipment_by_category': RentalEquipment.objects.values('category').annotate(count=Count('id')),
        'overdue_rentals': RentalAgreement.objects.filter(status='overdue').count()
    }
    return render(request, 'rental_management/dashboard.html', context)


@login_required
def rental_equipment(request):
    """Rental equipment management"""
    equipment = RentalEquipment.objects.all().order_by('name')
    return render(request, 'rental_management/equipment.html', {'equipment': equipment})


@login_required
def rental_agreements(request):
    """Rental agreements management"""
    agreements = RentalAgreement.objects.all().order_by('-created_at')
    return render(request, 'rental_management/agreements.html', {'agreements': agreements})


@login_required
def rental_payments(request):
    """Rental payments management"""
    payments = RentalPayment.objects.all().order_by('-created_at')
    return render(request, 'rental_management/payments.html', {'payments': payments}) 