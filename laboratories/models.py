from django.db import models
from patients.models import Paciente
from professionals.models import ProfesionalSalud
from medical_records.models import Consulta # Para vincular órdenes a consultas

class TipoExamen(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    es_imagen = models.BooleanField(default=False, help_text="Indica si este tipo de examen es una imagen diagnóstica")

    def __str__(self):
        return self.nombre

class EquipoLaboratorio(models.Model):
    nombre = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100, blank=True, null=True)
    numero_serie = models.CharField(max_length=100, unique=True, blank=True, null=True)
    ubicacion = models.CharField(max_length=200, blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class OrdenExamen(models.Model):
    ESTADO_ORDEN_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('TOMADA', 'Muestra Tomada'),
        ('PROCESANDO', 'Procesando'),
        ('COMPLETADA', 'Completada'),
        ('CANCELADA', 'Cancelada'),
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='ordenes_examen')
    profesional_solicitante = models.ForeignKey(ProfesionalSalud, on_delete=models.SET_NULL, null=True, blank=True, related_name='ordenes_solicitadas')
    tipo_examen = models.ForeignKey(TipoExamen, on_delete=models.PROTECT, related_name='ordenes')
    consulta = models.ForeignKey(Consulta, on_delete=models.SET_NULL, null=True, blank=True, related_name='ordenes_examen') # Opcional
    fecha_orden = models.DateTimeField(auto_now_add=True)
    fecha_toma_muestra = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_ORDEN_CHOICES, default='PENDIENTE')
    notas = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Orden de {self.tipo_examen.nombre} para {self.paciente.nombres} ({self.fecha_orden.strftime('%d/%m/%Y')})"

class ResultadoExamen(models.Model):
    orden_examen = models.OneToOneField(OrdenExamen, on_delete=models.CASCADE, related_name='resultado')
    profesional_responsable = models.ForeignKey(ProfesionalSalud, on_delete=models.SET_NULL, null=True, blank=True, related_name='resultados_emitidos')
    fecha_resultado = models.DateTimeField(auto_now_add=True)
    resultado_texto = models.TextField(blank=True, null=True, help_text="Resultados textuales del examen")
    archivo_resultado = models.FileField(upload_to='resultados_laboratorio/', blank=True, null=True, help_text="Archivo del resultado (PDF, JPG, DICOM, etc.)")
    equipo_utilizado = models.ForeignKey(EquipoLaboratorio, on_delete=models.SET_NULL, null=True, blank=True, related_name='resultados')
    validado = models.BooleanField(default=False)

    def __str__(self):
        return f"Resultado de {self.orden_examen.tipo_examen.nombre} para {self.orden_examen.paciente.nombres} ({self.fecha_resultado.strftime('%d/%m/%Y')})"
