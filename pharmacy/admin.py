from django.contrib import admin
from .models import Medicamento, Receta, DetalleReceta

@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ('producto', 'dosis', 'presentacion', 'requiere_receta')
    search_fields = ('producto__nombre', 'presentacion')
    list_filter = ('requiere_receta',)

class DetalleRecetaInline(admin.TabularInline):
    model = DetalleReceta
    extra = 1
    raw_id_fields = ('medicamento',)

@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'profesional_prescriptor', 'fecha_emision', 'activa')
    list_filter = ('activa', 'fecha_emision', 'profesional_prescriptor')
    search_fields = ('paciente__nombres', 'paciente__apellidos', 'instrucciones_generales')
    date_hierarchy = 'fecha_emision'
    inlines = [DetalleRecetaInline]
    raw_id_fields = ('paciente', 'profesional_prescriptor')

@admin.register(DetalleReceta)
class DetalleRecetaAdmin(admin.ModelAdmin):
    list_display = ('receta', 'medicamento', 'cantidad', 'unidad', 'dosis_indicada')
    search_fields = ('receta__paciente__nombres', 'medicamento__producto__nombre')
    raw_id_fields = ('receta', 'medicamento')
