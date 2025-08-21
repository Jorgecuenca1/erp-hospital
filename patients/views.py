from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.utils import timezone
from .models import Paciente, HistoriaClinica
from .forms import PacienteForm, HistoriaClinicaForm

# Create your views here.

# Dashboard principal
class PacienteDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'patients/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estadísticas de pacientes
        context['total_pacientes'] = Paciente.objects.count()
        context['pacientes_hoy'] = Paciente.objects.filter(
            historiaClinica__consultas__fecha_consulta__date=timezone.now().date()
        ).count()
        context['pacientes_mes'] = Paciente.objects.filter(
            created_at__month=timezone.now().month
        ).count() if hasattr(Paciente, 'created_at') else 0
        
        # Últimos pacientes
        context['ultimos_pacientes'] = Paciente.objects.order_by('-id')[:5]
        
        # Distribución por régimen
        context['regimen_stats'] = Paciente.objects.values('tipo_regimen').annotate(
            count=Count('id')
        )
        
        return context

# Vistas para Paciente
class PacienteListView(LoginRequiredMixin, ListView):
    model = Paciente
    template_name = 'patients/paciente_list.html'
    context_object_name = 'pacientes'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Paciente.objects.all()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(nombres__icontains=search) | 
                Q(apellidos__icontains=search) |
                Q(numero_identificacion__icontains=search)
            )
        return queryset.order_by('apellidos', 'nombres')

class PacienteDetailView(LoginRequiredMixin, DetailView):
    model = Paciente
    template_name = 'patients/paciente_detail.html'
    context_object_name = 'paciente'

class PacienteCreateView(LoginRequiredMixin, CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'patients/paciente_form.html'
    success_url = reverse_lazy('patients:paciente_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Crear una HistoriaClinica asociada automáticamente al nuevo Paciente
        if hasattr(self.object, 'historia_clinica'):
            HistoriaClinica.objects.get_or_create(paciente=self.object)
        return response

class PacienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'patients/paciente_form.html'
    success_url = reverse_lazy('patients:paciente_list')

class PacienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Paciente
    template_name = 'patients/paciente_confirm_delete.html'
    success_url = reverse_lazy('patients:paciente_list')

# Vistas adicionales
class HistoriasClinicasView(LoginRequiredMixin, TemplateView):
    template_name = 'patients/historias.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['historias'] = HistoriaClinica.objects.select_related('paciente').all()[:50]
        return context

class CitasPacientesView(LoginRequiredMixin, TemplateView):
    template_name = 'patients/citas.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Aquí se conectaría con el módulo de citas
        context['title'] = 'Citas de Pacientes'
        return context

class IngresosPacientesView(LoginRequiredMixin, TemplateView):
    template_name = 'patients/ingresos.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ingresos Hospitalarios'
        return context

class EmergenciasPacientesView(LoginRequiredMixin, TemplateView):
    template_name = 'patients/emergencias.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Emergencias'
        return context

class ReportesPacientesView(LoginRequiredMixin, TemplateView):
    template_name = 'patients/reportes.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reportes de Pacientes'
        return context
