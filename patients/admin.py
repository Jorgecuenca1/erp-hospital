from django.contrib import admin
from .models import Paciente, HistoriaClinica

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('numero_identificacion', 'nombres', 'apellidos', 'tipo_regimen', 'eps')
    search_fields = ('numero_identificacion', 'nombres', 'apellidos')
    list_filter = ('tipo_regimen', 'sexo')

@admin.register(HistoriaClinica)
class HistoriaClinicaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'fecha_apertura', 'activo')
    list_filter = ('activo', 'fecha_apertura')
    search_fields = ('paciente__nombres', 'paciente__apellidos', 'paciente__numero_identificacion')
