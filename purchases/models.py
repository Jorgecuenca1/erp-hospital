from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal

class Proveedor(models.Model):
    """Modelo para proveedores del hospital"""
    
    TIPO_PROVEEDOR_CHOICES = [
        ('MEDICAMENTOS', 'Medicamentos'),
        ('EQUIPOS', 'Equipos Médicos'),
        ('INSUMOS', 'Insumos'),
        ('SERVICIOS', 'Servicios'),
        ('ALIMENTOS', 'Alimentos'),
        ('OTROS', 'Otros'),
    ]
    
    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
        ('SUSPENDIDO', 'Suspendido'),
    ]
    
    nombre = models.CharField(max_length=200)
    tipo_proveedor = models.CharField(max_length=20, choices=TIPO_PROVEEDOR_CHOICES, default='OTROS')
    identificacion = models.CharField(max_length=50, unique=True, null=True, blank=True)
    direccion = models.TextField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    contacto_principal = models.CharField(max_length=100, blank=True)
    telefono_contacto = models.CharField(max_length=20, blank=True)
    email_contacto = models.EmailField(blank=True)
    terminos_pago = models.CharField(max_length=100, blank=True)
    limite_credito = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    saldo_actual = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='ACTIVO')
    calificacion = models.IntegerField(default=5, help_text="Calificación del 1 al 5")
    fecha_registro = models.DateTimeField(auto_now_add=True)
    notas = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} ({self.identificacion})"
    
    @property
    def credito_disponible(self):
        return self.limite_credito - self.saldo_actual

class ProductoCompra(models.Model):
    """Modelo para productos que se pueden comprar"""
    
    CATEGORIA_CHOICES = [
        ('MEDICAMENTOS', 'Medicamentos'),
        ('EQUIPOS', 'Equipos Médicos'),
        ('INSUMOS', 'Insumos'),
        ('ALIMENTOS', 'Alimentos'),
        ('LIMPEZA', 'Limpieza'),
        ('OFICINA', 'Oficina'),
        ('OTROS', 'Otros'),
    ]
    
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, default='OTROS')
    unidad_medida = models.CharField(max_length=20, default='UNIDAD')
    precio_estimado = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    stock_minimo = models.IntegerField(default=0)
    stock_actual = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)
    requiere_autorizacion = models.BooleanField(default=False)
    proveedores_preferidos = models.ManyToManyField(Proveedor, blank=True, related_name='productos_preferidos')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Producto de Compra'
        verbose_name_plural = 'Productos de Compra'
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    @property
    def necesita_compra(self):
        return self.stock_actual <= self.stock_minimo

class OrdenCompra(models.Model):
    """Modelo para órdenes de compra"""
    
    ESTADO_CHOICES = [
        ('BORRADOR', 'Borrador'),
        ('ENVIADA', 'Enviada'),
        ('CONFIRMADA', 'Confirmada'),
        ('EN_TRANSITO', 'En Tránsito'),
        ('RECIBIDA', 'Recibida'),
        ('CANCELADA', 'Cancelada'),
    ]
    
    PRIORIDAD_CHOICES = [
        ('BAJA', 'Baja'),
        ('MEDIA', 'Media'),
        ('ALTA', 'Alta'),
        ('URGENTE', 'Urgente'),
    ]
    
    numero_orden = models.CharField(max_length=20, unique=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='ordenes_compra')
    fecha_orden = models.DateTimeField(default=timezone.now)
    fecha_entrega_esperada = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='BORRADOR')
    prioridad = models.CharField(max_length=20, choices=PRIORIDAD_CHOICES, default='MEDIA')
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    impuestos = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    comprador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='ordenes_compradas')
    autorizado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='ordenes_autorizadas')
    fecha_autorizacion = models.DateTimeField(null=True, blank=True)
    notas = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Orden de Compra'
        verbose_name_plural = 'Órdenes de Compra'
        ordering = ['-fecha_orden']
    
    def __str__(self):
        return f"Orden {self.numero_orden} - {self.proveedor.nombre}"
    
    def calcular_totales(self):
        """Calcula los totales de la orden"""
        self.subtotal = sum(item.subtotal for item in self.items.all())
        self.impuestos = sum(item.impuesto for item in self.items.all())
        self.total = self.subtotal + self.impuestos - self.descuento
        self.save()

