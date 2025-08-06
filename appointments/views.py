from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import Cita
from .forms import CitaForm

# Create your views here.

# Vistas para Cita
class CitaListView(ListView):
    model = Cita
    template_name = 'appointments/cita_list.html'
    context_object_name = 'citas'
    paginate_by = 10

class CitaDetailView(DetailView):
    model = Cita
    template_name = 'appointments/cita_detail.html'
    context_object_name = 'cita'

class CitaCreateView(CreateView):
    model = Cita
    form_class = CitaForm
    template_name = 'appointments/cita_form.html'
    success_url = reverse_lazy('cita_list')

class CitaUpdateView(UpdateView):
    model = Cita
    form_class = CitaForm
    template_name = 'appointments/cita_form.html'
    success_url = reverse_lazy('cita_list')

class CitaDeleteView(DeleteView):
    model = Cita
    template_name = 'appointments/cita_confirm_delete.html'
    success_url = reverse_lazy('cita_list')
