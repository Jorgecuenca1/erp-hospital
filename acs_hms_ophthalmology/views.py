from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q, Count
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import (
    EyeExamination, OphthalmologyProcedure, EyeDisease, OpticalPrescription,
    VisualFieldTest, OphthalmologyEquipment
)

class OphthalmologyDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_ophthalmology/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Ophthalmology'
        context['module_type'] = 'hms'
        
        # Estadísticas del dashboard
        today = timezone.now().date()
        this_month = timezone.now().replace(day=1).date()
        
        context['total_patients'] = EyeExamination.objects.values('patient').distinct().count()
        context['examinations_today'] = EyeExamination.objects.filter(examination_date__date=today).count()
        context['scheduled_procedures'] = OphthalmologyProcedure.objects.filter(
            scheduled_date__date=today, status='SCHEDULED'
        ).count()
        context['eye_examinations'] = EyeExamination.objects.filter(examination_date__date__gte=this_month).count()
        context['prescriptions'] = OpticalPrescription.objects.filter(prescription_date__gte=this_month).count()
        context['visual_field_tests'] = VisualFieldTest.objects.filter(test_date__date__gte=this_month).count()
        context['todays_procedures'] = OphthalmologyProcedure.objects.filter(scheduled_date__date=today).count()
        
        # Procedimientos de hoy
        context['today_procedures'] = OphthalmologyProcedure.objects.filter(
            scheduled_date__date=today
        ).select_related('patient', 'primary_surgeon').order_by('scheduled_date')
        
        # Exámenes recientes
        context['recent_examinations'] = EyeExamination.objects.select_related(
            'patient', 'ophthalmologist'
        ).order_by('-examination_date')[:5]
        
        # Estado de equipos
        context['equipment_status'] = OphthalmologyEquipment.objects.values('status').annotate(
            count=Count('id')
        )
        
        return context

# Vistas para EyeExamination
class EyeExaminationListView(LoginRequiredMixin, ListView):
    model = EyeExamination
    template_name = 'acs_hms_ophthalmology/examination_list.html'
    context_object_name = 'examinations'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = EyeExamination.objects.select_related('patient', 'ophthalmologist').order_by('-examination_date')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(patient__first_name__icontains=search) |
                Q(patient__last_name__icontains=search) |
                Q(examination_number__icontains=search) |
                Q(diagnosis__icontains=search)
            )
        return queryset

class EyeExaminationDetailView(LoginRequiredMixin, DetailView):
    model = EyeExamination
    template_name = 'acs_hms_ophthalmology/examination_detail.html'
    context_object_name = 'examination'

class EyeExaminationCreateView(LoginRequiredMixin, CreateView):
    model = EyeExamination
    template_name = 'acs_hms_ophthalmology/examination_form.html'
    fields = [
        'patient', 'appointment', 'ophthalmologist', 'chief_complaint', 'history_present_illness',
        'va_right_uncorrected', 'va_left_uncorrected', 'va_right_corrected', 'va_left_corrected',
        'sphere_right', 'cylinder_right', 'axis_right', 'sphere_left', 'cylinder_left', 'axis_left',
        'iop_right', 'iop_left', 'iop_method', 'diagnosis', 'treatment_plan', 'medications', 'follow_up_date'
    ]
    success_url = reverse_lazy('ophthalmology:examination_list')
    
    def form_valid(self, form):
        # Auto-generar número de examen
        if not form.instance.examination_number:
            last_exam = EyeExamination.objects.order_by('-id').first()
            if last_exam:
                try:
                    last_number = int(last_exam.examination_number.split('-')[-1])
                    form.instance.examination_number = f"EYE-{last_number + 1:06d}"
                except:
                    form.instance.examination_number = "EYE-000001"
            else:
                form.instance.examination_number = "EYE-000001"
        
        messages.success(self.request, 'Examen oftalmológico creado exitosamente.')
        return super().form_valid(form)

class EyeExaminationUpdateView(LoginRequiredMixin, UpdateView):
    model = EyeExamination
    template_name = 'acs_hms_ophthalmology/examination_form.html'
    fields = [
        'patient', 'appointment', 'ophthalmologist', 'chief_complaint', 'history_present_illness',
        'va_right_uncorrected', 'va_left_uncorrected', 'va_right_corrected', 'va_left_corrected',
        'sphere_right', 'cylinder_right', 'axis_right', 'sphere_left', 'cylinder_left', 'axis_left',
        'iop_right', 'iop_left', 'iop_method', 'diagnosis', 'treatment_plan', 'medications', 'follow_up_date'
    ]
    success_url = reverse_lazy('ophthalmology:examination_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Examen oftalmológico actualizado exitosamente.')
        return super().form_valid(form)

class EyeExaminationDeleteView(LoginRequiredMixin, DeleteView):
    model = EyeExamination
    template_name = 'acs_hms_ophthalmology/examination_confirm_delete.html'
    success_url = reverse_lazy('ophthalmology:examination_list')

# Vistas para OphthalmologyProcedure
class ProcedureListView(LoginRequiredMixin, ListView):
    model = OphthalmologyProcedure
    template_name = 'acs_hms_ophthalmology/procedure_list.html'
    context_object_name = 'procedures'
    paginate_by = 20
    
    def get_queryset(self):
        return OphthalmologyProcedure.objects.select_related(
            'patient', 'primary_surgeon'
        ).order_by('-scheduled_date')

class ProcedureDetailView(LoginRequiredMixin, DetailView):
    model = OphthalmologyProcedure
    template_name = 'acs_hms_ophthalmology/procedure_detail.html'
    context_object_name = 'procedure'

