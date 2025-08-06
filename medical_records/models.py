from django.db import models
from patients.models import HistoriaClinica
from professionals.models import ProfesionalSalud

class Consulta(models.Model):
    historia_clinica = models.ForeignKey(HistoriaClinica, on_delete=models.CASCADE, related_name='consultas')
    profesional = models.ForeignKey(ProfesionalSalud, on_delete=models.CASCADE, related_name='consultas')
    fecha_hora = models.DateTimeField(auto_now_add=True)
    motivo_consulta = models.TextField()
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Consulta de {self.historia_clinica.paciente.nombres} ({self.fecha_hora.strftime('%d/%m/%Y %H:%M')})"

class Diagnostico(models.Model):
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name='diagnosticos')
    codigo_cie10 = models.CharField(max_length=10, blank=True, null=True)
    descripcion = models.TextField()
    principal = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.descripcion} ({self.codigo_cie10})"

class Procedimiento(models.Model):
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name='procedimientos')
    codigo_cups = models.CharField(max_length=10, blank=True, null=True)
    descripcion = models.TextField()
    fecha_hora_realizacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.descripcion} ({self.codigo_cups})"

class SignosVitales(models.Model):
    consulta = models.OneToOneField(Consulta, on_delete=models.CASCADE, related_name='signos_vitales')
    tension_sistolica = models.IntegerField(blank=True, null=True)
    tension_diastolica = models.IntegerField(blank=True, null=True)
    frecuencia_cardiaca = models.IntegerField(blank=True, null=True)
    frecuencia_respiratoria = models.IntegerField(blank=True, null=True)
    temperatura = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    peso = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    altura = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Signos Vitales de Consulta {self.consulta.id}"

class NotaEvolucion(models.Model):
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name='notas_evolucion')
    fecha_hora = models.DateTimeField(auto_now_add=True)
    nota = models.TextField()
    profesional = models.ForeignKey(ProfesionalSalud, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Nota de evolución ({self.fecha_hora.strftime('%d/%m/%Y %H:%M')})"

class DocumentoAdjunto(models.Model):
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name='documentos_adjuntos')
    nombre = models.CharField(max_length=255)
    archivo = models.FileField(upload_to='documentos_clinicos/')
    fecha_subida = models.DateTimeField(auto_now_add=True)
    tipo_documento = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre
