from django.db import models

# Modelos para la aplicación de Informes
# En general, los informes no suelen tener modelos complejos propios,
# ya que agregan datos de otras aplicaciones (patients, appointments, medical_records, inventories, billing).
# Sin embargo, se podrían añadir modelos para:
# - Configuración de informes personalizados
# - Programación de informes
# - Almacenamiento de informes generados (e.g., PDF)

class ReporteGenerado(models.Model):
    nombre_reporte = models.CharField(max_length=255)
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    archivo_reporte = models.FileField(upload_to='generated_reports/', blank=True, null=True)
    parametros_filtro = models.TextField(blank=True, null=True, help_text="JSON de los parámetros usados para generar el reporte")

    def __str__(self):
        return f"Reporte {self.nombre_reporte} del {self.fecha_generacion.strftime('%Y-%m-%d %H:%M')}"
