from django.db import models
from django.conf import settings
from decimal import Decimal
import datetime
from django.contrib.auth import get_user_model
from django.db.models import Sum

User = get_user_model()

class DatosEmpresa(models.Model):
    """Datos básicos de la empresa"""
    nombre = models.CharField(max_length=255)
    nit = models.CharField(max_length=20, unique=True)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=30)
    email = models.EmailField()
    ciudad = models.CharField(max_length=100)
    representante_legal = models.CharField(max_length=255)
    cargo_representante = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

class CentroCosto(models.Model):
    """Centros de costos para contratos y convenios"""
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    contrato = models.CharField(max_length=100, blank=True, null=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

class PeriodoContable(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True, help_text="Dejar vacío para período indefinido")
    cerrado = models.BooleanField(default=False)
    
    def __str__(self):
        if self.fecha_fin:
            return f"{self.nombre} ({self.fecha_inicio} a {self.fecha_fin})"
        else:
            return f"{self.nombre} (desde {self.fecha_inicio} - indefinido)"

class CuentaContable(models.Model):
    TIPO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('PASIVO', 'Pasivo'),
        ('PATRIMONIO', 'Patrimonio'),
        ('INGRESO', 'Ingreso'),
        ('GASTO', 'Gasto'),
        ('COSTO', 'Costo'),
        ('ORDEN', 'Cuentas de Orden'),
    ]
    
    codigo = models.CharField(max_length=20, unique=True, help_text="Código PUC")
    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    nivel = models.IntegerField(default=1)
    padre = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subcuentas')
    activa = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Cuenta Contable"
        verbose_name_plural = "Cuentas Contables"
        ordering = ['codigo']
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

class Pais(models.Model):
    codigo = models.CharField(max_length=3, unique=True, help_text="Código ISO del país")
    nombre = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = "País"
        verbose_name_plural = "Países"
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

class Departamento(models.Model):
    codigo = models.CharField(max_length=5, unique=True, help_text="Código DANE del departamento")
    nombre = models.CharField(max_length=100)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, related_name='departamentos')
    
    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

class Ciudad(models.Model):
    codigo = models.CharField(max_length=8, unique=True, help_text="Código DANE de la ciudad")
    nombre = models.CharField(max_length=100)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, related_name='ciudades')
    
    class Meta:
        verbose_name = "Ciudad"
        verbose_name_plural = "Ciudades"
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}, {self.departamento.nombre}"

class Tercero(models.Model):
    TIPO_CHOICES = [('NATURAL','Persona Natural'),('JURIDICA','Persona Jurídica')]
    REGIMEN_CHOICES = [
        ('SIMPLIFICADO', 'Régimen Simplificado'),
        ('COMUN', 'Régimen Común'),
        ('GRAN_CONTRIBUYENTE', 'Gran Contribuyente'),
        ('NO_RESPONSABLE', 'No Responsable de IVA'),
    ]
    
    # Campos básicos existentes
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    nombre = models.CharField(max_length=255)
    nit = models.CharField(max_length=20, unique=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    activa = models.BooleanField(default=True)
    
    # Nuevos campos colombianos (todos opcionales para no afectar datos existentes)
    codigo_tercero = models.CharField(max_length=2, blank=True, null=True, help_text="13=Natural, 31=Jurídica")
    primer_nombre = models.CharField(max_length=50, blank=True, null=True)
    segundo_nombre = models.CharField(max_length=50, blank=True, null=True)
    primer_apellido = models.CharField(max_length=50, blank=True, null=True)
    segundo_apellido = models.CharField(max_length=50, blank=True, null=True)
    razon_social = models.CharField(max_length=255, blank=True, null=True)
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT, blank=True, null=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT, blank=True, null=True)
    ciudad_nueva = models.ForeignKey(Ciudad, on_delete=models.PROTECT, blank=True, null=True)
    regimen_iva = models.CharField(max_length=20, choices=REGIMEN_CHOICES, blank=True, null=True)
    responsable_ica = models.BooleanField(default=False)
    cupo_credito = models.DecimalField(max_digits=16, decimal_places=2, default=0, blank=True, null=True)
    
    class Meta:
        verbose_name = "Tercero"
        verbose_name_plural = "Terceros"
        ordering = ['nombre']
    
    def save(self, *args, **kwargs):
        # Asignar código automáticamente según el tipo
        if self.tipo == 'NATURAL' and not self.codigo_tercero:
            self.codigo_tercero = '13'
        elif self.tipo == 'JURIDICA' and not self.codigo_tercero:
            self.codigo_tercero = '31'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.nombre} ({self.nit})"

