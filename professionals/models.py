from django.db import models

# Create your models here.

class Especialidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class ProfesionalSalud(models.Model):
    TIPO_PROFESIONAL_CHOICES = [
        ('MEDICO', 'Médico'),
        ('ENFERMERO', 'Enfermero/a'),
        ('TECNICO', 'Técnico/a'),
        ('ADMINISTRATIVO', 'Administrativo/a'), # Added based on HR module
    ]

    TIPO_IDENTIFICACION_CHOICES = [
        ('CC', 'Cédula de Ciudadanía'),
        ('TI', 'Tarjeta de Identidad'),
        ('CE', 'Cédula de Extranjería'),
        ('PA', 'Pasaporte'),
    ]

    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    tipo_identificacion = models.CharField(max_length=2, choices=TIPO_IDENTIFICACION_CHOICES, default='CC')
    numero_identificacion = models.CharField(max_length=20, unique=True)
    tipo_profesional = models.CharField(max_length=20, choices=TIPO_PROFESIONAL_CHOICES)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.SET_NULL, null=True, blank=True)
    registro_profesional = models.CharField(max_length=50, blank=True, null=True, help_text="Número de registro profesional (ej. Tarjeta Profesional)")
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.get_tipo_profesional_display()})"
