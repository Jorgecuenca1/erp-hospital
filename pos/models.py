from django.db import models
from django.conf import settings
from django.utils import timezone
from decimal import Decimal
from billing.models import Factura
from accounting.models import CuentaContable, Diario, Tercero, AsientoContable, Impuesto
from inventories.models import Producto, MovimientoInventario

User = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

class PuntoVenta(models.Model):
    """Configuración de puntos de venta del hospital"""
    TIPO_POS_CHOICES = [
        ('FARMACIA', 'Farmacia'),
        ('CAFETERIA', 'Cafetería'),
        ('TIENDA', 'Tienda'),
        ('SERVICIOS', 'Servicios Médicos'),
        ('LABORATORIO', 'Laboratorio'),
        ('GENERAL', 'General'),
    ]
    
    # Información básica
    codigo = models.CharField(max_length=20, unique=True, blank=True, null=True, help_text="Código del punto de venta")
    nombre = models.CharField(max_length=100)
    tipo_pos = models.CharField(max_length=20, choices=TIPO_POS_CHOICES, default='GENERAL')
    ubicacion = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    
    # Configuración contable
    diario_ventas = models.ForeignKey(Diario, on_delete=models.PROTECT, related_name='puntos_venta',
                                    blank=True, null=True, help_text="Diario contable para las ventas de este POS")
    cuenta_ventas_default = models.ForeignKey(CuentaContable, on_delete=models.PROTECT, 
                                            related_name='puntos_venta_ventas', blank=True, null=True,
                                            help_text="Cuenta contable por defecto para ventas")
    
    # Configuración operativa
    permite_ventas_credito = models.BooleanField(default=False)
    limite_credito_diario = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    requiere_autorizacion_descuentos = models.BooleanField(default=True)
    descuento_maximo_permitido = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # Configuración de impresión
    impresora_tickets = models.CharField(max_length=200, blank=True, null=True)
    template_ticket = models.TextField(blank=True, null=True)
    imprimir_automatico = models.BooleanField(default=True)
    
    # Estado y control
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Punto de Venta"
        verbose_name_plural = "Puntos de Venta"
        ordering = ['codigo']
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    def save(self, *args, **kwargs):
        if not self.codigo:
            # Generar código automáticamente
            ultimo_numero = PuntoVenta.objects.count() + 1
            self.codigo = f"POS{ultimo_numero:03d}"
        super().save(*args, **kwargs)

class Caja(models.Model):
    """Cajas registradoras del punto de venta"""
    # Información básica
    codigo = models.CharField(max_length=20, unique=True, blank=True, null=True)
    nombre = models.CharField(max_length=100)
    punto_venta = models.ForeignKey(PuntoVenta, on_delete=models.CASCADE, related_name='cajas')
    
    # Configuración contable
    cuenta_contable = models.ForeignKey(CuentaContable, on_delete=models.PROTECT,
                                      help_text="Cuenta contable para el efectivo de esta caja")
    
    # Configuración operativa
    saldo_minimo = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                     help_text="Saldo mínimo requerido para operar")
    saldo_maximo = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                     help_text="Saldo máximo permitido")
    
    # Control de acceso
    usuarios_autorizados = models.ManyToManyField(User, blank=True, 
                                                related_name='cajas_autorizadas')
    requiere_autorizacion_cierre = models.BooleanField(default=True)
    
    # Configuración física
    ubicacion_fisica = models.CharField(max_length=200, blank=True, null=True)
    numero_serie = models.CharField(max_length=100, blank=True, null=True)
    modelo = models.CharField(max_length=100, blank=True, null=True)
    
    # Estado
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Caja Registradora"
        verbose_name_plural = "Cajas Registradoras"
        ordering = ['codigo']
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre} ({self.punto_venta})"
    
    def save(self, *args, **kwargs):
        if not self.codigo:
            # Generar código automáticamente
            ultimo_numero = Caja.objects.filter(punto_venta=self.punto_venta).count() + 1
            self.codigo = f"{self.punto_venta.codigo}-CAJA{ultimo_numero:02d}"
        super().save(*args, **kwargs)
    
    @property
    def sesion_activa(self):
        """Retorna la sesión activa de esta caja"""
        return self.sesiones.filter(abierta=True).first()
    
    @property
    def saldo_actual(self):
        """Calcula el saldo actual de la caja"""
        sesion = self.sesion_activa
        if sesion:
            return sesion.calcular_saldo_actual()
        return Decimal('0.00')

