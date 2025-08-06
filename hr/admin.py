from django.contrib import admin
from .models import Cargo, Empleado, Contrato, Nomina

@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'salario_base')
    search_fields = ('nombre',)

class ContratoInline(admin.StackedInline):
    model = Contrato
    extra = 0 # No mostrar formularios extra por defecto
    max_num = 1 # Solo un contrato por empleado
    raw_id_fields = ('empleado',)

class NominaInline(admin.TabularInline):
    model = Nomina
    extra = 0
    raw_id_fields = ('empleado',)

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'numero_identificacion', 'cargo', 'fecha_contratacion', 'activo')
    list_filter = ('activo', 'cargo', 'fecha_contratacion')
    search_fields = ('nombres', 'apellidos', 'numero_identificacion', 'email')
    date_hierarchy = 'fecha_contratacion'
    inlines = [ContratoInline, NominaInline]
    raw_id_fields = ('cargo', 'profesional_salud')

@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'tipo_contrato', 'fecha_inicio', 'fecha_fin', 'salario')
    list_filter = ('tipo_contrato', 'fecha_inicio', 'fecha_fin')
    search_fields = ('empleado__nombres', 'empleado__apellidos')
    date_hierarchy = 'fecha_inicio'
    raw_id_fields = ('empleado',)

@admin.register(Nomina)
class NominaAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'fecha_pago', 'periodo_inicio', 'periodo_fin', 'salario_neto')
    list_filter = ('fecha_pago', 'periodo_inicio', 'periodo_fin')
    search_fields = ('empleado__nombres', 'empleado__apellidos')
    date_hierarchy = 'fecha_pago'
    raw_id_fields = ('empleado',)