class Diario(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, unique=True)
    tipo = models.CharField(max_length=20, choices=[('GENERAL','General'),('CAJA','Caja'),('BANCO','Banco'),('VENTAS','Ventas'),('COMPRAS','Compras')])
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

class Impuesto(models.Model):
    TIPO_IMPUESTO_CHOICES = [
        ('IVA', 'IVA - Impuesto al Valor Agregado'),
        ('RETEICA', 'RETEICA - Retención de Industria y Comercio'),
        ('RETEFUENTE', 'RETEFUENTE - Retención en la Fuente'),
        ('RETEIVA', 'RETEIVA - Retención de IVA'),
        ('CONSUMO', 'Impuesto al Consumo'),
        ('OTRO', 'Otro Impuesto'),
    ]
    
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20, unique=True)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2, help_text="Porcentaje del impuesto")
    tipo = models.CharField(max_length=20, choices=TIPO_IMPUESTO_CHOICES)
    activo = models.BooleanField(default=True)
    
    # Nuevos campos colombianos (opcionales)
    inicio_vigencia = models.DateField(blank=True, null=True, help_text="Fecha de inicio de vigencia")
    fin_vigencia = models.DateField(blank=True, null=True, help_text="Fecha de fin de vigencia")
    valor_base_minimo = models.DecimalField(max_digits=16, decimal_places=2, default=0, blank=True, null=True)
    
    class Meta:
        verbose_name = "Impuesto"
        verbose_name_plural = "Impuestos"
        ordering = ['codigo']
    
    def __str__(self):
        return f"{self.nombre} ({self.porcentaje}%)"

class ComprobanteContable(models.Model):
    """Comprobantes contables con tipos específicos"""
    TIPO_CHOICES = [
        ('FC', 'Factura de Compra'),
        ('CE', 'Comprobante de Egreso'),
        ('FVE', 'Factura Electrónica'),
        ('CI', 'Comprobante de Ingreso'),
    ]
    
    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('ANULADO', 'Anulado'),
        ('SIN_PROCESAR', 'Sin Procesar'),
    ]
    
    tipo = models.CharField(max_length=3, choices=TIPO_CHOICES)
    numero = models.CharField(max_length=20, unique=True)
    fecha = models.DateField()
    tercero = models.ForeignKey(Tercero, on_delete=models.PROTECT)
    centro_costo = models.ForeignKey(CentroCosto, on_delete=models.PROTECT, blank=True, null=True)
    descripcion = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=16, decimal_places=2)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='ACTIVO')
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.tipo}-{self.numero} - {self.fecha} - {self.tercero.nombre}"
    
    def generar_numero(self):
        """Genera número consecutivo según formato especificado"""
        año = datetime.date.today().year
        mes = datetime.date.today().month
        dia = datetime.date.today().day
        
        # Buscar último número del tipo
        ultimo = ComprobanteContable.objects.filter(
            tipo=self.tipo,
            numero__startswith=f"{año}{mes:02d}{dia:02d}"
        ).order_by('-numero').first()
        
        if ultimo:
            try:
                ultimo_numero = int(ultimo.numero[-4:])
                nuevo_numero = ultimo_numero + 1
            except ValueError:
                nuevo_numero = 1
        else:
            nuevo_numero = 1
        
        return f"{año}{mes:02d}{dia:02d}{nuevo_numero:04d}"

class AsientoContable(models.Model):
    fecha = models.DateField()
    descripcion = models.CharField(max_length=255)
    diario = models.ForeignKey(Diario, on_delete=models.PROTECT)
    periodo = models.ForeignKey(PeriodoContable, on_delete=models.PROTECT)
    tercero = models.ForeignKey(Tercero, on_delete=models.PROTECT, blank=True, null=True)
    centro_costo = models.ForeignKey(CentroCosto, on_delete=models.PROTECT, blank=True, null=True)
    comprobante = models.ForeignKey(ComprobanteContable, on_delete=models.SET_NULL, blank=True, null=True)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    referencia = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        pk = getattr(self, 'pk', None)
        return f"Asiento {pk if pk is not None else ''} - {self.fecha} - {self.descripcion}"