class SesionCaja(models.Model):
    """Sesiones de trabajo en cada caja registradora"""
    ESTADO_CHOICES = [
        ('ABIERTA', 'Abierta'),
        ('CERRADA', 'Cerrada'),
        ('SUSPENDIDA', 'Suspendida'),
        ('CANCELADA', 'Cancelada'),
    ]
    
    # Información básica
    numero_sesion = models.CharField(max_length=50, unique=True, blank=True)
    caja = models.ForeignKey(Caja, on_delete=models.CASCADE, related_name='sesiones')
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name='sesiones_caja')
    
    # Fechas y tiempos
    fecha_apertura = models.DateTimeField(auto_now_add=True)
    fecha_cierre = models.DateTimeField(blank=True, null=True)
    duracion_minutos = models.IntegerField(default=0, help_text="Duración de la sesión en minutos")
    
    # Saldos iniciales
    saldo_inicial_efectivo = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    saldo_inicial_sistema = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    diferencia_inicial = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    
    # Saldos finales
    saldo_final_efectivo = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    saldo_final_sistema = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    diferencia_final = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    
    # Totales de la sesión
    total_ventas_efectivo = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    total_ventas_tarjeta = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    total_ventas_transferencia = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    total_ventas_credito = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    total_ventas = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    
    # Otros movimientos
    total_retiros = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    total_ingresos_extra = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    total_devoluciones = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    
    # Contadores
    numero_transacciones = models.IntegerField(default=0)
    numero_clientes = models.IntegerField(default=0)
    
    # Estado y control
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='ABIERTA')
    abierta = models.BooleanField(default=True)
    observaciones_apertura = models.TextField(blank=True, null=True)
    observaciones_cierre = models.TextField(blank=True, null=True)
    
    # Autorización y supervisión
    supervisor_apertura = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                          related_name='sesiones_supervisor_apertura')
    supervisor_cierre = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name='sesiones_supervisor_cierre')
    
    # Integración contable
    asiento_apertura = models.ForeignKey(AsientoContable, on_delete=models.SET_NULL, null=True, blank=True,
                                       related_name='sesiones_apertura')
    asiento_cierre = models.ForeignKey(AsientoContable, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='sesiones_cierre')
    contabilizada = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Sesión de Caja"
        verbose_name_plural = "Sesiones de Caja"
        ordering = ['-fecha_apertura']
    
    def __str__(self):
        return f"Sesión {self.numero_sesion} - {self.caja} - {self.usuario}"
    
    def save(self, *args, **kwargs):
        if not self.numero_sesion:
            # Generar número de sesión automáticamente
            fecha = timezone.now()
            contador = SesionCaja.objects.filter(
                fecha_apertura__date=fecha.date(),
                caja=self.caja
            ).count() + 1
            self.numero_sesion = f"{self.caja.codigo}-{fecha.strftime('%Y%m%d')}-{contador:03d}"
        super().save(*args, **kwargs)
    
    def calcular_saldo_actual(self):
        """Calcula el saldo actual de la sesión"""
        return (self.saldo_inicial_efectivo + 
                self.total_ventas_efectivo + 
                self.total_ingresos_extra - 
                self.total_retiros - 
                self.total_devoluciones)
    
    def calcular_totales(self):
        """Calcula todos los totales de la sesión"""
        ventas = self.ventas.all()
        
        self.total_ventas_efectivo = sum(
            v.total for v in ventas.filter(metodo_pago__nombre__icontains='efectivo')
        )
        self.total_ventas_tarjeta = sum(
            v.total for v in ventas.filter(metodo_pago__nombre__icontains='tarjeta')
        )
        self.total_ventas_transferencia = sum(
            v.total for v in ventas.filter(metodo_pago__nombre__icontains='transferencia')
        )
        self.total_ventas_credito = sum(
            v.total for v in ventas.filter(metodo_pago__nombre__icontains='credito')
        )
        
        self.total_ventas = sum(v.total for v in ventas)
        self.numero_transacciones = ventas.count()
        self.numero_clientes = ventas.exclude(tercero__isnull=True).values('tercero').distinct().count()
        
        # Calcular saldo final del sistema
        self.saldo_final_sistema = self.calcular_saldo_actual()
        
        self.save()
    
    def cerrar_sesion(self, saldo_efectivo_contado, supervisor=None, observaciones=''):
        """Cierra la sesión de caja"""
        if not self.abierta:
            return False
        
        self.fecha_cierre = timezone.now()
        self.duracion_minutos = int((self.fecha_cierre - self.fecha_apertura).total_seconds() / 60)
        self.saldo_final_efectivo = saldo_efectivo_contado
        self.diferencia_final = self.saldo_final_efectivo - self.saldo_final_sistema
        self.observaciones_cierre = observaciones
        self.supervisor_cierre = supervisor
        self.estado = 'CERRADA'
        self.abierta = False
        
        # Calcular totales finales
        self.calcular_totales()
        
        self.save()
        return True

