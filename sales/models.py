from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal

class Cliente(models.Model):
    """Modelo para clientes del hospital (pacientes externos, seguros, etc.)"""
    
    TIPO_CLIENTE_CHOICES = [
        ('PACIENTE', 'Paciente'),
        ('SEGURO', 'Seguro'),
        ('EMPRESA', 'Empresa'),
        ('GUBERNAMENTAL', 'Gubernamental'),
        ('OTRO', 'Otro'),
    ]
    
    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
        ('SUSPENDIDO', 'Suspendido'),
    ]
    
    nombre = models.CharField(max_length=200)
    tipo_cliente = models.CharField(max_length=20, choices=TIPO_CLIENTE_CHOICES, default='PACIENTE')
    identificacion = models.CharField(max_length=50, unique=True)
    direccion = models.TextField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    contacto_principal = models.CharField(max_length=100, blank=True)
    limite_credito = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    saldo_actual = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='ACTIVO')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    notas = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} ({self.identificacion})"
    
    @property
    def credito_disponible(self):
        return self.limite_credito - self.saldo_actual

class ProductoServicio(models.Model):
    """Modelo para productos y servicios vendibles"""
    
    TIPO_CHOICES = [
        ('PRODUCTO', 'Producto'),
        ('SERVICIO', 'Servicio'),
        ('PROCEDIMIENTO', 'Procedimiento'),
    ]
    
    CATEGORIA_CHOICES = [
        ('MEDICAMENTOS', 'Medicamentos'),
        ('EQUIPOS', 'Equipos Médicos'),
        ('CONSULTAS', 'Consultas'),
        ('PROCEDIMIENTOS', 'Procedimientos'),
        ('LABORATORIO', 'Laboratorio'),
        ('IMAGENES', 'Imágenes'),
        ('OTROS', 'Otros'),
    ]
    
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='SERVICIO')
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, default='OTROS')
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    precio_especial = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    impuesto = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Porcentaje
    activo = models.BooleanField(default=True)
    requiere_autorizacion = models.BooleanField(default=False)
    stock_disponible = models.IntegerField(default=0)  # Solo para productos
    stock_minimo = models.IntegerField(default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Producto/Servicio'
        verbose_name_plural = 'Productos/Servicios'
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    @property
    def precio_final(self):
        return self.precio_especial if self.precio_especial else self.precio_unitario
    
    @property
    def precio_con_impuesto(self):
        return self.precio_final * (1 + self.impuesto / 100)

class OrdenVenta(models.Model):
    """Modelo para órdenes de venta"""
    
    ESTADO_CHOICES = [
        ('BORRADOR', 'Borrador'),
        ('CONFIRMADA', 'Confirmada'),
        ('EN_PROCESO', 'En Proceso'),
        ('COMPLETADA', 'Completada'),
        ('CANCELADA', 'Cancelada'),
    ]
    
    numero_orden = models.CharField(max_length=20, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='ordenes_venta')
    fecha_orden = models.DateTimeField(default=timezone.now)
    fecha_entrega_esperada = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='BORRADOR')
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    impuestos = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    vendedor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='ordenes_vendidas')
    notas = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Orden de Venta'
        verbose_name_plural = 'Órdenes de Venta'
        ordering = ['-fecha_orden']
    
    def __str__(self):
        return f"Orden {self.numero_orden} - {self.cliente.nombre}"
    
    def calcular_totales(self):
        """Calcula los totales de la orden"""
        self.subtotal = sum(item.subtotal for item in self.items.all())
        self.impuestos = sum(item.impuesto for item in self.items.all())
        self.total = self.subtotal + self.impuestos - self.descuento
        self.save()

class DetalleOrdenVenta(models.Model):
    """Detalles de las órdenes de venta"""
    
    orden = models.ForeignKey(OrdenVenta, on_delete=models.CASCADE, related_name='items')
    producto_servicio = models.ForeignKey(ProductoServicio, on_delete=models.CASCADE)
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Porcentaje
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    impuesto = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    notas = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Detalle de Orden de Venta'
        verbose_name_plural = 'Detalles de Órdenes de Venta'
    
    def __str__(self):
        return f"{self.producto_servicio.nombre} - {self.cantidad} x ${self.precio_unitario}"
    
    def save(self, *args, **kwargs):
        # Calcular subtotal
        self.subtotal = self.cantidad * self.precio_unitario * (1 - self.descuento / 100)
        # Calcular impuesto
        self.impuesto = self.subtotal * (self.producto_servicio.impuesto / 100)
        # Calcular total
        self.total = self.subtotal + self.impuesto
        super().save(*args, **kwargs)

