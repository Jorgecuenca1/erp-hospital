from django.contrib import admin
from django.utils.html import format_html
from .models import (
    PuntoVenta, Caja, SesionCaja, MetodoPagoPOS, VentaPOS, LineaVentaPOS,
    PromocionesPOS, MovimientoCaja
)

@admin.register(PuntoVenta)
class PuntoVentaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'tipo_pos', 'ubicacion', 'activo')
    list_filter = ('tipo_pos', 'activo')
    search_fields = ('codigo', 'nombre', 'ubicacion')

@admin.register(Caja) 
class CajaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'punto_venta', 'activo')
    list_filter = ('punto_venta', 'activo')
    search_fields = ('codigo', 'nombre')

@admin.register(SesionCaja)
class SesionCajaAdmin(admin.ModelAdmin):
    list_display = ('numero_sesion', 'caja', 'usuario', 'fecha_apertura', 'estado')
    list_filter = ('estado', 'fecha_apertura')
    search_fields = ('numero_sesion', 'caja__nombre')

@admin.register(MetodoPagoPOS)
class MetodoPagoPOSAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'tipo_metodo', 'activo')
    list_filter = ('tipo_metodo', 'activo')
    search_fields = ('codigo', 'nombre')

class LineaVentaPOSInline(admin.TabularInline):
    model = LineaVentaPOS
    extra = 0

@admin.register(VentaPOS)
class VentaPOSAdmin(admin.ModelAdmin):
    list_display = ('numero_ticket', 'fecha', 'vendedor', 'total', 'estado')
    list_filter = ('estado', 'fecha', 'metodo_pago')
    search_fields = ('numero_ticket', 'nombre_cliente')
    inlines = [LineaVentaPOSInline]

@admin.register(PromocionesPOS)
class PromocionesPOSAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'tipo_promocion', 'activa')
    list_filter = ('tipo_promocion', 'activa')
    search_fields = ('codigo', 'nombre')

@admin.register(MovimientoCaja)
class MovimientoCajaAdmin(admin.ModelAdmin):
    list_display = ('sesion', 'tipo_movimiento', 'monto', 'concepto', 'fecha')
    list_filter = ('tipo_movimiento', 'fecha')
    search_fields = ('concepto',)