class MetodoPagoPOS(models.Model):
    """Métodos de pago disponibles en el POS"""
    TIPO_METODO_CHOICES = [
        ('EFECTIVO', 'Efectivo'),
        ('TARJETA_DEBITO', 'Tarjeta Débito'),
        ('TARJETA_CREDITO', 'Tarjeta Crédito'),
        ('TRANSFERENCIA', 'Transferencia Bancaria'),
        ('CHEQUE', 'Cheque'),
        ('CREDITO', 'Crédito'),
        ('VALE', 'Vale/Cupón'),
        ('MIXTO', 'Pago Mixto'),
    ]
    
    # Información básica
    codigo = models.CharField(max_length=20, unique=True, blank=True, null=True)
    nombre = models.CharField(max_length=50)
    tipo_metodo = models.CharField(max_length=20, choices=TIPO_METODO_CHOICES, default='EFECTIVO')
    descripcion = models.TextField(blank=True, null=True)
    
    # Configuración contable
    cuenta_contable = models.ForeignKey(CuentaContable, on_delete=models.PROTECT,
                                      help_text="Cuenta contable para este método de pago")
    cuenta_comision = models.ForeignKey(CuentaContable, on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='metodos_pago_comision',
                                      help_text="Cuenta para registrar comisiones")
    
    # Configuración operativa
    requiere_autorizacion = models.BooleanField(default=False)
    limite_maximo = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                      help_text="Límite máximo por transacción (0 = sin límite)")
    porcentaje_comision = models.DecimalField(max_digits=5, decimal_places=4, default=0,
                                            help_text="Porcentaje de comisión")
    valor_fijo_comision = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                            help_text="Valor fijo de comisión")
    
    # Configuración de validación
    requiere_referencia = models.BooleanField(default=False)
    requiere_autorizacion_banco = models.BooleanField(default=False)
    dias_compensacion = models.IntegerField(default=0, help_text="Días para compensación del pago")
    
    # Integración externa
    codigo_proveedor = models.CharField(max_length=100, blank=True, null=True)
    url_api = models.URLField(blank=True, null=True)
    requiere_pin = models.BooleanField(default=False)
    
    # Estado
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    orden_visualizacion = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Método de Pago POS"
        verbose_name_plural = "Métodos de Pago POS"
        ordering = ['orden_visualizacion', 'nombre']
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    def save(self, *args, **kwargs):
        if not self.codigo:
            # Generar código automáticamente
            prefijo = self.tipo_metodo[:3].upper()
            ultimo_numero = MetodoPagoPOS.objects.filter(tipo_metodo=self.tipo_metodo).count() + 1
            self.codigo = f"{prefijo}{ultimo_numero:03d}"
        super().save(*args, **kwargs)
    
    def calcular_comision(self, monto):
        """Calcula la comisión para un monto dado"""
        comision_porcentaje = monto * (self.porcentaje_comision / 100)
        return comision_porcentaje + self.valor_fijo_comision

