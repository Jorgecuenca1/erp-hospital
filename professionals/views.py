from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import Especialidad, ProfesionalSalud
from .forms import EspecialidadForm, ProfesionalSaludForm

# Create your views here.

# Vistas para Especialidad
class EspecialidadListView(ListView):
    model = Especialidad
    template_name = 'professionals/especialidad_list.html'
    context_object_name = 'especialidades'

class EspecialidadDetailView(DetailView):
    model = Especialidad
    template_name = 'professionals/especialidad_detail.html'
    context_object_name = 'especialidad'

class EspecialidadCreateView(CreateView):
    model = Especialidad
    form_class = EspecialidadForm
    template_name = 'professionals/especialidad_form.html'
    success_url = reverse_lazy('especialidad_list')

class EspecialidadUpdateView(UpdateView):
    model = Especialidad
    form_class = EspecialidadForm
    template_name = 'professionals/especialidad_form.html'
    success_url = reverse_lazy('especialidad_list')

class EspecialidadDeleteView(DeleteView):
    model = Especialidad
    template_name = 'professionals/especialidad_confirm_delete.html'
    success_url = reverse_lazy('especialidad_list')

# Vistas para ProfesionalSalud
class ProfesionalSaludListView(ListView):
    model = ProfesionalSalud
    template_name = 'professionals/profesionalsalud_list.html'
    context_object_name = 'profesionales'
    paginate_by = 10

class ProfesionalSaludDetailView(DetailView):
    model = ProfesionalSalud
    template_name = 'professionals/profesionalsalud_detail.html'
    context_object_name = 'profesional'

class ProfesionalSaludCreateView(CreateView):
    model = ProfesionalSalud
    form_class = ProfesionalSaludForm
    template_name = 'professionals/profesionalsalud_form.html'
    success_url = reverse_lazy('profesional_list')

class ProfesionalSaludUpdateView(UpdateView):
    model = ProfesionalSalud
    form_class = ProfesionalSaludForm
    template_name = 'professionals/profesionalsalud_form.html'
    success_url = reverse_lazy('profesional_list')

class ProfesionalSaludDeleteView(DeleteView):
    model = ProfesionalSalud
    template_name = 'professionals/profesionalsalud_confirm_delete.html'
    success_url = reverse_lazy('profesional_list')