class LineaAsiento(models.Model):
    asiento = models.ForeignKey(AsientoContable, on_delete=models.CASCADE, related_name='lineas')
    cuenta = models.ForeignKey(CuentaContable, on_delete=models.PROTECT)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    debito = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    credito = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    impuesto = models.ForeignKey(Impuesto, on_delete=models.SET_NULL, null=True, blank=True)
    tercero = models.ForeignKey(Tercero, on_delete=models.PROTECT, blank=True, null=True)
    centro_costo = models.ForeignKey(CentroCosto, on_delete=models.PROTECT, blank=True, null=True)
    
    def __str__(self):
        cuenta_codigo = getattr(self.cuenta, 'codigo', '') if self.cuenta else ''
        return f"{cuenta_codigo} - D: {self.debito} C: {self.credito}"

class CertificadoRetencion(models.Model):
    """Certificados de retención en la fuente"""
    TIPO_CHOICES = [
        ('RENTA', 'Renta'),
        ('ICA', 'ICA'),
        ('IVA', 'IVA'),
        ('OTRO', 'Otro'),
    ]
    
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    numero = models.CharField(max_length=20, unique=True)
    fecha = models.DateField()
    tercero = models.ForeignKey(Tercero, on_delete=models.PROTECT)
    base_gravable = models.DecimalField(max_digits=16, decimal_places=2)
    porcentaje_retencion = models.DecimalField(max_digits=5, decimal_places=2)
    valor_retenido = models.DecimalField(max_digits=16, decimal_places=2)
    concepto = models.CharField(max_length=255)
    asiento = models.ForeignKey(AsientoContable, on_delete=models.CASCADE, blank=True, null=True)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Certificado {self.tipo}-{self.numero} - {self.fecha} - {self.tercero.nombre}"
    
    def calcular_retencion(self):
        """Calcula automáticamente el valor retenido"""
        self.valor_retenido = self.base_gravable * (self.porcentaje_retencion / 100)
        return self.valor_retenido

class MovimientoBancario(models.Model):
    """Movimientos bancarios para conciliación"""
    banco = models.CharField(max_length=100)
    cuenta_bancaria = models.CharField(max_length=50)
    fecha = models.DateField()
    descripcion = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=16, decimal_places=2)
    tipo = models.CharField(max_length=20, choices=[('DEBITO','Débito'),('CREDITO','Crédito')])
    conciliado = models.BooleanField(default=False)
    asiento = models.ForeignKey(AsientoContable, on_delete=models.SET_NULL, null=True, blank=True)
    referencia = models.CharField(max_length=100, blank=True, null=True)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.banco} - {self.fecha} - {self.descripcion} - ${self.valor}"
    
    class Meta:
        ordering = ['-fecha', '-id']

class CierreContable(models.Model):
    """Cierre contable de períodos"""
    periodo = models.ForeignKey(PeriodoContable, on_delete=models.CASCADE)
    fecha_cierre = models.DateTimeField(auto_now_add=True)
    asientos_cierre = models.ManyToManyField(AsientoContable, blank=True)
    cerrado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    observaciones = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Cierre {self.periodo.nombre} - {self.fecha_cierre}"
    
    class Meta:
        ordering = ['-fecha_cierre']

class AuditLog(models.Model):
    """Log de auditoría para cambios en registros contables"""
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    accion = models.CharField(max_length=50, choices=[
        ('CREATE', 'Crear'),
        ('UPDATE', 'Actualizar'),
        ('DELETE', 'Eliminar'),
        ('VIEW', 'Ver'),
    ])
    modelo = models.CharField(max_length=50)
    registro_id = models.IntegerField()
    datos_anteriores = models.JSONField(null=True, blank=True)
    datos_nuevos = models.JSONField(null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.accion} - {self.modelo} - {self.registro_id} - {self.fecha}"
    
    class Meta:
        ordering = ['-fecha']

class Presupuesto(models.Model):
    """Presupuestos por cuenta y centro de costo"""
    TIPO_PRESUPUESTO_CHOICES = [
        ('INGRESO', 'Presupuesto de Ingresos'),
        ('GASTO', 'Presupuesto de Gastos'),
        ('INVERSION', 'Presupuesto de Inversión'),
    ]
    
    periodo = models.ForeignKey(PeriodoContable, on_delete=models.CASCADE)
    cuenta = models.ForeignKey(CuentaContable, on_delete=models.CASCADE)
    centro_costo = models.ForeignKey(CentroCosto, on_delete=models.CASCADE, blank=True, null=True)
    tipo_presupuesto = models.CharField(max_length=20, choices=TIPO_PRESUPUESTO_CHOICES, blank=True, null=True)
    monto_presupuestado = models.DecimalField(max_digits=16, decimal_places=2)
    monto_real = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Presupuesto"
        verbose_name_plural = "Presupuestos"
        unique_together = ['periodo', 'cuenta', 'centro_costo']
        ordering = ['periodo', 'cuenta__codigo']
    
    def __str__(self):
        centro = f" - {self.centro_costo.nombre}" if self.centro_costo else ""
        tipo = f" ({self.get_tipo_presupuesto_display()})" if self.tipo_presupuesto else ""
        return f"{self.cuenta.codigo} - {self.periodo.nombre}{centro}{tipo}"
    
    def variacion_porcentual(self):
        """Calcula la variación porcentual entre presupuesto y real"""
        if self.monto_presupuestado > 0:
            return ((self.monto_real - self.monto_presupuestado) / self.monto_presupuestado) * 100
        return 0
    
    class Meta:
        unique_together = ['periodo', 'cuenta', 'centro_costo']
        ordering = ['periodo', 'cuenta__codigo']