class VentaPOS(models.Model):
    """Ventas realizadas a través del punto de venta"""
    ESTADO_CHOICES = [
        ('BORRADOR', 'Borrador'),
        ('CONFIRMADA', 'Confirmada'),
        ('PAGADA', 'Pagada'),
        ('DEVOLUCION_PARCIAL', 'Devolución Parcial'),
        ('DEVOLUCION_TOTAL', 'Devolución Total'),
        ('CANCELADA', 'Cancelada'),
    ]
    
    TIPO_VENTA_CHOICES = [
        ('MOSTRADOR', 'Venta Mostrador'),
        ('DOMICILIO', 'Venta Domicilio'),
        ('TELEFONICA', 'Venta Telefónica'),
        ('ONLINE', 'Venta Online'),
        ('PRESCRIPCION', 'Venta con Prescripción'),
    ]
    
    # Información básica
    numero_ticket = models.CharField(max_length=50, unique=True, blank=True)
    sesion = models.ForeignKey(SesionCaja, on_delete=models.PROTECT, related_name='ventas')
    fecha = models.DateTimeField(auto_now_add=True)
    tipo_venta = models.CharField(max_length=20, choices=TIPO_VENTA_CHOICES, default='MOSTRADOR')
    
    # Cliente
    tercero = models.ForeignKey(Tercero, on_delete=models.PROTECT, blank=True, null=True)
    nombre_cliente = models.CharField(max_length=200, blank=True, null=True, 
                                    help_text="Nombre del cliente si no está registrado")
    telefono_cliente = models.CharField(max_length=50, blank=True, null=True)
    email_cliente = models.EmailField(blank=True, null=True)
    
    # Totales
    subtotal = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    descuento_total = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    impuestos_total = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=16, decimal_places=2)
    
    # Pago
    metodo_pago = models.ForeignKey(MetodoPagoPOS, on_delete=models.PROTECT)
    monto_recibido = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    cambio = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    referencia_pago = models.CharField(max_length=100, blank=True, null=True)
    autorizacion_pago = models.CharField(max_length=100, blank=True, null=True)
    
    # Integración contable y facturación
    factura = models.OneToOneField(Factura, on_delete=models.SET_NULL, blank=True, null=True)
    asiento_contable = models.ForeignKey(AsientoContable, on_delete=models.SET_NULL, null=True, blank=True)
    diario = models.ForeignKey(Diario, on_delete=models.PROTECT)
    contabilizada = models.BooleanField(default=False)
    
    # Prescripción médica (para farmacias)
    numero_prescripcion = models.CharField(max_length=100, blank=True, null=True)
    medico_prescriptor = models.CharField(max_length=200, blank=True, null=True)
    fecha_prescripcion = models.DateField(blank=True, null=True)
    
    # Delivery/domicilio
    direccion_entrega = models.TextField(blank=True, null=True)
    fecha_entrega = models.DateTimeField(blank=True, null=True)
    costo_domicilio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    entregado = models.BooleanField(default=False)
    
    # Estado y control
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='BORRADOR')
    observaciones = models.TextField(blank=True, null=True)
    
    # Usuarios
    vendedor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='ventas_realizadas', 
                               blank=True, null=True)
    supervisor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='ventas_supervisadas')
    
    # Fechas de control
    fecha_confirmacion = models.DateTimeField(blank=True, null=True)
    fecha_pago = models.DateTimeField(blank=True, null=True)
    fecha_entrega = models.DateTimeField(blank=True, null=True)
    
    # Integración con inventario
    actualizo_inventario = models.BooleanField(default=False)
    
    # Promociones y descuentos
    codigo_promocion = models.CharField(max_length=50, blank=True, null=True)
    porcentaje_descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # Información adicional
    comentarios_internos = models.TextField(blank=True, null=True)
    requiere_seguimiento = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Venta POS"
        verbose_name_plural = "Ventas POS"
        ordering = ['-fecha']
        indexes = [
            models.Index(fields=['numero_ticket']),
            models.Index(fields=['fecha', 'sesion']),
            models.Index(fields=['estado']),
            models.Index(fields=['tercero']),
        ]
    
    def __str__(self):
        return f"Ticket {self.numero_ticket} - {self.fecha.strftime('%d/%m/%Y %H:%M')} - ${self.total}"
    
    def save(self, *args, **kwargs):
        if not self.numero_ticket:
            # Generar número de ticket automáticamente
            fecha = timezone.now()
            contador = VentaPOS.objects.filter(
                fecha__date=fecha.date(),
                sesion__caja=self.sesion.caja
            ).count() + 1
            self.numero_ticket = f"{self.sesion.caja.codigo}-{fecha.strftime('%Y%m%d')}-{contador:04d}"
        
        # Asignar vendedor si no está definido
        if not self.vendedor_id and hasattr(self, '_vendedor'):
            self.vendedor = self._vendedor
            
        super().save(*args, **kwargs)
    
    def calcular_totales(self):
        """Calcula todos los totales de la venta"""
        lineas = self.lineas.all()
        
        self.subtotal = sum(linea.subtotal for linea in lineas)
        self.descuento_total = sum(linea.descuento_valor for linea in lineas)
        self.impuestos_total = sum(linea.impuesto_valor for linea in lineas)
        self.total = self.subtotal - self.descuento_total + self.impuestos_total + self.costo_domicilio
        
        # Calcular cambio si es efectivo
        if self.metodo_pago.tipo_metodo == 'EFECTIVO':
            self.cambio = max(0, self.monto_recibido - self.total)
        else:
            self.cambio = 0
            
        self.save()
    
    def confirmar_venta(self):
        """Confirma la venta y actualiza inventario"""
        if self.estado != 'BORRADOR':
            return False
        
        # Verificar stock disponible
        for linea in self.lineas.all():
            if linea.producto and linea.producto.stock_actual < linea.cantidad:
                raise ValueError(f"Stock insuficiente para {linea.producto.nombre}")
        
        # Actualizar inventario
        for linea in self.lineas.all():
            if linea.producto:
                # Crear movimiento de salida de inventario
                MovimientoInventario.objects.create(
                    producto=linea.producto,
                    tipo_movimiento='SALIDA',
                    cantidad=linea.cantidad,
                    precio_unitario=linea.precio_unitario,
                    valor_total=linea.subtotal,
                    numero_documento=self.numero_ticket,
                    observaciones=f"Venta POS - Ticket {self.numero_ticket}",
                    estado='CONFIRMADO',
                    usuario=self.vendedor
                )
        
        self.estado = 'CONFIRMADA'
        self.fecha_confirmacion = timezone.now()
        self.actualizo_inventario = True
        self.save()
        
        return True
    
    def generar_asiento_contable(self):
        """Genera el asiento contable para esta venta"""
        if self.contabilizada:
            return self.asiento_contable
        
        from accounting.models import PeriodoContable, LineaAsiento
        
        # Obtener período contable
        periodo = PeriodoContable.objects.filter(
            fecha_inicio__lte=self.fecha.date(),
            fecha_fin__gte=self.fecha.date(),
            cerrado=False
        ).first()
        
        if not periodo:
            return None
        
        # Crear asiento contable
        asiento = AsientoContable.objects.create(
            fecha=self.fecha.date(),
            descripcion=f"Venta POS - Ticket {self.numero_ticket}",
            diario=self.diario,
            periodo=periodo,
            tercero=self.tercero,
            referencia=self.numero_ticket
        )
        
        # Débito: Método de pago (Caja, Banco, etc.)
        LineaAsiento.objects.create(
            asiento=asiento,
            cuenta=self.metodo_pago.cuenta_contable,
            descripcion=f"Venta POS - {self.metodo_pago.nombre}",
            debito=self.total,
            credito=0
        )
        
        # Crédito: Ventas
        cuenta_ventas = self.sesion.caja.punto_venta.cuenta_ventas_default
        LineaAsiento.objects.create(
            asiento=asiento,
            cuenta=cuenta_ventas,
            descripcion=f"Venta POS - Ticket {self.numero_ticket}",
            debito=0,
            credito=self.subtotal
        )
        
        # Crédito: Impuestos si los hay
        if self.impuestos_total > 0:
            # Buscar cuenta de IVA por cobrar
            cuenta_iva = CuentaContable.objects.filter(
                codigo__startswith='2408'  # IVA por pagar
            ).first()
            
            if cuenta_iva:
                LineaAsiento.objects.create(
                    asiento=asiento,
                    cuenta=cuenta_iva,
                    descripcion=f"IVA Venta POS - Ticket {self.numero_ticket}",
                    debito=0,
                    credito=self.impuestos_total
                )
        
        self.asiento_contable = asiento
        self.contabilizada = True
        self.save()
        
        return asiento

