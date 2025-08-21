from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count, Q, F
from django.utils import timezone
from datetime import timedelta
from .models import (
    UbicacionAlmacen, CategoriaProducto, Producto, MovimientoInventario, 
    OrdenDispensacion, DetalleOrdenDispensacion, OrdenCompra, DetalleOrdenCompra,
    RecepcionMercancia, DetalleRecepcionMercancia, InventarioFisico, DetalleInventarioFisico
)
from .forms import (
    UbicacionAlmacenForm, CategoriaProductoForm, ProductoForm, MovimientoInventarioForm, 
    OrdenDispensacionForm, DetalleOrdenDispensacionForm
)

# Dashboard principal
class InventoryDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'inventories/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estadísticas generales
        context['total_productos'] = Producto.objects.filter(activo=True).count()
        context['total_categorias'] = CategoriaProducto.objects.count()
        context['total_ubicaciones'] = UbicacionAlmacen.objects.count()
        context['total_movimientos'] = MovimientoInventario.objects.count()
        
        # Productos con stock bajo
        context['productos_stock_bajo'] = Producto.objects.filter(
            activo=True,
            stock_actual__lte=F('stock_minimo')
        ).count()
        
        # Productos próximos a caducar (30 días)
        fecha_limite = timezone.now().date() + timedelta(days=30)
        context['productos_caducando'] = Producto.objects.filter(
            activo=True,
            fecha_caducidad__lte=fecha_limite,
            fecha_caducidad__gte=timezone.now().date()
        ).count()
        
        # Últimos movimientos
        context['ultimos_movimientos'] = MovimientoInventario.objects.select_related('producto').order_by('-fecha_hora')[:5]
        
        # Productos más movidos
        context['productos_mas_movidos'] = Producto.objects.annotate(
            total_movimientos=Count('movimientos')
        ).order_by('-total_movimientos')[:5]
        
        # Stock por categoría
        context['stock_por_categoria'] = CategoriaProducto.objects.annotate(
            total_stock=Sum('productos__stock_actual')
        ).filter(total_stock__gt=0)
        
        # Valor total del inventario
        context['valor_total_inventario'] = Producto.objects.filter(activo=True).aggregate(
            total=Sum(F('stock_actual') * F('precio_venta'))
        )['total'] or 0
        
        # Movimientos por tipo en el último mes
        fecha_inicio_mes = timezone.now().date() - timedelta(days=30)
        context['movimientos_entrada'] = MovimientoInventario.objects.filter(
            tipo_movimiento='ENTRADA',
            fecha_hora__date__gte=fecha_inicio_mes
        ).count()
        context['movimientos_salida'] = MovimientoInventario.objects.filter(
            tipo_movimiento='SALIDA',
            fecha_hora__date__gte=fecha_inicio_mes
        ).count()
        
        return context

# Vistas para UbicacionAlmacen
class UbicacionAlmacenListView(LoginRequiredMixin, ListView):
    model = UbicacionAlmacen
    template_name = 'inventories/ubicacionalmacen_list.html'
    context_object_name = 'ubicaciones'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = UbicacionAlmacen.objects.all()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(nombre__icontains=search) |
                Q(descripcion__icontains=search)
            )
        return queryset

class UbicacionAlmacenDetailView(LoginRequiredMixin, DetailView):
    model = UbicacionAlmacen
    template_name = 'inventories/ubicacionalmacen_detail.html'
    context_object_name = 'ubicacion'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['productos_en_ubicacion'] = self.object.productos.filter(activo=True)
        return context

class UbicacionAlmacenCreateView(LoginRequiredMixin, CreateView):
    model = UbicacionAlmacen
    form_class = UbicacionAlmacenForm
    template_name = 'inventories/ubicacionalmacen_form.html'
    success_url = reverse_lazy('inventories:ubicacion_list')

class UbicacionAlmacenUpdateView(LoginRequiredMixin, UpdateView):
    model = UbicacionAlmacen
    form_class = UbicacionAlmacenForm
    template_name = 'inventories/ubicacionalmacen_form.html'
    success_url = reverse_lazy('inventories:ubicacion_list')

class UbicacionAlmacenDeleteView(LoginRequiredMixin, DeleteView):
    model = UbicacionAlmacen
    template_name = 'inventories/ubicacionalmacen_confirm_delete.html'
    success_url = reverse_lazy('inventories:ubicacion_list')

# Vistas para CategoriaProducto
class CategoriaProductoListView(LoginRequiredMixin, ListView):
    model = CategoriaProducto
    template_name = 'inventories/categoriaproducto_list.html'
    context_object_name = 'categorias'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = CategoriaProducto.objects.all()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(nombre__icontains=search)
        return queryset

