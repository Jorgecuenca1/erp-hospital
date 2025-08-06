from django.db import models
from patients.models import Paciente # Para futuras órdenes de dispensación

class UbicacionAlmacen(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class CategoriaProducto(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categorías de Producto"

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    TIPO_PRODUCTO_CHOICES = [
        ('MEDICAMENTO', 'Medicamento'),
        ('INSUMO', 'Insumo'),
        ('EQUIPO', 'Equipo'),
    ]

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    tipo_producto = models.CharField(max_length=20, choices=TIPO_PRODUCTO_CHOICES)
    categoria = models.ForeignKey(CategoriaProducto, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos')
    unidad_medida = models.CharField(max_length=50, help_text="Ej: mg, ml, unidades, cajas")
    stock_actual = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_minimo = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Alerta cuando el stock es inferior a este valor")
    ubicacion = models.ForeignKey(UbicacionAlmacen, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos')
    fecha_caducidad = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.unidad_medida})"

class MovimientoInventario(models.Model):
    TIPO_MOVIMIENTO_CHOICES = [
        ('ENTRADA', 'Entrada'),
        ('SALIDA', 'Salida'),
        ('AJUSTE', 'Ajuste'),
    ]

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='movimientos')
    tipo_movimiento = models.CharField(max_length=10, choices=TIPO_MOVIMIENTO_CHOICES)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    razon = models.TextField(blank=True, null=True)
    referencia_documento = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.tipo_movimiento} de {self.cantidad} {self.producto.unidad_medida} de {self.producto.nombre}"

# Futuro modelo para Órdenes de Dispensación (vinculado a Historia Clínica/Paciente)
class OrdenDispensacion(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='ordenes_dispensacion')
    fecha_dispensacion = models.DateTimeField(auto_now_add=True)
    productos = models.ManyToManyField(Producto, through='DetalleOrdenDispensacion')
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Orden de Dispensación para {self.paciente.nombres} {self.paciente.apellidos} ({self.fecha_dispensacion.strftime('%d/%m/%Y %H:%M')})"

class DetalleOrdenDispensacion(models.Model):
    orden = models.ForeignKey(OrdenDispensacion, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} de {self.producto.nombre} en Orden {self.orden.id}"
