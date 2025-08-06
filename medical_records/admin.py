from django.contrib import admin
from .models import Consulta, Diagnostico, Procedimiento, SignosVitales, NotaEvolucion, DocumentoAdjunto

@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('historia_clinica', 'profesional', 'fecha_hora', 'motivo_consulta')
    list_filter = ('profesional', 'fecha_hora')
    search_fields = ('historia_clinica__paciente__nombres', 'historia_clinica__paciente__apellidos', 'profesional__nombres', 'profesional__apellidos', 'motivo_consulta')
    date_hierarchy = 'fecha_hora'

@admin.register(Diagnostico)
class DiagnosticoAdmin(admin.ModelAdmin):
    list_display = ('consulta', 'descripcion', 'codigo_cie10', 'principal')
    list_filter = ('principal',)
    search_fields = ('descripcion', 'codigo_cie10')

@admin.register(Procedimiento)
class ProcedimientoAdmin(admin.ModelAdmin):
    list_display = ('consulta', 'descripcion', 'codigo_cups', 'fecha_hora_realizacion')
    list_filter = ('fecha_hora_realizacion',)
    search_fields = ('descripcion', 'codigo_cups')

@admin.register(SignosVitales)
class SignosVitalesAdmin(admin.ModelAdmin):
    list_display = ('consulta', 'tension_sistolica', 'tension_diastolica', 'temperatura', 'fecha_registro')
    list_filter = ('fecha_registro',)

@admin.register(NotaEvolucion)
class NotaEvolucionAdmin(admin.ModelAdmin):
    list_display = ('consulta', 'fecha_hora', 'profesional')
    list_filter = ('fecha_hora', 'profesional')
    search_fields = ('nota',)

@admin.register(DocumentoAdjunto)
class DocumentoAdjuntoAdmin(admin.ModelAdmin):
    list_display = ('consulta', 'nombre', 'tipo_documento', 'fecha_subida')
    list_filter = ('tipo_documento', 'fecha_subida')
    search_fields = ('nombre', 'tipo_documento')
