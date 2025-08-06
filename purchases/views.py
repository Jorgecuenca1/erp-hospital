from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView, View, TemplateView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count, Q, F
from django.utils import timezone
from datetime import timedelta
from .models import (
    Proveedor, ProductoCompra, OrdenCompra, DetalleOrdenCompra,
    FacturaCompra, DetalleFacturaCompra, PagoCompra, RecepcionCompra, 
    DetalleRecepcionCompra, CotizacionCompra, DetalleCotizacionCompra
)
from .forms import (
    ProveedorForm, ProductoCompraForm, OrdenCompraForm, DetalleOrdenCompraForm,
    FacturaCompraForm, DetalleFacturaCompraForm, PagoCompraForm, RecepcionCompraForm,
    CotizacionCompraForm, DetalleCotizacionCompraForm
)
from django.forms import inlineformset_factory

# Inline formsets
DetalleOrdenCompraFormSet = inlineformset_factory(OrdenCompra, DetalleOrdenCompra, form=DetalleOrdenCompraForm, extra=1, can_delete=True)
DetalleFacturaCompraFormSet = inlineformset_factory(FacturaCompra, DetalleFacturaCompra, form=DetalleFacturaCompraForm, extra=1, can_delete=True)
DetalleCotizacionCompraFormSet = inlineformset_factory(CotizacionCompra, DetalleCotizacionCompra, form=DetalleCotizacionCompraForm, extra=1, can_delete=True)

# Dashboard principal
class PurchasesDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'purchases/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estadísticas generales
        context['total_proveedores'] = Proveedor.objects.filter(estado='ACTIVO').count()
        context['total_productos'] = ProductoCompra.objects.filter(activo=True).count()
        context['ordenes_pendientes'] = OrdenCompra.objects.filter(estado__in=['BORRADOR', 'ENVIADA', 'CONFIRMADA']).count()
        context['facturas_pendientes'] = FacturaCompra.objects.filter(estado='RECIBIDA').count()
        
        # Compras del mes actual
        fecha_inicio_mes = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        context['compras_mes'] = FacturaCompra.objects.filter(
            fecha_emision__gte=fecha_inicio_mes,
            estado__in=['RECIBIDA', 'PAGADA']
        ).aggregate(total=Sum('total'))['total'] or 0
        
        # Compras del mes anterior
        fecha_inicio_mes_anterior = (fecha_inicio_mes - timedelta(days=1)).replace(day=1)
        fecha_fin_mes_anterior = fecha_inicio_mes - timedelta(days=1)
        context['compras_mes_anterior'] = FacturaCompra.objects.filter(
            fecha_emision__range=[fecha_inicio_mes_anterior, fecha_fin_mes_anterior],
            estado__in=['RECIBIDA', 'PAGADA']
        ).aggregate(total=Sum('total'))['total'] or 0
        
        # Crecimiento de compras
        if context['compras_mes_anterior'] > 0:
            context['crecimiento_compras'] = ((context['compras_mes'] - context['compras_mes_anterior']) / context['compras_mes_anterior']) * 100
        else:
            context['crecimiento_compras'] = 0
        
        # Facturas recientes
        context['facturas_recientes'] = FacturaCompra.objects.select_related('proveedor').order_by('-fecha_emision')[:5]
        
        # Top proveedores
        context['top_proveedores'] = Proveedor.objects.annotate(
            total_compras=Sum('facturas_compra__total')
        ).filter(total_compras__gt=0).order_by('-total_compras')[:5]
        
        # Productos que necesitan compra
        context['productos_necesitan_compra'] = ProductoCompra.objects.filter(
            activo=True,
            stock_actual__lte=F('stock_minimo')
        ).count()
        
        # Compras por estado
        context['compras_por_estado'] = FacturaCompra.objects.values('estado').annotate(
            count=Count('id'),
            total=Sum('total')
        )
        
        # Compras por mes (últimos 6 meses)
        context['compras_por_mes'] = []
        for i in range(6):
            fecha = timezone.now().date() - timedelta(days=30*i)
            inicio_mes = fecha.replace(day=1)
            fin_mes = (inicio_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            
            compras_mes = FacturaCompra.objects.filter(
                fecha_emision__date__range=[inicio_mes, fin_mes],
                estado__in=['RECIBIDA', 'PAGADA']
            ).aggregate(
                total=Sum('total'),
                count=Count('id')
            )
            
            context['compras_por_mes'].append({
                'mes': inicio_mes.strftime('%B %Y'),
                'total': compras_mes['total'] or 0,
                'cantidad': compras_mes['count'] or 0
            })
        
        return context

# Vistas para Proveedor
class ProveedorListView(LoginRequiredMixin, ListView):
    model = Proveedor
    template_name = 'purchases/proveedor_list.html'
    context_object_name = 'proveedores'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Proveedor.objects.all()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(nombre__icontains=search) |
                Q(identificacion__icontains=search) |
                Q(email__icontains=search)
            )
        return queryset

