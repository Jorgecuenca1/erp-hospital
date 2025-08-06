from django.contrib import admin
from .models import Incidente, Auditoria, HallazgoAuditoria, PlanMejora, DocumentoCalidad

@admin.register(Incidente)
class IncidenteAdmin(admin.ModelAdmin):
    list_display = ('tipo_incidente', 'fecha_hora_incidente', 'severidad', 'estado', 'reportado_por', 'paciente_afectado')
    list_filter = ('tipo_incidente', 'severidad', 'estado', 'fecha_hora_reporte')
    search_fields = ('descripcion', 'paciente_afectado__nombres', 'paciente_afectado__apellidos')
    raw_id_fields = ('reportado_por', 'investigador_asignado', 'paciente_afectado')

@admin.register(Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_auditoria', 'fecha_inicio', 'fecha_fin', 'estado')
    list_filter = ('tipo_auditoria', 'estado', 'fecha_inicio')
    search_fields = ('nombre', 'alcance')
    filter_horizontal = ('equipo_auditor',)

@admin.register(HallazgoAuditoria)
class HallazgoAuditoriaAdmin(admin.ModelAdmin):
    list_display = ('auditoria', 'clasificacion', 'fecha_creacion', 'fecha_limite_correccion', 'cerrado', 'responsable_correccion')
    list_filter = ('clasificacion', 'cerrado', 'fecha_creacion')
    search_fields = ('descripcion', 'auditoria__nombre')
    raw_id_fields = ('auditoria', 'responsable_correccion')

@admin.register(PlanMejora)
class PlanMejoraAdmin(admin.ModelAdmin):
    list_display = ('nombre_plan', 'fecha_creacion', 'fecha_limite', 'responsable', 'estado', 'efectividad')
    list_filter = ('estado', 'efectividad', 'fecha_creacion')
    search_fields = ('nombre_plan', 'descripcion', 'hallazgo__descripcion')
    raw_id_fields = ('hallazgo', 'responsable')

@admin.register(DocumentoCalidad)
class DocumentoCalidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo', 'tipo_documento', 'version', 'fecha_emision', 'activo', 'aprobado_por')
    list_filter = ('tipo_documento', 'activo', 'fecha_emision')
    search_fields = ('nombre', 'codigo')
    raw_id_fields = ('aprobado_por',)
