from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView)
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ReporteGenerado
from .forms import ReporteGeneradoForm

class ReportsDashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard principal de reportes"""
    template_name = 'reports/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Reportes'
        context['reportes_total'] = ReporteGenerado.objects.count()
        return context

# Vistas para ReporteGenerado
class ReporteGeneradoListView(ListView):
    model = ReporteGenerado
    template_name = 'reports/reportegenerado_list.html'
    context_object_name = 'reportes'
    paginate_by = 10

class ReporteGeneradoDetailView(DetailView):
    model = ReporteGenerado
    template_name = 'reports/reportegenerado_detail.html'
    context_object_name = 'reporte'

class ReporteGeneradoCreateView(CreateView):
    model = ReporteGenerado
    form_class = ReporteGeneradoForm
    template_name = 'reports/reportegenerado_form.html'
    success_url = reverse_lazy('reporte_list')

class ReporteGeneradoUpdateView(UpdateView):
    model = ReporteGenerado
    form_class = ReporteGeneradoForm
    template_name = 'reports/reportegenerado_form.html'
    success_url = reverse_lazy('reporte_list')

class ReporteGeneradoDeleteView(DeleteView):
    model = ReporteGenerado
    template_name = 'reports/reportegenerado_confirm_delete.html'
    success_url = reverse_lazy('reporte_list')
