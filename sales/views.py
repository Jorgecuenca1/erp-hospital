from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView, View, TemplateView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count, Q, F
from django.utils import timezone
from datetime import timedelta
from .models import (
    Cliente, ProductoServicio, OrdenVenta, DetalleOrdenVenta, 
    FacturaVenta, DetalleFacturaVenta, PagoVenta, DevolucionVenta, DetalleDevolucionVenta
)
from .forms import (
    ClienteForm, ProductoServicioForm, OrdenVentaForm, DetalleOrdenVentaForm,
    FacturaVentaForm, DetalleFacturaVentaForm, PagoVentaForm, DevolucionVentaForm
)
from django.forms import inlineformset_factory

# Inline formsets
DetalleOrdenVentaFormSet = inlineformset_factory(OrdenVenta, DetalleOrdenVenta, form=DetalleOrdenVentaForm, extra=1, can_delete=True)
DetalleFacturaVentaFormSet = inlineformset_factory(FacturaVenta, DetalleFacturaVenta, form=DetalleFacturaVentaForm, extra=1, can_delete=True)

# Dashboard principal
class SalesDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'sales/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estadísticas generales
        context['total_clientes'] = Cliente.objects.filter(estado='ACTIVO').count()
        context['total_productos'] = ProductoServicio.objects.filter(activo=True).count()
        context['ordenes_pendientes'] = OrdenVenta.objects.filter(estado__in=['BORRADOR', 'CONFIRMADA']).count()
        context['facturas_pendientes'] = FacturaVenta.objects.filter(estado='EMITIDA').count()
        
        # Ventas del mes actual
        fecha_inicio_mes = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        context['ventas_mes'] = FacturaVenta.objects.filter(
            fecha_emision__gte=fecha_inicio_mes,
            estado__in=['EMITIDA', 'PAGADA']
        ).aggregate(total=Sum('total'))['total'] or 0
        
        # Ventas del mes anterior
        fecha_inicio_mes_anterior = (fecha_inicio_mes - timedelta(days=1)).replace(day=1)
        fecha_fin_mes_anterior = fecha_inicio_mes - timedelta(days=1)
        context['ventas_mes_anterior'] = FacturaVenta.objects.filter(
            fecha_emision__range=[fecha_inicio_mes_anterior, fecha_fin_mes_anterior],
            estado__in=['EMITIDA', 'PAGADA']
        ).aggregate(total=Sum('total'))['total'] or 0
        
        # Crecimiento de ventas
        if context['ventas_mes_anterior'] > 0:
            context['crecimiento_ventas'] = ((context['ventas_mes'] - context['ventas_mes_anterior']) / context['ventas_mes_anterior']) * 100
        else:
            context['crecimiento_ventas'] = 0
        
        # Facturas recientes
        context['facturas_recientes'] = FacturaVenta.objects.select_related('cliente').order_by('-fecha_emision')[:5]
        
        # Top clientes
        context['top_clientes'] = Cliente.objects.annotate(
            total_ventas=Sum('facturas__total')
        ).filter(total_ventas__gt=0).order_by('-total_ventas')[:5]
        
        # Productos más vendidos
        context['productos_mas_vendidos'] = ProductoServicio.objects.annotate(
            total_vendido=Sum('detallefacturaventa__cantidad')
        ).filter(total_vendido__gt=0).order_by('-total_vendido')[:5]
        
        # Ventas por estado
        context['ventas_por_estado'] = FacturaVenta.objects.values('estado').annotate(
            count=Count('id'),
            total=Sum('total')
        )
        
        # Ventas por mes (últimos 6 meses)
        context['ventas_por_mes'] = []
        for i in range(6):
            fecha = timezone.now().date() - timedelta(days=30*i)
            inicio_mes = fecha.replace(day=1)
            fin_mes = (inicio_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            
            ventas_mes = FacturaVenta.objects.filter(
                fecha_emision__date__range=[inicio_mes, fin_mes],
                estado__in=['EMITIDA', 'PAGADA']
            ).aggregate(
                total=Sum('total'),
                count=Count('id')
            )
            
            context['ventas_por_mes'].append({
                'mes': inicio_mes.strftime('%B %Y'),
                'total': ventas_mes['total'] or 0,
                'cantidad': ventas_mes['count'] or 0
            })
        
        return context

# Vistas para Cliente
class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'sales/cliente_list.html'
    context_object_name = 'clientes'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Cliente.objects.all()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(nombre__icontains=search) |
                Q(identificacion__icontains=search) |
                Q(email__icontains=search)
            )
        return queryset

