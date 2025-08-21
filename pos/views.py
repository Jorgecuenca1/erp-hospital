from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import PuntoVenta, Caja, SesionCaja, MetodoPagoPOS, VentaPOS, LineaVentaPOS, PromocionesPOS, MovimientoCaja
from .forms import PuntoVentaForm, CajaForm, SesionCajaForm, MetodoPagoPOSForm, VentaPOSForm, LineaVentaPOSForm

# Create your views here.

# PuntoVenta
class PuntoVentaListView(ListView):
    model = PuntoVenta
class PuntoVentaDetailView(DetailView):
    model = PuntoVenta
class PuntoVentaCreateView(CreateView):
    model = PuntoVenta
    form_class = PuntoVentaForm
    success_url = reverse_lazy('pos:puntoventa_list')
class PuntoVentaUpdateView(UpdateView):
    model = PuntoVenta
    form_class = PuntoVentaForm
    success_url = reverse_lazy('pos:puntoventa_list')
class PuntoVentaDeleteView(DeleteView):
    model = PuntoVenta
    success_url = reverse_lazy('pos:puntoventa_list')

# Caja
class CajaListView(ListView):
    model = Caja
class CajaDetailView(DetailView):
    model = Caja
class CajaCreateView(CreateView):
    model = Caja
    form_class = CajaForm
    success_url = reverse_lazy('pos:caja_list')
class CajaUpdateView(UpdateView):
    model = Caja
    form_class = CajaForm
    success_url = reverse_lazy('pos:caja_list')
class CajaDeleteView(DeleteView):
    model = Caja
    success_url = reverse_lazy('pos:caja_list')

# SesionCaja
class SesionCajaListView(ListView):
    model = SesionCaja
class SesionCajaDetailView(DetailView):
    model = SesionCaja
class SesionCajaCreateView(CreateView):
    model = SesionCaja
    form_class = SesionCajaForm
    success_url = reverse_lazy('pos:sesioncaja_list')
class SesionCajaUpdateView(UpdateView):
    model = SesionCaja
    form_class = SesionCajaForm
    success_url = reverse_lazy('pos:sesioncaja_list')
class SesionCajaDeleteView(DeleteView):
    model = SesionCaja
    success_url = reverse_lazy('pos:sesioncaja_list')

# MetodoPagoPOS
class MetodoPagoPOSListView(ListView):
    model = MetodoPagoPOS
class MetodoPagoPOSDetailView(DetailView):
    model = MetodoPagoPOS
class MetodoPagoPOSCreateView(CreateView):
    model = MetodoPagoPOS
    form_class = MetodoPagoPOSForm
    success_url = reverse_lazy('pos:metodopagopos_list')
class MetodoPagoPOSUpdateView(UpdateView):
    model = MetodoPagoPOS
    form_class = MetodoPagoPOSForm
    success_url = reverse_lazy('pos:metodopagopos_list')
class MetodoPagoPOSDeleteView(DeleteView):
    model = MetodoPagoPOS
    success_url = reverse_lazy('pos:metodopagopos_list')

# VentaPOS
class VentaPOSListView(ListView):
    model = VentaPOS
class VentaPOSDetailView(DetailView):
    model = VentaPOS
class VentaPOSCreateView(CreateView):
    model = VentaPOS
    form_class = VentaPOSForm
    success_url = reverse_lazy('pos:ventapos_list')
class VentaPOSUpdateView(UpdateView):
    model = VentaPOS
    form_class = VentaPOSForm
    success_url = reverse_lazy('pos:ventapos_list')
class VentaPOSDeleteView(DeleteView):
    model = VentaPOS
    success_url = reverse_lazy('pos:ventapos_list')

# LineaVentaPOS
class LineaVentaPOSListView(ListView):
    model = LineaVentaPOS
class LineaVentaPOSDetailView(DetailView):
    model = LineaVentaPOS
class LineaVentaPOSCreateView(CreateView):
    model = LineaVentaPOS
    form_class = LineaVentaPOSForm
    success_url = reverse_lazy('pos:lineaventapos_list')
class LineaVentaPOSUpdateView(UpdateView):
    model = LineaVentaPOS
    form_class = LineaVentaPOSForm
    success_url = reverse_lazy('pos:lineaventapos_list')
class LineaVentaPOSDeleteView(DeleteView):
    model = LineaVentaPOS
    success_url = reverse_lazy('pos:lineaventapos_list')

# PromocionesPOS
class PromocionesPOSListView(ListView):
    model = PromocionesPOS
    template_name = 'pos/promocionespos_list.html'
    context_object_name = 'promociones'
    paginate_by = 20

class PromocionesPOSDetailView(DetailView):
    model = PromocionesPOS
    template_name = 'pos/promocionespos_detail.html'

class PromocionesPOSCreateView(CreateView):
    model = PromocionesPOS
    template_name = 'pos/promocionespos_form.html'
    fields = ['codigo', 'nombre', 'descripcion', 'tipo_promocion', 'valor_descuento', 
              'porcentaje_descuento', 'monto_minimo_compra', 'fecha_inicio', 'fecha_fin', 
              'activa', 'productos', 'categorias', 'puntos_venta']
    success_url = reverse_lazy('pos:promocionespos_list')

class PromocionesPOSUpdateView(UpdateView):
    model = PromocionesPOS
    template_name = 'pos/promocionespos_form.html'
    fields = ['codigo', 'nombre', 'descripcion', 'tipo_promocion', 'valor_descuento', 
              'porcentaje_descuento', 'monto_minimo_compra', 'fecha_inicio', 'fecha_fin', 
              'activa', 'productos', 'categorias', 'puntos_venta']
    success_url = reverse_lazy('pos:promocionespos_list')

class PromocionesPOSDeleteView(DeleteView):
    model = PromocionesPOS
    template_name = 'pos/promocionespos_confirm_delete.html'
    success_url = reverse_lazy('pos:promocionespos_list')

# MovimientoCaja
class MovimientoCajaListView(ListView):
    model = MovimientoCaja
    template_name = 'pos/movimientocaja_list.html'
    context_object_name = 'movimientos'
    paginate_by = 20
    
    def get_queryset(self):
        return MovimientoCaja.objects.select_related('sesion', 'usuario').order_by('-fecha')

class MovimientoCajaDetailView(DetailView):
    model = MovimientoCaja
    template_name = 'pos/movimientocaja_detail.html'

class MovimientoCajaCreateView(CreateView):
    model = MovimientoCaja
    template_name = 'pos/movimientocaja_form.html'
    fields = ['sesion', 'tipo_movimiento', 'monto', 'concepto', 'descripcion', 'usuario', 'autorizado_por']
    success_url = reverse_lazy('pos:movimientocaja_list')

class MovimientoCajaUpdateView(UpdateView):
    model = MovimientoCaja
    template_name = 'pos/movimientocaja_form.html'
    fields = ['sesion', 'tipo_movimiento', 'monto', 'concepto', 'descripcion', 'usuario', 'autorizado_por']
    success_url = reverse_lazy('pos:movimientocaja_list')

class MovimientoCajaDeleteView(DeleteView):
    model = MovimientoCaja
    template_name = 'pos/movimientocaja_confirm_delete.html'
    success_url = reverse_lazy('pos:movimientocaja_list')