class ProveedorDetailView(LoginRequiredMixin, DetailView):
    model = Proveedor
    template_name = 'purchases/proveedor_detail.html'
    context_object_name = 'proveedor'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ordenes_recientes'] = self.object.ordenes_compra.order_by('-fecha_orden')[:5]
        context['facturas_recientes'] = self.object.facturas_compra.order_by('-fecha_emision')[:5]
        return context

class ProveedorCreateView(LoginRequiredMixin, CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'purchases/proveedor_form.html'
    success_url = reverse_lazy('purchases:proveedor_list')

class ProveedorUpdateView(LoginRequiredMixin, UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'purchases/proveedor_form.html'
    success_url = reverse_lazy('purchases:proveedor_list')

class ProveedorDeleteView(LoginRequiredMixin, DeleteView):
    model = Proveedor
    template_name = 'purchases/proveedor_confirm_delete.html'
    success_url = reverse_lazy('purchases:proveedor_list')

# Vistas para ProductoCompra
class ProductoCompraListView(LoginRequiredMixin, ListView):
    model = ProductoCompra
    template_name = 'purchases/productocompra_list.html'
    context_object_name = 'productos'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = ProductoCompra.objects.filter(activo=True)
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(nombre__icontains=search) |
                Q(codigo__icontains=search) |
                Q(descripcion__icontains=search)
            )
        return queryset

class ProductoCompraDetailView(LoginRequiredMixin, DetailView):
    model = ProductoCompra
    template_name = 'purchases/productocompra_detail.html'
    context_object_name = 'producto'

class ProductoCompraCreateView(LoginRequiredMixin, CreateView):
    model = ProductoCompra
    form_class = ProductoCompraForm
    template_name = 'purchases/productocompra_form.html'
    success_url = reverse_lazy('purchases:productocompra_list')

class ProductoCompraUpdateView(LoginRequiredMixin, UpdateView):
    model = ProductoCompra
    form_class = ProductoCompraForm
    template_name = 'purchases/productocompra_form.html'
    success_url = reverse_lazy('purchases:productocompra_list')

class ProductoCompraDeleteView(LoginRequiredMixin, DeleteView):
    model = ProductoCompra
    template_name = 'purchases/productocompra_confirm_delete.html'
    success_url = reverse_lazy('purchases:productocompra_list')

# Vistas para OrdenCompra
class OrdenCompraListView(LoginRequiredMixin, ListView):
    model = OrdenCompra
    template_name = 'purchases/ordencompra_list.html'
    context_object_name = 'ordenes'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = OrdenCompra.objects.select_related('proveedor', 'comprador').order_by('-fecha_orden')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(numero_orden__icontains=search) |
                Q(proveedor__nombre__icontains=search)
            )
        return queryset

class OrdenCompraDetailView(LoginRequiredMixin, DetailView):
    model = OrdenCompra
    template_name = 'purchases/ordencompra_detail.html'
    context_object_name = 'orden'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = self.object.items.all()
        return context

class OrdenCompraCreateView(LoginRequiredMixin, CreateView):
    model = OrdenCompra
    form_class = OrdenCompraForm
    template_name = 'purchases/ordencompra_form.html'
    success_url = reverse_lazy('purchases:ordencompra_list')
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['items_formset'] = DetalleOrdenCompraFormSet(self.request.POST, self.request.FILES)
        else:
            data['items_formset'] = DetalleOrdenCompraFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        items_formset = context['items_formset']
        self.object = form.save(commit=False)
        self.object.comprador = self.request.user
        self.object.save()

        if items_formset.is_valid():
            items_formset.instance = self.object
            items_formset.save()
            self.object.calcular_totales()
        else:
            return self.form_invalid(form)
        return super().form_valid(form)

class OrdenCompraUpdateView(LoginRequiredMixin, UpdateView):
    model = OrdenCompra
    form_class = OrdenCompraForm
    template_name = 'purchases/ordencompra_form.html'
    success_url = reverse_lazy('purchases:ordencompra_list')
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['items_formset'] = DetalleOrdenCompraFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['items_formset'] = DetalleOrdenCompraFormSet(instance=self.object)
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

class OrdenCompraDeleteView(LoginRequiredMixin, DeleteView):
    model = OrdenCompra
    template_name = 'purchases/ordencompra_confirm_delete.html'
    success_url = reverse_lazy('purchases:ordencompra_list')

# Vistas para FacturaCompra
class FacturaCompraListView(LoginRequiredMixin, ListView):
    model = FacturaCompra
    template_name = 'purchases/facturacompra_list.html'
    context_object_name = 'facturas'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = FacturaCompra.objects.select_related('proveedor', 'recibido_por').order_by('-fecha_emision')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(numero_factura__icontains=search) |
                Q(proveedor__nombre__icontains=search)
            )
        return queryset

