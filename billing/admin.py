from django.contrib import admin
from .models import Factura, DetalleFactura, TransaccionDIAN

class DetalleFacturaInline(admin.TabularInline):
    model = DetalleFactura
    extra = 1
    raw_id_fields = ('producto',)

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('numero_factura', 'paciente', 'fecha_emision', 'total_neto', 'estado', 'cufe')
    list_filter = ('estado', 'fecha_emision')
    search_fields = ('numero_factura', 'paciente__nombres', 'paciente__apellidos', 'cufe', 'uuid')
    date_hierarchy = 'fecha_emision'
    inlines = [DetalleFacturaInline]
    raw_id_fields = ('paciente',)

@admin.register(DetalleFactura)
class DetalleFacturaAdmin(admin.ModelAdmin):
    list_display = ('factura', 'producto', 'descripcion', 'cantidad', 'precio_unitario', 'total_linea')
    search_fields = ('factura__numero_factura', 'producto__nombre', 'descripcion')
    raw_id_fields = ('factura', 'producto')

@admin.register(TransaccionDIAN)
class TransaccionDIANAdmin(admin.ModelAdmin):
    list_display = ('factura', 'fecha_transaccion', 'tipo_transaccion', 'estado_respuesta')
    list_filter = ('tipo_transaccion', 'estado_respuesta', 'fecha_transaccion')
    search_fields = ('factura__numero_factura', 'tipo_transaccion', 'mensaje_error')
    date_hierarchy = 'fecha_transaccion'
    raw_id_fields = ('factura',)
