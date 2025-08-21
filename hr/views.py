from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView)
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Cargo, Empleado, Contrato, Nomina
from .forms import CargoForm, EmpleadoForm, ContratoForm, NominaForm

# Create your views here.

class HRDashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard principal de recursos humanos"""
    template_name = 'hr/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Recursos Humanos'
        context['empleados_total'] = Empleado.objects.count()
        return context

# Vistas para Cargo
class CargoListView(ListView):
    model = Cargo
    template_name = 'hr/cargo_list.html'
    context_object_name = 'cargos'

class CargoDetailView(DetailView):
    model = Cargo
    template_name = 'hr/cargo_detail.html'
    context_object_name = 'cargo'

class CargoCreateView(CreateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'hr/cargo_form.html'
    success_url = reverse_lazy('cargo_list')

class CargoUpdateView(UpdateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'hr/cargo_form.html'
    success_url = reverse_lazy('cargo_list')

class CargoDeleteView(DeleteView):
    model = Cargo
    template_name = 'hr/cargo_confirm_delete.html'
    success_url = reverse_lazy('cargo_list')

# Vistas para Empleado
class EmpleadoListView(ListView):
    model = Empleado
    template_name = 'hr/empleado_list.html'
    context_object_name = 'empleados'
    paginate_by = 10

class EmpleadoDetailView(DetailView):
    model = Empleado
    template_name = 'hr/empleado_detail.html'
    context_object_name = 'empleado'

class EmpleadoCreateView(CreateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'hr/empleado_form.html'
    success_url = reverse_lazy('empleado_list')

class EmpleadoUpdateView(UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'hr/empleado_form.html'
    success_url = reverse_lazy('empleado_list')

class EmpleadoDeleteView(DeleteView):
    model = Empleado
    template_name = 'hr/empleado_confirm_delete.html'
    success_url = reverse_lazy('empleado_list')

# Vistas para Contrato
class ContratoListView(ListView):
    model = Contrato
    template_name = 'hr/contrato_list.html'
    context_object_name = 'contratos'
    paginate_by = 10

class ContratoDetailView(DetailView):
    model = Contrato
    template_name = 'hr/contrato_detail.html'
    context_object_name = 'contrato'

class ContratoCreateView(CreateView):
    model = Contrato
    form_class = ContratoForm
    template_name = 'hr/contrato_form.html'
    success_url = reverse_lazy('contrato_list')

class ContratoUpdateView(UpdateView):
    model = Contrato
    form_class = ContratoForm
    template_name = 'hr/contrato_form.html'
    success_url = reverse_lazy('contrato_list')

class ContratoDeleteView(DeleteView):
    model = Contrato
    template_name = 'hr/contrato_confirm_delete.html'
    success_url = reverse_lazy('contrato_list')

# Vistas para Nomina
class NominaListView(ListView):
    model = Nomina
    template_name = 'hr/nomina_list.html'
    context_object_name = 'nominas'
    paginate_by = 10

class NominaDetailView(DetailView):
    model = Nomina
    template_name = 'hr/nomina_detail.html'
    context_object_name = 'nomina'

class NominaCreateView(CreateView):
    model = Nomina
    form_class = NominaForm
    template_name = 'hr/nomina_form.html'
    success_url = reverse_lazy('nomina_list')

class NominaUpdateView(UpdateView):
    model = Nomina
    form_class = NominaForm
    template_name = 'hr/nomina_form.html'
    success_url = reverse_lazy('nomina_list')

class NominaDeleteView(DeleteView):
    model = Nomina
    template_name = 'hr/nomina_confirm_delete.html'
    success_url = reverse_lazy('nomina_list')