class ClienteDetailView(LoginRequiredMixin, DetailView):
    model = Cliente
    template_name = 'sales/cliente_detail.html'
    context_object_name = 'cliente'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ordenes_recientes'] = self.object.ordenes_venta.order_by('-fecha_orden')[:5]
        context['facturas_recientes'] = self.object.facturas.order_by('-fecha_emision')[:5]
        return context

class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'sales/cliente_form.html'
    success_url = reverse_lazy('sales:cliente_list')

class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'sales/cliente_form.html'
    success_url = reverse_lazy('sales:cliente_list')

class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Cliente
    template_name = 'sales/cliente_confirm_delete.html'
    success_url = reverse_lazy('sales:cliente_list')

# Vistas para ProductoServicio
class ProductoServicioListView(LoginRequiredMixin, ListView):
    model = ProductoServicio
    template_name = 'sales/productoservicio_list.html'
    context_object_name = 'productos'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = ProductoServicio.objects.filter(activo=True)
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(nombre__icontains=search) |
                Q(codigo__icontains=search) |
                Q(descripcion__icontains=search)
            )
        return queryset

class ProductoServicioDetailView(LoginRequiredMixin, DetailView):
    model = ProductoServicio
    template_name = 'sales/productoservicio_detail.html'
    context_object_name = 'producto'

class ProductoServicioCreateView(LoginRequiredMixin, CreateView):
    model = ProductoServicio
    form_class = ProductoServicioForm
    template_name = 'sales/productoservicio_form.html'
    success_url = reverse_lazy('sales:productoservicio_list')

class ProductoServicioUpdateView(LoginRequiredMixin, UpdateView):
    model = ProductoServicio
    form_class = ProductoServicioForm
    template_name = 'sales/productoservicio_form.html'
    success_url = reverse_lazy('sales:productoservicio_list')

class ProductoServicioDeleteView(LoginRequiredMixin, DeleteView):
    model = ProductoServicio
    template_name = 'sales/productoservicio_confirm_delete.html'
    success_url = reverse_lazy('sales:productoservicio_list')

# Vistas para OrdenVenta
class OrdenVentaListView(LoginRequiredMixin, ListView):
    model = OrdenVenta
    template_name = 'sales/ordenventa_list.html'
    context_object_name = 'ordenes'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = OrdenVenta.objects.select_related('cliente', 'vendedor').order_by('-fecha_orden')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(numero_orden__icontains=search) |
                Q(cliente__nombre__icontains=search)
            )
        return queryset

class OrdenVentaDetailView(LoginRequiredMixin, DetailView):
    model = OrdenVenta
    template_name = 'sales/ordenventa_detail.html'
    context_object_name = 'orden'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = self.object.items.all()
        return context

class OrdenVentaCreateView(LoginRequiredMixin, CreateView):
    model = OrdenVenta
    form_class = OrdenVentaForm
    template_name = 'sales/ordenventa_form.html'
    success_url = reverse_lazy('sales:ordenventa_list')
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['items_formset'] = DetalleOrdenVentaFormSet(self.request.POST, self.request.FILES)
        else:
            data['items_formset'] = DetalleOrdenVentaFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        items_formset = context['items_formset']
        self.object = form.save(commit=False)
        self.object.vendedor = self.request.user
        self.object.save()

        if items_formset.is_valid():
            items_formset.instance = self.object
            items_formset.save()
            self.object.calcular_totales()
        else:
            return self.form_invalid(form)
        return super().form_valid(form)

