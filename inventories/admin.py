from django.contrib import admin
from .models import UbicacionAlmacen, CategoriaProducto, Producto, MovimientoInventario, OrdenDispensacion, DetalleOrdenDispensacion

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
    list_display = ('nombre', 'tipo_producto', 'stock_actual', 'stock_minimo', 'ubicacion', 'activo', 'fecha_caducidad')
    list_filter = ('tipo_producto', 'categoria', 'ubicacion', 'activo')
    search_fields = ('nombre', 'descripcion', 'unidad_medida')
    raw_id_fields = ('categoria', 'ubicacion')

@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ('producto', 'tipo_movimiento', 'cantidad', 'fecha_hora', 'razon')
    list_filter = ('tipo_movimiento', 'fecha_hora')
    search_fields = ('producto__nombre', 'razon', 'referencia_documento')
    date_hierarchy = 'fecha_hora'
    raw_id_fields = ('producto',)

class DetalleOrdenDispensacionInline(admin.TabularInline):
    model = DetalleOrdenDispensacion
    extra = 1
    raw_id_fields = ('producto',)

@admin.register(OrdenDispensacion)
class OrdenDispensacionAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'fecha_dispensacion',)
    list_filter = ('fecha_dispensacion',)
    search_fields = ('paciente__nombres', 'paciente__apellidos', 'observaciones')
    date_hierarchy = 'fecha_dispensacion'
    inlines = [DetalleOrdenDispensacionInline]
    raw_id_fields = ('paciente',)
