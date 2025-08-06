from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
import uuid
from .models import Ambulance, EmergencyCall, EmergencyCase, AmbulanceTrip


@receiver(pre_save, sender=Ambulance)
def generate_ambulance_number(sender, instance, **kwargs):
    """Generate unique ambulance number if not provided"""
    if not instance.ambulance_number:
        # Generate format: AMB-YYYY-XXXX
        year = timezone.now().year
        last_ambulance = Ambulance.objects.filter(
            ambulance_number__startswith=f'AMB-{year}'
        ).order_by('-ambulance_number').first()
        
        if last_ambulance:
            # Extract number and increment
            try:
                last_number = int(last_ambulance.ambulance_number.split('-')[2])
                new_number = last_number + 1
            except (ValueError, IndexError):
                new_number = 1
        else:
            new_number = 1
        
        instance.ambulance_number = f'AMB-{year}-{new_number:04d}'


@receiver(pre_save, sender=EmergencyCall)
def generate_call_number(sender, instance, **kwargs):
    """Generate unique call number if not provided"""
    if not instance.call_number:
        # Generate format: CALL-YYYYMMDD-XXXX
        today = timezone.now().date()
        date_str = today.strftime('%Y%m%d')
        
        last_call = EmergencyCall.objects.filter(
            call_number__startswith=f'CALL-{date_str}'
        ).order_by('-call_number').first()
        
        if last_call:
            try:
                last_number = int(last_call.call_number.split('-')[2])
                new_number = last_number + 1
            except (ValueError, IndexError):
                new_number = 1
        else:
            new_number = 1
        
        instance.call_number = f'CALL-{date_str}-{new_number:04d}'


@receiver(pre_save, sender=EmergencyCase)
def generate_case_number(sender, instance, **kwargs):
    """Generate unique case number if not provided"""
    if not instance.case_number:
        # Generate format: ER-YYYYMMDD-XXXX
        today = timezone.now().date()
        date_str = today.strftime('%Y%m%d')
        
        last_case = EmergencyCase.objects.filter(
            case_number__startswith=f'ER-{date_str}'
        ).order_by('-case_number').first()
        
        if last_case:
            try:
                last_number = int(last_case.case_number.split('-')[2])
                new_number = last_number + 1
            except (ValueError, IndexError):
                new_number = 1
        else:
            new_number = 1
        
        instance.case_number = f'ER-{date_str}-{new_number:04d}'


@receiver(pre_save, sender=AmbulanceTrip)
def generate_trip_number(sender, instance, **kwargs):
    """Generate unique trip number if not provided"""
    if not instance.trip_number:
        # Generate format: TRIP-YYYYMMDD-XXXX
        today = timezone.now().date()
        date_str = today.strftime('%Y%m%d')
        
        last_trip = AmbulanceTrip.objects.filter(
            trip_number__startswith=f'TRIP-{date_str}'
        ).order_by('-trip_number').first()
        
        if last_trip:
            try:
                last_number = int(last_trip.trip_number.split('-')[2])
                new_number = last_number + 1
            except (ValueError, IndexError):
                new_number = 1
        else:
            new_number = 1
        
        instance.trip_number = f'TRIP-{date_str}-{new_number:04d}' 