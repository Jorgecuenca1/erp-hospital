from django.contrib import admin
from .models import TipoExamen, EquipoLaboratorio, OrdenExamen, ResultadoExamen

@admin.register(TipoExamen)
class TipoExamenAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'es_imagen')
    search_fields = ('nombre',)
    list_filter = ('es_imagen',)

@admin.register(EquipoLaboratorio)
class EquipoLaboratorioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'modelo', 'numero_serie', 'activo')
    search_fields = ('nombre', 'numero_serie')
    list_filter = ('activo',)

@admin.register(OrdenExamen)
class OrdenExamenAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'tipo_examen', 'fecha_orden', 'estado', 'profesional_solicitante')
    list_filter = ('estado', 'tipo_examen', 'fecha_orden')
    search_fields = ('paciente__nombres', 'paciente__apellidos', 'tipo_examen__nombre', 'notas')
    date_hierarchy = 'fecha_orden'
    raw_id_fields = ('paciente', 'profesional_solicitante', 'tipo_examen', 'consulta')

@admin.register(ResultadoExamen)
class ResultadoExamenAdmin(admin.ModelAdmin):
    list_display = ('orden_examen', 'fecha_resultado', 'validado', 'profesional_responsable')
    list_filter = ('validado', 'fecha_resultado', 'profesional_responsable')
    search_fields = ('orden_examen__tipo_examen__nombre', 'orden_examen__paciente__nombres', 'resultado_texto')
    date_hierarchy = 'fecha_resultado'
    raw_id_fields = ('orden_examen', 'profesional_responsable', 'equipo_utilizado')
