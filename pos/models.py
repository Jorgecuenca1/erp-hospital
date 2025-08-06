from django.db import models
from django.conf import settings
from billing.models import Factura
from accounting.models import CuentaContable, Diario, Tercero

class PuntoVenta(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=255, blank=True, null=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre

class Caja(models.Model):
    nombre = models.CharField(max_length=100)
    punto_venta = models.ForeignKey(PuntoVenta, on_delete=models.CASCADE)
    cuenta_contable = models.ForeignKey(CuentaContable, on_delete=models.PROTECT)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.nombre} ({self.punto_venta})"

class SesionCaja(models.Model):
    caja = models.ForeignKey(Caja, on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    fecha_apertura = models.DateTimeField(auto_now_add=True)
    fecha_cierre = models.DateTimeField(blank=True, null=True)
    saldo_inicial = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    saldo_final = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    abierta = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Sesion {self.id} - {self.caja} - {self.usuario}"

class MetodoPagoPOS(models.Model):
    nombre = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)
    cuenta_contable = models.ForeignKey(CuentaContable, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.nombre

class VentaPOS(models.Model):
    sesion = models.ForeignKey(SesionCaja, on_delete=models.PROTECT)
    fecha = models.DateTimeField(auto_now_add=True)
    tercero = models.ForeignKey(Tercero, on_delete=models.PROTECT, blank=True, null=True)
    factura = models.OneToOneField(Factura, on_delete=models.SET_NULL, blank=True, null=True)
    total = models.DecimalField(max_digits=16, decimal_places=2)
    metodo_pago = models.ForeignKey(MetodoPagoPOS, on_delete=models.PROTECT)
    diario = models.ForeignKey(Diario, on_delete=models.PROTECT)
    referencia = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"Venta POS {self.id} - {self.fecha} - {self.total}"

class LineaVentaPOS(models.Model):
    venta = models.ForeignKey(VentaPOS, on_delete=models.CASCADE, related_name='lineas')
    descripcion = models.CharField(max_length=255)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=16, decimal_places=2)
    subtotal = models.DecimalField(max_digits=16, decimal_places=2)
    impuesto = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=16, decimal_places=2)
    
    def __str__(self):
        return f"{self.descripcion} x {self.cantidad}"
