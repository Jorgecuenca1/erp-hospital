from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView, View, TemplateView)
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Medicamento, Receta, DetalleReceta
from .forms import MedicamentoForm, RecetaForm, DetalleRecetaForm
from django.forms import inlineformset_factory

# Inline formset para DetalleReceta
DetalleRecetaFormSet = inlineformset_factory(Receta, DetalleReceta, form=DetalleRecetaForm, extra=1, can_delete=True)

class PharmacyDashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard principal de farmacia"""
    template_name = 'pharmacy/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Farmacia'
        context['medicamentos_total'] = Medicamento.objects.count()
        return context

# Vistas para Medicamento
class MedicamentoListView(ListView):
    model = Medicamento
    template_name = 'pharmacy/medicamento_list.html'
    context_object_name = 'medicamentos'
    paginate_by = 10

class MedicamentoDetailView(DetailView):
    model = Medicamento
    template_name = 'pharmacy/medicamento_detail.html'
    context_object_name = 'medicamento'

class MedicamentoCreateView(CreateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = 'pharmacy/medicamento_form.html'
    success_url = reverse_lazy('medicamento_list')

class MedicamentoUpdateView(UpdateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = 'pharmacy/medicamento_form.html'
    success_url = reverse_lazy('medicamento_list')

class MedicamentoDeleteView(DeleteView):
    model = Medicamento
    template_name = 'pharmacy/medicamento_confirm_delete.html'
    success_url = reverse_lazy('medicamento_list')

# Vistas para Receta
class RecetaListView(ListView):
    model = Receta
    template_name = 'pharmacy/receta_list.html'
    context_object_name = 'recetas'
    paginate_by = 10

class RecetaDetailView(DetailView):
    model = Receta
    template_name = 'pharmacy/receta_detail.html'
    context_object_name = 'receta'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        receta = self.get_object()
        context['detalles'] = receta.detalles.all()
        return context

class RecetaCreateView(CreateView):
    model = Receta
    form_class = RecetaForm
    template_name = 'pharmacy/receta_form.html'
    success_url = reverse_lazy('receta_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['detalles_formset'] = DetalleRecetaFormSet(self.request.POST, self.request.FILES)
        else:
            data['detalles_formset'] = DetalleRecetaFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        detalles_formset = context['detalles_formset']
        self.object = form.save()

        if detalles_formset.is_valid():
            detalles_formset.instance = self.object
            detalles_formset.save()
        else:
            return self.form_invalid(form)
        return super().form_valid(form)

class RecetaUpdateView(UpdateView):
    model = Receta
    form_class = RecetaForm
    template_name = 'pharmacy/receta_form.html'
    success_url = reverse_lazy('receta_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['detalles_formset'] = DetalleRecetaFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['detalles_formset'] = DetalleRecetaFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        detalles_formset = context['detalles_formset']
        self.object = form.save()

        if detalles_formset.is_valid():
            detalles_formset.instance = self.object
            detalles_formset.save()
        else:
            return self.form_invalid(form)
        return super().form_valid(form)

class RecetaDeleteView(DeleteView):
    model = Receta
    template_name = 'pharmacy/receta_confirm_delete.html'
    success_url = reverse_lazy('receta_list')
