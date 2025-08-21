from django.db import models
from django.conf import settings
from django.utils import timezone
from decimal import Decimal
from patients.models import Paciente # Para futuras órdenes de dispensación
from accounting.models import Tercero, CuentaContable, AsientoContable

User = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

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
        ('INSUMO', 'Insumo Médico'),
        ('EQUIPO', 'Equipo Médico'),
        ('DISPOSITIVO', 'Dispositivo Médico'),
        ('MATERIAL', 'Material de Oficina'),
        ('CONSUMIBLE', 'Consumible'),
    ]
    
    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('DESCONTINUADO', 'Descontinuado'),
        ('AGOTADO', 'Agotado'),
        ('BLOQUEADO', 'Bloqueado'),
    ]

    # Información básica
    codigo = models.CharField(max_length=50, unique=True, help_text="Código interno del producto")
    codigo_barras = models.CharField(max_length=100, blank=True, null=True, help_text="Código de barras")
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    tipo_producto = models.CharField(max_length=20, choices=TIPO_PRODUCTO_CHOICES)
    categoria = models.ForeignKey(CategoriaProducto, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos')
    
    # Unidades y medidas
    unidad_medida = models.CharField(max_length=50, help_text="Ej: mg, ml, unidades, cajas")
    peso = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, help_text="Peso en gramos")
    volumen = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True, help_text="Volumen en ml")
    
    # Stock y ubicación
    stock_actual = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_minimo = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Alerta cuando el stock es inferior a este valor")
    stock_maximo = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Stock máximo recomendado")
    ubicacion = models.ForeignKey(UbicacionAlmacen, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos')
    
    # Precios y costos
    precio_compra = models.DecimalField(max_digits=15, decimal_places=2, default=0, help_text="Precio de compra unitario")
    precio_venta = models.DecimalField(max_digits=15, decimal_places=2, default=0, help_text="Precio de venta unitario")
    margen_ganancia = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Margen de ganancia en %")
    
    # Fechas importantes
    fecha_caducidad = models.DateField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    # Proveedor principal
    proveedor_principal = models.ForeignKey(Tercero, on_delete=models.SET_NULL, null=True, blank=True, 
                                          related_name='productos_suministrados',
                                          help_text="Proveedor principal del producto")
    
    # Integración contable
    cuenta_inventario = models.ForeignKey(CuentaContable, on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name='productos_inventario',
                                        help_text="Cuenta contable para el inventario del producto")
    cuenta_costo_venta = models.ForeignKey(CuentaContable, on_delete=models.SET_NULL, null=True, blank=True,
                                         related_name='productos_costo_venta',
                                         help_text="Cuenta contable para el costo de venta")
    
    # Estado y control
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='ACTIVO')
    activo = models.BooleanField(default=True)
    requiere_prescripcion = models.BooleanField(default=False, help_text="Requiere prescripción médica")
    controlado = models.BooleanField(default=False, help_text="Producto controlado")
    
    # Usuario que creó/modificó
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos_creados')
    modificado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos_modificados')

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['codigo', 'nombre']
        indexes = [
            models.Index(fields=['codigo']),
            models.Index(fields=['codigo_barras']),
            models.Index(fields=['tipo_producto']),
            models.Index(fields=['estado']),
        ]

    def __str__(self):
        return f"{self.codigo} - {self.nombre} ({self.unidad_medida})"
    
    @property
    def valor_inventario(self):
        """Calcula el valor total del inventario actual"""
        return self.stock_actual * self.precio_compra
    
    @property
    def necesita_restock(self):
        """Indica si el producto necesita reposición"""
        return self.stock_actual <= self.stock_minimo
    
    @property
    def esta_caducado(self):
        """Indica si el producto está caducado"""
        if self.fecha_caducidad:
            return self.fecha_caducidad < timezone.now().date()
        return False
    
    @property
    def dias_para_caducar(self):
        """Calcula los días restantes para la caducidad"""
        if self.fecha_caducidad:
            return (self.fecha_caducidad - timezone.now().date()).days
        return None
    
    def calcular_precio_venta(self):
        """Calcula el precio de venta basado en el margen de ganancia"""
        if self.precio_compra > 0 and self.margen_ganancia > 0:
            return self.precio_compra * (1 + (self.margen_ganancia / 100))
        return self.precio_venta
    
    def save(self, *args, **kwargs):
        # Generar código automáticamente si no existe
        if not self.codigo:
            ultimo_numero = Producto.objects.filter(
                tipo_producto=self.tipo_producto
            ).count() + 1
            prefijo = self.tipo_producto[:3].upper()
            self.codigo = f"{prefijo}{ultimo_numero:06d}"
        
        # Calcular precio de venta automáticamente si no está definido
        if not self.precio_venta and self.precio_compra > 0 and self.margen_ganancia > 0:
            self.precio_venta = self.calcular_precio_venta()
            
        super().save(*args, **kwargs)

