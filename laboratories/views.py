from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView)
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import TipoExamen, EquipoLaboratorio, OrdenExamen, ResultadoExamen
from .forms import TipoExamenForm, EquipoLaboratorioForm, OrdenExamenForm, ResultadoExamenForm

# Create your views here.

class LaboratoriesDashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard principal de laboratorios"""
    template_name = 'laboratories/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Laboratorios'
        context['examenes_total'] = OrdenExamen.objects.count()
        return context

# Vistas para TipoExamen
class TipoExamenListView(ListView):
    model = TipoExamen
    template_name = 'laboratories/tipoexamen_list.html'
    context_object_name = 'tipos_examen'

class TipoExamenDetailView(DetailView):
    model = TipoExamen
    template_name = 'laboratories/tipoexamen_detail.html'
    context_object_name = 'tipo_examen'

class TipoExamenCreateView(CreateView):
    model = TipoExamen
    form_class = TipoExamenForm
    template_name = 'laboratories/tipoexamen_form.html'
    success_url = reverse_lazy('tipo_examen_list')

class TipoExamenUpdateView(UpdateView):
    model = TipoExamen
    form_class = TipoExamenForm
    template_name = 'laboratories/tipoexamen_form.html'
    success_url = reverse_lazy('tipo_examen_list')

class TipoExamenDeleteView(DeleteView):
    model = TipoExamen
    template_name = 'laboratories/tipoexamen_confirm_delete.html'
    success_url = reverse_lazy('tipo_examen_list')

# Vistas para EquipoLaboratorio
class EquipoLaboratorioListView(ListView):
    model = EquipoLaboratorio
    template_name = 'laboratories/equipolaboratorio_list.html'
    context_object_name = 'equipos'

class EquipoLaboratorioDetailView(DetailView):
    model = EquipoLaboratorio
    template_name = 'laboratories/equipolaboratorio_detail.html'
    context_object_name = 'equipo'

class EquipoLaboratorioCreateView(CreateView):
    model = EquipoLaboratorio
    form_class = EquipoLaboratorioForm
    template_name = 'laboratories/equipolaboratorio_form.html'
    success_url = reverse_lazy('equipo_list')

class EquipoLaboratorioUpdateView(UpdateView):
    model = EquipoLaboratorio
    form_class = EquipoLaboratorioForm
    template_name = 'laboratories/equipolaboratorio_form.html'
    success_url = reverse_lazy('equipo_list')

class EquipoLaboratorioDeleteView(DeleteView):
    model = EquipoLaboratorio
    template_name = 'laboratories/equipolaboratorio_confirm_delete.html'
    success_url = reverse_lazy('equipo_list')

# Vistas para OrdenExamen
class OrdenExamenListView(ListView):
    model = OrdenExamen
    template_name = 'laboratories/ordenexamen_list.html'
    context_object_name = 'ordenes_examen'
    paginate_by = 10

class OrdenExamenDetailView(DetailView):
    model = OrdenExamen
    template_name = 'laboratories/ordenexamen_detail.html'
    context_object_name = 'orden_examen'

class OrdenExamenCreateView(CreateView):
    model = OrdenExamen
    form_class = OrdenExamenForm
    template_name = 'laboratories/ordenexamen_form.html'
    success_url = reverse_lazy('orden_examen_list')

class OrdenExamenUpdateView(UpdateView):
    model = OrdenExamen
    form_class = OrdenExamenForm
    template_name = 'laboratories/ordenexamen_form.html'
    success_url = reverse_lazy('orden_examen_list')

class OrdenExamenDeleteView(DeleteView):
    model = OrdenExamen
    template_name = 'laboratories/ordenexamen_confirm_delete.html'
    success_url = reverse_lazy('orden_examen_list')

# Vistas para ResultadoExamen
class ResultadoExamenListView(ListView):
    model = ResultadoExamen
    template_name = 'laboratories/resultadoexamen_list.html'
    context_object_name = 'resultados_examen'
    paginate_by = 10

class ResultadoExamenDetailView(DetailView):
    model = ResultadoExamen
    template_name = 'laboratories/resultadoexamen_detail.html'
    context_object_name = 'resultado_examen'

class ResultadoExamenCreateView(CreateView):
    model = ResultadoExamen
    form_class = ResultadoExamenForm
    template_name = 'laboratories/resultadoexamen_form.html'
    success_url = reverse_lazy('resultado_examen_list')

class ResultadoExamenUpdateView(UpdateView):
    model = ResultadoExamen
    form_class = ResultadoExamenForm
    template_name = 'laboratories/resultadoexamen_form.html'
    success_url = reverse_lazy('resultado_examen_list')

class ResultadoExamenDeleteView(DeleteView):
    model = ResultadoExamen
    template_name = 'laboratories/resultadoexamen_confirm_delete.html'
    success_url = reverse_lazy('resultado_examen_list')
