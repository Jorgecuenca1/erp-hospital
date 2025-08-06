from django.db import models
from patients.models import Paciente
from professionals.models import ProfesionalSalud

class Cita(models.Model):
    ESTADO_CITA_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADA', 'Confirmada'),
        ('CANCELADA', 'Cancelada'),
        ('FINALIZADA', 'Finalizada'),
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='citas')
    profesional = models.ForeignKey(ProfesionalSalud, on_delete=models.CASCADE, related_name='citas')
    fecha_hora_inicio = models.DateTimeField()
    fecha_hora_fin = models.DateTimeField()
    motivo = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CITA_CHOICES, default='PENDIENTE')
    notas = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['fecha_hora_inicio']
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'

    def __str__(self):
        return f"Cita de {self.paciente.nombres} {self.paciente.apellidos} con {self.profesional.nombres} {self.profesional.apellidos} el {self.fecha_hora_inicio.strftime('%d/%m/%Y %H:%M')}"
