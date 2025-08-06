from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, 
    TemplateView, FormView
)
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.db.models import Q, Count, Avg, Sum
from django.utils import timezone
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
import json
import csv
from datetime import datetime, timedelta
from decimal import Decimal

from .models import (
    NursingUnit, NursingShift, NursingAssessment, NursingCare,
    MedicationAdministration, NursingHandoff, PatientHandoff,
    NursingIncident, NursingSettings
)

class NursingDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'nursing/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Dashboard statistics
        context['total_units'] = NursingUnit.objects.count()
        context['active_units'] = NursingUnit.objects.filter(is_active=True).count()
        context['total_shifts'] = NursingShift.objects.count()
        context['active_shifts'] = NursingShift.objects.filter(status='in_progress').count()
        context['total_assessments'] = NursingAssessment.objects.count()
        context['total_care_activities'] = NursingCare.objects.count()
        context['pending_care'] = NursingCare.objects.filter(status='scheduled').count()
        context['total_medications'] = MedicationAdministration.objects.count()
        context['pending_medications'] = MedicationAdministration.objects.filter(status='scheduled').count()
        
        # Today's activities
        today = timezone.now().date()
        context['todays_shifts'] = NursingShift.objects.filter(shift_date=today).count()
        context['todays_assessments'] = NursingAssessment.objects.filter(assessment_date__date=today).count()
        context['todays_care'] = NursingCare.objects.filter(scheduled_time__date=today).count()
        
        # Recent activities
        context['recent_assessments'] = NursingAssessment.objects.order_by('-assessment_date')[:5]
        context['recent_incidents'] = NursingIncident.objects.order_by('-occurred_at')[:5]
        context['recent_handoffs'] = NursingHandoff.objects.order_by('-handoff_date')[:5]
        
        return context

# Nursing Unit Views
class NursingUnitListView(LoginRequiredMixin, ListView):
    model = NursingUnit
    template_name = 'nursing/unit_list.html'
    context_object_name = 'units'
    paginate_by = 20
    
    def get_queryset(self):
        return NursingUnit.objects.all().order_by('name')

class NursingUnitDetailView(LoginRequiredMixin, DetailView):
    model = NursingUnit
    template_name = 'nursing/unit_detail.html'

# Nursing Shift Views
class NursingShiftListView(LoginRequiredMixin, ListView):
    model = NursingShift
    template_name = 'nursing/shift_list.html'
    context_object_name = 'shifts'
    paginate_by = 20
    
    def get_queryset(self):
        return NursingShift.objects.select_related('nurse', 'unit').order_by('-shift_date', '-start_time')

class NursingShiftDetailView(LoginRequiredMixin, DetailView):
    model = NursingShift
    template_name = 'nursing/shift_detail.html'

# Nursing Assessment Views
class NursingAssessmentListView(LoginRequiredMixin, ListView):
    model = NursingAssessment
    template_name = 'nursing/assessment_list.html'
    context_object_name = 'assessments'
    paginate_by = 20
    
    def get_queryset(self):
        return NursingAssessment.objects.select_related('patient', 'nurse').order_by('-assessment_date')

class NursingAssessmentDetailView(LoginRequiredMixin, DetailView):
    model = NursingAssessment
    template_name = 'nursing/assessment_detail.html'

# Nursing Care Views
class NursingCareListView(LoginRequiredMixin, ListView):
    model = NursingCare
    template_name = 'nursing/care_list.html'
    context_object_name = 'care_activities'
    paginate_by = 20
    
    def get_queryset(self):
        return NursingCare.objects.select_related('patient', 'nurse').order_by('-scheduled_time')

class NursingCareDetailView(LoginRequiredMixin, DetailView):
    model = NursingCare
    template_name = 'nursing/care_detail.html'

# Medication Administration Views
class MedicationAdministrationListView(LoginRequiredMixin, ListView):
    model = MedicationAdministration
    template_name = 'nursing/medication_list.html'
    context_object_name = 'medications'
    paginate_by = 20
    
    def get_queryset(self):
        return MedicationAdministration.objects.select_related('patient', 'nurse').order_by('-scheduled_time')

class MedicationAdministrationDetailView(LoginRequiredMixin, DetailView):
    model = MedicationAdministration
    template_name = 'nursing/medication_detail.html'

# Nursing Handoff Views
class NursingHandoffListView(LoginRequiredMixin, ListView):
    model = NursingHandoff
    template_name = 'nursing/handoff_list.html'
    context_object_name = 'handoffs'
    paginate_by = 20
    
    def get_queryset(self):
        return NursingHandoff.objects.select_related('outgoing_nurse', 'incoming_nurse', 'unit').order_by('-handoff_date')

class NursingHandoffDetailView(LoginRequiredMixin, DetailView):
    model = NursingHandoff
    template_name = 'nursing/handoff_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient_handoffs'] = PatientHandoff.objects.filter(handoff=self.object)
        return context

# Nursing Incident Views
class NursingIncidentListView(LoginRequiredMixin, ListView):
    model = NursingIncident
    template_name = 'nursing/incident_list.html'
    context_object_name = 'incidents'
    paginate_by = 20
    
    def get_queryset(self):
        return NursingIncident.objects.select_related('patient', 'unit', 'reported_by').order_by('-occurred_at')

class NursingIncidentDetailView(LoginRequiredMixin, DetailView):
    model = NursingIncident
    template_name = 'nursing/incident_detail.html'

# Export Views
@login_required
def export_nursing_data(request):
    """Export nursing data to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="nursing_data.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Patient', 'Nurse', 'Assessment Date', 'Type'])
    
    assessments = NursingAssessment.objects.select_related('patient', 'nurse')
    for assessment in assessments:
        writer.writerow([
            f"{assessment.patient.first_name} {assessment.patient.last_name}",
            assessment.nurse.user.get_full_name(),
            assessment.assessment_date.strftime('%Y-%m-%d %H:%M'),
            assessment.assessment_type
        ])
    
    return response

# AJAX Views
@login_required
def get_patient_nursing_data(request):
    """Get patient nursing data for AJAX requests"""
    patient_id = request.GET.get('patient_id')
    if not patient_id:
        return JsonResponse({'error': 'Patient ID required'}, status=400)
    
    assessments = NursingAssessment.objects.filter(patient_id=patient_id).order_by('-assessment_date')
    data = []
    for assessment in assessments:
        data.append({
            'id': assessment.id,
            'date': assessment.assessment_date.strftime('%Y-%m-%d %H:%M'),
            'type': assessment.assessment_type,
            'nurse': assessment.nurse.user.get_full_name()
        })
    
    return JsonResponse({'assessments': data})

@login_required
def update_medication_status(request):
    """Update medication administration status via AJAX"""
    if request.method == 'POST':
        med_id = request.POST.get('medication_id')
        status = request.POST.get('status')
        
        if not med_id or not status:
            return JsonResponse({'error': 'Medication ID and status required'}, status=400)
        
        try:
            medication = MedicationAdministration.objects.get(id=med_id)
            medication.status = status
            if status == 'given':
                medication.administration_time = timezone.now()
            medication.save()
            
            return JsonResponse({'success': True, 'message': 'Medication status updated successfully'})
        except MedicationAdministration.DoesNotExist:
            return JsonResponse({'error': 'Medication record not found'}, status=404)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def get_unit_census(request):
    """Get unit census data for AJAX requests"""
    unit_id = request.GET.get('unit_id')
    if not unit_id:
        return JsonResponse({'error': 'Unit ID required'}, status=400)
    
    try:
        unit = NursingUnit.objects.get(id=unit_id)
        shifts = NursingShift.objects.filter(
            unit=unit,
            shift_date=timezone.now().date()
        ).select_related('nurse')
        
        data = {
            'unit_name': unit.name,
            'bed_capacity': unit.bed_capacity,
            'current_occupancy': unit.current_occupancy,
            'shifts': [
                {
                    'nurse': shift.nurse.user.get_full_name(),
                    'shift_type': shift.shift_type,
                    'status': shift.status
                } for shift in shifts
            ]
        }
        
        return JsonResponse(data)
    except NursingUnit.DoesNotExist:
        return JsonResponse({'error': 'Unit not found'}, status=404) 