class MovimientoInventario(models.Model):
    TIPO_MOVIMIENTO_CHOICES = [
        ('ENTRADA', 'Entrada'),
        ('SALIDA', 'Salida'),
        ('AJUSTE_POSITIVO', 'Ajuste Positivo'),
        ('AJUSTE_NEGATIVO', 'Ajuste Negativo'),
        ('TRANSFERENCIA', 'Transferencia'),
        ('DEVOLUCION', 'Devolución'),
        ('MERMA', 'Merma'),
        ('VENCIMIENTO', 'Vencimiento'),
    ]
    
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADO', 'Confirmado'),
        ('CANCELADO', 'Cancelado'),
    ]

    # Información básica del movimiento
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='movimientos')
    tipo_movimiento = models.CharField(max_length=20, choices=TIPO_MOVIMIENTO_CHOICES)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=15, decimal_places=2, default=0, help_text="Precio unitario del movimiento")
    valor_total = models.DecimalField(max_digits=15, decimal_places=2, default=0, help_text="Valor total del movimiento")
    
    # Fechas y control
    fecha_hora = models.DateTimeField(auto_now_add=True)
    fecha_documento = models.DateField(blank=True, null=True, help_text="Fecha del documento origen")
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='PENDIENTE')
    
    # Documentos y referencias
    numero_documento = models.CharField(max_length=100, blank=True, null=True, help_text="Número del documento origen")
    referencia_documento = models.CharField(max_length=100, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    
    # Terceros relacionados
    proveedor = models.ForeignKey(Tercero, on_delete=models.SET_NULL, null=True, blank=True, 
                                related_name='movimientos_inventario', help_text="Proveedor en caso de entrada")
    
    # Ubicaciones (para transferencias)
    ubicacion_origen = models.ForeignKey(UbicacionAlmacen, on_delete=models.SET_NULL, null=True, blank=True,
                                       related_name='movimientos_origen')
    ubicacion_destino = models.ForeignKey(UbicacionAlmacen, on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name='movimientos_destino')
    
    # Stock antes y después del movimiento
    stock_anterior = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Stock antes del movimiento")
    stock_nuevo = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Stock después del movimiento")
    
    # Integración contable
    asiento_contable = models.ForeignKey(AsientoContable, on_delete=models.SET_NULL, null=True, blank=True,
                                       help_text="Asiento contable generado por este movimiento")
    requiere_contabilizacion = models.BooleanField(default=True, help_text="Si requiere generar asiento contable")
    contabilizado = models.BooleanField(default=False, help_text="Si ya se generó el asiento contable")
    
    # Usuario que realizó el movimiento
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    autorizado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                     related_name='movimientos_autorizados')

    class Meta:
        verbose_name = "Movimiento de Inventario"
        verbose_name_plural = "Movimientos de Inventario"
        ordering = ['-fecha_hora']
        indexes = [
            models.Index(fields=['producto', 'tipo_movimiento']),
            models.Index(fields=['fecha_hora']),
            models.Index(fields=['numero_documento']),
            models.Index(fields=['estado']),
        ]

    def __str__(self):
        return f"{self.get_tipo_movimiento_display()} - {self.cantidad} {self.producto.unidad_medida} de {self.producto.nombre}"
    
    def save(self, *args, **kwargs):
        # Calcular valor total si no está definido
        if not self.valor_total and self.precio_unitario > 0:
            self.valor_total = self.cantidad * self.precio_unitario
        
        # Registrar stock anterior si es nuevo movimiento
        if not self.pk:
            self.stock_anterior = self.producto.stock_actual
            
            # Calcular nuevo stock
            if self.tipo_movimiento in ['ENTRADA', 'AJUSTE_POSITIVO']:
                self.stock_nuevo = self.stock_anterior + self.cantidad
            elif self.tipo_movimiento in ['SALIDA', 'AJUSTE_NEGATIVO', 'MERMA', 'VENCIMIENTO']:
                self.stock_nuevo = self.stock_anterior - self.cantidad
            else:
                self.stock_nuevo = self.stock_anterior
        
        super().save(*args, **kwargs)
        
        # Actualizar stock del producto si está confirmado
        if self.estado == 'CONFIRMADO':
            self.actualizar_stock_producto()
    
    def actualizar_stock_producto(self):
        """Actualiza el stock del producto según el movimiento"""
        if self.tipo_movimiento in ['ENTRADA', 'AJUSTE_POSITIVO']:
            self.producto.stock_actual += self.cantidad
        elif self.tipo_movimiento in ['SALIDA', 'AJUSTE_NEGATIVO', 'MERMA', 'VENCIMIENTO']:
            self.producto.stock_actual -= self.cantidad
        
        self.producto.save()
    
    def generar_asiento_contable(self):
        """Genera el asiento contable para este movimiento"""
        if not self.requiere_contabilizacion or self.contabilizado:
            return None
        
        from accounting.models import Diario, PeriodoContable
        
        # Obtener diario de inventarios
        diario_inventario = Diario.objects.filter(tipo='GENERAL').first()
        if not diario_inventario:
            return None
        
        # Obtener período contable actual
        periodo = PeriodoContable.objects.filter(
            fecha_inicio__lte=self.fecha_hora.date(),
            fecha_fin__gte=self.fecha_hora.date(),
            cerrado=False
        ).first()
        
        if not periodo:
            return None
        
        # Crear asiento contable
        asiento = AsientoContable.objects.create(
            fecha=self.fecha_hora.date(),
            descripcion=f"Movimiento de inventario: {self.get_tipo_movimiento_display()} - {self.producto.nombre}",
            diario=diario_inventario,
            periodo=periodo,
            tercero=self.proveedor,
            referencia=self.numero_documento
        )
        
        # Crear líneas de asiento según el tipo de movimiento
        if self.tipo_movimiento == 'ENTRADA' and self.producto.cuenta_inventario:
            # Débito: Inventario, Crédito: Cuentas por pagar o Caja
            from accounting.models import LineaAsiento
            
            LineaAsiento.objects.create(
                asiento=asiento,
                cuenta=self.producto.cuenta_inventario,
                descripcion=f"Entrada de {self.producto.nombre}",
                debito=self.valor_total,
                credito=0
            )
            
            # Buscar cuenta de cuentas por pagar (habría que definirla)
            # LineaAsiento.objects.create(...)
        
        self.asiento_contable = asiento
        self.contabilizado = True
        self.save()
        
        return asiento

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