class OrdenVentaUpdateView(LoginRequiredMixin, UpdateView):
    model = OrdenVenta
    form_class = OrdenVentaForm
    template_name = 'sales/ordenventa_form.html'
    success_url = reverse_lazy('sales:ordenventa_list')
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['items_formset'] = DetalleOrdenVentaFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['items_formset'] = DetalleOrdenVentaFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        items_formset = context['items_formset']
        self.object = form.save()

        if items_formset.is_valid():
            items_formset.instance = self.object
            items_formset.save()
            self.object.calcular_totales()
        else:
            return self.form_invalid(form)
        return super().form_valid(form)

class OrdenVentaDeleteView(LoginRequiredMixin, DeleteView):
    model = OrdenVenta
    template_name = 'sales/ordenventa_confirm_delete.html'
    success_url = reverse_lazy('sales:ordenventa_list')

# Vistas para FacturaVenta
class FacturaVentaListView(LoginRequiredMixin, ListView):
    model = FacturaVenta
    template_name = 'sales/facturaventa_list.html'
    context_object_name = 'facturas'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = FacturaVenta.objects.select_related('cliente', 'vendedor').order_by('-fecha_emision')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(numero_factura__icontains=search) |
                Q(cliente__nombre__icontains=search)
            )
        return queryset

class FacturaVentaDetailView(LoginRequiredMixin, DetailView):
    model = FacturaVenta
    template_name = 'sales/facturaventa_detail.html'
    context_object_name = 'factura'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = self.object.items.all()
        context['pagos'] = self.object.pagos.all()
        return context

class FacturaVentaCreateView(LoginRequiredMixin, CreateView):
    model = FacturaVenta
    form_class = FacturaVentaForm
    template_name = 'sales/facturaventa_form.html'
    success_url = reverse_lazy('sales:facturaventa_list')
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['items_formset'] = DetalleFacturaVentaFormSet(self.request.POST, self.request.FILES)
        else:
            data['items_formset'] = DetalleFacturaVentaFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        items_formset = context['items_formset']
        self.object = form.save(commit=False)
        self.object.vendedor = self.request.user
        self.object.save()

        if items_formset.is_valid():
            items_formset.instance = self.object
            items_formset.save()
            self.object.calcular_totales()
        else:
            return self.form_invalid(form)
        return super().form_valid(form)

class FacturaVentaUpdateView(LoginRequiredMixin, UpdateView):
    model = FacturaVenta
    form_class = FacturaVentaForm
    template_name = 'sales/facturaventa_form.html'
    success_url = reverse_lazy('sales:facturaventa_list')
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['items_formset'] = DetalleFacturaVentaFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['items_formset'] = DetalleFacturaVentaFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        items_formset = context['items_formset']
        self.object = form.save()

        if items_formset.is_valid():
            items_formset.instance = self.object
            items_formset.save()
            self.object.calcular_totales()
        else:
            return self.form_invalid(form)
        return super().form_valid(form)

class FacturaVentaDeleteView(LoginRequiredMixin, DeleteView):
    model = FacturaVenta
    template_name = 'sales/facturaventa_confirm_delete.html'
    success_url = reverse_lazy('sales:facturaventa_list')

# Vistas para PagoVenta
class PagoVentaListView(LoginRequiredMixin, ListView):
    model = PagoVenta
    template_name = 'sales/pagoventa_list.html'
    context_object_name = 'pagos'
    paginate_by = 20

class PagoVentaDetailView(LoginRequiredMixin, DetailView):
    model = PagoVenta
    template_name = 'sales/pagoventa_detail.html'
    context_object_name = 'pago'

class PagoVentaCreateView(LoginRequiredMixin, CreateView):
    model = PagoVenta
    form_class = PagoVentaForm
    template_name = 'sales/pagoventa_form.html'
    success_url = reverse_lazy('sales:pagoventa_list')
    
    def form_valid(self, form):
        form.instance.registrado_por = self.request.user
        return super().form_valid(form)

class PagoVentaUpdateView(LoginRequiredMixin, UpdateView):
    model = PagoVenta
    form_class = PagoVentaForm
    template_name = 'sales/pagoventa_form.html'
    success_url = reverse_lazy('sales:pagoventa_list')

