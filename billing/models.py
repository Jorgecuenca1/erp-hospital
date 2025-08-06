from django.db import models
from patients.models import Paciente
from inventories.models import Producto # Usaremos productos del inventario

class Factura(models.Model):
    ESTADO_FACTURA_CHOICES = [
        ('BORRADOR', 'Borrador'),
        ('EMITIDA', 'Emitida'),
        ('VALIDADA_DIAN', 'Validada por DIAN'),
        ('ANULADA', 'Anulada'),
        ('PAGADA', 'Pagada'),
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT, related_name='facturas')
    fecha_emision = models.DateTimeField(auto_now_add=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    numero_factura = models.CharField(max_length=50, unique=True, blank=True, null=True)
    total_bruto = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_impuestos = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_neto = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, choices=ESTADO_FACTURA_CHOICES, default='BORRADOR')
    # Campos específicos DIAN
    cufe = models.CharField(max_length=100, unique=True, blank=True, null=True, help_text="Código Único de Factura Electrónica")
    uuid = models.CharField(max_length=100, unique=True, blank=True, null=True, help_text="Universal Unique Identifier para facturación electrónica")
    xml_dian = models.FileField(upload_to='facturas_xml/', blank=True, null=True, help_text="XML de la factura enviado a la DIAN")
    pdf_factura = models.FileField(upload_to='facturas_pdf/', blank=True, null=True, help_text="PDF de la representación gráfica de la factura")
    qr_code = models.ImageField(upload_to='facturas_qr/', blank=True, null=True)

    def __str__(self):
        return f"Factura #{self.numero_factura or 'BORRADOR'} - {self.paciente.nombres} {self.paciente.apellidos}"

class DetalleFactura(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='detalles_factura', null=True, blank=True)
    descripcion = models.TextField(help_text="Descripción del ítem facturado, si no es un producto del inventario.", blank=True, null=True)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    impuesto_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    valor_impuesto = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_linea = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = 'Detalle de Factura'
        verbose_name_plural = 'Detalles de Factura'

    def __str__(self):
        return f"Item de Factura {self.factura.id}: {self.descripcion or self.producto.nombre}"

class TransaccionDIAN(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='transacciones_dian')
    fecha_transaccion = models.DateTimeField(auto_now_add=True)
    tipo_transaccion = models.CharField(max_length=50, help_text="Ej: SendBillAsync, GetStatusCufe")
    request_payload = models.TextField(blank=True, null=True)
    response_payload = models.TextField(blank=True, null=True)
    estado_respuesta = models.CharField(max_length=50, blank=True, null=True, help_text="Ej: Aceptado, Rechazado, Pendiente")
    mensaje_error = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Transacción DIAN'
        verbose_name_plural = 'Transacciones DIAN'

    def __str__(self):
        return f"Transacción DIAN para Factura {self.factura.numero_factura or self.factura.id} - {self.tipo_transaccion}"
