from django.contrib import admin
from .models import Especialidad, ProfesionalSalud

@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

@admin.register(ProfesionalSalud)
class ProfesionalSaludAdmin(admin.ModelAdmin):
    list_display = ('numero_identificacion', 'nombres', 'apellidos', 'tipo_profesional', 'especialidad', 'activo')
    search_fields = ('numero_identificacion', 'nombres', 'apellidos', 'registro_profesional')
    list_filter = ('tipo_profesional', 'especialidad', 'activo')
