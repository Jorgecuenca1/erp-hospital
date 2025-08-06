from django.db import models
from professionals.models import ProfesionalSalud # Para vincular profesionales a empleados

class Cargo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    salario_base = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.nombre

class Empleado(models.Model):
    TIPO_IDENTIFICACION_CHOICES = [
        ('CC', 'Cédula de Ciudadanía'),
        ('CE', 'Cédula de Extranjería'),
        ('PA', 'Pasaporte'),
    ]
    TIPO_CONTRATO_CHOICES = [
        ('FIJO', 'Término Fijo'),
        ('INDEFINIDO', 'Término Indefinido'),
        ('OBRALABOR', 'Obra o Labor'),
        ('SERVICIOS', 'Prestación de Servicios'),
    ]

    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    tipo_identificacion = models.CharField(max_length=5, choices=TIPO_IDENTIFICACION_CHOICES, default='CC')
    numero_identificacion = models.CharField(max_length=20, unique=True)
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=200, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT, related_name='empleados')
    fecha_contratacion = models.DateField(auto_now_add=True)
    profesional_salud = models.OneToOneField(ProfesionalSalud, on_delete=models.SET_NULL, null=True, blank=True, related_name='empleado_asociado', help_text="Si es un profesional de la salud, vincular con su registro de ProfesionalSalud")
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.cargo.nombre})"

class Contrato(models.Model):
    empleado = models.OneToOneField(Empleado, on_delete=models.CASCADE, related_name='contrato')
    tipo_contrato = models.CharField(max_length=20, choices=Empleado.TIPO_CONTRATO_CHOICES)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    documento_contrato = models.FileField(upload_to='contratos/', blank=True, null=True)

    def __str__(self):
        return f"Contrato de {self.empleado.nombres} {self.empleado.apellidos} ({self.tipo_contrato})"

class Nomina(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.PROTECT, related_name='nominas')
    fecha_pago = models.DateField(auto_now_add=True)
    periodo_inicio = models.DateField()
    periodo_fin = models.DateField()
    salario_base = models.DecimalField(max_digits=10, decimal_places=2)
    bonificaciones = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deducciones = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    salario_neto = models.DecimalField(max_digits=10, decimal_places=2)
    comprobante_pago = models.FileField(upload_to='comprobantes_nomina/', blank=True, null=True)

    def __str__(self):
        return f"Nómina de {self.empleado.nombres} {self.empleado.apellidos} - {self.periodo_inicio} a {self.periodo_fin}"