class DetalleOrdenCompra(models.Model):
    """Detalles de las órdenes de compra"""
    
    orden = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(ProductoCompra, on_delete=models.CASCADE)
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Porcentaje
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    impuesto = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    cantidad_recibida = models.IntegerField(default=0)
    notas = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Detalle de Orden de Compra'
        verbose_name_plural = 'Detalles de Órdenes de Compra'
    
    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad} x ${self.precio_unitario}"
    
    def save(self, *args, **kwargs):
        # Calcular subtotal
        self.subtotal = self.cantidad * self.precio_unitario * (1 - self.descuento / 100)
        # Calcular impuesto (asumiendo 19% IVA)
        self.impuesto = self.subtotal * Decimal('0.19')
        # Calcular total
        self.total = self.subtotal + self.impuesto
        super().save(*args, **kwargs)
    
    @property
    def pendiente_por_recibir(self):
        return self.cantidad - self.cantidad_recibida

class FacturaCompra(models.Model):
    """Modelo para facturas de compra"""
    
    ESTADO_CHOICES = [
        ('BORRADOR', 'Borrador'),
        ('RECIBIDA', 'Recibida'),
        ('PAGADA', 'Pagada'),
        ('ANULADA', 'Anulada'),
    ]
    
    numero_factura = models.CharField(max_length=20)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='facturas_compra')
    orden_compra = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE, related_name='facturas', null=True, blank=True)
    fecha_emision = models.DateTimeField(default=timezone.now)
    fecha_recepcion = models.DateTimeField(null=True, blank=True)
    fecha_vencimiento = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='BORRADOR')
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    impuestos = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    descuento = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    saldo_pendiente = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    recibido_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='facturas_recibidas')
    notas = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Factura de Compra'
        verbose_name_plural = 'Facturas de Compra'
        ordering = ['-fecha_emision']
        unique_together = ['numero_factura', 'proveedor']
    
    def __str__(self):
        return f"Factura {self.numero_factura} - {self.proveedor.nombre}"
    
    def calcular_totales(self):
        """Calcula los totales de la factura"""
        self.subtotal = sum(item.subtotal for item in self.items.all())
        self.impuestos = sum(item.impuesto for item in self.items.all())
        self.total = self.subtotal + self.impuestos - self.descuento
        self.saldo_pendiente = self.total
        self.save()

class DetalleFacturaCompra(models.Model):
    """Detalles de las facturas de compra"""
    
    factura = models.ForeignKey(FacturaCompra, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(ProductoCompra, on_delete=models.CASCADE)
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    impuesto = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    
    class Meta:
        verbose_name = 'Detalle de Factura de Compra'
        verbose_name_plural = 'Detalles de Facturas de Compra'
    
    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad} x ${self.precio_unitario}"
    
    def save(self, *args, **kwargs):
        # Calcular subtotal
        self.subtotal = self.cantidad * self.precio_unitario * (1 - self.descuento / 100)
        # Calcular impuesto (asumiendo 19% IVA)
        self.impuesto = self.subtotal * Decimal('0.19')
        # Calcular total
        self.total = self.subtotal + self.impuesto
        super().save(*args, **kwargs)

class PagoCompra(models.Model):
    """Modelo para pagos de compras"""
    
    METODO_PAGO_CHOICES = [
        ('EFECTIVO', 'Efectivo'),
        ('TARJETA', 'Tarjeta'),
        ('TRANSFERENCIA', 'Transferencia'),
        ('CHEQUE', 'Cheque'),
        ('CREDITO', 'Crédito'),
    ]
    
    factura = models.ForeignKey(FacturaCompra, on_delete=models.CASCADE, related_name='pagos')
    fecha_pago = models.DateTimeField(default=timezone.now)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    metodo_pago = models.CharField(max_length=20, choices=METODO_PAGO_CHOICES)
    referencia = models.CharField(max_length=100, blank=True)
    notas = models.TextField(blank=True)
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name = 'Pago de Compra'
        verbose_name_plural = 'Pagos de Compra'
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

