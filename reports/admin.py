from django.contrib import admin
from .models import ReporteGenerado

@admin.register(ReporteGenerado)
class ReporteGeneradoAdmin(admin.ModelAdmin):
    list_display = ('nombre_reporte', 'fecha_generacion', 'archivo_reporte')
    list_filter = ('fecha_generacion',)
    search_fields = ('nombre_reporte', 'parametros_filtro')
    date_hierarchy = 'fecha_generacion'
