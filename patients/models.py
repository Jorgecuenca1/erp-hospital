from django.db import models

# Create your models here.

class Paciente(models.Model):
    REGIMEN_CHOICES = [
        ('SUBSIDIADO', 'Subsidiado'),
        ('CONTRIBUTIVO', 'Contributivo'),
    ]

    TIPO_IDENTIFICACION_CHOICES = [
        ('CC', 'Cédula de Ciudadanía'),
        ('TI', 'Tarjeta de Identidad'),
        ('CE', 'Cédula de Extranjería'),
        ('PA', 'Pasaporte'),
        ('RC', 'Registro Civil'),
    ]

    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    tipo_identificacion = models.CharField(max_length=2, choices=TIPO_IDENTIFICACION_CHOICES, default='CC')
    numero_identificacion = models.CharField(max_length=20, unique=True)
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino')])
    direccion = models.CharField(max_length=200, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    tipo_regimen = models.CharField(max_length=20, choices=REGIMEN_CHOICES, default='CONTRIBUTIVO')
    eps = models.CharField(max_length=100, blank=True, null=True) # Entidad Promotora de Salud

    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.numero_identificacion})"

class HistoriaClinica(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE, related_name='historia_clinica')
    fecha_apertura = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"Historia Clínica de {self.paciente.nombres} {self.paciente.apellidos}"
