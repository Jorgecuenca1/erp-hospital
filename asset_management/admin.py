from django.contrib import admin
from .models import CategoriaActivo, ActivoFijo, Mantenimiento, BajaActivo

@admin.register(CategoriaActivo)
class CategoriaActivoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

@admin.register(ActivoFijo)
class ActivoFijoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo_activo', 'numero_serie', 'categoria', 'estado', 'fecha_adquisicion', 'responsable')
    search_fields = ('nombre', 'codigo_activo', 'numero_serie')
    list_filter = ('categoria', 'estado', 'fecha_adquisicion')
    raw_id_fields = ('responsable',)

@admin.register(Mantenimiento)
class MantenimientoAdmin(admin.ModelAdmin):
    list_display = ('activo', 'tipo_mantenimiento', 'fecha_inicio', 'fecha_fin', 'costo', 'responsable_mantenimiento')
    search_fields = ('activo__nombre', 'responsable_mantenimiento')
    list_filter = ('tipo_mantenimiento', 'fecha_inicio')
    raw_id_fields = ('activo',)

@admin.register(BajaActivo)
class BajaActivoAdmin(admin.ModelAdmin):
    list_display = ('activo', 'fecha_baja', 'razon_baja', 'aprobado_por')
    search_fields = ('activo__nombre', 'razon_baja')
    list_filter = ('fecha_baja',)
    raw_id_fields = ('activo', 'aprobado_por',)
