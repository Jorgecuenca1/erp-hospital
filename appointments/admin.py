from django.contrib import admin
from .models import Cita

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'profesional', 'fecha_hora_inicio', 'fecha_hora_fin', 'estado')
    list_filter = ('estado', 'fecha_hora_inicio', 'profesional')
    search_fields = ('paciente__nombres', 'paciente__apellidos', 'profesional__nombres', 'profesional__apellidos', 'motivo')
    date_hierarchy = 'fecha_hora_inicio'