class LineaVentaPOS(models.Model):
    """Líneas de detalle de cada venta POS"""
    # Venta principal
    venta = models.ForeignKey(VentaPOS, on_delete=models.CASCADE, related_name='lineas')
    numero_linea = models.IntegerField(default=1)
    
    # Producto (si existe en inventario)
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True)
    descripcion = models.CharField(max_length=255)
    codigo_producto = models.CharField(max_length=100, blank=True, null=True)
    codigo_barras = models.CharField(max_length=100, blank=True, null=True)
    
    # Cantidades y precios
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=16, decimal_places=2)
    precio_original = models.DecimalField(max_digits=16, decimal_places=2, default=0, 
                                        help_text="Precio antes de descuentos")
    
    # Descuentos
    descuento_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    descuento_valor = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    motivo_descuento = models.CharField(max_length=200, blank=True, null=True)
    autorizado_descuento_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                                related_name='descuentos_autorizados')
    
    # Impuestos
    impuesto = models.ForeignKey(Impuesto, on_delete=models.SET_NULL, null=True, blank=True)
    porcentaje_impuesto = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    impuesto_valor = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    
    # Totales
    subtotal = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    
    # Información adicional para productos médicos
    lote = models.CharField(max_length=100, blank=True, null=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    requiere_receta = models.BooleanField(default=False)
    numero_receta = models.CharField(max_length=100, blank=True, null=True)
    
    # Control de devoluciones
    devuelto = models.BooleanField(default=False)
    cantidad_devuelta = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_devolucion = models.DateTimeField(blank=True, null=True)
    motivo_devolucion = models.CharField(max_length=200, blank=True, null=True)
    
    # Notas y observaciones
    observaciones = models.TextField(blank=True, null=True)
    comentarios_vendedor = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Línea Venta POS"
        verbose_name_plural = "Líneas Venta POS"
        ordering = ['numero_linea']
        unique_together = ['venta', 'numero_linea']

    def __str__(self):
        return f"{self.descripcion} x {self.cantidad} - ${self.total}"
    
    def save(self, *args, **kwargs):
        # Calcular totales automáticamente
        self.subtotal = self.cantidad * self.precio_unitario
        self.descuento_valor = self.subtotal * (self.descuento_porcentaje / 100) if self.descuento_porcentaje > 0 else self.descuento_valor
        subtotal_con_descuento = self.subtotal - self.descuento_valor
        self.impuesto_valor = subtotal_con_descuento * (self.porcentaje_impuesto / 100)
        self.total = subtotal_con_descuento + self.impuesto_valor
        
        # Asignar número de línea si es nueva
        if not self.numero_linea:
            ultima_linea = LineaVentaPOS.objects.filter(venta=self.venta).order_by('-numero_linea').first()
            self.numero_linea = (ultima_linea.numero_linea + 1) if ultima_linea else 1
        
        # Copiar información del producto si existe
        if self.producto and not self.codigo_producto:
            self.codigo_producto = self.producto.codigo
            self.codigo_barras = self.producto.codigo_barras
            self.precio_original = self.producto.precio_venta
            if not self.precio_unitario:
                self.precio_unitario = self.producto.precio_venta
            if not self.descripcion:
                self.descripcion = self.producto.nombre
            self.requiere_receta = self.producto.requiere_prescripcion
            
        super().save(*args, **kwargs)
    
    def aplicar_descuento(self, porcentaje=0, valor=0, motivo='', autorizado_por=None):
        """Aplica un descuento a esta línea"""
        if porcentaje > 0:
            self.descuento_porcentaje = porcentaje
            self.descuento_valor = self.subtotal * (porcentaje / 100)
        elif valor > 0:
            self.descuento_valor = valor
            self.descuento_porcentaje = (valor / self.subtotal) * 100 if self.subtotal > 0 else 0
        
        self.motivo_descuento = motivo
        self.autorizado_descuento_por = autorizado_por
        self.save()
    
    def devolver(self, cantidad_devolver, motivo=''):
        """Procesa una devolución de esta línea"""
        if cantidad_devolver <= 0 or cantidad_devolver > (self.cantidad - self.cantidad_devuelta):
            return False
        
        self.cantidad_devuelta += cantidad_devolver
        self.devuelto = self.cantidad_devuelta >= self.cantidad
        self.fecha_devolucion = timezone.now()
        self.motivo_devolucion = motivo
        
        # Si hay producto en inventario, crear movimiento de entrada
        if self.producto:
            MovimientoInventario.objects.create(
                producto=self.producto,
                tipo_movimiento='DEVOLUCION',
                cantidad=cantidad_devolver,
                precio_unitario=self.precio_unitario,
                valor_total=cantidad_devolver * self.precio_unitario,
                numero_documento=f"DEV-{self.venta.numero_ticket}",
                observaciones=f"Devolución de venta POS - {motivo}",
                estado='CONFIRMADO'
            )
        
        self.save()
        return True

# ========== MODELOS ADICIONALES PARA POS COMPLETO ==========

class PromocionesPOS(models.Model):
    """Promociones y descuentos especiales para el POS"""
    TIPO_PROMOCION_CHOICES = [
        ('PORCENTAJE', 'Descuento Porcentual'),
        ('VALOR_FIJO', 'Valor Fijo'),
        ('2X1', '2x1'),
        ('COMBO', 'Combo'),
        ('COMPRA_MINIMA', 'Descuento por Compra Mínima'),
    ]
    
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    tipo_promocion = models.CharField(max_length=20, choices=TIPO_PROMOCION_CHOICES)
    
    # Configuración del descuento
    valor_descuento = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    porcentaje_descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    monto_minimo_compra = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Vigencia
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    activa = models.BooleanField(default=True)
    
    # Restricciones
    productos = models.ManyToManyField(Producto, blank=True)
    categorias = models.ManyToManyField('inventories.CategoriaProducto', blank=True)
    puntos_venta = models.ManyToManyField(PuntoVenta, blank=True)
    
    # Límites
    limite_usos_total = models.IntegerField(default=0, help_text="0 = sin límite")
    limite_usos_cliente = models.IntegerField(default=0, help_text="0 = sin límite")
    usos_actuales = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = "Promoción POS"
        verbose_name_plural = "Promociones POS"
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

class MovimientoCaja(models.Model):
    """Movimientos de efectivo en la caja registradora"""
    TIPO_MOVIMIENTO_CHOICES = [
        ('INGRESO', 'Ingreso'),
        ('RETIRO', 'Retiro'),
        ('AJUSTE', 'Ajuste'),
        ('CAMBIO_INICIAL', 'Cambio Inicial'),
    ]
    
    sesion = models.ForeignKey(SesionCaja, on_delete=models.CASCADE, related_name='movimientos_caja')
    tipo_movimiento = models.CharField(max_length=20, choices=TIPO_MOVIMIENTO_CHOICES)
    monto = models.DecimalField(max_digits=15, decimal_places=2)
    concepto = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    
    # Autorización
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    autorizado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='movimientos_caja_autorizados')
    
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Movimiento de Caja"
        verbose_name_plural = "Movimientos de Caja"
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.get_tipo_movimiento_display()} - ${self.monto} - {self.concepto}"
