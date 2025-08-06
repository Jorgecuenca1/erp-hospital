from django.shortcuts import render
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import (
    GynecologyPatient, Pregnancy, AntenatalVisit, GynecologyProcedure,
    GynecologyMedicalRecord, ContraceptiveConsultation, MenopauseManagement
)
from .forms import (
    GynecologyPatientForm, PregnancyForm, AntenatalVisitForm, GynecologyProcedureForm,
    GynecologyMedicalRecordForm, ContraceptiveConsultationForm, MenopauseManagementForm
)

class GynecDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_gynec/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Gynec'
        context['module_type'] = 'hms'
        
        # Estadísticas del dashboard
        context['total_patients'] = GynecologyPatient.objects.count()
        context['ongoing_pregnancies'] = Pregnancy.objects.filter(status='ONGOING').count()
        context['total_procedures'] = GynecologyProcedure.objects.count()
        context['recent_visits'] = AntenatalVisit.objects.select_related('pregnancy__patient__patient').order_by('-visit_date')[:5]
        
        # Embarazos por estado
        context['pregnancies_by_status'] = Pregnancy.objects.values('status').annotate(count=Count('id'))
        
        # Procedimientos por tipo
        context['procedures_by_type'] = GynecologyProcedure.objects.values('procedure_type').annotate(count=Count('id'))[:5]
        
        return context

# Vistas para GynecologyPatient
class GynecPatientListView(LoginRequiredMixin, ListView):
    model = GynecologyPatient
    template_name = 'acs_hms_gynec/list.html'
    context_object_name = 'patients'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = GynecologyPatient.objects.select_related('patient')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(patient__first_name__icontains=search) |
                Q(patient__last_name__icontains=search) |
                Q(patient__identification_number__icontains=search)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Gynec'
        context['list_type'] = 'patients'
        return context

class GynecPatientDetailView(LoginRequiredMixin, DetailView):
    model = GynecologyPatient
    template_name = 'acs_hms_gynec/detail.html'
    context_object_name = 'patient'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Gynec'
        context['detail_type'] = 'patient'
        context['pregnancies'] = self.object.pregnancies.all()
        context['procedures'] = self.object.procedures.all()
        context['contraceptive_consultations'] = self.object.contraceptive_consultations.all()
        return context