class CategoriaProductoDetailView(LoginRequiredMixin, DetailView):
    model = CategoriaProducto
    template_name = 'inventories/categoriaproducto_detail.html'
    context_object_name = 'categoria'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['productos_en_categoria'] = self.object.productos.filter(activo=True)
        context['total_stock_categoria'] = self.object.productos.filter(activo=True).aggregate(
            total=Sum('stock_actual')
        )['total'] or 0
        return context

class CategoriaProductoCreateView(LoginRequiredMixin, CreateView):
    model = CategoriaProducto
    form_class = CategoriaProductoForm
    template_name = 'inventories/categoriaproducto_form.html'
    success_url = reverse_lazy('inventories:categoria_list')

class CategoriaProductoUpdateView(LoginRequiredMixin, UpdateView):
    model = CategoriaProducto
    form_class = CategoriaProductoForm
    template_name = 'inventories/categoriaproducto_form.html'
    success_url = reverse_lazy('inventories:categoria_list')

class CategoriaProductoDeleteView(LoginRequiredMixin, DeleteView):
    model = CategoriaProducto
    template_name = 'inventories/categoriaproducto_confirm_delete.html'
    success_url = reverse_lazy('inventories:categoria_list')

# Vistas para Producto
class ProductoListView(LoginRequiredMixin, ListView):
    model = Producto
    template_name = 'inventories/producto_list.html'
    context_object_name = 'productos'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Producto.objects.filter(activo=True).select_related('categoria', 'ubicacion')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(nombre__icontains=search) |
                Q(descripcion__icontains=search) |
                Q(categoria__nombre__icontains=search)
            )
        return queryset

class ProductoDetailView(LoginRequiredMixin, DetailView):
    model = Producto
    template_name = 'inventories/producto_detail.html'
    context_object_name = 'producto'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movimientos_recientes'] = self.object.movimientos.order_by('-fecha_hora')[:10]
        context['valor_total_stock'] = self.object.stock_actual * self.object.precio_unitario
        return context

