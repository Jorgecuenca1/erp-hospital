from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    UbicacionAlmacen, CategoriaProducto, Producto, MovimientoInventario, 
    OrdenDispensacion, DetalleOrdenDispensacion, OrdenCompra, DetalleOrdenCompra,
    RecepcionMercancia, DetalleRecepcionMercancia, InventarioFisico, DetalleInventarioFisico
)

@admin.register(UbicacionAlmacen)
class UbicacionAlmacenAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

@admin.register(CategoriaProducto)
class CategoriaProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'tipo_producto', 'stock_actual', 'stock_minimo', 'precio_venta', 
                   'estado', 'necesita_restock_display', 'valor_inventario_display')
    list_filter = ('tipo_producto', 'categoria', 'ubicacion', 'activo', 'estado', 'requiere_prescripcion')
    search_fields = ('codigo', 'codigo_barras', 'nombre', 'descripcion')
    readonly_fields = ('stock_actual', 'valor_inventario', 'fecha_creacion', 'fecha_actualizacion')
    raw_id_fields = ('categoria', 'ubicacion', 'proveedor_principal', 'cuenta_inventario', 
                    'cuenta_costo_venta', 'creado_por', 'modificado_por')
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('codigo', 'codigo_barras', 'nombre', 'descripcion', 'tipo_producto', 'categoria')
        }),
        ('Inventario', {
            'fields': ('stock_actual', 'stock_minimo', 'stock_maximo', 'ubicacion', 'unidad_medida')
        }),
        ('Precios y Costos', {
            'fields': ('precio_compra', 'precio_venta', 'margen_ganancia')
        }),
        ('Información Física', {
            'fields': ('peso', 'volumen', 'fecha_caducidad')
        }),
        ('Control y Estado', {
            'fields': ('estado', 'activo', 'requiere_prescripcion', 'controlado')
        }),
        ('Contabilidad', {
            'fields': ('cuenta_inventario', 'cuenta_costo_venta')
        }),
        ('Proveedor', {
            'fields': ('proveedor_principal',)
        }),
        ('Auditoría', {
            'fields': ('creado_por', 'modificado_por', 'fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        })
    )
    
    def necesita_restock_display(self, obj):
        if obj.necesita_restock:
            return format_html('<span style="color: red; font-weight: bold;">SÍ</span>')
        return format_html('<span style="color: green;">No</span>')
    necesita_restock_display.short_description = 'Necesita Restock'
    
    def valor_inventario_display(self, obj):
        valor = obj.valor_inventario
        return format_html('<span style="font-weight: bold;">${:,.2f}</span>', valor)
    valor_inventario_display.short_description = 'Valor Inventario'

@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ('producto', 'tipo_movimiento', 'cantidad', 'fecha_hora', 'estado', 'observaciones')
    list_filter = ('tipo_movimiento', 'fecha_hora', 'estado')
    search_fields = ('producto__nombre', 'observaciones', 'referencia_documento')
    date_hierarchy = 'fecha_hora'
    raw_id_fields = ('producto', 'proveedor', 'ubicacion_origen', 'ubicacion_destino')

class DetalleOrdenDispensacionInline(admin.TabularInline):
    model = DetalleOrdenDispensacion
    extra = 1
    raw_id_fields = ('producto',)

# ==================== ÓRDENES DE COMPRA ====================

class DetalleOrdenCompraInline(admin.TabularInline):
    model = DetalleOrdenCompra
    extra = 1
    raw_id_fields = ('producto',)
    readonly_fields = ('subtotal',)
    fields = ('producto', 'cantidad', 'precio_unitario', 'subtotal', 'observaciones')

@admin.register(OrdenCompra)
class OrdenCompraAdmin(admin.ModelAdmin):
    list_display = ('numero', 'proveedor', 'fecha_orden', 'estado', 'total', 'contabilizada')
    list_filter = ('estado', 'fecha_orden', 'contabilizada')
    search_fields = ('numero', 'proveedor__nombre', 'observaciones')
    date_hierarchy = 'fecha_orden'
    readonly_fields = ('numero', 'total')
    raw_id_fields = ('proveedor', 'asiento_contable')
    inlines = [DetalleOrdenCompraInline]
    
    fieldsets = (
        ('Información General', {
            'fields': ('numero', 'proveedor', 'fecha_orden', 'fecha_entrega_esperada')
        }),
        ('Estado y Control', {
            'fields': ('estado', 'observaciones')
        }),
        ('Totales', {
            'fields': ('subtotal', 'impuestos', 'total'),
            'classes': ('collapse',)
        }),
        ('Contabilidad', {
            'fields': ('asiento_contable', 'contabilizada'),
            'classes': ('collapse',)
        })
    )

# ==================== RECEPCIÓN DE MERCANCÍA ====================

class DetalleRecepcionMercanciaInline(admin.TabularInline):
    model = DetalleRecepcionMercancia
    extra = 0
    raw_id_fields = ('detalle_orden',)

@admin.register(RecepcionMercancia)
class RecepcionMercanciaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'orden_compra', 'fecha_recepcion', 'estado')
    list_filter = ('estado', 'fecha_recepcion')
    search_fields = ('numero', 'orden_compra__numero', 'observaciones')
    date_hierarchy = 'fecha_recepcion'
    readonly_fields = ('numero', 'fecha_recepcion')
    raw_id_fields = ('orden_compra',)
    inlines = [DetalleRecepcionMercanciaInline]

# ==================== INVENTARIO FÍSICO ====================

class DetalleInventarioFisicoInline(admin.TabularInline):
    model = DetalleInventarioFisico
    extra = 0
    raw_id_fields = ('producto',)

@admin.register(InventarioFisico)
class InventarioFisicoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_planificada', 'fecha_inicio', 'fecha_fin', 'estado')
    list_filter = ('estado', 'fecha_planificada')
    search_fields = ('nombre',)
    date_hierarchy = 'fecha_planificada'
    readonly_fields = ('fecha_inicio', 'fecha_fin')
    filter_horizontal = ('categorias', 'ubicaciones')
    inlines = [DetalleInventarioFisicoInline]
    
    fieldsets = (
        ('Información General', {
            'fields': ('nombre', 'fecha_planificada', 'fecha_inicio', 'fecha_fin')
        }),
        ('Alcance', {
            'fields': ('categorias', 'ubicaciones', 'tipos_producto')
        }),
        ('Estado', {
            'fields': ('estado',)
        })
    )

# ==================== DISPENSACIÓN ====================

@admin.register(OrdenDispensacion)
class OrdenDispensacionAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'fecha_dispensacion',)
    list_filter = ('fecha_dispensacion',)
    search_fields = ('paciente__nombres', 'paciente__apellidos', 'observaciones')
    date_hierarchy = 'fecha_dispensacion'
    inlines = [DetalleOrdenDispensacionInline]
    raw_id_fields = ('paciente',)