# ========== NUEVOS MODELOS PARA COMPRAS E INVENTARIOS ==========

class OrdenCompra(models.Model):
    ESTADO_CHOICES = [
        ('BORRADOR', 'Borrador'),
        ('ENVIADA', 'Enviada'),
        ('CONFIRMADA', 'Confirmada'),
        ('RECIBIDA', 'Recibida'),
        ('FACTURADA', 'Facturada'),
        ('CANCELADA', 'Cancelada'),
    ]
    
    # Información básica
    numero = models.CharField(max_length=50, unique=True, help_text="Número de orden de compra")
    fecha_orden = models.DateField(default=timezone.now)
    fecha_entrega_esperada = models.DateField(blank=True, null=True)
    
    # Proveedor
    proveedor = models.ForeignKey(Tercero, on_delete=models.PROTECT, related_name='ordenes_compra')
    
    # Totales
    subtotal = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    impuestos = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Estado y control
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='BORRADOR')
    observaciones = models.TextField(blank=True, null=True)
    
    # Integración contable
    asiento_contable = models.ForeignKey(AsientoContable, on_delete=models.SET_NULL, null=True, blank=True)
    contabilizada = models.BooleanField(default=False)
    
    # Usuarios
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    autorizado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                     related_name='ordenes_compra_inventario_autorizadas')
    
    # Fechas de control
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_autorizacion = models.DateTimeField(blank=True, null=True)
    fecha_recepcion = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Orden de Compra"
        verbose_name_plural = "Órdenes de Compra"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"OC-{self.numero} - {self.proveedor.nombre}"
    
    def save(self, *args, **kwargs):
        if not self.numero:
            # Generar número de orden automáticamente
            ultimo_numero = OrdenCompra.objects.count() + 1
            self.numero = f"{ultimo_numero:06d}"
        super().save(*args, **kwargs)
    
    def calcular_totales(self):
        """Calcula los totales de la orden de compra"""
        detalles = self.detalles.all()
        self.subtotal = sum(detalle.subtotal for detalle in detalles)
        self.impuestos = sum(detalle.impuesto_valor for detalle in detalles)
        self.total = self.subtotal + self.impuestos
        self.save()

class DetalleOrdenCompra(models.Model):
    orden = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_pedida = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_recibida = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    precio_unitario = models.DecimalField(max_digits=15, decimal_places=2)
    subtotal = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    porcentaje_impuesto = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    impuesto_valor = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_linea = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Detalle Orden de Compra"
        verbose_name_plural = "Detalles Orden de Compra"

    def __str__(self):
        return f"{self.cantidad_pedida} {self.producto.unidad_medida} de {self.producto.nombre}"
    
    def save(self, *args, **kwargs):
        # Calcular totales automáticamente
        self.subtotal = self.cantidad_pedida * self.precio_unitario
        self.impuesto_valor = self.subtotal * (self.porcentaje_impuesto / 100)
        self.total_linea = self.subtotal + self.impuesto_valor
        super().save(*args, **kwargs)