class ProcedureCreateView(LoginRequiredMixin, CreateView):
    model = OphthalmologyProcedure
    template_name = 'acs_hms_ophthalmology/procedure_form.html'
    fields = [
        'patient', 'eye_examination', 'procedure_type', 'procedure_name', 'description',
        'eye_operated', 'scheduled_date', 'primary_surgeon', 'preop_diagnosis'
    ]
    success_url = reverse_lazy('ophthalmology:procedure_list')
    
    def form_valid(self, form):
        # Auto-generar número de procedimiento
        if not form.instance.procedure_number:
            last_proc = OphthalmologyProcedure.objects.order_by('-id').first()
            if last_proc:
                try:
                    last_number = int(last_proc.procedure_number.split('-')[-1])
                    form.instance.procedure_number = f"PROC-{last_number + 1:06d}"
                except:
                    form.instance.procedure_number = "PROC-000001"
            else:
                form.instance.procedure_number = "PROC-000001"
        
        messages.success(self.request, 'Procedimiento programado exitosamente.')
        return super().form_valid(form)

class ProcedureUpdateView(LoginRequiredMixin, UpdateView):
    model = OphthalmologyProcedure
    template_name = 'acs_hms_ophthalmology/procedure_form.html'
    fields = [
        'patient', 'eye_examination', 'procedure_type', 'procedure_name', 'description',
        'eye_operated', 'scheduled_date', 'primary_surgeon', 'preop_diagnosis', 'status'
    ]
    success_url = reverse_lazy('ophthalmology:procedure_list')

# Vistas para OpticalPrescription
class PrescriptionListView(LoginRequiredMixin, ListView):
    model = OpticalPrescription
    template_name = 'acs_hms_ophthalmology/prescription_list.html'
    context_object_name = 'prescriptions'
    paginate_by = 20

class PrescriptionCreateView(LoginRequiredMixin, CreateView):
    model = OpticalPrescription
    template_name = 'acs_hms_ophthalmology/prescription_form.html'
    fields = [
        'patient', 'eye_examination', 'prescribed_by', 'sphere_right', 'cylinder_right', 'axis_right', 'add_right',
        'sphere_left', 'cylinder_left', 'axis_left', 'add_left', 'lens_type', 'pupillary_distance', 'valid_until'
    ]
    success_url = reverse_lazy('ophthalmology:prescription_list')
    
    def form_valid(self, form):
        # Auto-generar número de receta
        if not form.instance.prescription_number:
            last_pres = OpticalPrescription.objects.order_by('-id').first()
            if last_pres:
                try:
                    last_number = int(last_pres.prescription_number.split('-')[-1])
                    form.instance.prescription_number = f"RX-{last_number + 1:06d}"
                except:
                    form.instance.prescription_number = "RX-000001"
            else:
                form.instance.prescription_number = "RX-000001"
        
        messages.success(self.request, 'Receta óptica creada exitosamente.')
        return super().form_valid(form)

# Vistas para VisualFieldTest
class VisualFieldTestListView(LoginRequiredMixin, ListView):
    model = VisualFieldTest
    template_name = 'acs_hms_ophthalmology/visual_field_list.html'
    context_object_name = 'tests'
    paginate_by = 20

class VisualFieldTestCreateView(LoginRequiredMixin, CreateView):
    model = VisualFieldTest
    template_name = 'acs_hms_ophthalmology/visual_field_form.html'
    fields = [
        'patient', 'eye_examination', 'performed_by', 'test_type', 'eye_tested',
        'test_strategy', 'mean_deviation', 'pattern_standard_deviation', 'interpretation'
    ]
    success_url = reverse_lazy('ophthalmology:visual_field_list')
    
    def form_valid(self, form):
        # Auto-generar número de test
        if not form.instance.test_number:
            last_test = VisualFieldTest.objects.order_by('-id').first()
            if last_test:
                try:
                    last_number = int(last_test.test_number.split('-')[-1])
                    form.instance.test_number = f"VF-{last_number + 1:06d}"
                except:
                    form.instance.test_number = "VF-000001"
            else:
                form.instance.test_number = "VF-000001"
        
        messages.success(self.request, 'Test de campo visual creado exitosamente.')
        return super().form_valid(form)

# Vistas para Equipment
class EquipmentListView(LoginRequiredMixin, ListView):
    model = OphthalmologyEquipment
    template_name = 'acs_hms_ophthalmology/equipment_list.html'
    context_object_name = 'equipment'
    
    def get_queryset(self):
        return OphthalmologyEquipment.objects.order_by('equipment_name')

class EquipmentCreateView(LoginRequiredMixin, CreateView):
    model = OphthalmologyEquipment
    template_name = 'acs_hms_ophthalmology/equipment_form.html'
    fields = [
        'equipment_name', 'equipment_type', 'model', 'manufacturer', 'serial_number',
        'location', 'purchase_date', 'installation_date', 'status'
    ]
    success_url = reverse_lazy('ophthalmology:equipment_list')

# API Views para AJAX
class OphthalmologyStatsAPIView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        today = timezone.now().date()
        this_month = timezone.now().replace(day=1).date()
        
        stats = {
            'examinations_today': EyeExamination.objects.filter(examination_date__date=today).count(),
            'procedures_today': OphthalmologyProcedure.objects.filter(scheduled_date__date=today).count(),
            'active_equipment': OphthalmologyEquipment.objects.filter(status='ACTIVE').count(),
            'pending_prescriptions': OpticalPrescription.objects.filter(dispensed=False).count(),
        }
        return JsonResponse(stats)

# Vistas Legacy para compatibilidad
class OphthalmologyListView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_ophthalmology/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Ophthalmology'
        return context

class OphthalmologyCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_ophthalmology/create.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Ophthalmology'
        return context

class OphthalmologyDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_ophthalmology/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Ophthalmology'
        return context

class OphthalmologyUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_ophthalmology/update.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Ophthalmology'
        return context