class FacturaVenta(models.Model):
    """Modelo para facturas de venta"""
    
    ESTADO_CHOICES = [
        ('BORRADOR', 'Borrador'),
        ('EMITIDA', 'Emitida'),
        ('PAGADA', 'Pagada'),
        ('ANULADA', 'Anulada'),
    ]
    
    numero_factura = models.CharField(max_length=20, unique=True)
    orden_venta = models.ForeignKey(OrdenVenta, on_delete=models.CASCADE, related_name='facturas')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='facturas')
    fecha_emision = models.DateTimeField(default=timezone.now)
    fecha_vencimiento = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='BORRADOR')
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    impuestos = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    saldo_pendiente = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    vendedor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='facturas_vendidas')
    notas = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Factura de Venta'
        verbose_name_plural = 'Facturas de Venta'
        ordering = ['-fecha_emision']
    
    def __str__(self):
        return f"Factura {self.numero_factura} - {self.cliente.nombre}"
    
    def calcular_totales(self):
        """Calcula los totales de la factura"""
        self.subtotal = sum(item.subtotal for item in self.items.all())
        self.impuestos = sum(item.impuesto for item in self.items.all())
        self.total = self.subtotal + self.impuestos - self.descuento
        self.saldo_pendiente = self.total
        self.save()

class DetalleFacturaVenta(models.Model):
    """Detalles de las facturas de venta"""
    
    factura = models.ForeignKey(FacturaVenta, on_delete=models.CASCADE, related_name='items')
    producto_servicio = models.ForeignKey(ProductoServicio, on_delete=models.CASCADE)
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    impuesto = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    
    class Meta:
        verbose_name = 'Detalle de Factura de Venta'
        verbose_name_plural = 'Detalles de Facturas de Venta'
    
    def __str__(self):
        return f"{self.producto_servicio.nombre} - {self.cantidad} x ${self.precio_unitario}"
    
    def save(self, *args, **kwargs):
        # Calcular subtotal
        self.subtotal = self.cantidad * self.precio_unitario * (1 - self.descuento / 100)
        # Calcular impuesto
        self.impuesto = self.subtotal * (self.producto_servicio.impuesto / 100)
        # Calcular total
        self.total = self.subtotal + self.impuesto
        super().save(*args, **kwargs)

class PagoVenta(models.Model):
    """Modelo para pagos de ventas"""
    
    METODO_PAGO_CHOICES = [
        ('EFECTIVO', 'Efectivo'),
        ('TARJETA', 'Tarjeta'),
        ('TRANSFERENCIA', 'Transferencia'),
        ('CHEQUE', 'Cheque'),
        ('CREDITO', 'Crédito'),
    ]
    
    factura = models.ForeignKey(FacturaVenta, on_delete=models.CASCADE, related_name='pagos')
    fecha_pago = models.DateTimeField(default=timezone.now)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    metodo_pago = models.CharField(max_length=20, choices=METODO_PAGO_CHOICES)
    referencia = models.CharField(max_length=100, blank=True)
    notas = models.TextField(blank=True)
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name = 'Pago de Venta'
        verbose_name_plural = 'Pagos de Venta'
        ordering = ['-fecha_pago']
    
    def __str__(self):
        return f"Pago ${self.monto} - {self.factura.numero_factura}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Actualizar saldo pendiente de la factura
        self.factura.saldo_pendiente -= self.monto
        if self.factura.saldo_pendiente <= 0:
            self.factura.estado = 'PAGADA'
        self.factura.save()

class DevolucionVenta(models.Model):
    """Modelo para devoluciones de venta"""
    
    ESTADO_CHOICES = [
        ('SOLICITADA', 'Solicitada'),
        ('APROBADA', 'Aprobada'),
        ('PROCESADA', 'Procesada'),
        ('RECHAZADA', 'Rechazada'),
    ]
    
    factura = models.ForeignKey(FacturaVenta, on_delete=models.CASCADE, related_name='devoluciones')
    fecha_solicitud = models.DateTimeField(default=timezone.now)
    fecha_procesamiento = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='SOLICITADA')
    motivo = models.TextField()
    monto_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    procesado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notas = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Devolución de Venta'
        verbose_name_plural = 'Devoluciones de Venta'
        ordering = ['-fecha_solicitud']
    
    def __str__(self):
        return f"Devolución {self.id} - {self.factura.numero_factura}"

class DetalleDevolucionVenta(models.Model):
    """Detalles de las devoluciones de venta"""
    
    devolucion = models.ForeignKey(DevolucionVenta, on_delete=models.CASCADE, related_name='items')
    producto_servicio = models.ForeignKey(ProductoServicio, on_delete=models.CASCADE)
    cantidad_devuelta = models.IntegerField(validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    motivo = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Detalle de Devolución'
        verbose_name_plural = 'Detalles de Devoluciones'
    
    def __str__(self):
        return f"{self.producto_servicio.nombre} - {self.cantidad_devuelta} unidades"
    
    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad_devuelta * self.precio_unitario
        super().save(*args, **kwargs)