class FacturaCompraDetailView(LoginRequiredMixin, DetailView):
    model = FacturaCompra
    template_name = 'purchases/facturacompra_detail.html'
    context_object_name = 'factura'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = self.object.items.all()
        context['pagos'] = self.object.pagos.all()
        return context

class FacturaCompraCreateView(LoginRequiredMixin, CreateView):
    model = FacturaCompra
    form_class = FacturaCompraForm
    template_name = 'purchases/facturacompra_form.html'
    success_url = reverse_lazy('purchases:facturacompra_list')
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['items_formset'] = DetalleFacturaCompraFormSet(self.request.POST, self.request.FILES)
        else:
            data['items_formset'] = DetalleFacturaCompraFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        items_formset = context['items_formset']
        self.object = form.save(commit=False)
        self.object.recibido_por = self.request.user
        self.object.save()

        if items_formset.is_valid():
            items_formset.instance = self.object
            items_formset.save()
            self.object.calcular_totales()
        else:
            return self.form_invalid(form)
        return super().form_valid(form)

class FacturaCompraUpdateView(LoginRequiredMixin, UpdateView):
    model = FacturaCompra
    form_class = FacturaCompraForm
    template_name = 'purchases/facturacompra_form.html'
    success_url = reverse_lazy('purchases:facturacompra_list')
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['items_formset'] = DetalleFacturaCompraFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['items_formset'] = DetalleFacturaCompraFormSet(instance=self.object)
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

class FacturaCompraDeleteView(LoginRequiredMixin, DeleteView):
    model = FacturaCompra
    template_name = 'purchases/facturacompra_confirm_delete.html'
    success_url = reverse_lazy('purchases:facturacompra_list')

# Vistas para PagoCompra
class PagoCompraListView(LoginRequiredMixin, ListView):
    model = PagoCompra
    template_name = 'purchases/pagocompra_list.html'
    context_object_name = 'pagos'
    paginate_by = 20

class PagoCompraDetailView(LoginRequiredMixin, DetailView):
    model = PagoCompra
    template_name = 'purchases/pagocompra_detail.html'
    context_object_name = 'pago'

class PagoCompraCreateView(LoginRequiredMixin, CreateView):
    model = PagoCompra
    form_class = PagoCompraForm
    template_name = 'purchases/pagocompra_form.html'
    success_url = reverse_lazy('purchases:pagocompra_list')
    
    def form_valid(self, form):
        form.instance.registrado_por = self.request.user
        return super().form_valid(form)

class PagoCompraUpdateView(LoginRequiredMixin, UpdateView):
    model = PagoCompra
    form_class = PagoCompraForm
    template_name = 'purchases/pagocompra_form.html'
    success_url = reverse_lazy('purchases:pagocompra_list')

class PagoCompraDeleteView(LoginRequiredMixin, DeleteView):
    model = PagoCompra
    template_name = 'purchases/pagocompra_confirm_delete.html'
    success_url = reverse_lazy('purchases:pagocompra_list')

# Vistas para RecepcionCompra
class RecepcionCompraListView(LoginRequiredMixin, ListView):
    model = RecepcionCompra
    template_name = 'purchases/recepcioncompra_list.html'
    context_object_name = 'recepciones'
    paginate_by = 10

class RecepcionCompraDetailView(LoginRequiredMixin, DetailView):
    model = RecepcionCompra
    template_name = 'purchases/recepcioncompra_detail.html'
    context_object_name = 'recepcion'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = self.object.items.all()
        return context

class RecepcionCompraCreateView(LoginRequiredMixin, CreateView):
    model = RecepcionCompra
    form_class = RecepcionCompraForm
    template_name = 'purchases/recepcioncompra_form.html'
    success_url = reverse_lazy('purchases:recepcioncompra_list')
    
    def form_valid(self, form):
        form.instance.recibido_por = self.request.user
        return super().form_valid(form)

class RecepcionCompraUpdateView(LoginRequiredMixin, UpdateView):
    model = RecepcionCompra
    form_class = RecepcionCompraForm
    template_name = 'purchases/recepcioncompra_form.html'
    success_url = reverse_lazy('purchases:recepcioncompra_list')

class RecepcionCompraDeleteView(LoginRequiredMixin, DeleteView):
    model = RecepcionCompra
    template_name = 'purchases/recepcioncompra_confirm_delete.html'
    success_url = reverse_lazy('purchases:recepcioncompra_list')

# Vistas para CotizacionCompra
class CotizacionCompraListView(LoginRequiredMixin, ListView):
    model = CotizacionCompra
    template_name = 'purchases/cotizacioncompra_list.html'
    context_object_name = 'cotizaciones'
    paginate_by = 10

