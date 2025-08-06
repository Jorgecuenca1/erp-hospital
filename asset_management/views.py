from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import CategoriaActivo, ActivoFijo, Mantenimiento, BajaActivo
from .forms import CategoriaActivoForm, ActivoFijoForm, MantenimientoForm, BajaActivoForm

# Create your views here.

# Vistas para CategoriaActivo
class CategoriaActivoListView(ListView):
    model = CategoriaActivo
    template_name = 'asset_management/categoriaactivo_list.html'
    context_object_name = 'categorias_activo'
    paginate_by = 10

class CategoriaActivoDetailView(DetailView):
    model = CategoriaActivo
    template_name = 'asset_management/categoriaactivo_detail.html'
    context_object_name = 'categoria_activo'

class CategoriaActivoCreateView(CreateView):
    model = CategoriaActivo
    form_class = CategoriaActivoForm
    template_name = 'asset_management/categoriaactivo_form.html'
    success_url = reverse_lazy('asset_management:categoriaactivo_list')

class CategoriaActivoUpdateView(UpdateView):
    model = CategoriaActivo
    form_class = CategoriaActivoForm
    template_name = 'asset_management/categoriaactivo_form.html'
    success_url = reverse_lazy('asset_management:categoriaactivo_list')

class CategoriaActivoDeleteView(DeleteView):
    model = CategoriaActivo
    template_name = 'asset_management/categoriaactivo_confirm_delete.html'
    success_url = reverse_lazy('asset_management:categoriaactivo_list')

# Vistas para ActivoFijo
class ActivoFijoListView(ListView):
    model = ActivoFijo
    template_name = 'asset_management/activofijo_list.html'
    context_object_name = 'activos_fijos'
    paginate_by = 10

class ActivoFijoDetailView(DetailView):
    model = ActivoFijo
    template_name = 'asset_management/activofijo_detail.html'
    context_object_name = 'activo_fijo'

class ActivoFijoCreateView(CreateView):
    model = ActivoFijo
    form_class = ActivoFijoForm
    template_name = 'asset_management/activofijo_form.html'
    success_url = reverse_lazy('asset_management:activofijo_list')

class ActivoFijoUpdateView(UpdateView):
    model = ActivoFijo
    form_class = ActivoFijoForm
    template_name = 'asset_management/activofijo_form.html'
    success_url = reverse_lazy('asset_management:activofijo_list')

class ActivoFijoDeleteView(DeleteView):
    model = ActivoFijo
    template_name = 'asset_management/activofijo_confirm_delete.html'
    success_url = reverse_lazy('asset_management:activofijo_list')

# Vistas para Mantenimiento
class MantenimientoListView(ListView):
    model = Mantenimiento
    template_name = 'asset_management/mantenimiento_list.html'
    context_object_name = 'mantenimientos'
    paginate_by = 10

class MantenimientoDetailView(DetailView):
    model = Mantenimiento
    template_name = 'asset_management/mantenimiento_detail.html'
    context_object_name = 'mantenimiento'

class MantenimientoCreateView(CreateView):
    model = Mantenimiento
    form_class = MantenimientoForm
    template_name = 'asset_management/mantenimiento_form.html'
    success_url = reverse_lazy('asset_management:mantenimiento_list')

    def get_initial(self):
        initial = super().get_initial()
        activo_pk = self.kwargs.get('activo_pk')
        if activo_pk:
            initial['activo'] = get_object_or_404(ActivoFijo, pk=activo_pk)
        return initial

class MantenimientoUpdateView(UpdateView):
    model = Mantenimiento
    form_class = MantenimientoForm
    template_name = 'asset_management/mantenimiento_form.html'
    success_url = reverse_lazy('asset_management:mantenimiento_list')

class MantenimientoDeleteView(DeleteView):
    model = Mantenimiento
    template_name = 'asset_management/mantenimiento_confirm_delete.html'
    success_url = reverse_lazy('asset_management:mantenimiento_list')

# Vistas para BajaActivo
class BajaActivoListView(ListView):
    model = BajaActivo
    template_name = 'asset_management/bajaactivo_list.html'
    context_object_name = 'bajas_activo'
    paginate_by = 10

class BajaActivoDetailView(DetailView):
    model = BajaActivo
    template_name = 'asset_management/bajaactivo_detail.html'
    context_object_name = 'baja_activo'

class BajaActivoCreateView(CreateView):
    model = BajaActivo
    form_class = BajaActivoForm
    template_name = 'asset_management/bajaactivo_form.html'
    success_url = reverse_lazy('asset_management:bajaactivo_list')

    def get_initial(self):
        initial = super().get_initial()
        activo_pk = self.kwargs.get('activo_pk')
        if activo_pk:
            initial['activo'] = get_object_or_404(ActivoFijo, pk=activo_pk)
        return initial

class BajaActivoUpdateView(UpdateView):
    model = BajaActivo
    form_class = BajaActivoForm
    template_name = 'asset_management/bajaactivo_form.html'
    success_url = reverse_lazy('asset_management:bajaactivo_list')

class BajaActivoDeleteView(DeleteView):
    model = BajaActivo
    template_name = 'asset_management/bajaactivo_confirm_delete.html'
    success_url = reverse_lazy('asset_management:bajaactivo_list')