class RecepcionCompra(models.Model):
    """Modelo para recepciones de compra"""
    
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROCESO', 'En Proceso'),
        ('COMPLETADA', 'Completada'),
        ('RECHAZADA', 'Rechazada'),
    ]
    
    orden_compra = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE, related_name='recepciones')
    fecha_recepcion = models.DateTimeField(default=timezone.now)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')
    recibido_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='recepciones_realizadas')
    notas = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Recepción de Compra'
        verbose_name_plural = 'Recepciones de Compra'
        ordering = ['-fecha_recepcion']
    
    def __str__(self):
        return f"Recepción {self.id} - Orden {self.orden_compra.numero_orden}"

class DetalleRecepcionCompra(models.Model):
    """Detalles de las recepciones de compra"""
    
    recepcion = models.ForeignKey(RecepcionCompra, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(ProductoCompra, on_delete=models.CASCADE)
    cantidad_esperada = models.IntegerField()
    cantidad_recibida = models.IntegerField()
    cantidad_rechazada = models.IntegerField(default=0)
    motivo_rechazo = models.TextField(blank=True)
    lote = models.CharField(max_length=50, blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Detalle de Recepción'
        verbose_name_plural = 'Detalles de Recepciones'
    
    def __str__(self):
        return f"{self.producto.nombre} - Recibido: {self.cantidad_recibida}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Actualizar stock del producto
        if self.cantidad_recibida > 0:
            self.producto.stock_actual += self.cantidad_recibida
            self.producto.save()

class CotizacionCompra(models.Model):
    """Modelo para cotizaciones de compra"""
    
    ESTADO_CHOICES = [
        ('BORRADOR', 'Borrador'),
        ('ENVIADA', 'Enviada'),
        ('RECIBIDA', 'Recibida'),
        ('APROBADA', 'Aprobada'),
        ('RECHAZADA', 'Rechazada'),
    ]
    
    numero_cotizacion = models.CharField(max_length=20, unique=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='cotizaciones')
    fecha_solicitud = models.DateTimeField(default=timezone.now)
    fecha_respuesta = models.DateTimeField(null=True, blank=True)
    fecha_validez = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='BORRADOR')
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    impuestos = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    solicitado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='cotizaciones_solicitadas')
    notas = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Cotización de Compra'
        verbose_name_plural = 'Cotizaciones de Compra'
        ordering = ['-fecha_solicitud']
    
    def __str__(self):
        return f"Cotización {self.numero_cotizacion} - {self.proveedor.nombre}"
    
    def calcular_totales(self):
        """Calcula los totales de la cotización"""
        self.subtotal = sum(item.subtotal for item in self.items.all())
        self.impuestos = sum(item.impuesto for item in self.items.all())
        self.total = self.subtotal + self.impuestos
        self.save()

class DetalleCotizacionCompra(models.Model):
    """Detalles de las cotizaciones de compra"""
    
    cotizacion = models.ForeignKey(CotizacionCompra, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(ProductoCompra, on_delete=models.CASCADE)
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    impuesto = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    observaciones = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Detalle de Cotización'
        verbose_name_plural = 'Detalles de Cotizaciones'
    
    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad} x ${self.precio_unitario}"
    
    def save(self, *args, **kwargs):
        # Calcular subtotal
        self.subtotal = self.cantidad * self.precio_unitario
        # Calcular impuesto (asumiendo 19% IVA)
        self.impuesto = self.subtotal * Decimal('0.19')
        # Calcular total
        self.total = self.subtotal + self.impuesto
        super().save(*args, **kwargs)