class CotizacionCompraDetailView(LoginRequiredMixin, DetailView):
    model = CotizacionCompra
    template_name = 'purchases/cotizacioncompra_detail.html'
    context_object_name = 'cotizacion'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = self.object.items.all()
        return context

class CotizacionCompraCreateView(LoginRequiredMixin, CreateView):
    model = CotizacionCompra
    form_class = CotizacionCompraForm
    template_name = 'purchases/cotizacioncompra_form.html'
    success_url = reverse_lazy('purchases:cotizacioncompra_list')
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['items_formset'] = DetalleCotizacionCompraFormSet(self.request.POST, self.request.FILES)
        else:
            data['items_formset'] = DetalleCotizacionCompraFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        items_formset = context['items_formset']
        self.object = form.save(commit=False)
        self.object.solicitado_por = self.request.user
        self.object.save()

        if items_formset.is_valid():
            items_formset.instance = self.object
            items_formset.save()
            self.object.calcular_totales()
        else:
            return self.form_invalid(form)
        return super().form_valid(form)

class CotizacionCompraUpdateView(LoginRequiredMixin, UpdateView):
    model = CotizacionCompra
    form_class = CotizacionCompraForm
    template_name = 'purchases/cotizacioncompra_form.html'
    success_url = reverse_lazy('purchases:cotizacioncompra_list')
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['items_formset'] = DetalleCotizacionCompraFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['items_formset'] = DetalleCotizacionCompraFormSet(instance=self.object)
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

class CotizacionCompraDeleteView(LoginRequiredMixin, DeleteView):
    model = CotizacionCompra
    template_name = 'purchases/cotizacioncompra_confirm_delete.html'
    success_url = reverse_lazy('purchases:cotizacioncompra_list')

# Vistas para Reportes
class PurchasesReportsView(LoginRequiredMixin, TemplateView):
    template_name = 'purchases/reports.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estadísticas para reportes
        context['total_compras'] = FacturaCompra.objects.filter(estado__in=['RECIBIDA', 'PAGADA']).count()
        context['compras_por_estado'] = FacturaCompra.objects.values('estado').annotate(
            count=Count('id'),
            total=Sum('total')
        )
        
        # Top 5 proveedores con más compras
        context['top_proveedores'] = Proveedor.objects.annotate(
            total_compras=Sum('facturas_compra__total'),
            cantidad_facturas=Count('facturas_compra')
        ).filter(total_compras__gt=0).order_by('-total_compras')[:5]
        
        # Top 5 productos más comprados
        context['top_productos'] = ProductoCompra.objects.annotate(
            total_comprado=Sum('detallefacturacompra__cantidad'),
            total_gastado=Sum('detallefacturacompra__total')
        ).filter(total_comprado__gt=0).order_by('-total_gastado')[:5]
        
        # Compras por mes (últimos 12 meses)
        context['compras_por_mes'] = []
        for i in range(12):
            fecha = timezone.now().date() - timedelta(days=30*i)
            inicio_mes = fecha.replace(day=1)
            fin_mes = (inicio_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            
            compras_mes = FacturaCompra.objects.filter(
                fecha_emision__date__range=[inicio_mes, fin_mes],
                estado__in=['RECIBIDA', 'PAGADA']
            ).aggregate(
                total=Sum('total'),
                count=Count('id')
            )
            
            context['compras_por_mes'].append({
                'mes': inicio_mes.strftime('%B %Y'),
                'total': compras_mes['total'] or 0,
                'cantidad': compras_mes['count'] or 0
            })
        
        return context

# Vistas adicionales
class FacturasPendientesView(LoginRequiredMixin, ListView):
    model = FacturaCompra
    template_name = 'purchases/facturas_pendientes.html'
    context_object_name = 'facturas'
    paginate_by = 20
    
    def get_queryset(self):
        return FacturaCompra.objects.filter(
            estado='RECIBIDA'
        ).select_related('proveedor').order_by('fecha_vencimiento')

class FacturasVencidasView(LoginRequiredMixin, ListView):
    model = FacturaCompra
    template_name = 'purchases/facturas_vencidas.html'
    context_object_name = 'facturas'
    paginate_by = 20
    
    def get_queryset(self):
        return FacturaCompra.objects.filter(
            estado='RECIBIDA',
            fecha_vencimiento__lt=timezone.now().date()
        ).select_related('proveedor').order_by('fecha_vencimiento')

class ProductosNecesitanCompraView(LoginRequiredMixin, ListView):
    model = ProductoCompra
    template_name = 'purchases/productos_necesitan_compra.html'
    context_object_name = 'productos'
    paginate_by = 20
    
    def get_queryset(self):
        return ProductoCompra.objects.filter(
            activo=True,
            stock_actual__lte=F('stock_minimo')
        ).order_by('stock_actual')