class RecepcionMercancia(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('PARCIAL', 'Parcial'),
        ('COMPLETA', 'Completa'),
        ('CERRADA', 'Cerrada'),
    ]
    
    # Información básica
    numero = models.CharField(max_length=50, unique=True)
    fecha_recepcion = models.DateTimeField(default=timezone.now)
    orden_compra = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE, related_name='recepciones')
    
    # Documentos del proveedor
    numero_factura_proveedor = models.CharField(max_length=100, blank=True, null=True)
    numero_remision = models.CharField(max_length=100, blank=True, null=True)
    
    # Estado
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='PENDIENTE')
    observaciones = models.TextField(blank=True, null=True)
    
    # Control de calidad
    inspeccion_realizada = models.BooleanField(default=False)
    inspeccion_aprobada = models.BooleanField(default=False)
    observaciones_inspeccion = models.TextField(blank=True, null=True)
    
    # Usuario
    recibido_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    inspeccionado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name='inspecciones_realizadas')

    class Meta:
        verbose_name = "Recepción de Mercancía"
        verbose_name_plural = "Recepciones de Mercancía"
        ordering = ['-fecha_recepcion']

    def __str__(self):
        return f"REC-{self.numero} - OC-{self.orden_compra.numero}"
    
    def save(self, *args, **kwargs):
        if not self.numero:
            ultimo_numero = RecepcionMercancia.objects.count() + 1
            self.numero = f"{ultimo_numero:06d}"
        super().save(*args, **kwargs)

class DetalleRecepcionMercancia(models.Model):
    recepcion = models.ForeignKey(RecepcionMercancia, on_delete=models.CASCADE, related_name='detalles')
    detalle_orden = models.ForeignKey(DetalleOrdenCompra, on_delete=models.CASCADE)
    cantidad_recibida = models.DecimalField(max_digits=10, decimal_places=2)
    lote = models.CharField(max_length=100, blank=True, null=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Detalle Recepción"
        verbose_name_plural = "Detalles Recepción"

    def __str__(self):
        return f"Recibido: {self.cantidad_recibida} {self.detalle_orden.producto.unidad_medida} de {self.detalle_orden.producto.nombre}"

class InventarioFisico(models.Model):
    """Modelo para realizar inventarios físicos periódicos"""
    ESTADO_CHOICES = [
        ('PLANIFICADO', 'Planificado'),
        ('EN_PROCESO', 'En Proceso'),
        ('COMPLETADO', 'Completado'),
        ('AJUSTADO', 'Ajustado'),
        ('CANCELADO', 'Cancelado'),
    ]
    
    nombre = models.CharField(max_length=200)
    fecha_planificada = models.DateField()
    fecha_inicio = models.DateTimeField(blank=True, null=True)
    fecha_fin = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='PLANIFICADO')
    
    # Filtros del inventario
    ubicaciones = models.ManyToManyField(UbicacionAlmacen, blank=True)
    categorias = models.ManyToManyField(CategoriaProducto, blank=True)
    tipos_producto = models.CharField(max_length=500, blank=True, null=True, 
                                    help_text="Tipos de producto separados por coma")
    
    # Totales y diferencias
    total_productos_contados = models.IntegerField(default=0)
    total_diferencias = models.IntegerField(default=0)
    valor_diferencias = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Control
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    observaciones = models.TextField(blank=True, null=True)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Inventario Físico"
        verbose_name_plural = "Inventarios Físicos"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.nombre} - {self.fecha_planificada}"

class DetalleInventarioFisico(models.Model):
    inventario = models.ForeignKey(InventarioFisico, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    stock_sistema = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_fisico = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    diferencia = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_diferencia = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Conteo
    contado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_conteo = models.DateTimeField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    
    # Ajuste
    ajustado = models.BooleanField(default=False)
    movimiento_ajuste = models.ForeignKey(MovimientoInventario, on_delete=models.SET_NULL, 
                                        null=True, blank=True)

    class Meta:
        verbose_name = "Detalle Inventario Físico"
        verbose_name_plural = "Detalles Inventario Físico"
        unique_together = ['inventario', 'producto']

    def __str__(self):
        return f"{self.producto.nombre} - Dif: {self.diferencia}"
    
    def save(self, *args, **kwargs):
        # Calcular diferencia automáticamente
        self.diferencia = self.stock_fisico - self.stock_sistema
        self.valor_diferencia = self.diferencia * self.producto.precio_compra
        super().save(*args, **kwargs)
