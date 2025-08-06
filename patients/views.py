from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import Paciente, HistoriaClinica
from .forms import PacienteForm, HistoriaClinicaForm

# Create your views here.

# Vistas para Paciente
class PacienteListView(ListView):
    model = Paciente
    template_name = 'patients/paciente_list.html'  # Crear este template
    context_object_name = 'pacientes'
    paginate_by = 10

class PacienteDetailView(DetailView):
    model = Paciente
    template_name = 'patients/paciente_detail.html' # Crear este template
    context_object_name = 'paciente'

class PacienteCreateView(CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'patients/paciente_form.html'   # Reutilizar este template para crear y actualizar
    success_url = reverse_lazy('paciente_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Crear una HistoriaClinica asociada automáticamente al nuevo Paciente
        HistoriaClinica.objects.create(paciente=self.object)
        return response

class PacienteUpdateView(UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'patients/paciente_form.html'   # Reutilizar este template para crear y actualizar
    success_url = reverse_lazy('paciente_list')

class PacienteDeleteView(DeleteView):
    model = Paciente
    template_name = 'patients/paciente_confirm_delete.html' # Crear este template
    success_url = reverse_lazy('paciente_list')
