from django.db import models
from patients.models import Paciente # Assuming subscriptions are tied to patients/clients
from django.utils import timezone

class PlanSuscripcion(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    periodo_facturacion = models.CharField(
        max_length=20,
        choices=[
            ('MENSUAL', 'Mensual'),
            ('TRIMESTRAL', 'Trimestral'),
            ('ANUAL', 'Anual'),
        ],
        default='MENSUAL'
    )
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Suscripcion(models.Model):
    ESTADO_SUSCRIPCION_CHOICES = [
        ('ACTIVA', 'Activa'),
        ('PENDIENTE_PAGO', 'Pendiente de Pago'),
        ('CANCELADA', 'Cancelada'),
        ('EXPIRADA', 'Expirada'),
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='suscripciones')
    plan = models.ForeignKey(PlanSuscripcion, on_delete=models.PROTECT, related_name='suscripciones')
    fecha_inicio = models.DateField(default=timezone.now)
    fecha_fin = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_SUSCRIPCION_CHOICES, default='ACTIVA')
    renovacion_automatica = models.BooleanField(default=True)
    notas = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Suscripción de {self.paciente.nombres} a {self.plan.nombre}"

class PagoSuscripcion(models.Model):
    suscripcion = models.ForeignKey(Suscripcion, on_delete=models.CASCADE, related_name='pagos')
    fecha_pago = models.DateField(default=timezone.now)
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(
        max_length=20,
        choices=[
            ('EFECTIVO', 'Efectivo'),
            ('TARJETA', 'Tarjeta de Crédito/Débito'),
            ('TRANSFERENCIA', 'Transferencia Bancaria'),
            ('CHEQUE', 'Cheque'),
        ],
        default='TARJETA'
    )
    referencia_transaccion = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Pago de {self.monto_pagado} por Suscripción {self.suscripcion.id} el {self.fecha_pago}"