class GynecPatientCreateView(LoginRequiredMixin, CreateView):
    model = GynecologyPatient
    form_class = GynecologyPatientForm
    template_name = 'acs_hms_gynec/create.html'
    success_url = reverse_lazy('gynec:patient_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Gynec'
        context['create_type'] = 'patient'
        return context

class GynecPatientUpdateView(LoginRequiredMixin, UpdateView):
    model = GynecologyPatient
    form_class = GynecologyPatientForm
    template_name = 'acs_hms_gynec/update.html'
    success_url = reverse_lazy('gynec:patient_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Gynec'
        context['update_type'] = 'patient'
        return context

class GynecPatientDeleteView(LoginRequiredMixin, DeleteView):
    model = GynecologyPatient
    template_name = 'acs_hms_gynec/delete.html'
    success_url = reverse_lazy('gynec:patient_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Gynec'
        context['delete_type'] = 'patient'
        return context

# Vistas para Pregnancy
class PregnancyListView(LoginRequiredMixin, ListView):
    model = Pregnancy
    template_name = 'acs_hms_gynec/list.html'
    context_object_name = 'pregnancies'
    paginate_by = 10
    
    def get_queryset(self):
        return Pregnancy.objects.select_related('patient__patient').order_by('-created_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Gynec'
        context['list_type'] = 'pregnancies'
        return context

class PregnancyDetailView(LoginRequiredMixin, DetailView):
    model = Pregnancy
    template_name = 'acs_hms_gynec/detail.html'
    context_object_name = 'pregnancy'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Gynec'
        context['detail_type'] = 'pregnancy'
        context['antenatal_visits'] = self.object.antenatal_visits.all()
        return context

class PregnancyCreateView(LoginRequiredMixin, CreateView):
    model = Pregnancy
    form_class = PregnancyForm
    template_name = 'acs_hms_gynec/create.html'
    success_url = reverse_lazy('gynec:pregnancy_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Gynec'
        context['create_type'] = 'pregnancy'
        return context

class PregnancyUpdateView(LoginRequiredMixin, UpdateView):
    model = Pregnancy
    form_class = PregnancyForm
    template_name = 'acs_hms_gynec/update.html'
    success_url = reverse_lazy('gynec:pregnancy_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Gynec'
        context['update_type'] = 'pregnancy'
        return context

class PregnancyDeleteView(LoginRequiredMixin, DeleteView):
    model = Pregnancy
    template_name = 'acs_hms_gynec/delete.html'
    success_url = reverse_lazy('gynec:pregnancy_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Gynec'
        context['delete_type'] = 'pregnancy'
        return context

# Vistas para AntenatalVisit
class AntenatalVisitListView(LoginRequiredMixin, ListView):
    model = AntenatalVisit
    template_name = 'acs_hms_gynec/list.html'
    context_object_name = 'visits'
    paginate_by = 10
    
    def get_queryset(self):
        return AntenatalVisit.objects.select_related('pregnancy__patient__patient', 'doctor').order_by('-visit_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Gynec'
        context['list_type'] = 'antenatal_visits'
        return context

class AntenatalVisitDetailView(LoginRequiredMixin, DetailView):
    model = AntenatalVisit
    template_name = 'acs_hms_gynec/detail.html'
    context_object_name = 'visit'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Gynec'
        context['detail_type'] = 'antenatal_visit'
        return context

class AntenatalVisitCreateView(LoginRequiredMixin, CreateView):
    model = AntenatalVisit
    form_class = AntenatalVisitForm
    template_name = 'acs_hms_gynec/create.html'
    success_url = reverse_lazy('gynec:antenatal_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Gynec'
        context['create_type'] = 'antenatal_visit'
        return context

class AntenatalVisitUpdateView(LoginRequiredMixin, UpdateView):
    model = AntenatalVisit
    form_class = AntenatalVisitForm
    template_name = 'acs_hms_gynec/update.html'
    success_url = reverse_lazy('gynec:antenatal_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Gynec'
        context['update_type'] = 'antenatal_visit'
        return context

class AntenatalVisitDeleteView(LoginRequiredMixin, DeleteView):
    model = AntenatalVisit
    template_name = 'acs_hms_gynec/delete.html'
    success_url = reverse_lazy('gynec:antenatal_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Gynec'
        context['delete_type'] = 'antenatal_visit'
        return context

# Vistas para GynecologyProcedure
class GynecologyProcedureListView(LoginRequiredMixin, ListView):
    model = GynecologyProcedure
    template_name = 'acs_hms_gynec/list.html'
    context_object_name = 'procedures'
    paginate_by = 10
    
    def get_queryset(self):
        return GynecologyProcedure.objects.select_related('patient__patient', 'doctor').order_by('-procedure_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Gynec'
        context['list_type'] = 'procedures'
        return context

class GynecologyProcedureDetailView(LoginRequiredMixin, DetailView):
    model = GynecologyProcedure
    template_name = 'acs_hms_gynec/detail.html'
    context_object_name = 'procedure'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Gynec'
        context['detail_type'] = 'procedure'
        return context

class GynecologyProcedureCreateView(LoginRequiredMixin, CreateView):
    model = GynecologyProcedure
    form_class = GynecologyProcedureForm
    template_name = 'acs_hms_gynec/create.html'
    success_url = reverse_lazy('gynec:procedure_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Gynec'
        context['create_type'] = 'procedure'
        return context

class GynecologyProcedureUpdateView(LoginRequiredMixin, UpdateView):
    model = GynecologyProcedure
    form_class = GynecologyProcedureForm
    template_name = 'acs_hms_gynec/update.html'
    success_url = reverse_lazy('gynec:procedure_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Gynec'
        context['update_type'] = 'procedure'
        return context

class GynecologyProcedureDeleteView(LoginRequiredMixin, DeleteView):
    model = GynecologyProcedure
    template_name = 'acs_hms_gynec/delete.html'
    success_url = reverse_lazy('gynec:procedure_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Gynec'
        context['delete_type'] = 'procedure'
        return context

# Vistas para ContraceptiveConsultation
class ContraceptiveConsultationListView(LoginRequiredMixin, ListView):
    model = ContraceptiveConsultation
    template_name = 'acs_hms_gynec/list.html'
    context_object_name = 'consultations'
    paginate_by = 10
    
    def get_queryset(self):
        return ContraceptiveConsultation.objects.select_related('patient__patient', 'doctor').order_by('-consultation_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Gynec'
        context['list_type'] = 'contraceptive_consultations'
        return context

class ContraceptiveConsultationDetailView(LoginRequiredMixin, DetailView):
    model = ContraceptiveConsultation
    template_name = 'acs_hms_gynec/detail.html'
    context_object_name = 'consultation'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Gynec'
        context['detail_type'] = 'contraceptive_consultation'
        return context

class ContraceptiveConsultationCreateView(LoginRequiredMixin, CreateView):
    model = ContraceptiveConsultation
    form_class = ContraceptiveConsultationForm
    template_name = 'acs_hms_gynec/create.html'
    success_url = reverse_lazy('gynec:contraceptive_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Gynec'
        context['create_type'] = 'contraceptive_consultation'
        return context

class ContraceptiveConsultationUpdateView(LoginRequiredMixin, UpdateView):
    model = ContraceptiveConsultation
    form_class = ContraceptiveConsultationForm
    template_name = 'acs_hms_gynec/update.html'
    success_url = reverse_lazy('gynec:contraceptive_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Gynec'
        context['update_type'] = 'contraceptive_consultation'
        return context

class ContraceptiveConsultationDeleteView(LoginRequiredMixin, DeleteView):
    model = ContraceptiveConsultation
    template_name = 'acs_hms_gynec/delete.html'
    success_url = reverse_lazy('gynec:contraceptive_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Gynec'
        context['delete_type'] = 'contraceptive_consultation'
        return context

# Vistas para MenopauseManagement
class MenopauseManagementListView(LoginRequiredMixin, ListView):
    model = MenopauseManagement
    template_name = 'acs_hms_gynec/list.html'
    context_object_name = 'menopause_records'
    paginate_by = 10
    
    def get_queryset(self):
        return MenopauseManagement.objects.select_related('patient__patient', 'doctor').order_by('-assessment_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Gynec'
        context['list_type'] = 'menopause_management'
        return context

class MenopauseManagementDetailView(LoginRequiredMixin, DetailView):
    model = MenopauseManagement
    template_name = 'acs_hms_gynec/detail.html'
    context_object_name = 'menopause_record'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Gynec'
        context['detail_type'] = 'menopause_management'
        return context

class MenopauseManagementCreateView(LoginRequiredMixin, CreateView):
    model = MenopauseManagement
    form_class = MenopauseManagementForm
    template_name = 'acs_hms_gynec/create.html'
    success_url = reverse_lazy('gynec:menopause_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Gynec'
        context['create_type'] = 'menopause_management'
        return context

class MenopauseManagementUpdateView(LoginRequiredMixin, UpdateView):
    model = MenopauseManagement
    form_class = MenopauseManagementForm
    template_name = 'acs_hms_gynec/update.html'
    success_url = reverse_lazy('gynec:menopause_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Gynec'
        context['update_type'] = 'menopause_management'
        return context

class MenopauseManagementDeleteView(LoginRequiredMixin, DeleteView):
    model = MenopauseManagement
    template_name = 'acs_hms_gynec/delete.html'
    success_url = reverse_lazy('gynec:menopause_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Gynec'
        context['delete_type'] = 'menopause_management'
        return context

# Vistas para GynecologyMedicalRecord
class GynecologyMedicalRecordListView(LoginRequiredMixin, ListView):
    model = GynecologyMedicalRecord
    template_name = 'acs_hms_gynec/list.html'
    context_object_name = 'medical_records'
    paginate_by = 10
    
    def get_queryset(self):
        return GynecologyMedicalRecord.objects.select_related('medical_record__patient', 'gynecology_patient__patient').order_by('-medical_record__created_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Gynec'
        context['list_type'] = 'medical_records'
        return context

class GynecologyMedicalRecordDetailView(LoginRequiredMixin, DetailView):
    model = GynecologyMedicalRecord
    template_name = 'acs_hms_gynec/detail.html'
    context_object_name = 'medical_record'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Gynec'
        context['detail_type'] = 'medical_record'
        return context

class GynecologyMedicalRecordCreateView(LoginRequiredMixin, CreateView):
    model = GynecologyMedicalRecord
    form_class = GynecologyMedicalRecordForm
    template_name = 'acs_hms_gynec/create.html'
    success_url = reverse_lazy('gynec:medical_record_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Gynec'
        context['create_type'] = 'medical_record'
        return context

class GynecologyMedicalRecordUpdateView(LoginRequiredMixin, UpdateView):
    model = GynecologyMedicalRecord
    form_class = GynecologyMedicalRecordForm
    template_name = 'acs_hms_gynec/update.html'
    success_url = reverse_lazy('gynec:medical_record_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Gynec'
        context['update_type'] = 'medical_record'
        return context

class GynecologyMedicalRecordDeleteView(LoginRequiredMixin, DeleteView):
    model = GynecologyMedicalRecord
    template_name = 'acs_hms_gynec/delete.html'
    success_url = reverse_lazy('gynec:medical_record_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Gynec'
        context['delete_type'] = 'medical_record'
        return context

class GynecReportsView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_gynec/reports.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Gynec'
        
        # Estadísticas para reportes
        context['total_patients'] = GynecologyPatient.objects.count()
        context['ongoing_pregnancies'] = Pregnancy.objects.filter(status='ONGOING').count()
        context['delivered_pregnancies'] = Pregnancy.objects.filter(status='DELIVERED').count()
        context['total_procedures'] = GynecologyProcedure.objects.count()
        context['total_antenatal_visits'] = AntenatalVisit.objects.count()
        
        # Embarazos por mes
        context['pregnancies_by_month'] = Pregnancy.objects.extra(
            select={'month': "EXTRACT(month FROM created_date)"}
        ).values('month').annotate(count=Count('id')).order_by('month')
        
        # Procedimientos por tipo
        context['procedures_by_type'] = GynecologyProcedure.objects.values('procedure_type').annotate(count=Count('id'))
        
        # Métodos anticonceptivos más usados
        context['contraceptive_methods'] = GynecologyPatient.objects.values('current_contraceptive').annotate(count=Count('id'))
        
        return context