class ReporteFiscal(models.Model):
    """Modelo para almacenar reportes fiscales generados"""
    TIPO_REPORTE = [
        ('IVA', 'Declaración de IVA'),
        ('RETENCION', 'Retenciones en la Fuente'),
        ('ICA', 'Impuesto de Industria y Comercio'),
        ('RENTA', 'Declaración de Renta'),
    ]
    
    tipo = models.CharField(max_length=20, choices=TIPO_REPORTE)
    periodo = models.ForeignKey(PeriodoContable, on_delete=models.CASCADE)
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    base_gravable = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    impuesto_generado = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    impuesto_descontable = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    impuesto_a_pagar = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, choices=[
        ('BORRADOR', 'Borrador'),
        ('GENERADO', 'Generado'),
        ('ENVIADO', 'Enviado'),
        ('APROBADO', 'Aprobado'),
    ], default='BORRADOR')
    observaciones = models.TextField(blank=True)
    generado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Reporte Fiscal'
        verbose_name_plural = 'Reportes Fiscales'
        ordering = ['-fecha_generacion']
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.periodo.nombre} ({self.fecha_inicio} a {self.fecha_fin})"
    
    def calcular_totales(self):
        """Calcula los totales basado en asientos contables"""
        asientos = AsientoContable.objects.filter(
            periodo=self.periodo,
            fecha__gte=self.fecha_inicio,
            fecha__lte=self.fecha_fin
        )
        
        if self.tipo == 'IVA':
            # IVA Generado (ventas)
            iva_generado = LineaAsiento.objects.filter(
                asiento__in=asientos,
                cuenta__codigo__startswith='2368',  # Cuenta de IVA generado
                credito__gt=0
            ).aggregate(total=Sum('credito'))['total'] or 0
            
            # IVA Descontable (compras)
            iva_descontable = LineaAsiento.objects.filter(
                asiento__in=asientos,
                cuenta__codigo__startswith='2368',  # Cuenta de IVA descontable
                debito__gt=0
            ).aggregate(total=Sum('debito'))['total'] or 0
            
            # Base gravable (ventas sin IVA)
            base_gravable = LineaAsiento.objects.filter(
                asiento__in=asientos,
                cuenta__codigo__startswith='41',  # Cuentas de ventas
                credito__gt=0
            ).aggregate(total=Sum('credito'))['total'] or 0
            
            self.base_gravable = base_gravable
            self.impuesto_generado = iva_generado
            self.impuesto_descontable = iva_descontable
            self.impuesto_a_pagar = iva_generado - iva_descontable
            
        elif self.tipo == 'RETENCION':
            # Retenciones en la fuente
            retenciones = LineaAsiento.objects.filter(
                asiento__in=asientos,
                cuenta__codigo__startswith='2368',  # Cuenta de retenciones
                debito__gt=0
            ).aggregate(total=Sum('debito'))['total'] or 0
            
            self.impuesto_a_pagar = retenciones
            
        self.save()
        return self

class DetalleFiscal(models.Model):
    """Detalle de movimientos fiscales"""
    reporte = models.ForeignKey(ReporteFiscal, on_delete=models.CASCADE, related_name='detalles')
    fecha = models.DateField()
    tercero = models.ForeignKey(Tercero, on_delete=models.CASCADE)
    concepto = models.CharField(max_length=200)
    base_gravable = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    porcentaje_impuesto = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    valor_impuesto = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    asiento = models.ForeignKey(AsientoContable, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Detalle Fiscal'
        verbose_name_plural = 'Detalles Fiscales'
    
    def __str__(self):
        return f"{self.reporte.tipo} - {self.tercero.nombre} - {self.fecha}"