class ProductoCreateView(LoginRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'inventories/producto_form.html'
    success_url = reverse_lazy('inventories:producto_list')

class ProductoUpdateView(LoginRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'inventories/producto_form.html'
    success_url = reverse_lazy('inventories:producto_list')

class ProductoDeleteView(LoginRequiredMixin, DeleteView):
    model = Producto
    template_name = 'inventories/producto_confirm_delete.html'
    success_url = reverse_lazy('inventories:producto_list')

# Vistas para MovimientoInventario
class MovimientoInventarioListView(LoginRequiredMixin, ListView):
    model = MovimientoInventario
    template_name = 'inventories/movimientoinventario_list.html'
    context_object_name = 'movimientos'
    paginate_by = 10
    
    def get_queryset(self):
        return MovimientoInventario.objects.select_related('producto').order_by('-fecha_hora')

class MovimientoInventarioDetailView(LoginRequiredMixin, DetailView):
    model = MovimientoInventario
    template_name = 'inventories/movimientoinventario_detail.html'
    context_object_name = 'movimiento'

class MovimientoInventarioCreateView(LoginRequiredMixin, CreateView):
    model = MovimientoInventario
    form_class = MovimientoInventarioForm
    template_name = 'inventories/movimientoinventario_form.html'
    success_url = reverse_lazy('inventories:movimiento_list')

class MovimientoInventarioUpdateView(LoginRequiredMixin, UpdateView):
    model = MovimientoInventario
    form_class = MovimientoInventarioForm
    template_name = 'inventories/movimientoinventario_form.html'
    success_url = reverse_lazy('inventories:movimiento_list')

class MovimientoInventarioDeleteView(LoginRequiredMixin, DeleteView):
    model = MovimientoInventario
    template_name = 'inventories/movimientoinventario_confirm_delete.html'
    success_url = reverse_lazy('inventories:movimiento_list')

# Vistas para OrdenDispensacion
class OrdenDispensacionListView(LoginRequiredMixin, ListView):
    model = OrdenDispensacion
    template_name = 'inventories/ordendispensacion_list.html'
    context_object_name = 'ordenes'
    paginate_by = 10
    
    def get_queryset(self):
        return OrdenDispensacion.objects.select_related('paciente').order_by('-fecha_dispensacion')

class OrdenDispensacionDetailView(LoginRequiredMixin, DetailView):
    model = OrdenDispensacion
    template_name = 'inventories/ordendispensacion_detail.html'
    context_object_name = 'orden'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detalles_orden'] = self.object.detalles.all()
        return context

class OrdenDispensacionCreateView(LoginRequiredMixin, CreateView):
    model = OrdenDispensacion
    form_class = OrdenDispensacionForm
    template_name = 'inventories/ordendispensacion_form.html'
    success_url = reverse_lazy('inventories:orden_list')

class OrdenDispensacionUpdateView(LoginRequiredMixin, UpdateView):
    model = OrdenDispensacion
    form_class = OrdenDispensacionForm
    template_name = 'inventories/ordendispensacion_form.html'
    success_url = reverse_lazy('inventories:orden_list')

class OrdenDispensacionDeleteView(LoginRequiredMixin, DeleteView):
    model = OrdenDispensacion
    template_name = 'inventories/ordendispensacion_confirm_delete.html'
    success_url = reverse_lazy('inventories:orden_list')

# Vistas para Reportes
class InventoryReportsView(LoginRequiredMixin, TemplateView):
    template_name = 'inventories/reports.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estadísticas para reportes
        context['total_productos'] = Producto.objects.filter(activo=True).count()
        context['productos_stock_bajo'] = Producto.objects.filter(
            activo=True,
            stock_actual__lte=F('stock_minimo')
        ).count()
        
        # Movimientos por tipo
        context['entradas'] = MovimientoInventario.objects.filter(tipo_movimiento='ENTRADA').count()
        context['salidas'] = MovimientoInventario.objects.filter(tipo_movimiento='SALIDA').count()
        context['ajustes'] = MovimientoInventario.objects.filter(tipo_movimiento='AJUSTE').count()
        
        # Productos por categoría
        context['productos_por_categoria'] = CategoriaProducto.objects.annotate(
            total_productos=Count('productos')
        ).filter(total_productos__gt=0)
        
        # Valor del inventario por categoría
        context['valor_por_categoria'] = CategoriaProducto.objects.annotate(
            valor_total=Sum(F('productos__stock_actual') * F('productos__precio_unitario'))
        ).filter(valor_total__gt=0)
        
        # Movimientos por mes (últimos 6 meses)
        context['movimientos_por_mes'] = []
        for i in range(6):
            fecha = timezone.now().date() - timedelta(days=30*i)
            inicio_mes = fecha.replace(day=1)
            fin_mes = (inicio_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            
            movimientos_mes = MovimientoInventario.objects.filter(
                fecha_hora__date__range=[inicio_mes, fin_mes]
            ).count()
            
            context['movimientos_por_mes'].append({
                'mes': inicio_mes.strftime('%B %Y'),
                'total': movimientos_mes
            })
        
        return context

class LowStockView(LoginRequiredMixin, ListView):
    model = Producto
    template_name = 'inventories/low_stock.html'
    context_object_name = 'productos'
    paginate_by = 20
    
    def get_queryset(self):
        return Producto.objects.filter(
            activo=True,
            stock_actual__lte=F('stock_minimo')
        ).select_related('categoria', 'ubicacion').order_by('stock_actual')

class ExpiredProductsView(LoginRequiredMixin, ListView):
    model = Producto
    template_name = 'inventories/expired_products.html'
    context_object_name = 'productos'
    paginate_by = 20
    
    def get_queryset(self):
        fecha_limite = timezone.now().date() + timedelta(days=30)
        return Producto.objects.filter(
            activo=True,
            fecha_caducidad__lte=fecha_limite,
            fecha_caducidad__gte=timezone.now().date()
        ).select_related('categoria', 'ubicacion').order_by('fecha_caducidad')

class MovementsSummaryView(LoginRequiredMixin, ListView):
    model = MovimientoInventario
    template_name = 'inventories/movements_summary.html'
    context_object_name = 'movimientos'
    paginate_by = 20
    
    def get_queryset(self):
        return MovimientoInventario.objects.select_related('producto').order_by('-fecha_hora')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Resumen de movimientos por tipo
        context['resumen_por_tipo'] = MovimientoInventario.objects.values('tipo_movimiento').annotate(
            total=Count('id'),
            cantidad_total=Sum('cantidad')
        )
        
        # Resumen por producto
        context['resumen_por_producto'] = MovimientoInventario.objects.values(
            'producto__nombre'
        ).annotate(
            total_movimientos=Count('id'),
            cantidad_total=Sum('cantidad')
        ).order_by('-total_movimientos')[:10]
        
        return context

# ==================== ÓRDENES DE COMPRA ====================

class OrdenCompraListView(LoginRequiredMixin, ListView):
    model = OrdenCompra
    template_name = 'inventories/ordencompra_list.html'
    context_object_name = 'ordenes'
    paginate_by = 20
    
    def get_queryset(self):
        return OrdenCompra.objects.select_related('proveedor').order_by('-fecha_orden')

class OrdenCompraDetailView(LoginRequiredMixin, DetailView):
    model = OrdenCompra
    template_name = 'inventories/ordencompra_detail.html'
    context_object_name = 'orden'

class OrdenCompraCreateView(LoginRequiredMixin, CreateView):
    model = OrdenCompra
    template_name = 'inventories/ordencompra_form.html'
    fields = ['proveedor', 'fecha_orden', 'fecha_entrega_esperada', 'observaciones']
    success_url = reverse_lazy('inventories:ordencompra_list')

class OrdenCompraUpdateView(LoginRequiredMixin, UpdateView):
    model = OrdenCompra
    template_name = 'inventories/ordencompra_form.html'
    fields = ['proveedor', 'fecha_orden', 'fecha_entrega_esperada', 'estado', 'observaciones']
    success_url = reverse_lazy('inventories:ordencompra_list')

class OrdenCompraDeleteView(LoginRequiredMixin, DeleteView):
    model = OrdenCompra
    template_name = 'inventories/ordencompra_confirm_delete.html'
    success_url = reverse_lazy('inventories:ordencompra_list')

# ==================== RECEPCIÓN DE MERCANCÍA ====================

class RecepcionMercanciaListView(LoginRequiredMixin, ListView):
    model = RecepcionMercancia
    template_name = 'inventories/recepcionmercancia_list.html'
    context_object_name = 'recepciones'
    paginate_by = 20
    
    def get_queryset(self):
        return RecepcionMercancia.objects.select_related('orden_compra', 'orden_compra__proveedor').order_by('-fecha_recepcion')

class RecepcionMercanciaDetailView(LoginRequiredMixin, DetailView):
    model = RecepcionMercancia
    template_name = 'inventories/recepcionmercancia_detail.html'
    context_object_name = 'recepcion'

class RecepcionMercanciaCreateView(LoginRequiredMixin, CreateView):
    model = RecepcionMercancia
    template_name = 'inventories/recepcionmercancia_form.html'
    fields = ['orden_compra', 'numero_factura_proveedor', 'numero_remision', 'observaciones']
    success_url = reverse_lazy('inventories:recepcionmercancia_list')

class RecepcionMercanciaUpdateView(LoginRequiredMixin, UpdateView):
    model = RecepcionMercancia
    template_name = 'inventories/recepcionmercancia_form.html'
    fields = ['orden_compra', 'numero_factura_proveedor', 'numero_remision', 'estado', 'observaciones']
    success_url = reverse_lazy('inventories:recepcionmercancia_list')

class RecepcionMercanciaDeleteView(LoginRequiredMixin, DeleteView):
    model = RecepcionMercancia
    template_name = 'inventories/recepcionmercancia_confirm_delete.html'
    success_url = reverse_lazy('inventories:recepcionmercancia_list')

# ==================== INVENTARIO FÍSICO ====================

class InventarioFisicoListView(LoginRequiredMixin, ListView):
    model = InventarioFisico
    template_name = 'inventories/inventariofisico_list.html'
    context_object_name = 'inventarios'
    paginate_by = 20
    
    def get_queryset(self):
        return InventarioFisico.objects.all().order_by('-fecha_planificada')

class InventarioFisicoDetailView(LoginRequiredMixin, DetailView):
    model = InventarioFisico
    template_name = 'inventories/inventariofisico_detail.html'
    context_object_name = 'inventario'

class InventarioFisicoCreateView(LoginRequiredMixin, CreateView):
    model = InventarioFisico
    template_name = 'inventories/inventariofisico_form.html'
    fields = ['nombre', 'fecha_planificada', 'ubicaciones', 'categorias', 'tipos_producto']
    success_url = reverse_lazy('inventories:inventariofisico_list')

class InventarioFisicoUpdateView(LoginRequiredMixin, UpdateView):
    model = InventarioFisico
    template_name = 'inventories/inventariofisico_form.html'
    fields = ['nombre', 'fecha_planificada', 'fecha_inicio', 'fecha_fin', 'estado', 'ubicaciones', 'categorias', 'tipos_producto']
    success_url = reverse_lazy('inventories:inventariofisico_list')

class InventarioFisicoDeleteView(LoginRequiredMixin, DeleteView):
    model = InventarioFisico
    template_name = 'inventories/inventariofisico_confirm_delete.html'
    success_url = reverse_lazy('inventories:inventariofisico_list')