class PagoVentaDeleteView(LoginRequiredMixin, DeleteView):
    model = PagoVenta
    template_name = 'sales/pagoventa_confirm_delete.html'
    success_url = reverse_lazy('sales:pagoventa_list')

# Vistas para DevolucionVenta
class DevolucionVentaListView(LoginRequiredMixin, ListView):
    model = DevolucionVenta
    template_name = 'sales/devolucionventa_list.html'
    context_object_name = 'devoluciones'
    paginate_by = 10

class DevolucionVentaDetailView(LoginRequiredMixin, DetailView):
    model = DevolucionVenta
    template_name = 'sales/devolucionventa_detail.html'
    context_object_name = 'devolucion'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = self.object.items.all()
        return context

class DevolucionVentaCreateView(LoginRequiredMixin, CreateView):
    model = DevolucionVenta
    form_class = DevolucionVentaForm
    template_name = 'sales/devolucionventa_form.html'
    success_url = reverse_lazy('sales:devolucionventa_list')

class DevolucionVentaUpdateView(LoginRequiredMixin, UpdateView):
    model = DevolucionVenta
    form_class = DevolucionVentaForm
    template_name = 'sales/devolucionventa_form.html'
    success_url = reverse_lazy('sales:devolucionventa_list')

class DevolucionVentaDeleteView(LoginRequiredMixin, DeleteView):
    model = DevolucionVenta
    template_name = 'sales/devolucionventa_confirm_delete.html'
    success_url = reverse_lazy('sales:devolucionventa_list')

# Vistas para Reportes
class SalesReportsView(LoginRequiredMixin, TemplateView):
    template_name = 'sales/reports.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estadísticas para reportes
        context['total_ventas'] = FacturaVenta.objects.filter(estado__in=['EMITIDA', 'PAGADA']).count()
        context['ventas_por_estado'] = FacturaVenta.objects.values('estado').annotate(
            count=Count('id'),
            total=Sum('total')
        )
        
        # Top 5 clientes con más ventas
        context['top_clientes'] = Cliente.objects.annotate(
            total_ventas=Sum('facturas__total'),
            cantidad_facturas=Count('facturas')
        ).filter(total_ventas__gt=0).order_by('-total_ventas')[:5]
        
        # Top 5 productos más vendidos
        context['top_productos'] = ProductoServicio.objects.annotate(
            total_vendido=Sum('detallefacturaventa__cantidad'),
            total_ingresos=Sum('detallefacturaventa__total')
        ).filter(total_vendido__gt=0).order_by('-total_ingresos')[:5]
        
        # Ventas por mes (últimos 12 meses)
        context['ventas_por_mes'] = []
        for i in range(12):
            fecha = timezone.now().date() - timedelta(days=30*i)
            inicio_mes = fecha.replace(day=1)
            fin_mes = (inicio_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            
            ventas_mes = FacturaVenta.objects.filter(
                fecha_emision__date__range=[inicio_mes, fin_mes],
                estado__in=['EMITIDA', 'PAGADA']
            ).aggregate(
                total=Sum('total'),
                count=Count('id')
            )
            
            context['ventas_por_mes'].append({
                'mes': inicio_mes.strftime('%B %Y'),
                'total': ventas_mes['total'] or 0,
                'cantidad': ventas_mes['count'] or 0
            })
        
        return context

# Vistas adicionales
class FacturasPendientesView(LoginRequiredMixin, ListView):
    model = FacturaVenta
    template_name = 'sales/facturas_pendientes.html'
    context_object_name = 'facturas'
    paginate_by = 20
    
    def get_queryset(self):
        return FacturaVenta.objects.filter(
            estado='EMITIDA'
        ).select_related('cliente').order_by('fecha_vencimiento')

class FacturasVencidasView(LoginRequiredMixin, ListView):
    model = FacturaVenta
    template_name = 'sales/facturas_vencidas.html'
    context_object_name = 'facturas'
    paginate_by = 20
    
    def get_queryset(self):
        return FacturaVenta.objects.filter(
            estado='EMITIDA',
            fecha_vencimiento__lt=timezone.now().date()
        ).select_related('cliente').order_by('fecha_vencimiento')
