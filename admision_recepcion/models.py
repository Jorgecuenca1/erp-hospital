from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from decimal import Decimal
import uuid


class Municipio(models.Model):
    """Municipios"""
    codigo = models.CharField(max_length=10, unique=True, verbose_name="Código")
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    departamento = models.CharField(max_length=50, verbose_name="Departamento")
    pais = models.CharField(max_length=50, default="COLOMBIA", verbose_name="País")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    
    class Meta:
        verbose_name = "Municipio"
        verbose_name_plural = "Municipios"
        ordering = ['departamento', 'nombre']
    
    def __str__(self):
        return f"{self.nombre} ({self.departamento}, {self.pais})"


class Empresa(models.Model):
    """Empresas para convenios y contratos"""
    TIPO_EMPRESA_CHOICES = [
        ('EPS', 'EPS'),
        ('ARL', 'ARL'),
        ('AFP', 'AFP'),
        ('EMPRESA', 'Empresa'),
        ('COOPERATIVA', 'Cooperativa'),
        ('FUNDACION', 'Fundación'),
        ('OTRO', 'Otro'),
    ]
    
    nit = models.CharField(max_length=20, unique=True, verbose_name="NIT")
    razon_social = models.CharField(max_length=200, verbose_name="Razón Social")
    nombre_comercial = models.CharField(max_length=200, blank=True, verbose_name="Nombre Comercial")
    tipo_empresa = models.CharField(max_length=20, choices=TIPO_EMPRESA_CHOICES, default='EMPRESA', verbose_name="Tipo de Empresa")
    
    direccion = models.TextField(verbose_name="Dirección")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    email = models.EmailField(verbose_name="Correo Electrónico")
    contacto_principal = models.CharField(max_length=100, blank=True, verbose_name="Contacto Principal")
    
    activo = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ['razon_social']
    
    def __str__(self):
        return self.razon_social


class Convenio(models.Model):
    """Convenios y contratos comerciales"""
    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
        ('SUSPENDIDO', 'Suspendido'),
        ('VENCIDO', 'Vencido'),
    ]
    
    codigo = models.CharField(max_length=50, unique=True, verbose_name="Código")
    nombre = models.CharField(max_length=200, verbose_name="Nombre del Convenio")
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='convenios', verbose_name="Empresa")
    
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio")
    fecha_fin = models.DateField(verbose_name="Fecha de Fin")
    valor_contrato = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name="Valor del Contrato")
    
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='ACTIVO', verbose_name="Estado")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Convenio"
        verbose_name_plural = "Convenios"
        ordering = ['-fecha_inicio']
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class Servicio(models.Model):
    """Servicios y productos médicos"""
    TIPO_CHOICES = [
        ('CONSULTA', 'Consulta'),
        ('EXAMEN', 'Examen'),
        ('PROCEDIMIENTO', 'Procedimiento'),
        ('CIRUGIA', 'Cirugía'),
        ('TERAPIA', 'Terapia'),
        ('MEDICAMENTO', 'Medicamento'),
        ('MATERIAL', 'Material'),
        ('OTRO', 'Otro'),
    ]
    
    codigo = models.CharField(max_length=50, unique=True, verbose_name="Código")
    nombre = models.CharField(max_length=200, verbose_name="Nombre del Servicio")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='CONSULTA', verbose_name="Tipo")
    
    valor_base = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Valor Base")
    requiere_autorizacion = models.BooleanField(default=False, verbose_name="Requiere Autorización")
    
    activo = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class Prestador(models.Model):
    """Prestadores de servicios (doctores, laboratorios, etc.)"""
    codigo = models.CharField(max_length=50, unique=True, verbose_name="Código")
    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    tipo = models.CharField(max_length=50, default='MEDICO', verbose_name="Tipo")
    especialidad = models.CharField(max_length=100, blank=True, verbose_name="Especialidad")
    
    telefono = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    email = models.EmailField(blank=True, verbose_name="Email")
    
    activo = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Prestador"
        verbose_name_plural = "Prestadores"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class OrdenServicio(models.Model):
    """Orden de Servicios principal"""
    TIPO_DOC_CHOICES = [
        ('CC', 'Cédula de Ciudadanía'),
        ('TI', 'Tarjeta de Identidad'),
        ('CE', 'Cédula de Extranjería'),
        ('PA', 'Pasaporte'),
        ('RC', 'Registro Civil'),
        ('MS', 'Menor sin Identificación'),
        ('AS', 'Adulto sin Identificación'),
    ]
    
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]
    
    ESTADO_CIVIL_CHOICES = [
        ('SOLTERO', 'Soltero'),
        ('CASADO', 'Casado'),
        ('UNION_LIBRE', 'Unión Libre'),
        ('DIVORCIADO', 'Divorciado'),
        ('VIUDO', 'Viudo'),
        ('OTRO', 'Otro'),
    ]
    
    NIVEL_EDUCATIVO_CHOICES = [
        ('NINGUNO', 'Ninguno'),
        ('PRIMARIA', 'Primaria'),
        ('SECUNDARIA', 'Secundaria'),
        ('TECNICO', 'Técnico'),
        ('TECNOLOGO', 'Tecnólogo'),
        ('PROFESIONAL', 'Profesional'),
        ('ESPECIALIZACION', 'Especialización'),
        ('MAESTRIA', 'Maestría'),
        ('DOCTORADO', 'Doctorado'),
    ]
    
    ZONA_CHOICES = [
        ('URBANA', 'Urbana'),
        ('RURAL', 'Rural'),
    ]
    
    ESTRATO_CHOICES = [
        ('1', 'Estrato 1'),
        ('2', 'Estrato 2'),
        ('3', 'Estrato 3'),
        ('4', 'Estrato 4'),
        ('5', 'Estrato 5'),
        ('6', 'Estrato 6'),
    ]
    
    SEDE_CHOICES = [
        ('PRINCIPAL', 'Principal'),
        ('SUCURSAL_1', 'Sucursal 1'),
        ('SUCURSAL_2', 'Sucursal 2'),
        ('CONSULTORIO_EXTERNO', 'Consultorio Externo'),
    ]
    
    ESTADO_ORDEN_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('AUTORIZADA', 'Autorizada'),
        ('EN_PROCESO', 'En Proceso'),
        ('COMPLETADA', 'Completada'),
        ('CANCELADA', 'Cancelada'),
        ('FACTURADA', 'Facturada'),
    ]
    
    # Identificación de la orden
    numero_orden = models.CharField(max_length=20, unique=True, blank=True, verbose_name="N°. O.S.")
    fecha_orden = models.DateField(default=timezone.now, verbose_name="Fecha")
    estado_orden = models.CharField(max_length=20, choices=ESTADO_ORDEN_CHOICES, default='PENDIENTE', verbose_name="Estado")
    
    # Datos Personales
    tipo_documento = models.CharField(max_length=10, choices=TIPO_DOC_CHOICES, default='CC', verbose_name="Tipo")
    numero_identificacion = models.CharField(max_length=20, verbose_name="N°. de Identificación")
    ciudad_nacimiento = models.CharField(max_length=100, blank=True, verbose_name="Ciudad de Nacimiento")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento")
    
    primer_apellido = models.CharField(max_length=50, verbose_name="Primer Apellido")
    segundo_apellido = models.CharField(max_length=50, blank=True, verbose_name="Segundo Apellido")
    primer_nombre = models.CharField(max_length=50, verbose_name="Primer Nombre")
    otros_nombres = models.CharField(max_length=100, blank=True, verbose_name="Otros Nombres")
    
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES, verbose_name="Género")
    estado_civil = models.CharField(max_length=20, choices=ESTADO_CIVIL_CHOICES, verbose_name="Estado Civil")
    nivel_educativo = models.CharField(max_length=20, choices=NIVEL_EDUCATIVO_CHOICES, verbose_name="Nivel Educativo")
    correo_electronico = models.EmailField(blank=True, verbose_name="Correo Electrónico")
    
    # Archivos adjuntos
    foto = models.ImageField(upload_to='ordenes/fotos/', blank=True, null=True, verbose_name="Foto")
    huella = models.ImageField(upload_to='ordenes/huellas/', blank=True, null=True, verbose_name="Huella")
    firma = models.ImageField(upload_to='ordenes/firmas/', blank=True, null=True, verbose_name="Firma")
    
    # Datos de Ubicación
    zona = models.CharField(max_length=10, choices=ZONA_CHOICES, default='URBANA', verbose_name="Zona")
    direccion = models.TextField(verbose_name="Dirección")
    barrio = models.CharField(max_length=100, blank=True, verbose_name="Barrio")
    localidad = models.CharField(max_length=100, blank=True, verbose_name="Localidad")
    sede = models.CharField(max_length=50, choices=SEDE_CHOICES, default='PRINCIPAL', verbose_name="Sede")
    estrato = models.CharField(max_length=1, choices=ESTRATO_CHOICES, verbose_name="Estrato")
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE, verbose_name="Municipio")
    
    celulares = models.CharField(max_length=50, blank=True, verbose_name="Celulares")
    telefonos = models.CharField(max_length=50, blank=True, verbose_name="Teléfonos")
    
    # Datos de Trabajo
    profesion_cargo = models.CharField(max_length=100, verbose_name="Profesión o Cargo")
    funciones_cargo = models.TextField(blank=True, verbose_name="Funciones del Cargo")
    tipo_evaluacion = models.CharField(max_length=200, verbose_name="Tipo de Evaluación Médica o Procedimiento")
    
    # Información comercial
    convenio = models.ForeignKey(Convenio, on_delete=models.CASCADE, verbose_name="Acuerdo Comercial, Contrato o Convenio")
    empresa_mision = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='ordenes_mision', verbose_name="Empresa en Misión")
    
    # Seguros
    eps = models.CharField(max_length=100, blank=True, verbose_name="EPS")
    afp = models.CharField(max_length=100, blank=True, verbose_name="AFP")
    arl = models.CharField(max_length=100, blank=True, verbose_name="ARL")
    
    # Observaciones
    observaciones = models.TextField(blank=True, verbose_name="Observaciones, N° de Autorización o Solicitud")
    fecha_solicitud = models.DateField(verbose_name="Fecha de Solicitud")
    
    # Totales
    total_orden = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Total de la Orden Servicios")
    total_pagar = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Total a Pagar")
    
    # Auditoría
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='ordenes_creadas')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Orden de Servicio"
        verbose_name_plural = "Órdenes de Servicios"
        ordering = ['-fecha_orden', '-numero_orden']
    
    def save(self, *args, **kwargs):
        if not self.numero_orden:
            # Generar número de orden automático
            today = timezone.now()
            prefix = f"OS{today.strftime('%Y%m%d')}"
            last_order = OrdenServicio.objects.filter(
                numero_orden__startswith=prefix
            ).order_by('-numero_orden').first()
            
            if last_order:
                last_number = int(last_order.numero_orden[-4:])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.numero_orden = f"{prefix}{new_number:04d}"
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"OS {self.numero_orden} - {self.primer_nombre} {self.primer_apellido}"
    
    @property
    def nombre_completo(self):
        nombres = [self.primer_nombre]
        if self.otros_nombres:
            nombres.append(self.otros_nombres)
        
        apellidos = [self.primer_apellido]
        if self.segundo_apellido:
            apellidos.append(self.segundo_apellido)
        
        return f"{' '.join(nombres)} {' '.join(apellidos)}"
    
    def calcular_totales(self):
        """Calcular totales de la orden"""
        detalles = self.detalles.all()
        self.total_orden = sum(detalle.valor_total for detalle in detalles)
        self.total_pagar = self.total_orden  # Puede incluir descuentos en el futuro
        self.save()


class DetalleOrdenServicio(models.Model):
    """Detalle de servicios en la orden"""
    FORMA_PAGO_CHOICES = [
        ('CONTADO', 'Contado'),
        ('CREDITO', 'Crédito'),
        ('CONVENIO', 'Convenio'),
        ('SEGURO', 'Seguro'),
        ('MIXTO', 'Mixto'),
    ]
    
    orden = models.ForeignKey(OrdenServicio, on_delete=models.CASCADE, related_name='detalles', verbose_name="Orden")
    cantidad = models.PositiveIntegerField(default=1, verbose_name="Cantidad")
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, verbose_name="Producto o Servicio")
    prestador = models.ForeignKey(Prestador, on_delete=models.CASCADE, verbose_name="Prestador del Servicio")
    
    valor_unitario = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Vr. Unitario")
    forma_pago = models.CharField(max_length=20, choices=FORMA_PAGO_CHOICES, default='CONTADO', verbose_name="Forma de Pago")
    valor_pagar = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Vr. Pagar")
    
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    autorizado = models.BooleanField(default=False, verbose_name="Autorizado")
    numero_autorizacion = models.CharField(max_length=50, blank=True, verbose_name="N° Autorización")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Detalle de Orden de Servicio"
        verbose_name_plural = "Detalles de Órdenes de Servicios"
        ordering = ['id']
    
    def __str__(self):
        return f"{self.servicio.nombre} - {self.cantidad} x {self.valor_unitario}"
    
    @property
    def valor_total(self):
        return Decimal(self.cantidad) * self.valor_unitario
    
    def save(self, *args, **kwargs):
        # Si valor_pagar no está establecido, usar valor_total
        if not self.valor_pagar:
            self.valor_pagar = self.valor_total
        
        super().save(*args, **kwargs)
        
        # Actualizar totales de la orden
        self.orden.calcular_totales()


class SeguimientoPaciente(models.Model):
    """Seguimiento a pacientes"""
    ESTADO_CHOICES = [
        ('INGRESADO', 'Ingresado'),
        ('EN_ESPERA', 'En Espera'),
        ('EN_ATENCION', 'En Atención'),
        ('ATENDIDO', 'Atendido'),
        ('ALTA', 'Alta'),
        ('REMITIDO', 'Remitido'),
        ('CANCELADO', 'Cancelado'),
    ]
    
    orden = models.ForeignKey(OrdenServicio, on_delete=models.CASCADE, related_name='seguimientos')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='INGRESADO')
    fecha_estado = models.DateTimeField(default=timezone.now)
    observaciones = models.TextField(blank=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = "Seguimiento de Paciente"
        verbose_name_plural = "Seguimientos de Pacientes"
        ordering = ['-fecha_estado']
    
    def __str__(self):
        return f"{self.orden.numero_orden} - {self.estado}"


class CitaEmpresarial(models.Model):
    """Citas programadas desde el portal de empresas"""
    ESTADO_CITA_CHOICES = [
        ('PROGRAMADA', 'Programada'),
        ('CONFIRMADA', 'Confirmada'),
        ('CANCELADA', 'Cancelada'),
        ('REPROGRAMADA', 'Reprogramada'),
        ('COMPLETADA', 'Completada'),
        ('NO_ASISTIO', 'No Asistió'),
    ]
    
    TIPO_SERVICIO_CHOICES = [
        ('EXAMEN_INGRESO', 'Examen de Ingreso'),
        ('EXAMEN_PERIODICO', 'Examen Periódico'),
        ('EXAMEN_RETIRO', 'Examen de Retiro'),
        ('EXAMEN_REINTEGRO', 'Examen de Reintegro'),
        ('CONSULTA_MEDICINA', 'Consulta Medicina General'),
        ('EXAMEN_ALTURA', 'Examen Trabajo en Alturas'),
        ('EXAMEN_ESPACIOS', 'Examen Espacios Confinados'),
        ('AUDIOMETRIA', 'Audiometría'),
        ('VISIOMETRIA', 'Visiometría'),
        ('LABORATORIO', 'Laboratorio Clínico'),
        ('ELECTROCARDIOGRAMA', 'Electrocardiograma'),
        ('RADIOGRAFIA', 'Radiografía'),
    ]
    
    # Identificación de la cita
    numero_cita = models.CharField(max_length=20, unique=True, blank=True, verbose_name="N° Cita")
    fecha_cita = models.DateField(verbose_name="Día de la Cita")
    hora_cita = models.TimeField(verbose_name="Hora de la Cita")
    estado = models.CharField(max_length=20, choices=ESTADO_CITA_CHOICES, default='PROGRAMADA', verbose_name="Estado")
    
    # Información del trabajador
    numero_identificacion = models.CharField(max_length=20, verbose_name="N°. de Identificación")
    tipo_documento = models.CharField(max_length=10, choices=OrdenServicio.TIPO_DOC_CHOICES, default='CC', verbose_name="Tipo Documento")
    nombre_trabajador = models.CharField(max_length=200, verbose_name="Nombre del Trabajador")
    telefono_trabajador = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    email_trabajador = models.EmailField(blank=True, verbose_name="Email Trabajador")
    
    # Información de la empresa
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='citas_portal', verbose_name="Empresa")
    contacto_empresa = models.CharField(max_length=100, blank=True, verbose_name="Contacto en la Empresa")
    telefono_empresa = models.CharField(max_length=20, blank=True, verbose_name="Teléfono Empresa")
    email_empresa = models.EmailField(blank=True, verbose_name="Email Empresa")
    
    # Información del servicio
    tipo_servicio = models.CharField(max_length=30, choices=TIPO_SERVICIO_CHOICES, verbose_name="Tipo de Servicio")
    servicios_adicionales = models.ManyToManyField(Servicio, blank=True, verbose_name="Servicios Adicionales")
    observaciones_servicio = models.TextField(blank=True, verbose_name="Observaciones del Servicio")
    
    # Información de la cita
    sede_cita = models.CharField(max_length=50, choices=OrdenServicio.SEDE_CHOICES, default='PRINCIPAL', verbose_name="Sede de la Cita")
    prestador_asignado = models.ForeignKey(Prestador, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Prestador Asignado")
    
    # Información de programación
    fecha_programacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Programación")
    programada_por_portal = models.BooleanField(default=True, verbose_name="Programada por Portal")
    ip_origen = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP de Origen")
    
    # Confirmación y cancelación
    fecha_confirmacion = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Confirmación")
    confirmada_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='citas_confirmadas', verbose_name="Confirmada Por")
    
    fecha_cancelacion = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Cancelación")
    motivo_cancelacion = models.TextField(blank=True, verbose_name="Motivo de Cancelación")
    cancelada_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='citas_canceladas', verbose_name="Cancelada Por")
    
    # Relación con orden de servicio (si se convierte en orden)
    orden_servicio = models.OneToOneField(OrdenServicio, on_delete=models.SET_NULL, null=True, blank=True, related_name='cita_empresarial', verbose_name="Orden de Servicio")
    
    # Información adicional
    requiere_autorizacion = models.BooleanField(default=False, verbose_name="Requiere Autorización")
    numero_autorizacion = models.CharField(max_length=50, blank=True, verbose_name="N° Autorización")
    valor_estimado = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Valor Estimado")
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Cita Empresarial"
        verbose_name_plural = "Citas Empresariales"
        ordering = ['-fecha_cita', '-hora_cita']
        indexes = [
            models.Index(fields=['fecha_cita', 'estado']),
            models.Index(fields=['numero_identificacion']),
            models.Index(fields=['empresa', 'fecha_cita']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.numero_cita:
            # Generar número de cita automático
            today = timezone.now()
            prefix = f"CE{today.strftime('%Y%m%d')}"
            last_cita = CitaEmpresarial.objects.filter(
                numero_cita__startswith=prefix
            ).order_by('-numero_cita').first()
            
            if last_cita:
                last_number = int(last_cita.numero_cita[-4:])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.numero_cita = f"{prefix}{new_number:04d}"
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.numero_cita} - {self.nombre_trabajador} ({self.empresa.razon_social})"
    
    def confirmar_cita(self, usuario=None):
        """Confirmar la cita"""
        self.estado = 'CONFIRMADA'
        self.fecha_confirmacion = timezone.now()
        self.confirmada_por = usuario
        self.save()
    
    def cancelar_cita(self, motivo="", usuario=None):
        """Cancelar la cita"""
        self.estado = 'CANCELADA'
        self.fecha_cancelacion = timezone.now()
        self.motivo_cancelacion = motivo
        self.cancelada_por = usuario
        self.save()
    
    def crear_orden_servicio(self, usuario=None):
        """Convertir la cita en una orden de servicio"""
        if self.orden_servicio:
            return self.orden_servicio
        
        # Crear la orden de servicio basada en la cita
        orden_data = {
            'tipo_documento': self.tipo_documento,
            'numero_identificacion': self.numero_identificacion,
            'primer_nombre': self.nombre_trabajador.split()[0],
            'primer_apellido': self.nombre_trabajador.split()[-1] if len(self.nombre_trabajador.split()) > 1 else '',
            'genero': 'M',  # Valor por defecto, se puede actualizar manualmente
            'fecha_nacimiento': timezone.now().date() - timezone.timedelta(days=365*30),  # Estimado
            'correo_electronico': self.email_trabajador,
            'zona': 'URBANA',
            'direccion': 'Por confirmar',
            'sede': self.sede_cita,
            'estrato': '3',
            'municipio': Municipio.objects.first(),  # Primer municipio disponible
            'celulares': self.telefono_trabajador,
            'profesion_cargo': 'Trabajador',
            'tipo_evaluacion': self.get_tipo_servicio_display(),
            'empresa_mision': self.empresa,
            'convenio': Convenio.objects.filter(empresa=self.empresa).first(),
            'observaciones': f"Orden generada desde cita empresarial {self.numero_cita}. {self.observaciones_servicio}",
            'fecha_solicitud': self.fecha_cita,
            'created_by': usuario
        }
        
        orden = OrdenServicio.objects.create(**orden_data)
        self.orden_servicio = orden
        self.save()
        
        return orden
    
    @property
    def puede_confirmar(self):
        """Verificar si la cita puede ser confirmada"""
        return self.estado == 'PROGRAMADA'
    
    @property
    def puede_cancelar(self):
        """Verificar si la cita puede ser cancelada"""
        return self.estado in ['PROGRAMADA', 'CONFIRMADA']
    
    @property
    def esta_vencida(self):
        """Verificar si la cita está vencida"""
        from datetime import datetime, time
        ahora = timezone.now()
        fecha_hora_cita = timezone.make_aware(
            datetime.combine(self.fecha_cita, self.hora_cita)
        )
        return ahora > fecha_hora_cita and self.estado in ['PROGRAMADA', 'CONFIRMADA']


class ListaPrecios(models.Model):
    """Lista de precios de productos y servicios médicos"""
    
    TIPO_RIPS_CHOICES = [
        ('CONSULTA', 'Consulta'),
        ('PROCEDIMIENTO', 'Procedimiento'),
        ('OTROS_SERVICIOS', 'Otros Servicios'),
        ('MEDICAMENTOS', 'Medicamentos'),
        ('HOSPITALIZACION', 'Hospitalización'),
        ('URGENCIAS', 'Urgencias'),
        ('', 'Sin Clasificar'),
    ]
    
    CATEGORIA_CHOICES = [
        ('LABORATORIO', 'Laboratorio Clínico'),
        ('IMAGENES', 'Imágenes Diagnósticas'),
        ('CONSULTAS', 'Consultas Médicas'),
        ('PROCEDIMIENTOS', 'Procedimientos'),
        ('MEDICAMENTOS', 'Medicamentos'),
        ('EXAMENES_OCUPACIONALES', 'Exámenes Ocupacionales'),
        ('OTROS', 'Otros Servicios'),
        ('ADMINISTRATIVOS', 'Servicios Administrativos'),
    ]
    
    # Información básica del producto/servicio
    codigo_interno = models.CharField(max_length=20, unique=True, blank=True, verbose_name="Código Interno")
    nombre_producto_servicio = models.CharField(max_length=500, verbose_name="Nombre del Producto o Servicio")
    descripcion = models.TextField(blank=True, verbose_name="Descripción Detallada")
    categoria = models.CharField(max_length=30, choices=CATEGORIA_CHOICES, default='OTROS', verbose_name="Categoría")
    
    # Precios
    precio = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Precio")
    precio_convenio = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name="Precio Convenio")
    precio_particular = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name="Precio Particular")
    
    # Códigos para RIPS y facturación
    codigo_cups = models.CharField(max_length=20, blank=True, verbose_name="CUPS", help_text="Código CUPS para RIPS")
    codigo_soat = models.CharField(max_length=20, blank=True, verbose_name="Código SOAT")
    codigo_iss = models.CharField(max_length=20, blank=True, verbose_name="Código ISS")
    codigo_cum = models.CharField(max_length=20, blank=True, verbose_name="Código CUM", help_text="Para medicamentos")
    codigo_cie10 = models.CharField(max_length=10, blank=True, verbose_name="CIE-10", help_text="Código diagnóstico asociado")
    
    # Información para RIPS
    tipo_rips = models.CharField(max_length=20, choices=TIPO_RIPS_CHOICES, blank=True, verbose_name="Tipo RIPS")
    generar_rips = models.BooleanField(default=True, verbose_name="Generar RIPS")
    
    # Impuestos
    porcentaje_iva = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="IVA (%)")
    gravado_iva = models.BooleanField(default=False, verbose_name="Gravado con IVA")
    
    # Convenios asociados
    convenios = models.ManyToManyField(Convenio, blank=True, verbose_name="Convenios")
    precio_por_convenio = models.JSONField(default=dict, blank=True, verbose_name="Precios por Convenio")
    
    # Control de estado
    activo = models.BooleanField(default=True, verbose_name="Activo")
    requiere_autorizacion = models.BooleanField(default=False, verbose_name="Requiere Autorización")
    ambulatorio = models.BooleanField(default=True, verbose_name="Ambulatorio")
    hospitalario = models.BooleanField(default=False, verbose_name="Hospitalario")
    
    # Información adicional
    unidad_medida = models.CharField(max_length=50, default='Unidad', verbose_name="Unidad de Medida")
    tiempo_estimado = models.PositiveIntegerField(null=True, blank=True, verbose_name="Tiempo Estimado (min)")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Creado Por")
    
    class Meta:
        verbose_name = "Lista de Precios"
        verbose_name_plural = "Listas de Precios"
        ordering = ['categoria', 'nombre_producto_servicio']
        indexes = [
            models.Index(fields=['codigo_cups']),
            models.Index(fields=['codigo_cum']),
            models.Index(fields=['categoria', 'activo']),
            models.Index(fields=['nombre_producto_servicio']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.codigo_interno:
            # Generar código interno automático
            prefix = self.categoria[:3].upper()
            last_item = ListaPrecios.objects.filter(
                codigo_interno__startswith=prefix
            ).order_by('-codigo_interno').first()
            
            if last_item and len(last_item.codigo_interno) >= 6:
                try:
                    last_number = int(last_item.codigo_interno[-4:])
                    new_number = last_number + 1
                except ValueError:
                    new_number = 1
            else:
                new_number = 1
            
            self.codigo_interno = f"{prefix}{new_number:04d}"
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        precio_formatted = f"${self.precio:,.0f}"
        return f"{self.nombre_producto_servicio} - {precio_formatted}"
    
    def get_precio_para_convenio(self, convenio_id):
        """Obtener precio específico para un convenio"""
        if convenio_id and str(convenio_id) in self.precio_por_convenio:
            return self.precio_por_convenio[str(convenio_id)]
        return self.precio_convenio or self.precio
    
    def get_precio_formatted(self):
        """Precio formateado para mostrar"""
        return f"${self.precio:,.0f}"
    
    def get_iva_valor(self):
        """Calcular valor del IVA"""
        if self.gravado_iva:
            return self.precio * (self.porcentaje_iva / 100)
        return 0
    
    def get_precio_con_iva(self):
        """Precio incluyendo IVA"""
        return self.precio + self.get_iva_valor()
    
    @property
    def es_medicamento(self):
        """Verificar si es un medicamento"""
        return bool(self.codigo_cum) or self.categoria == 'MEDICAMENTOS'
    
    @property
    def es_procedimiento(self):
        """Verificar si es un procedimiento"""
        return bool(self.codigo_cups) and self.tipo_rips in ['PROCEDIMIENTO', 'CONSULTA']
    
    @property
    def requiere_rips(self):
        """Verificar si requiere generar RIPS"""
        return self.generar_rips and self.tipo_rips and self.activo


class HistoriaClinica(models.Model):
    """Historia clínica de pacientes"""
    
    ESTADO_CHOICES = [
        ('ABIERTA', 'Abierta'),
        ('CERRADA', 'Cerrada'),
        ('ANULADA', 'Anulada'),
        ('EN_PROCESO', 'En Proceso'),
    ]
    
    TIPO_EXAMEN_CHOICES = [
        ('EVALUACION_MEDICO_OCUPACIONAL_INGRESO', 'Evaluación Médico Ocupacional de Ingreso'),
        ('EVALUACION_MEDICO_OCUPACIONAL_PERIODICO', 'Evaluación Médico Ocupacional Periódico'),
        ('EVALUACION_MEDICO_OCUPACIONAL_RETIRO', 'Evaluación Médico Ocupacional de Retiro'),
        ('EVALUACION_MEDICO_OCUPACIONAL_REINTEGRO', 'Evaluación Médico Ocupacional de Reintegro'),
        ('CONSULTA_MEDICINA_GENERAL', 'Consulta Medicina General'),
        ('CONSULTA_MEDICINA_ESPECIALIZADA', 'Consulta Medicina Especializada'),
        ('EXAMEN_TRABAJO_ALTURAS', 'Examen Trabajo en Alturas'),
        ('EXAMEN_ESPACIOS_CONFINADOS', 'Examen Espacios Confinados'),
        ('AUDIOMETRIA', 'Audiometría'),
        ('VISIOMETRIA', 'Visiometría'),
        ('OPTOMETRIA', 'Optometría'),
        ('PSICOLOGIA_OCUPACIONAL', 'Psicología Ocupacional'),
        ('OTROS', 'Otros Exámenes'),
    ]
    
    # Identificación de la historia clínica
    numero_hc = models.CharField(max_length=20, unique=True, verbose_name="N° H.C.")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha Creación")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='ABIERTA', verbose_name="Estado")
    
    # Información del paciente
    numero_identificacion = models.CharField(max_length=20, verbose_name="N°. Identificación")
    tipo_documento = models.CharField(max_length=10, choices=OrdenServicio.TIPO_DOC_CHOICES, default='CC', verbose_name="Tipo Documento")
    nombre_paciente = models.CharField(max_length=200, verbose_name="Nombre del Paciente")
    fecha_nacimiento = models.DateField(null=True, blank=True, verbose_name="Fecha de Nacimiento")
    genero = models.CharField(max_length=1, choices=OrdenServicio.GENERO_CHOICES, verbose_name="Género")
    telefono = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    email = models.EmailField(blank=True, verbose_name="Email")
    direccion = models.TextField(blank=True, verbose_name="Dirección")
    
    # Información de la empresa (si aplica)
    empresa = models.ForeignKey(Empresa, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Empresa")
    cargo = models.CharField(max_length=100, blank=True, verbose_name="Cargo")
    
    # Información del examen
    tipo_examen = models.CharField(max_length=50, choices=TIPO_EXAMEN_CHOICES, verbose_name="Tipo de Examen")
    profesional = models.ForeignKey(Prestador, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Profesional")
    
    # Relación con orden de servicio
    orden_servicio = models.OneToOneField(OrdenServicio, on_delete=models.SET_NULL, null=True, blank=True, related_name='historia_clinica', verbose_name="Orden de Servicio")
    
    # Información médica
    motivo_consulta = models.TextField(blank=True, verbose_name="Motivo de Consulta")
    antecedentes_personales = models.TextField(blank=True, verbose_name="Antecedentes Personales")
    antecedentes_familiares = models.TextField(blank=True, verbose_name="Antecedentes Familiares")
    antecedentes_ocupacionales = models.TextField(blank=True, verbose_name="Antecedentes Ocupacionales")
    revision_sistemas = models.TextField(blank=True, verbose_name="Revisión por Sistemas")
    
    # Examen físico
    signos_vitales = models.JSONField(default=dict, blank=True, verbose_name="Signos Vitales")
    examen_fisico = models.TextField(blank=True, verbose_name="Examen Físico")
    
    # Resultados de exámenes
    laboratorios = models.TextField(blank=True, verbose_name="Resultados de Laboratorio")
    imagenes = models.TextField(blank=True, verbose_name="Resultados de Imágenes")
    otros_examenes = models.TextField(blank=True, verbose_name="Otros Exámenes")
    
    # Diagnósticos
    diagnostico_principal = models.CharField(max_length=10, blank=True, verbose_name="Diagnóstico Principal (CIE-10)")
    diagnosticos_secundarios = models.TextField(blank=True, verbose_name="Diagnósticos Secundarios")
    aptitud_laboral = models.CharField(max_length=50, blank=True, verbose_name="Aptitud Laboral")
    
    # Recomendaciones y tratamiento
    recomendaciones = models.TextField(blank=True, verbose_name="Recomendaciones")
    tratamiento = models.TextField(blank=True, verbose_name="Tratamiento")
    incapacidad_dias = models.PositiveIntegerField(null=True, blank=True, verbose_name="Días de Incapacidad")
    restricciones = models.TextField(blank=True, verbose_name="Restricciones Laborales")
    
    # Control de estado
    fecha_cierre = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Cierre")
    cerrada_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='historias_cerradas', verbose_name="Cerrada Por")
    motivo_anulacion = models.TextField(blank=True, verbose_name="Motivo de Anulación")
    anulada_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='historias_anuladas', verbose_name="Anulada Por")
    fecha_anulacion = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Anulación")
    
    # Auditoría
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='historias_creadas', verbose_name="Creado Por")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Historia Clínica"
        verbose_name_plural = "Historias Clínicas"
        ordering = ['-numero_hc']
        indexes = [
            models.Index(fields=['numero_identificacion']),
            models.Index(fields=['empresa', 'fecha_creacion']),
            models.Index(fields=['estado', 'fecha_creacion']),
            models.Index(fields=['profesional', 'fecha_creacion']),
            models.Index(fields=['tipo_examen']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.numero_hc:
            # Generar número de historia clínica automático
            from datetime import datetime
            year = datetime.now().year
            last_hc = HistoriaClinica.objects.filter(
                numero_hc__startswith=str(year)
            ).order_by('-numero_hc').first()
            
            if last_hc:
                try:
                    last_number = int(last_hc.numero_hc[-4:])
                    new_number = last_number + 1
                except ValueError:
                    new_number = 1
            else:
                new_number = 1
            
            self.numero_hc = f"{year}{new_number:04d}"
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"H.C. {self.numero_hc} - {self.nombre_paciente}"
    
    def cerrar_historia(self, usuario=None):
        """Cerrar la historia clínica"""
        self.estado = 'CERRADA'
        self.fecha_cierre = timezone.now()
        self.cerrada_por = usuario
        self.save()
    
    def anular_historia(self, motivo="", usuario=None):
        """Anular la historia clínica"""
        self.estado = 'ANULADA'
        self.motivo_anulacion = motivo
        self.fecha_anulacion = timezone.now()
        self.anulada_por = usuario
        self.save()
    
    def reabrir_historia(self):
        """Reabrir una historia cerrada"""
        if self.estado == 'CERRADA':
            self.estado = 'ABIERTA'
            self.fecha_cierre = None
            self.cerrada_por = None
            self.save()
    
    @property
    def edad(self):
        """Calcular edad del paciente"""
        if self.fecha_nacimiento:
            from datetime import date
            today = date.today()
            return today.year - self.fecha_nacimiento.year - ((today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))
        return None
    
    @property
    def nombre_completo_profesional(self):
        """Nombre completo del profesional"""
        if self.profesional:
            return self.profesional.nombre
        return ""
    
    @property
    def empresa_nombre(self):
        """Nombre de la empresa"""
        if self.empresa:
            return self.empresa.razon_social
        return "Particular"
    
    @property
    def puede_cerrar(self):
        """Verificar si la historia puede ser cerrada"""
        return self.estado == 'ABIERTA'
    
    @property
    def puede_anular(self):
        """Verificar si la historia puede ser anulada"""
        return self.estado in ['ABIERTA', 'CERRADA']
    
    @property
    def puede_reabrir(self):
        """Verificar si la historia puede ser reabierta"""
        return self.estado == 'CERRADA'


class FichaClinica(models.Model):
    """Modelo base para fichas clínicas de diferentes tipos"""
    
    TIPO_FICHA_CHOICES = [
        ('EVALUACION_OCUPACIONAL', 'Evaluación Ocupacional'),
        ('EXAMEN_VISUAL', 'Examen Visual'),
        ('AUDIOMETRIA', 'Audiometría'),
        ('ESPIROMETRIA', 'Espirometría'),
        ('OSTEOMUSCULAR', 'Osteomuscular'),
        ('HISTORIA_GENERAL', 'Historia Clínica General'),
        ('TERAPIA_FISICA', 'Terapia Física'),
    ]
    
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('SIN_ATENCION', 'Sin Atención'),
        ('EN_PROCESO', 'En Proceso'),
        ('COMPLETADA', 'Completada'),
        ('CERRADA', 'Cerrada'),
    ]
    
    # Información básica
    numero_ficha = models.CharField(max_length=20, unique=True, verbose_name="N° Ficha")
    tipo_ficha = models.CharField(max_length=30, choices=TIPO_FICHA_CHOICES, verbose_name="Tipo de Ficha")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha Creación")
    fecha_evaluacion = models.DateField(verbose_name="Fecha de Evaluación")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE', verbose_name="Estado")
    
    # Información del paciente/trabajador
    numero_identificacion = models.CharField(max_length=20, verbose_name="N° Identificación")
    tipo_documento = models.CharField(max_length=10, choices=OrdenServicio.TIPO_DOC_CHOICES, default='CC', verbose_name="Tipo Documento")
    nombre_trabajador = models.CharField(max_length=200, verbose_name="Nombre del Trabajador")
    fecha_nacimiento = models.DateField(null=True, blank=True, verbose_name="Fecha de Nacimiento")
    genero = models.CharField(max_length=1, choices=OrdenServicio.GENERO_CHOICES, verbose_name="Género")
    edad = models.PositiveIntegerField(null=True, blank=True, verbose_name="Edad")
    
    # Información de contacto
    telefono = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    email = models.EmailField(blank=True, verbose_name="Email")
    direccion = models.TextField(blank=True, verbose_name="Dirección")
    municipio = models.ForeignKey(Municipio, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Municipio")
    
    # Información laboral
    empresa = models.ForeignKey(Empresa, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Empresa")
    cargo = models.CharField(max_length=100, blank=True, verbose_name="Cargo")
    profesional_evaluador = models.ForeignKey(Prestador, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Profesional Evaluador")
    
    # Relación con historia clínica si existe
    historia_clinica = models.ForeignKey(HistoriaClinica, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Historia Clínica")
    orden_servicio = models.ForeignKey(OrdenServicio, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Orden de Servicio")
    
    # Auditoría
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Creado Por")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Ficha Clínica"
        verbose_name_plural = "Fichas Clínicas"
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['numero_identificacion']),
            models.Index(fields=['tipo_ficha', 'estado']),
            models.Index(fields=['empresa', 'fecha_evaluacion']),
            models.Index(fields=['profesional_evaluador']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.numero_ficha:
            # Generar número de ficha automático
            prefix = self.tipo_ficha[:3].upper()
            from datetime import datetime
            year = datetime.now().year
            last_ficha = FichaClinica.objects.filter(
                numero_ficha__startswith=f"{prefix}{year}"
            ).order_by('-numero_ficha').first()
            
            if last_ficha:
                try:
                    last_number = int(last_ficha.numero_ficha[-4:])
                    new_number = last_number + 1
                except ValueError:
                    new_number = 1
            else:
                new_number = 1
            
            self.numero_ficha = f"{prefix}{year}{new_number:04d}"
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.numero_ficha} - {self.nombre_trabajador} - {self.get_tipo_ficha_display()}"


class EvaluacionOcupacional(models.Model):
    """Evaluación Médica Ocupacional completa"""
    
    TIPO_EVALUACION_CHOICES = [
        ('INGRESO', 'Evaluación de Ingreso'),
        ('PERIODICA', 'Evaluación Periódica'),
        ('RETIRO', 'Evaluación de Retiro'),
        ('REINTEGRO', 'Evaluación de Reintegro'),
        ('TRABAJO_ALTURAS', 'Trabajo en Alturas'),
        ('ESPACIOS_CONFINADOS', 'Espacios Confinados'),
        ('OTROS', 'Otros'),
    ]
    
    ESTADO_CIVIL_CHOICES = [
        ('SOLTERO', 'Soltero(a)'),
        ('CASADO', 'Casado(a)'),
        ('UNION_LIBRE', 'Unión Libre'),
        ('DIVORCIADO', 'Divorciado(a)'),
        ('VIUDO', 'Viudo(a)'),
        ('SEPARADO', 'Separado(a)'),
    ]
    
    NIVEL_EDUCATIVO_CHOICES = [
        ('PRIMARIA_INCOMPLETA', 'Primaria Incompleta'),
        ('PRIMARIA_COMPLETA', 'Primaria Completa'),
        ('SECUNDARIA_INCOMPLETA', 'Secundaria Incompleta'),
        ('SECUNDARIA_COMPLETA', 'Secundaria Completa'),
        ('TECNICO', 'Técnico'),
        ('TECNOLOGO', 'Tecnólogo'),
        ('UNIVERSITARIO', 'Universitario'),
        ('ESPECIALIZACION', 'Especialización'),
        ('MAESTRIA', 'Maestría'),
        ('DOCTORADO', 'Doctorado'),
    ]
    
    JORNADA_LABORAL_CHOICES = [
        ('DIURNA', 'Diurna'),
        ('NOCTURNA', 'Nocturna'),
        ('MIXTA', 'Mixta'),
        ('ROTATIVA', 'Rotativa'),
    ]
    
    TIPO_SANGRE_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    
    # Relación con ficha clínica base
    ficha_clinica = models.OneToOneField(FichaClinica, on_delete=models.CASCADE, related_name='evaluacion_ocupacional')
    
    # Información específica de evaluación ocupacional
    tipo_evaluacion = models.CharField(max_length=30, choices=TIPO_EVALUACION_CHOICES, verbose_name="Tipo de Evaluación")
    actividad_economica = models.TextField(blank=True, verbose_name="Actividad Económica")
    
    # Datos personales adicionales
    estado_civil = models.CharField(max_length=20, choices=ESTADO_CIVIL_CHOICES, blank=True, verbose_name="Estado Civil")
    nivel_educativo = models.CharField(max_length=30, choices=NIVEL_EDUCATIVO_CHOICES, blank=True, verbose_name="Nivel Educativo")
    eps = models.CharField(max_length=100, blank=True, verbose_name="EPS")
    afp = models.CharField(max_length=100, blank=True, verbose_name="AFP")
    arl = models.CharField(max_length=100, blank=True, verbose_name="ARL")
    tipo_sangre = models.CharField(max_length=5, choices=TIPO_SANGRE_CHOICES, blank=True, verbose_name="Tipo de Sangre")
    numero_hijos = models.PositiveIntegerField(null=True, blank=True, verbose_name="N° de Hijos")
    ingresos_promedio = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name="Ingresos Promedio")
    jornada_laboral = models.CharField(max_length=20, choices=JORNADA_LABORAL_CHOICES, blank=True, verbose_name="Jornada Laboral")
    
    # Información laboral específica
    area_cargo = models.CharField(max_length=200, blank=True, verbose_name="Área del Cargo")
    profesion_cargo = models.CharField(max_length=200, blank=True, verbose_name="Profesión o Cargo")
    funciones_cargo = models.TextField(blank=True, verbose_name="Funciones del Cargo")
    motivo_consulta = models.TextField(blank=True, verbose_name="Motivo de Consulta")
    
    # Elementos de Protección Personal (EPP)
    epp_casco = models.BooleanField(default=False, verbose_name="Casco")
    epp_gorro = models.BooleanField(default=False, verbose_name="Gorro")
    epp_respirador = models.BooleanField(default=False, verbose_name="Respirador")
    epp_gafas = models.BooleanField(default=False, verbose_name="Gafas")
    epp_peto = models.BooleanField(default=False, verbose_name="Peto")
    epp_bata = models.BooleanField(default=False, verbose_name="Bata")
    epp_overol = models.BooleanField(default=False, verbose_name="Overol")
    epp_delantal_plomo = models.BooleanField(default=False, verbose_name="Delantal de Plomo")
    epp_ropa_termica = models.BooleanField(default=False, verbose_name="Ropa Térmica")
    epp_auditivos = models.BooleanField(default=False, verbose_name="Protección Auditiva")
    epp_careta = models.BooleanField(default=False, verbose_name="Careta")
    epp_tapabocas = models.BooleanField(default=False, verbose_name="Tapabocas")
    epp_guantes = models.BooleanField(default=False, verbose_name="Guantes")
    epp_cinturon = models.BooleanField(default=False, verbose_name="Cinturón")
    epp_botas = models.BooleanField(default=False, verbose_name="Botas")
    epp_polainas = models.BooleanField(default=False, verbose_name="Polainas")
    epp_otros = models.CharField(max_length=200, blank=True, verbose_name="Otros EPP")
    
    # Campos para las diferentes secciones del examen
    historia_antecedentes = models.TextField(blank=True, verbose_name="Historia de Antecedentes")
    revision_sistemas = models.TextField(blank=True, verbose_name="Revisión por Sistemas y Hábitos")
    signos_vitales = models.JSONField(default=dict, blank=True, verbose_name="Signos Vitales y Examen Físico")
    anexo_alturas = models.TextField(blank=True, verbose_name="Anexo de Alturas")
    anexo_osteomuscular = models.TextField(blank=True, verbose_name="Anexo Osteomuscular")
    paraclinicos_diagnosticos = models.TextField(blank=True, verbose_name="Paraclínicos y Diagnósticos")
    concepto_aptitud = models.TextField(blank=True, verbose_name="Concepto de Aptitud y Conducta")
    ordenes_medicas = models.TextField(blank=True, verbose_name="Órdenes Médicas e Incapacidades")
    evoluciones_notas = models.TextField(blank=True, verbose_name="Evoluciones y Notas Adicionales")
    
    # Observaciones adicionales
    observaciones_adicionales = models.TextField(blank=True, verbose_name="Observaciones Adicionales a los Antecedentes")
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Evaluación Ocupacional"
        verbose_name_plural = "Evaluaciones Ocupacionales"
    
    def __str__(self):
        return f"Eval. Ocupacional - {self.ficha_clinica.nombre_trabajador}"


class AntecedenteFamiliar(models.Model):
    """Antecedentes familiares del paciente"""
    
    PATOLOGIA_CHOICES = [
        ('ASMA', 'Asma'),
        ('CANCER', 'Cáncer'),
        ('DIABETES', 'Diabetes'),
        ('ENFERMEDAD_CORONARIA', 'Enfermedad Coronaria'),
        ('ACCIDENTE_CEREBRO_VASCULAR', 'Accidente Cerebro Vascular'),
        ('HIPERTENSION_ARTERIAL', 'Hipertensión Arterial'),
        ('COLAGENOSIS', 'Colagenosis'),
        ('PATOLOGIAS_TIROIDEAS', 'Patologías Tiroideas'),
        ('OTROS', 'Otros'),
    ]
    
    PARENTESCO_CHOICES = [
        ('PADRE', 'Padre'),
        ('MADRE', 'Madre'),
        ('HERMANO', 'Hermano'),
        ('HERMANA', 'Hermana'),
        ('ABUELO_PATERNO', 'Abuelo Paterno'),
        ('ABUELA_PATERNA', 'Abuela Paterna'),
        ('ABUELO_MATERNO', 'Abuelo Materno'),
        ('ABUELA_MATERNA', 'Abuela Materna'),
        ('TIO', 'Tío'),
        ('TIA', 'Tía'),
        ('PRIMO', 'Primo'),
        ('PRIMA', 'Prima'),
        ('OTRO', 'Otro'),
        ('NO_REFIERE', 'No Refiere'),
    ]
    
    evaluacion_ocupacional = models.ForeignKey(EvaluacionOcupacional, on_delete=models.CASCADE, related_name='antecedentes_familiares')
    patologia = models.CharField(max_length=30, choices=PATOLOGIA_CHOICES, verbose_name="Patología")
    parentesco = models.CharField(max_length=20, choices=PARENTESCO_CHOICES, default='NO_REFIERE', verbose_name="Parentesco")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    fecha_registro = models.DateTimeField(auto_now_add=True)
    profesional = models.ForeignKey(Prestador, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Profesional")
    
    class Meta:
        verbose_name = "Antecedente Familiar"
        verbose_name_plural = "Antecedentes Familiares"
        unique_together = ['evaluacion_ocupacional', 'patologia']


class AntecedentePersonal(models.Model):
    """Antecedentes personales del paciente"""
    
    TIPO_ANTECEDENTE_CHOICES = [
        ('PATOLOGICOS', 'Patológicos'),
        ('QUIRURGICOS', 'Quirúrgicos'),
        ('TRAUMATICOS', 'Traumáticos'),
        ('FARMACOLOGICOS', 'Farmacológicos'),
        ('ALERGICOS', 'Alérgicos'),
        ('PSIQUIATRICOS', 'Psiquiátricos'),
        ('FOBIAS', 'Fobias'),
        ('OTROS', 'Otros'),
    ]
    
    evaluacion_ocupacional = models.ForeignKey(EvaluacionOcupacional, on_delete=models.CASCADE, related_name='antecedentes_personales')
    tipo_antecedente = models.CharField(max_length=20, choices=TIPO_ANTECEDENTE_CHOICES, verbose_name="Tipo de Antecedente")
    diagnostico_observaciones = models.TextField(default='NO REFIERE', verbose_name="Diagnóstico / Observaciones")
    fecha_registro = models.DateTimeField(auto_now_add=True)
    profesional = models.ForeignKey(Prestador, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Profesional")
    
    class Meta:
        verbose_name = "Antecedente Personal"
        verbose_name_plural = "Antecedentes Personales"
        unique_together = ['evaluacion_ocupacional', 'tipo_antecedente']


class AntecedenteSistema(models.Model):
    """Antecedentes personales por sistemas"""
    
    SISTEMA_CHOICES = [
        ('CABEZA', 'Cabeza'),
        ('OJOS', 'Ojos'),
        ('OIDOS', 'Oídos'),
        ('NARIZ', 'Nariz'),
        ('BOCA', 'Boca'),
        ('GARGANTA', 'Garganta'),
        ('CUELLO', 'Cuello'),
        ('SISTEMA_ENDOCRINO', 'Sistema Endocrino'),
        ('SISTEMA_CIRCULATORIO', 'Sistema Circulatorio'),
        ('SISTEMA_RESPIRATORIO', 'Sistema Respiratorio'),
        ('SISTEMA_GASTROINTESTINAL', 'Sistema Gastrointestinal'),
        ('SISTEMA_GENITOURINARIO', 'Sistema Genitourinario'),
        ('SISTEMA_OSTEOMUSCULAR', 'Sistema Osteomuscular'),
        ('SISTEMA_NERVIOSO', 'Sistema Nervioso'),
        ('PSIQUIATRICO', 'Psiquiátrico'),
        ('PIEL_ANEXOS', 'Piel y Anexos'),
    ]
    
    evaluacion_ocupacional = models.ForeignKey(EvaluacionOcupacional, on_delete=models.CASCADE, related_name='antecedentes_sistemas')
    nombre_sistema = models.CharField(max_length=30, choices=SISTEMA_CHOICES, verbose_name="Sistema")
    patologicos = models.CharField(max_length=200, default='NIEGA', verbose_name="Patológicos")
    quirurgicos = models.CharField(max_length=200, default='NIEGA', verbose_name="Quirúrgicos")
    traumaticos = models.CharField(max_length=200, default='NIEGA', verbose_name="Traumáticos")
    
    class Meta:
        verbose_name = "Antecedente por Sistema"
        verbose_name_plural = "Antecedentes por Sistemas"
        unique_together = ['evaluacion_ocupacional', 'nombre_sistema']


class ExposicionLaboral(models.Model):
    """Antecedentes de exposición laboral"""
    
    evaluacion_ocupacional = models.ForeignKey(EvaluacionOcupacional, on_delete=models.CASCADE, related_name='exposiciones_laborales')
    nombre_empresa = models.CharField(max_length=200, verbose_name="Nombre de la Empresa")
    actividad_economica = models.CharField(max_length=200, blank=True, verbose_name="Actividad Económica")
    cargo = models.CharField(max_length=200, verbose_name="Cargo")
    factores_riesgo = models.TextField(verbose_name="Factores de Riesgo (GTC-45)")
    tiempo_exposicion_anos = models.PositiveIntegerField(null=True, blank=True, verbose_name="Años de Exposición")
    tiempo_exposicion_meses = models.PositiveIntegerField(null=True, blank=True, verbose_name="Meses de Exposición")
    fecha_registro = models.DateTimeField(auto_now_add=True)
    profesional = models.ForeignKey(Prestador, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Profesional")
    
    class Meta:
        verbose_name = "Exposición Laboral"
        verbose_name_plural = "Exposiciones Laborales"


class AccidenteLaboral(models.Model):
    """Accidentes laborales del trabajador"""
    
    evaluacion_ocupacional = models.ForeignKey(EvaluacionOcupacional, on_delete=models.CASCADE, related_name='accidentes_laborales')
    nombre_empresa = models.CharField(max_length=200, verbose_name="Nombre de la Empresa")
    tipo_accidente = models.CharField(max_length=200, verbose_name="Tipo de Accidente")
    fecha_accidente = models.DateField(null=True, blank=True, verbose_name="Fecha del Accidente")
    parte_cuerpo_afectada = models.CharField(max_length=200, verbose_name="Parte del Cuerpo Afectada")
    secuelas = models.TextField(blank=True, verbose_name="Secuelas")
    dias_incapacidad = models.PositiveIntegerField(null=True, blank=True, verbose_name="Días de Incapacidad")
    reportado_arl = models.BooleanField(default=False, verbose_name="Reportado en ARL")
    atencion_recibida = models.TextField(blank=True, verbose_name="Atención Recibida")
    fecha_registro = models.DateTimeField(auto_now_add=True)
    profesional = models.ForeignKey(Prestador, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Profesional")
    
    class Meta:
        verbose_name = "Accidente Laboral"
        verbose_name_plural = "Accidentes Laborales"


class EnfermedadLaboral(models.Model):
    """Enfermedades laborales del trabajador"""
    
    evaluacion_ocupacional = models.ForeignKey(EvaluacionOcupacional, on_delete=models.CASCADE, related_name='enfermedades_laborales')
    descripcion_enfermedad = models.TextField(verbose_name="Descripción de la Enfermedad Laboral")
    fecha_diagnostico = models.DateField(null=True, blank=True, verbose_name="Fecha del Diagnóstico")
    fecha_registro = models.DateTimeField(auto_now_add=True)
    profesional = models.ForeignKey(Prestador, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Profesional")
    
    class Meta:
        verbose_name = "Enfermedad Laboral"
        verbose_name_plural = "Enfermedades Laborales"


class ExamenVisual(models.Model):
    """Examen Visual completo según formulario específico"""
    
    SINTOMATOLOGIA_CHOICES = [
        ('ASINTOMATICO', 'Asintomático'),
        ('SINTOMATICO', 'Sintomático'),
    ]
    
    VALORACION_CHOICES = [
        ('NORMAL', 'Normal'),
        ('ALTERADO', 'Alterado'),
        ('NO_APLICA', 'No Aplica'),
    ]
    
    USO_CHOICES = [
        ('NO_USA', 'No Usa'),
        ('USA', 'Usa'),
        ('NO_APLICA', 'No Aplica'),
    ]
    
    TIPO_USO_CHOICES = [
        ('PERMANENTE', 'Permanente'),
        ('OCASIONAL', 'Ocasional'),
        ('VISION_PROXIMA', 'Visión Próxima'),
        ('VISION_LEJANA', 'Visión Lejana'),
        ('NO_APLICA', 'No Aplica'),
    ]
    
    # Relación con ficha clínica base
    ficha_clinica = models.OneToOneField(FichaClinica, on_delete=models.CASCADE, related_name='examen_visual')
    
    # Información básica del examen
    ultimo_examen = models.CharField(max_length=200, blank=True, verbose_name="F. Último Examen")
    lugar_ultimo_examen = models.CharField(max_length=200, blank=True, verbose_name="Lugar del Último Examen")
    motivo_consulta = models.TextField(blank=True, verbose_name="Motivo de Consulta")
    
    # Sintomatología
    sintomatologia = models.CharField(max_length=20, choices=SINTOMATOLOGIA_CHOICES, default='ASINTOMATICO', verbose_name="Sintomatología")
    
    # Agudeza Visual Sin Corrección
    ojo_derecho_vl_sc = models.CharField(max_length=10, blank=True, verbose_name="OD V.L. 20/")
    ojo_derecho_vp_sc = models.CharField(max_length=10, blank=True, verbose_name="OD V.P.")
    ojo_derecho_ph_sc = models.CharField(max_length=10, blank=True, verbose_name="OD PH")
    
    ojo_izquierdo_vl_sc = models.CharField(max_length=10, blank=True, verbose_name="OI V.L. 20/")
    ojo_izquierdo_vp_sc = models.CharField(max_length=10, blank=True, verbose_name="OI V.P.")
    ojo_izquierdo_ph_sc = models.CharField(max_length=10, blank=True, verbose_name="OI PH")
    
    ambos_ojos_vl_sc = models.CharField(max_length=10, blank=True, verbose_name="AO V.L. 20/")
    ambos_ojos_vp_sc = models.CharField(max_length=10, blank=True, verbose_name="AO V.P.")
    ambos_ojos_ph_sc = models.CharField(max_length=10, blank=True, verbose_name="AO PH")
    
    # Agudeza Visual Con Corrección
    ojo_derecho_vl_cc = models.CharField(max_length=10, blank=True, verbose_name="OD V.L. 20/ (CC)")
    ojo_derecho_vp_cc = models.CharField(max_length=10, blank=True, verbose_name="OD V.P. (CC)")
    
    ojo_izquierdo_vl_cc = models.CharField(max_length=10, blank=True, verbose_name="OI V.L. 20/ (CC)")
    ojo_izquierdo_vp_cc = models.CharField(max_length=10, blank=True, verbose_name="OI V.P. (CC)")
    
    ambos_ojos_vl_cc = models.CharField(max_length=10, blank=True, verbose_name="AO V.L. 20/ (CC)")
    ambos_ojos_vp_cc = models.CharField(max_length=10, blank=True, verbose_name="AO V.P. (CC)")
    
    # Examen Externo
    ojo_derecho_externo = models.TextField(blank=True, verbose_name="Examen Externo OD")
    ojo_izquierdo_externo = models.TextField(blank=True, verbose_name="Examen Externo OI")
    
    # Reflejos
    reflejos_observacion = models.CharField(max_length=100, default='PRESENTES Y NORMALES', verbose_name="Reflejos")
    
    # Cover Test
    vision_lejana_cover = models.CharField(max_length=50, default='NORMAL', verbose_name="Visión Lejana Cover Test")
    vision_proxima_cover = models.CharField(max_length=50, default='NORMAL', verbose_name="Visión Próxima Cover Test")
    
    # Motilidad Ocular
    motilidad_observacion = models.CharField(max_length=100, default='NORMAL', verbose_name="Motilidad Ocular")
    
    # Punto Próximo de Convergencia
    convergencia_observacion = models.CharField(max_length=100, default='NORMAL', verbose_name="Punto Próximo de Convergencia")
    
    # Oftalmoscopía
    ojo_derecho_oftalmoscopia = models.CharField(max_length=100, default='FONDO DE OJO APARENTEMENTE NORMAL', verbose_name="Oftalmoscopía OD")
    ojo_izquierdo_oftalmoscopia = models.CharField(max_length=100, default='FONDO DE OJO APARENTEMENTE NORMAL', verbose_name="Oftalmoscopía OI")
    
    # Queratometría
    ojo_derecho_queratometria = models.CharField(max_length=20, blank=True, verbose_name="Queratometría OD K´=")
    ojo_izquierdo_queratometria = models.CharField(max_length=20, blank=True, verbose_name="Queratometría OI K´=")
    
    # Refracción
    ojo_derecho_refraccion_av = models.CharField(max_length=10, blank=True, verbose_name="Refracción OD A.V. 20/")
    ojo_izquierdo_refraccion_av = models.CharField(max_length=10, blank=True, verbose_name="Refracción OI A.V. 20/")
    
    # RX Final
    ojo_derecho_rx_vl = models.CharField(max_length=10, blank=True, verbose_name="RX Final OD V.L. 20/")
    ojo_derecho_rx_vp = models.CharField(max_length=10, blank=True, verbose_name="RX Final OD V.P.")
    ojo_derecho_rx_add = models.CharField(max_length=10, blank=True, verbose_name="RX Final OD ADD")
    
    ojo_izquierdo_rx_vl = models.CharField(max_length=10, blank=True, verbose_name="RX Final OI V.L. 20/")
    ojo_izquierdo_rx_vp = models.CharField(max_length=10, blank=True, verbose_name="RX Final OI V.P.")
    ojo_izquierdo_rx_add = models.CharField(max_length=10, blank=True, verbose_name="RX Final OI ADD")
    
    # Visión Color
    ojo_derecho_vision_color = models.CharField(max_length=50, default='NORMAL', verbose_name="Visión Color OD")
    ojo_izquierdo_vision_color = models.CharField(max_length=50, default='NORMAL', verbose_name="Visión Color OI")
    
    # Estereopsis
    estereopsis_observacion = models.CharField(max_length=100, default='NORMAL', verbose_name="Estereopsis")
    
    # Diagnósticos y Recomendaciones (usaremos campos separados por ser específicos)
    diagnostico_recomendaciones = models.TextField(blank=True, verbose_name="Diagnóstico y Recomendaciones")
    
    # Via de ingreso y otros campos para RIPS
    via_ingreso = models.CharField(max_length=10, default='01', verbose_name="Vía de Ingreso")
    finalidad_consulta = models.CharField(max_length=10, default='15', verbose_name="Finalidad de la Consulta")
    causa_externa = models.CharField(max_length=10, default='38', verbose_name="Causa Externa")
    
    # Observaciones adicionales
    otras_observaciones = models.TextField(blank=True, verbose_name="Otras Observaciones y Recomendaciones")
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Examen Visual"
        verbose_name_plural = "Exámenes Visuales"
    
    def __str__(self):
        return f"Examen Visual - {self.ficha_clinica.nombre_trabajador}"


class AntecedenteVisual(models.Model):
    """Antecedentes visuales específicos"""
    
    TIPO_ANTECEDENTE_CHOICES = [
        ('ANTECEDENTES_PERSONALES', 'Antecedentes Personales'),
        ('ANTECEDENTES_FAMILIARES', 'Antecedentes Familiares'),
        ('ANTECEDENTES_OCUPACIONALES', 'Antecedentes Ocupacionales'),
        ('EXPOSICION_LABORAL_VISUAL', 'Exposición Laboral Visual'),
        ('USA_ANTEOJOS', 'Usa Anteojos'),
        ('MULTIFOCAL', 'Multifocal'),
        ('LENTES_CONTACTO', 'Lentes de Contacto'),
        ('TRAE_RX', 'Trae RX'),
        ('TIPO_USO', 'Tipo de Uso'),
        ('ULTIMO_DIAGNOSTICO', 'Último Diagnóstico'),
    ]
    
    examen_visual = models.ForeignKey(ExamenVisual, on_delete=models.CASCADE, related_name='antecedentes_visuales')
    tipo_antecedente = models.CharField(max_length=30, choices=TIPO_ANTECEDENTE_CHOICES, verbose_name="Tipo de Antecedente")
    observacion = models.CharField(max_length=200, default='NIEGA', verbose_name="Observación")
    
    class Meta:
        verbose_name = "Antecedente Visual"
        verbose_name_plural = "Antecedentes Visuales"
        unique_together = ['examen_visual', 'tipo_antecedente']


class DiagnosticoVisual(models.Model):
    """Diagnósticos visuales específicos con códigos CIE-10"""
    
    TIPO_DIAGNOSTICO_CHOICES = [
        ('PRINCIPAL', 'Diagnóstico Principal'),
        ('RELACIONADO_1', 'Diagnóstico Relacionado 1'),
        ('RELACIONADO_2', 'Diagnóstico Relacionado 2'),
        ('RELACIONADO_3', 'Diagnóstico Relacionado 3'),
    ]
    
    LATERALIDAD_CHOICES = [
        ('', 'Seleccione'),
        ('BILATERAL', 'Bilateral'),
        ('DERECHO', 'Derecho'),
        ('IZQUIERDO', 'Izquierdo'),
        ('NO_APLICA', 'No Aplica'),
    ]
    
    TIPO_IMPRESION_CHOICES = [
        ('IMPRESION_DIAGNOSTICA', 'Impresión Diagnóstica'),
        ('CONFIRMADO', 'Confirmado'),
        ('REPETIDO', 'Repetido'),
    ]
    
    examen_visual = models.ForeignKey(ExamenVisual, on_delete=models.CASCADE, related_name='diagnosticos_visuales')
    tipo_diagnostico = models.CharField(max_length=20, choices=TIPO_DIAGNOSTICO_CHOICES, verbose_name="Tipo de Diagnóstico")
    codigo_cie10 = models.CharField(max_length=10, verbose_name="Código CIE10")
    nombre_diagnostico = models.CharField(max_length=200, verbose_name="Nombre del Diagnóstico")
    lateralidad = models.CharField(max_length=20, choices=LATERALIDAD_CHOICES, blank=True, verbose_name="Lateralidad")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    tipo_impresion = models.CharField(max_length=30, choices=TIPO_IMPRESION_CHOICES, blank=True, verbose_name="Tipo de Impresión")
    
    class Meta:
        verbose_name = "Diagnóstico Visual"
        verbose_name_plural = "Diagnósticos Visuales"


class ConductaRecomendacionVisual(models.Model):
    """Conductas y recomendaciones para examen visual"""
    
    CONDUCTA_CHOICES = [
        ('CONTROL_6_MESES', 'Control en 6 meses'),
        ('CONTROL_1_ANO', 'Control en un año'),
        ('INCLUIR_PVE_VISUAL', 'Incluir en el PVE Visual'),
        ('CORRECCION_OPTICA_PERMANENTE', 'Usar corrección óptica permanente'),
        ('CORRECCION_OPTICA_PROXIMA', 'Usar corrección óptica para visión próxima'),
        ('CORRECCION_OPTICA_LEJANA', 'Usar corrección óptica para visión lejana'),
        ('CORRECCION_OPTICA_OCASIONAL', 'Usar corrección óptica ocasional'),
        ('PROTECCION_VISUAL', 'Uso de elementos de protección visual'),
        ('PAUSAS_ACTIVAS', 'Realizar pausas activas'),
    ]
    
    REMISION_CHOICES = [
        ('ORTOPTICA', 'Valoración por Ortóptica'),
        ('OPTOMETRIA_CICLOPLEJIA', 'Valoración por Optometría bajo Cicloplejia'),
        ('TOPOGRAFIA_CORNEAL', 'Realización de Topografía Corneal'),
        ('OFTALMOLOGIA', 'Valoración por Oftalmología'),
        ('OTRAS', 'Otras'),
    ]
    
    examen_visual = models.ForeignKey(ExamenVisual, on_delete=models.CASCADE, related_name='conductas_recomendaciones')
    tipo_item = models.CharField(max_length=20, choices=[('CONDUCTA', 'Conducta'), ('REMISION', 'Remisión')], verbose_name="Tipo")
    codigo = models.CharField(max_length=50, verbose_name="Código")
    descripcion = models.CharField(max_length=200, verbose_name="Descripción")
    seleccionado = models.BooleanField(default=False, verbose_name="Seleccionado")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    
    class Meta:
        verbose_name = "Conducta y Recomendación Visual"
        verbose_name_plural = "Conductas y Recomendaciones Visuales"


class Audiometria(models.Model):
    """Audiometría completa según formulario específico"""
    
    TIPO_PROTECCION_CHOICES = [
        ('TAPONES_ESPUMA', 'Tapones de Espuma'),
        ('TAPONES_SILICONA', 'Tapones de Silicona'),
        ('PROTECTORES_COPA', 'Protectores de Copa'),
        ('PROTECTORES_INSERCION', 'Protectores de Inserción'),
        ('NINGUNA', 'Ninguna'),
        ('OTROS', 'Otros'),
    ]
    
    TOLERANCIA_CHOICES = [
        ('BUENA', 'Buena'),
        ('REGULAR', 'Regular'),
        ('MALA', 'Mala'),
        ('NO_USA', 'No Usa'),
    ]
    
    SEVERIDAD_CAOHC_CHOICES = [
        ('NORMAL', 'Normal (0-25 dB)'),
        ('LEVE', 'Leve (25 - 40 dB)'),
        ('MODERADA', 'Moderada (41 - 55 dB)'),
        ('MODERADA_SEVERA', 'Moderada - Severa (56 - 70 dB)'),
        ('SEVERA', 'Severa (71 - 85 dB)'),
        ('PROFUNDA', 'Profunda (> 85 dB)'),
    ]
    
    # Relación con ficha clínica base
    ficha_clinica = models.OneToOneField(FichaClinica, on_delete=models.CASCADE, related_name='audiometria')
    
    # Información básica del examen
    producto = models.CharField(max_length=200, blank=True, verbose_name="Producto")
    funciones_cargo = models.TextField(blank=True, verbose_name="Funciones del Cargo")
    eps = models.CharField(max_length=100, blank=True, verbose_name="EPS")
    
    # Condiciones de toma de la prueba
    descanso_auditivo_horas = models.PositiveIntegerField(null=True, blank=True, verbose_name="Descanso Auditivo (Horas)")
    realizo_retest = models.BooleanField(default=False, verbose_name="Realizó re test")
    uso_cabina_sonoamortiguada = models.BooleanField(default=True, verbose_name="Uso cabina sonoamortiguada")
    marca_audiometro = models.CharField(max_length=200, blank=True, verbose_name="Marca y referencia audiómetro utilizado")
    fecha_ultima_calibracion = models.DateField(null=True, blank=True, verbose_name="F. Última Calibración")
    
    # Otoscopia
    otoscopia_oido_izquierdo = models.TextField(blank=True, verbose_name="Otoscopia Oído Izquierdo")
    otoscopia_oido_derecho = models.TextField(blank=True, verbose_name="Otoscopia Oído Derecho")
    
    # Audiometría - Frecuencias estándar (en dB)
    # Vía Aérea Oído Derecho
    va_od_250 = models.IntegerField(null=True, blank=True, verbose_name="VA OD 250 Hz")
    va_od_500 = models.IntegerField(null=True, blank=True, verbose_name="VA OD 500 Hz")
    va_od_1000 = models.IntegerField(null=True, blank=True, verbose_name="VA OD 1000 Hz")
    va_od_2000 = models.IntegerField(null=True, blank=True, verbose_name="VA OD 2000 Hz")
    va_od_3000 = models.IntegerField(null=True, blank=True, verbose_name="VA OD 3000 Hz")
    va_od_4000 = models.IntegerField(null=True, blank=True, verbose_name="VA OD 4000 Hz")
    va_od_6000 = models.IntegerField(null=True, blank=True, verbose_name="VA OD 6000 Hz")
    va_od_8000 = models.IntegerField(null=True, blank=True, verbose_name="VA OD 8000 Hz")
    
    # Vía Aérea Oído Izquierdo
    va_oi_250 = models.IntegerField(null=True, blank=True, verbose_name="VA OI 250 Hz")
    va_oi_500 = models.IntegerField(null=True, blank=True, verbose_name="VA OI 500 Hz")
    va_oi_1000 = models.IntegerField(null=True, blank=True, verbose_name="VA OI 1000 Hz")
    va_oi_2000 = models.IntegerField(null=True, blank=True, verbose_name="VA OI 2000 Hz")
    va_oi_3000 = models.IntegerField(null=True, blank=True, verbose_name="VA OI 3000 Hz")
    va_oi_4000 = models.IntegerField(null=True, blank=True, verbose_name="VA OI 4000 Hz")
    va_oi_6000 = models.IntegerField(null=True, blank=True, verbose_name="VA OI 6000 Hz")
    va_oi_8000 = models.IntegerField(null=True, blank=True, verbose_name="VA OI 8000 Hz")
    
    # Vía Ósea Oído Derecho
    vo_od_250 = models.IntegerField(null=True, blank=True, verbose_name="VO OD 250 Hz")
    vo_od_500 = models.IntegerField(null=True, blank=True, verbose_name="VO OD 500 Hz")
    vo_od_1000 = models.IntegerField(null=True, blank=True, verbose_name="VO OD 1000 Hz")
    vo_od_2000 = models.IntegerField(null=True, blank=True, verbose_name="VO OD 2000 Hz")
    vo_od_3000 = models.IntegerField(null=True, blank=True, verbose_name="VO OD 3000 Hz")
    vo_od_4000 = models.IntegerField(null=True, blank=True, verbose_name="VO OD 4000 Hz")
    vo_od_6000 = models.IntegerField(null=True, blank=True, verbose_name="VO OD 6000 Hz")
    vo_od_8000 = models.IntegerField(null=True, blank=True, verbose_name="VO OD 8000 Hz")
    
    # Vía Ósea Oído Izquierdo
    vo_oi_250 = models.IntegerField(null=True, blank=True, verbose_name="VO OI 250 Hz")
    vo_oi_500 = models.IntegerField(null=True, blank=True, verbose_name="VO OI 500 Hz")
    vo_oi_1000 = models.IntegerField(null=True, blank=True, verbose_name="VO OI 1000 Hz")
    vo_oi_2000 = models.IntegerField(null=True, blank=True, verbose_name="VO OI 2000 Hz")
    vo_oi_3000 = models.IntegerField(null=True, blank=True, verbose_name="VO OI 3000 Hz")
    vo_oi_4000 = models.IntegerField(null=True, blank=True, verbose_name="VO OI 4000 Hz")
    vo_oi_6000 = models.IntegerField(null=True, blank=True, verbose_name="VO OI 6000 Hz")
    vo_oi_8000 = models.IntegerField(null=True, blank=True, verbose_name="VO OI 8000 Hz")
    
    # Vía Aérea con Campo Electromagnético
    va_od_ce_250 = models.IntegerField(null=True, blank=True, verbose_name="VA OD CE 250 Hz")
    va_od_ce_500 = models.IntegerField(null=True, blank=True, verbose_name="VA OD CE 500 Hz")
    va_od_ce_1000 = models.IntegerField(null=True, blank=True, verbose_name="VA OD CE 1000 Hz")
    va_od_ce_2000 = models.IntegerField(null=True, blank=True, verbose_name="VA OD CE 2000 Hz")
    va_od_ce_3000 = models.IntegerField(null=True, blank=True, verbose_name="VA OD CE 3000 Hz")
    va_od_ce_4000 = models.IntegerField(null=True, blank=True, verbose_name="VA OD CE 4000 Hz")
    va_od_ce_6000 = models.IntegerField(null=True, blank=True, verbose_name="VA OD CE 6000 Hz")
    va_od_ce_8000 = models.IntegerField(null=True, blank=True, verbose_name="VA OD CE 8000 Hz")
    
    va_oi_ce_250 = models.IntegerField(null=True, blank=True, verbose_name="VA OI CE 250 Hz")
    va_oi_ce_500 = models.IntegerField(null=True, blank=True, verbose_name="VA OI CE 500 Hz")
    va_oi_ce_1000 = models.IntegerField(null=True, blank=True, verbose_name="VA OI CE 1000 Hz")
    va_oi_ce_2000 = models.IntegerField(null=True, blank=True, verbose_name="VA OI CE 2000 Hz")
    va_oi_ce_3000 = models.IntegerField(null=True, blank=True, verbose_name="VA OI CE 3000 Hz")
    va_oi_ce_4000 = models.IntegerField(null=True, blank=True, verbose_name="VA OI CE 4000 Hz")
    va_oi_ce_6000 = models.IntegerField(null=True, blank=True, verbose_name="VA OI CE 6000 Hz")
    va_oi_ce_8000 = models.IntegerField(null=True, blank=True, verbose_name="VA OI CE 8000 Hz")
    
    # Vía Ósea con Campo Electromagnético
    vo_od_ce_250 = models.IntegerField(null=True, blank=True, verbose_name="VO OD CE 250 Hz")
    vo_od_ce_500 = models.IntegerField(null=True, blank=True, verbose_name="VO OD CE 500 Hz")
    vo_od_ce_1000 = models.IntegerField(null=True, blank=True, verbose_name="VO OD CE 1000 Hz")
    vo_od_ce_2000 = models.IntegerField(null=True, blank=True, verbose_name="VO OD CE 2000 Hz")
    vo_od_ce_3000 = models.IntegerField(null=True, blank=True, verbose_name="VO OD CE 3000 Hz")
    vo_od_ce_4000 = models.IntegerField(null=True, blank=True, verbose_name="VO OD CE 4000 Hz")
    vo_od_ce_6000 = models.IntegerField(null=True, blank=True, verbose_name="VO OD CE 6000 Hz")
    vo_od_ce_8000 = models.IntegerField(null=True, blank=True, verbose_name="VO OD CE 8000 Hz")
    
    vo_oi_ce_250 = models.IntegerField(null=True, blank=True, verbose_name="VO OI CE 250 Hz")
    vo_oi_ce_500 = models.IntegerField(null=True, blank=True, verbose_name="VO OI CE 500 Hz")
    vo_oi_ce_1000 = models.IntegerField(null=True, blank=True, verbose_name="VO OI CE 1000 Hz")
    vo_oi_ce_2000 = models.IntegerField(null=True, blank=True, verbose_name="VO OI CE 2000 Hz")
    vo_oi_ce_3000 = models.IntegerField(null=True, blank=True, verbose_name="VO OI CE 3000 Hz")
    vo_oi_ce_4000 = models.IntegerField(null=True, blank=True, verbose_name="VO OI CE 4000 Hz")
    vo_oi_ce_6000 = models.IntegerField(null=True, blank=True, verbose_name="VO OI CE 6000 Hz")
    vo_oi_ce_8000 = models.IntegerField(null=True, blank=True, verbose_name="VO OI CE 8000 Hz")
    
    # Clasificación de severidad CAOHC
    severidad_od = models.CharField(max_length=20, choices=SEVERIDAD_CAOHC_CHOICES, blank=True, verbose_name="Severidad OD")
    severidad_oi = models.CharField(max_length=20, choices=SEVERIDAD_CAOHC_CHOICES, blank=True, verbose_name="Severidad OI")
    
    # Via de ingreso y otros campos para RIPS
    via_ingreso = models.CharField(max_length=10, default='01', verbose_name="Vía de Ingreso")
    finalidad_consulta = models.CharField(max_length=10, default='15', verbose_name="Finalidad de la Consulta")
    causa_externa = models.CharField(max_length=10, default='38', verbose_name="Causa Externa")
    
    # Observaciones adicionales
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Audiometría"
        verbose_name_plural = "Audiometrías"
    
    def __str__(self):
        return f"Audiometría - {self.ficha_clinica.nombre_trabajador}"
    
    def calcular_severidad_od(self):
        """Calcular severidad CAOHC para oído derecho"""
        # Promedio de frecuencias conversacionales (500, 1000, 2000 Hz)
        frecuencias = [self.va_od_500, self.va_od_1000, self.va_od_2000]
        frecuencias_validas = [f for f in frecuencias if f is not None]
        
        if not frecuencias_validas:
            return 'NORMAL'
        
        promedio = sum(frecuencias_validas) / len(frecuencias_validas)
        
        if promedio <= 25:
            return 'NORMAL'
        elif promedio <= 40:
            return 'LEVE'
        elif promedio <= 55:
            return 'MODERADA'
        elif promedio <= 70:
            return 'MODERADA_SEVERA'
        elif promedio <= 85:
            return 'SEVERA'
        else:
            return 'PROFUNDA'
    
    def calcular_severidad_oi(self):
        """Calcular severidad CAOHC para oído izquierdo"""
        # Promedio de frecuencias conversacionales (500, 1000, 2000 Hz)
        frecuencias = [self.va_oi_500, self.va_oi_1000, self.va_oi_2000]
        frecuencias_validas = [f for f in frecuencias if f is not None]
        
        if not frecuencias_validas:
            return 'NORMAL'
        
        promedio = sum(frecuencias_validas) / len(frecuencias_validas)
        
        if promedio <= 25:
            return 'NORMAL'
        elif promedio <= 40:
            return 'LEVE'
        elif promedio <= 55:
            return 'MODERADA'
        elif promedio <= 70:
            return 'MODERADA_SEVERA'
        elif promedio <= 85:
            return 'SEVERA'
        else:
            return 'PROFUNDA'
    
    def save(self, *args, **kwargs):
        # Auto-calcular severidad si no está definida
        if not self.severidad_od:
            self.severidad_od = self.calcular_severidad_od()
        if not self.severidad_oi:
            self.severidad_oi = self.calcular_severidad_oi()
        super().save(*args, **kwargs)


class AntecedenteAuditivo(models.Model):
    """Antecedentes auditivos específicos"""
    
    TIPO_ANTECEDENTE_CHOICES = [
        # Antecedentes Familiares
        ('OTITIS', 'Otitis'),
        ('TRAUMA', 'Trauma'),
        ('CIRUGIA', 'Cirugía'),
        ('INGESTA_OTOTOXICOS', 'Ingesta Ototóxicos'),
        ('HIPOACUSIA_SUBJETIVA', 'Hipoacusia Subjetiva'),
        ('ACUFENOS', 'Acúfenos'),
        ('OTROS_FAMILIARES', 'Otros'),
        
        # Exposición Ruido Extralaboral
        ('TEJO', 'Tejo'),
        ('MOTO', 'Moto'),
        ('DISCOTECA', 'Discoteca'),
        ('SERVICIO_MILITAR', 'Servicio Militar'),
        ('POLIGONO', 'Polígono'),
        ('AUDIFONOS', 'Audífonos'),
        ('OTROS_EXTRALABORAL', 'Otro'),
    ]
    
    audiometria = models.ForeignKey(Audiometria, on_delete=models.CASCADE, related_name='antecedentes_auditivos')
    tipo_antecedente = models.CharField(max_length=30, choices=TIPO_ANTECEDENTE_CHOICES, verbose_name="Tipo de Antecedente")
    observacion = models.CharField(max_length=200, default='NO REFIERE', verbose_name="Observación")
    
    class Meta:
        verbose_name = "Antecedente Auditivo"
        verbose_name_plural = "Antecedentes Auditivos"
        unique_together = ['audiometria', 'tipo_antecedente']


class AntecedenteAuditivoLaboral(models.Model):
    """Antecedentes auditivos laborales específicos"""
    
    audiometria = models.ForeignKey(Audiometria, on_delete=models.CASCADE, related_name='antecedentes_laborales')
    empresa = models.CharField(max_length=200, verbose_name="Empresa")
    cargo = models.CharField(max_length=200, verbose_name="Cargo")
    tipo_proteccion = models.CharField(max_length=30, choices=Audiometria.TIPO_PROTECCION_CHOICES, verbose_name="Tipo de Protección")
    tolerancia_proteccion = models.CharField(max_length=20, choices=Audiometria.TOLERANCIA_CHOICES, verbose_name="Tolerancia Elemento Protección")
    tiempo_exposicion_anos = models.PositiveIntegerField(null=True, blank=True, verbose_name="Años de Exposición")
    tiempo_exposicion_meses = models.PositiveIntegerField(null=True, blank=True, verbose_name="Meses de Exposición")
    
    class Meta:
        verbose_name = "Antecedente Auditivo Laboral"
        verbose_name_plural = "Antecedentes Auditivos Laborales"


class DiagnosticoAuditivo(models.Model):
    """Diagnósticos auditivos específicos con códigos CIE-10"""
    
    TIPO_DIAGNOSTICO_CHOICES = [
        ('PRINCIPAL', 'Diagnóstico Principal'),
        ('RELACIONADO_1', 'Diagnóstico Relacionado 1'),
        ('RELACIONADO_2', 'Diagnóstico Relacionado 2'),
        ('RELACIONADO_3', 'Diagnóstico Relacionado 3'),
    ]
    
    LATERALIDAD_CHOICES = [
        ('', 'Seleccione'),
        ('BILATERAL', 'Bilateral'),
        ('DERECHO', 'Derecho'),
        ('IZQUIERDO', 'Izquierdo'),
        ('NO_APLICA', 'No Aplica'),
    ]
    
    TIPO_IMPRESION_CHOICES = [
        ('IMPRESION_DIAGNOSTICA', 'Impresión Diagnóstica'),
        ('CONFIRMADO', 'Confirmado'),
        ('REPETIDO', 'Repetido'),
    ]
    
    audiometria = models.ForeignKey(Audiometria, on_delete=models.CASCADE, related_name='diagnosticos_auditivos')
    tipo_diagnostico = models.CharField(max_length=20, choices=TIPO_DIAGNOSTICO_CHOICES, verbose_name="Tipo de Diagnóstico")
    codigo_cie10 = models.CharField(max_length=10, verbose_name="Código CIE10")
    nombre_diagnostico = models.CharField(max_length=200, verbose_name="Nombre del Diagnóstico")
    lateralidad = models.CharField(max_length=20, choices=LATERALIDAD_CHOICES, blank=True, verbose_name="Lateralidad")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    tipo_impresion = models.CharField(max_length=30, choices=TIPO_IMPRESION_CHOICES, blank=True, verbose_name="Tipo de Impresión")
    
    class Meta:
        verbose_name = "Diagnóstico Auditivo"
        verbose_name_plural = "Diagnósticos Auditivos"


class RecomendacionAuditiva(models.Model):
    """Recomendaciones audiológicas específicas"""
    
    RECOMENDACION_CHOICES = [
        ('CONTROL_AUDITIVO_1_ANO', 'Control Auditivo En Un Año'),
        ('CONTROL_AUDITIVO_6_MESES', 'Control Auditivo En Seis Meses'),
        ('USE_PROTECCION_AUDITIVA', 'Use protección auditiva'),
        ('CONTROL_OTORRINO', 'Control Por Otorinolaringología'),
        ('LAVADO_AUDITIVO_OD', 'Lavado Auditivo oído derecho'),
        ('LAVADO_AUDITIVO_OI', 'Lavado Auditivo oído izquierdo'),
        ('AUDIOMETRIA_CONFIRMATORIA', 'Audiometría Confirmatoria'),
        ('EXAMENES_COMPLEMENTARIOS', 'Exámenes Audiológicos complementarios'),
    ]
    
    audiometria = models.ForeignKey(Audiometria, on_delete=models.CASCADE, related_name='recomendaciones_auditivas')
    codigo = models.CharField(max_length=50, choices=RECOMENDACION_CHOICES, verbose_name="Recomendación")
    seleccionado = models.BooleanField(default=False, verbose_name="Seleccionado")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    
    class Meta:
        verbose_name = "Recomendación Auditiva"
        verbose_name_plural = "Recomendaciones Auditivas"
        unique_together = ['audiometria', 'codigo']


class Espirometria(models.Model):
    """Espirometría completa según formulario específico"""
    
    ESCALA_INTERPRETACION_CHOICES = [
        ('KNUDSON', 'Knudson'),
        ('ATS', 'ATS'),
        ('ERS', 'ERS'),
        ('NHANES', 'NHANES'),
    ]
    
    PATRON_FUNCIONAL_CHOICES = [
        ('NORMAL', 'Normal'),
        ('OBSTRUCTIVO', 'Obstructivo'),
        ('RESTRICTIVO', 'Restrictivo'),
        ('MIXTO', 'Mixto'),
    ]
    
    SEVERIDAD_CHOICES = [
        ('LEVE', 'Leve'),
        ('MODERADO', 'Moderado'),
        ('SEVERO', 'Severo'),
        ('MUY_SEVERO', 'Muy Severo'),
    ]
    
    FRECUENCIA_TABACO_CHOICES = [
        ('CONSUMO_DIA', 'Consumo/Día'),
        ('HORAS_SEMANA', 'Horas/Semana'),
        ('NA', 'N/A'),
    ]
    
    # Relación con ficha clínica base
    ficha_clinica = models.OneToOneField(FichaClinica, on_delete=models.CASCADE, related_name='espirometria')
    
    # Información básica del examen
    producto = models.CharField(max_length=200, blank=True, verbose_name="Producto")
    peso_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Peso (kg)")
    talla_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Talla (cm)")
    imc = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Índice de masa corporal (IMC)")
    fecha_ingreso_empresa = models.DateField(null=True, blank=True, verbose_name="Fecha Ingreso Empresa")
    antiguedad_cargo_anos = models.PositiveIntegerField(null=True, blank=True, verbose_name="Antigüedad Cargo Actual (Años)")
    antiguedad_cargo_meses = models.PositiveIntegerField(null=True, blank=True, verbose_name="Antigüedad Cargo Actual (Meses)")
    funciones_cargo = models.TextField(blank=True, verbose_name="Funciones del Cargo")
    eps = models.CharField(max_length=100, blank=True, verbose_name="EPS")
    fecha_ultimo_examen = models.DateField(null=True, blank=True, verbose_name="Fecha último Examen")
    resultado_anterior = models.CharField(max_length=50, default='NO APLICA', verbose_name="Resultado Anterior")
    
    # Características de exposición
    caracteristica_exposicion = models.TextField(blank=True, verbose_name="Característica Exposición")
    riesgos_ocupacionales = models.TextField(blank=True, verbose_name="Riesgos Ocupacionales")
    
    # Elementos de protección personal
    uso_mascarilla = models.BooleanField(default=False, verbose_name="Mascarilla")
    uso_respirador = models.BooleanField(default=False, verbose_name="Respirador")
    uso_otros_epp = models.BooleanField(default=False, verbose_name="Otros EPP")
    otros_epp_cual = models.CharField(max_length=200, blank=True, verbose_name="¿Cuál?")
    
    # Factores de riesgo
    factor_polvo = models.BooleanField(default=False, verbose_name="Polvo")
    factor_humos = models.BooleanField(default=False, verbose_name="Humos")
    factor_gases = models.BooleanField(default=False, verbose_name="Gases")
    factor_vapores = models.BooleanField(default=False, verbose_name="Vapores")
    factor_neblinas = models.BooleanField(default=False, verbose_name="Neblinas")
    tiempo_exposicion_anos = models.PositiveIntegerField(null=True, blank=True, verbose_name="Tiempo Exposición (Años)")
    tiempo_exposicion_meses = models.PositiveIntegerField(null=True, blank=True, verbose_name="Tiempo Exposición (Meses)")
    
    # Hábitos personales
    fuma_tabaco = models.BooleanField(default=False, verbose_name="¿Fuma cigarrillo, tabaco o pipa?")
    fuma_cantidad = models.CharField(max_length=50, blank=True, verbose_name="Cantidad")
    fuma_tiempo = models.CharField(max_length=50, blank=True, verbose_name="¿Hace cuánto tiempo?")
    es_exfumador = models.BooleanField(default=False, verbose_name="¿Es exfumador?")
    exfumador_cantidad = models.CharField(max_length=50, blank=True, verbose_name="Cantidad (exfumador)")
    ano_dejo_fumar = models.PositiveIntegerField(null=True, blank=True, verbose_name="Año en que dejó de fumar")
    practica_deporte = models.BooleanField(default=False, verbose_name="¿Practica algún deporte?")
    deporte_horas_semana = models.CharField(max_length=50, blank=True, verbose_name="Horas/Semana")
    deporte_cual = models.CharField(max_length=100, blank=True, verbose_name="¿Cuál deporte?")
    cocina_lena = models.BooleanField(default=False, verbose_name="¿Cocina o cocinó con leña?")
    lena_tiempo_exposicion = models.CharField(max_length=50, blank=True, verbose_name="Tiempo de exposición leña")
    
    # Sintomatología
    dificultad_respirar = models.BooleanField(default=False, verbose_name="Dificultad al respirar")
    dificultad_esfuerzo_fisico = models.BooleanField(default=False, verbose_name="Con el esfuerzo físico")
    tos_frecuente = models.BooleanField(default=False, verbose_name="Tos frecuente")
    tos_con_esputo = models.BooleanField(default=False, verbose_name="Con esputo")
    enfermedad_cardiaca = models.BooleanField(default=False, verbose_name="Enfermedad cardíaca")
    enfermedad_cardiaca_cual = models.CharField(max_length=200, blank=True, verbose_name="¿Cuál enfermedad cardíaca?")
    dolor_respirar = models.BooleanField(default=False, verbose_name="Dolor al respirar")
    dolor_respirar_donde = models.CharField(max_length=200, blank=True, verbose_name="¿Dónde duele?")
    alergia_respiratoria = models.BooleanField(default=False, verbose_name="Alergia respiratoria")
    alergia_respiratoria_que = models.CharField(max_length=200, blank=True, verbose_name="¿A qué?")
    asma = models.BooleanField(default=False, verbose_name="Asma")
    asma_edad_ultima_crisis = models.CharField(max_length=50, blank=True, verbose_name="Edad última crisis")
    otra_enfermedad_respiratoria = models.BooleanField(default=False, verbose_name="Otra enfermedad respiratoria")
    otra_enfermedad_cual = models.CharField(max_length=200, blank=True, verbose_name="¿Cuál otra enfermedad?")
    
    # Valores observados de espirometría
    cvf_pre = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="CVF PRE (Lt)")
    cvf_post = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="CVF POST (Lt)")
    cvf_teor = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="CVF TEOR (Lt)")
    cvf_observaciones = models.TextField(blank=True, verbose_name="CVF Observaciones")
    
    vef1_pre = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="VEF1 PRE (Lt)")
    vef1_post = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="VEF1 POST (Lt)")
    vef1_teor = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="VEF1 TEOR (Lt)")
    vef1_observaciones = models.TextField(blank=True, verbose_name="VEF1 Observaciones")
    
    vef1_cvf_pre = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="VEF1/CVF(%) PRE")
    vef1_cvf_post = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="VEF1/CVF(%) POST")
    vef1_cvf_teor = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="VEF1/CVF(%) TEOR")
    vef1_cvf_observaciones = models.TextField(blank=True, verbose_name="VEF1/CVF Observaciones")
    
    fef_25_75_pre = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="FEF 25-75 PRE (Lt/SEG)")
    fef_25_75_post = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="FEF 25-75 POST (Lt/SEG)")
    fef_25_75_teor = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="FEF 25-75 TEOR (Lt/SEG)")
    fef_25_75_observaciones = models.TextField(blank=True, verbose_name="FEF 25-75 Observaciones")
    
    # Interpretación
    marca_espirometro = models.CharField(max_length=200, blank=True, verbose_name="Marca y referencia espirómetro utilizado")
    fecha_ultima_calibracion = models.DateField(null=True, blank=True, verbose_name="F Última Calibración")
    escala_interpretacion = models.CharField(max_length=20, choices=ESCALA_INTERPRETACION_CHOICES, default='KNUDSON', verbose_name="Escala interpretación")
    patron_funcional = models.CharField(max_length=20, choices=PATRON_FUNCIONAL_CHOICES, blank=True, verbose_name="Patrón Funcional")
    severidad = models.CharField(max_length=20, choices=SEVERIDAD_CHOICES, blank=True, verbose_name="Severidad")
    
    # Observaciones y archivos
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    resultado_archivo = models.FileField(upload_to='espirometrias/', blank=True, null=True, verbose_name="Resultado del Espirómetro")
    
    # Via de ingreso y otros campos para RIPS
    via_ingreso = models.CharField(max_length=10, default='01', verbose_name="Vía de Ingreso")
    finalidad_consulta = models.CharField(max_length=10, default='15', verbose_name="Finalidad de la Consulta")
    causa_externa = models.CharField(max_length=10, default='38', verbose_name="Causa Externa")
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Espirometría"
        verbose_name_plural = "Espirometrías"
    
    def __str__(self):
        return f"Espirometría - {self.ficha_clinica.nombre_trabajador}"
    
    def calcular_imc(self):
        """Calcular IMC automáticamente"""
        if self.peso_kg and self.talla_cm:
            talla_m = float(self.talla_cm) / 100
            imc = float(self.peso_kg) / (talla_m ** 2)
            return round(imc, 2)
        return None
    
    def interpretar_patron_funcional(self):
        """Interpretar patrón funcional basado en valores espirométricos"""
        if not (self.vef1_post and self.cvf_post and self.vef1_cvf_post):
            return 'NORMAL'
        
        vef1_cvf_ratio = float(self.vef1_cvf_post)
        vef1_percent = self.calcular_porcentaje_predicho('vef1')
        cvf_percent = self.calcular_porcentaje_predicho('cvf')
        
        # Criterios estándar de interpretación
        if vef1_cvf_ratio < 70:  # Obstrucción
            if cvf_percent < 80:  # También hay restricción
                return 'MIXTO'
            else:
                return 'OBSTRUCTIVO'
        elif cvf_percent < 80:  # Solo restricción
            return 'RESTRICTIVO'
        else:
            return 'NORMAL'
    
    def calcular_porcentaje_predicho(self, parametro):
        """Calcular porcentaje del valor predicho"""
        if parametro == 'vef1' and self.vef1_post and self.vef1_teor:
            return (float(self.vef1_post) / float(self.vef1_teor)) * 100
        elif parametro == 'cvf' and self.cvf_post and self.cvf_teor:
            return (float(self.cvf_post) / float(self.cvf_teor)) * 100
        return None
    
    def calcular_severidad(self):
        """Calcular severidad basada en VEF1"""
        vef1_percent = self.calcular_porcentaje_predicho('vef1')
        if not vef1_percent:
            return None
        
        if vef1_percent >= 80:
            return 'LEVE'
        elif vef1_percent >= 50:
            return 'MODERADO'
        elif vef1_percent >= 30:
            return 'SEVERO'
        else:
            return 'MUY_SEVERO'
    
    def save(self, *args, **kwargs):
        # Auto-calcular IMC
        if not self.imc:
            calculated_imc = self.calcular_imc()
            if calculated_imc:
                self.imc = calculated_imc
        
        # Auto-interpretar patrón funcional si no está definido
        if not self.patron_funcional:
            self.patron_funcional = self.interpretar_patron_funcional()
        
        # Auto-calcular severidad si no está definida
        if not self.severidad:
            calculated_severity = self.calcular_severidad()
            if calculated_severity:
                self.severidad = calculated_severity
        
        super().save(*args, **kwargs)


class RecomendacionEspirometria(models.Model):
    """Recomendaciones específicas de espirometría"""
    
    TIPO_RECOMENDACION_CHOICES = [
        ('CONTROL', 'Control'),
        ('TRATAMIENTO', 'Tratamiento'),
        ('EXAMEN', 'Examen'),
        ('REMISION', 'Remisión'),
        ('PREVENCION', 'Prevención'),
    ]
    
    espirometria = models.ForeignKey(Espirometria, on_delete=models.CASCADE, related_name='recomendaciones_espirometria')
    recomendacion = models.TextField(verbose_name="Recomendación")
    tipo = models.CharField(max_length=20, choices=TIPO_RECOMENDACION_CHOICES, verbose_name="Tipo")
    fecha = models.DateField(auto_now_add=True, verbose_name="Fecha")
    
    class Meta:
        verbose_name = "Recomendación Espirometría"
        verbose_name_plural = "Recomendaciones Espirometría"


class EvaluacionOsteomuscular(models.Model):
    """Evaluación Osteomuscular completa con evaluación postural, movilidad articular y pruebas"""
    
    RESULTADO_PRUEBA_CHOICES = [
        ('NORMAL', 'Normal'),
        ('ALTERADO', 'Alterado'),
        ('POSITIVO', 'Positivo'),
        ('NEGATIVO', 'Negativo'),
        ('NO_EVALUADO', 'No Evaluado'),
    ]
    
    GRADO_FLEXIBILIDAD_CHOICES = [
        ('LEVE', 'Leve'),
        ('MODERADO', 'Moderado'),
        ('SEVERO', 'Severo'),
        ('NO_APLICA', 'No Aplica'),
    ]
    
    FASE_MARCHA_CHOICES = [
        ('NORMAL', 'Normal'),
        ('ALTERADA', 'Alterada'),
        ('NO_EVALUADA', 'No Evaluada'),
    ]
    
    # Relación con ficha clínica base
    ficha_clinica = models.OneToOneField(FichaClinica, on_delete=models.CASCADE, related_name='evaluacion_osteomuscular')
    
    # Información básica del examen
    producto = models.CharField(max_length=200, blank=True, verbose_name="Producto")
    peso_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Peso (kg)")
    talla_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Talla (cm)")
    imc = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Índice de masa corporal (IMC)")
    funciones_cargo = models.TextField(blank=True, verbose_name="Funciones del Cargo")
    
    # Evaluación Postural - Diagrama anatómico
    evaluacion_postural_observaciones = models.TextField(blank=True, verbose_name="Observaciones Evaluación Postural")
    postura_anterior = models.JSONField(default=dict, blank=True, verbose_name="Alteraciones Vista Anterior")
    postura_posterior = models.JSONField(default=dict, blank=True, verbose_name="Alteraciones Vista Posterior")
    postura_lateral_izq = models.JSONField(default=dict, blank=True, verbose_name="Alteraciones Vista Lateral Izquierda")
    postura_lateral_der = models.JSONField(default=dict, blank=True, verbose_name="Alteraciones Vista Lateral Derecha")
    
    # Movilidad Articular - Medidas de longitud
    longitud_real = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Longitud Real")
    longitud_aparente = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Longitud Aparente")
    
    # Medidas de flexibilidad específicas con diagramas
    extensibilidad = models.CharField(max_length=20, choices=GRADO_FLEXIBILIDAD_CHOICES, blank=True, verbose_name="Extensibilidad")
    extensibilidad_observaciones = models.TextField(blank=True, verbose_name="Observaciones Extensibilidad")
    
    flexibilidad_columna = models.CharField(max_length=20, choices=GRADO_FLEXIBILIDAD_CHOICES, blank=True, verbose_name="Flexibilidad de Columna")
    flexibilidad_columna_observaciones = models.TextField(blank=True, verbose_name="Observaciones Flexibilidad Columna")
    
    flexibilidad_hombros_izq = models.CharField(max_length=20, choices=GRADO_FLEXIBILIDAD_CHOICES, blank=True, verbose_name="Flexibilidad Hombros Izq")
    flexibilidad_hombros_der = models.CharField(max_length=20, choices=GRADO_FLEXIBILIDAD_CHOICES, blank=True, verbose_name="Flexibilidad Hombros Der")
    flexibilidad_hombros_observaciones = models.TextField(blank=True, verbose_name="Observaciones Flexibilidad Hombros")
    
    aductores_izq = models.CharField(max_length=20, choices=GRADO_FLEXIBILIDAD_CHOICES, blank=True, verbose_name="Aductores Izquierda")
    aductores_der = models.CharField(max_length=20, choices=GRADO_FLEXIBILIDAD_CHOICES, blank=True, verbose_name="Aductores Derecha")
    aductores_observaciones = models.TextField(blank=True, verbose_name="Observaciones Aductores")
    
    gastrocnemios_izq = models.CharField(max_length=20, choices=GRADO_FLEXIBILIDAD_CHOICES, blank=True, verbose_name="Gastrocnemios Izquierda")
    gastrocnemios_der = models.CharField(max_length=20, choices=GRADO_FLEXIBILIDAD_CHOICES, blank=True, verbose_name="Gastrocnemios Derecha")
    gastrocnemios_observaciones = models.TextField(blank=True, verbose_name="Observaciones Gastrocnemios")
    
    isquiotibiales_izq = models.CharField(max_length=20, choices=GRADO_FLEXIBILIDAD_CHOICES, blank=True, verbose_name="Isquiotibiales Izquierda")
    isquiotibiales_der = models.CharField(max_length=20, choices=GRADO_FLEXIBILIDAD_CHOICES, blank=True, verbose_name="Isquiotibiales Derecha")
    isquiotibiales_observaciones = models.TextField(blank=True, verbose_name="Observaciones Isquiotibiales")
    
    # Pruebas de Flexibilidad - Semiológicas
    bostezo_medial_izq = models.CharField(max_length=20, choices=RESULTADO_PRUEBA_CHOICES, blank=True, verbose_name="Bostezo Medial Izquierda")
    bostezo_medial_der = models.CharField(max_length=20, choices=RESULTADO_PRUEBA_CHOICES, blank=True, verbose_name="Bostezo Medial Derecha")
    
    bostezo_lateral_izq = models.CharField(max_length=20, choices=RESULTADO_PRUEBA_CHOICES, blank=True, verbose_name="Bostezo Lateral Izquierda")
    bostezo_lateral_der = models.CharField(max_length=20, choices=RESULTADO_PRUEBA_CHOICES, blank=True, verbose_name="Bostezo Lateral Derecha")
    
    cajon_anterior_izq = models.CharField(max_length=20, choices=RESULTADO_PRUEBA_CHOICES, blank=True, verbose_name="Cajón Anterior Izquierda")
    cajon_anterior_der = models.CharField(max_length=20, choices=RESULTADO_PRUEBA_CHOICES, blank=True, verbose_name="Cajón Anterior Derecha")
    
    cajon_posterior_izq = models.CharField(max_length=20, choices=RESULTADO_PRUEBA_CHOICES, blank=True, verbose_name="Cajón Posterior Izquierda")
    cajon_posterior_der = models.CharField(max_length=20, choices=RESULTADO_PRUEBA_CHOICES, blank=True, verbose_name="Cajón Posterior Derecha")
    
    thomas_izq = models.CharField(max_length=20, choices=RESULTADO_PRUEBA_CHOICES, blank=True, verbose_name="Thomas Izquierda")
    thomas_der = models.CharField(max_length=20, choices=RESULTADO_PRUEBA_CHOICES, blank=True, verbose_name="Thomas Derecha")
    
    ober_izq = models.CharField(max_length=20, choices=RESULTADO_PRUEBA_CHOICES, blank=True, verbose_name="Ober Izquierda")
    ober_der = models.CharField(max_length=20, choices=RESULTADO_PRUEBA_CHOICES, blank=True, verbose_name="Ober Derecha")
    
    ely_izq = models.CharField(max_length=20, choices=RESULTADO_PRUEBA_CHOICES, blank=True, verbose_name="Ely Izquierda")
    ely_der = models.CharField(max_length=20, choices=RESULTADO_PRUEBA_CHOICES, blank=True, verbose_name="Ely Derecha")
    
    lasegue_izq = models.CharField(max_length=20, choices=RESULTADO_PRUEBA_CHOICES, blank=True, verbose_name="Laségue Izquierda")
    lasegue_der = models.CharField(max_length=20, choices=RESULTADO_PRUEBA_CHOICES, blank=True, verbose_name="Laségue Derecha")
    
    # Fase de Apoyo
    choque_talon_izq = models.CharField(max_length=20, choices=FASE_MARCHA_CHOICES, blank=True, verbose_name="Choque de Talón Izquierda")
    choque_talon_der = models.CharField(max_length=20, choices=FASE_MARCHA_CHOICES, blank=True, verbose_name="Choque de Talón Derecha")
    
    apoyo_plantar_izq = models.CharField(max_length=20, choices=FASE_MARCHA_CHOICES, blank=True, verbose_name="Apoyo Plantar Izquierda")
    apoyo_plantar_der = models.CharField(max_length=20, choices=FASE_MARCHA_CHOICES, blank=True, verbose_name="Apoyo Plantar Derecha")
    
    apoyo_medio_izq = models.CharField(max_length=20, choices=FASE_MARCHA_CHOICES, blank=True, verbose_name="Apoyo Medio Izquierda")
    apoyo_medio_der = models.CharField(max_length=20, choices=FASE_MARCHA_CHOICES, blank=True, verbose_name="Apoyo Medio Derecha")
    
    empuje_izq = models.CharField(max_length=20, choices=FASE_MARCHA_CHOICES, blank=True, verbose_name="Empuje Izquierda")
    empuje_der = models.CharField(max_length=20, choices=FASE_MARCHA_CHOICES, blank=True, verbose_name="Empuje Derecha")
    
    # Fase de Balanceo
    aceleracion_izq = models.CharField(max_length=20, choices=FASE_MARCHA_CHOICES, blank=True, verbose_name="Aceleración Izquierda")
    aceleracion_der = models.CharField(max_length=20, choices=FASE_MARCHA_CHOICES, blank=True, verbose_name="Aceleración Derecha")
    
    balanceo_medio_izq = models.CharField(max_length=20, choices=FASE_MARCHA_CHOICES, blank=True, verbose_name="Balanceo Medio Izquierda")
    balanceo_medio_der = models.CharField(max_length=20, choices=FASE_MARCHA_CHOICES, blank=True, verbose_name="Balanceo Medio Derecha")
    
    desaceleracion_izq = models.CharField(max_length=20, choices=FASE_MARCHA_CHOICES, blank=True, verbose_name="Desaceleración Izquierda")
    desaceleracion_der = models.CharField(max_length=20, choices=FASE_MARCHA_CHOICES, blank=True, verbose_name="Desaceleración Derecha")
    
    # Observaciones generales y recomendaciones
    observaciones = models.TextField(blank=True, verbose_name="Observaciones y Recomendaciones")
    
    # Via de ingreso y otros campos para RIPS
    via_ingreso = models.CharField(max_length=10, default='01', verbose_name="Vía de Ingreso")
    finalidad_consulta = models.CharField(max_length=10, default='15', verbose_name="Finalidad de la Consulta")
    causa_externa = models.CharField(max_length=10, default='38', verbose_name="Causa Externa")
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Evaluación Osteomuscular"
        verbose_name_plural = "Evaluaciones Osteomusculares"
    
    def __str__(self):
        return f"Evaluación Osteomuscular - {self.ficha_clinica.nombre_trabajador}"
    
    def calcular_imc(self):
        """Calcular IMC automáticamente"""
        if self.peso_kg and self.talla_cm:
            talla_m = float(self.talla_cm) / 100
            imc = float(self.peso_kg) / (talla_m ** 2)
            return round(imc, 2)
        return None
    
    def get_alteraciones_posturales_total(self):
        """Contar total de alteraciones posturales encontradas"""
        total_alteraciones = 0
        for vista in [self.postura_anterior, self.postura_posterior, self.postura_lateral_izq, self.postura_lateral_der]:
            if isinstance(vista, dict):
                total_alteraciones += len([k for k, v in vista.items() if v])
        return total_alteraciones
    
    def get_pruebas_positivas(self):
        """Obtener lista de pruebas semiológicas positivas"""
        pruebas_positivas = []
        
        # Verificar todas las pruebas semiológicas
        pruebas = [
            ('Bostezo Medial', self.bostezo_medial_izq, self.bostezo_medial_der),
            ('Bostezo Lateral', self.bostezo_lateral_izq, self.bostezo_lateral_der),
            ('Cajón Anterior', self.cajon_anterior_izq, self.cajon_anterior_der),
            ('Cajón Posterior', self.cajon_posterior_izq, self.cajon_posterior_der),
            ('Thomas', self.thomas_izq, self.thomas_der),
            ('Ober', self.ober_izq, self.ober_der),
            ('Ely', self.ely_izq, self.ely_der),
            ('Laségue', self.lasegue_izq, self.lasegue_der),
        ]
        
        for nombre_prueba, resultado_izq, resultado_der in pruebas:
            if resultado_izq == 'POSITIVO':
                pruebas_positivas.append(f"{nombre_prueba} Izquierda")
            if resultado_der == 'POSITIVO':
                pruebas_positivas.append(f"{nombre_prueba} Derecha")
        
        return pruebas_positivas
    
    def get_alteraciones_marcha(self):
        """Obtener alteraciones en la marcha"""
        alteraciones_marcha = []
        
        # Fase de apoyo
        fases_apoyo = [
            ('Choque de Talón', self.choque_talon_izq, self.choque_talon_der),
            ('Apoyo Plantar', self.apoyo_plantar_izq, self.apoyo_plantar_der),
            ('Apoyo Medio', self.apoyo_medio_izq, self.apoyo_medio_der),
            ('Empuje', self.empuje_izq, self.empuje_der),
        ]
        
        # Fase de balanceo
        fases_balanceo = [
            ('Aceleración', self.aceleracion_izq, self.aceleracion_der),
            ('Balanceo Medio', self.balanceo_medio_izq, self.balanceo_medio_der),
            ('Desaceleración', self.desaceleracion_izq, self.desaceleracion_der),
        ]
        
        for nombre_fase, resultado_izq, resultado_der in fases_apoyo + fases_balanceo:
            if resultado_izq == 'ALTERADA':
                alteraciones_marcha.append(f"{nombre_fase} Izquierda")
            if resultado_der == 'ALTERADA':
                alteraciones_marcha.append(f"{nombre_fase} Derecha")
        
        return alteraciones_marcha
    
    def get_resumen_flexibilidad(self):
        """Obtener resumen de alteraciones de flexibilidad"""
        alteraciones_flexibilidad = []
        
        flexibilidades = [
            ('Extensibilidad', self.extensibilidad),
            ('Flexibilidad Columna', self.flexibilidad_columna),
            ('Aductores Izq', self.aductores_izq),
            ('Aductores Der', self.aductores_der),
            ('Gastrocnemios Izq', self.gastrocnemios_izq),
            ('Gastrocnemios Der', self.gastrocnemios_der),
            ('Isquiotibiales Izq', self.isquiotibiales_izq),
            ('Isquiotibiales Der', self.isquiotibiales_der),
            ('Flexibilidad Hombros Izq', self.flexibilidad_hombros_izq),
            ('Flexibilidad Hombros Der', self.flexibilidad_hombros_der),
        ]
        
        for nombre, valor in flexibilidades:
            if valor and valor != 'NO_APLICA':
                alteraciones_flexibilidad.append(f"{nombre}: {valor}")
        
        return alteraciones_flexibilidad
    
    def save(self, *args, **kwargs):
        # Auto-calcular IMC
        if not self.imc:
            calculated_imc = self.calcular_imc()
            if calculated_imc:
                self.imc = calculated_imc
        
        super().save(*args, **kwargs)


class RecomendacionOsteomuscular(models.Model):
    """Recomendaciones específicas de evaluación osteomuscular"""
    
    TIPO_RECOMENDACION_CHOICES = [
        ('FISIOTERAPIA', 'Fisioterapia'),
        ('ERGONOMIA', 'Ergonomía'),
        ('CONTROL_MEDICO', 'Control Médico'),
        ('EJERCICIO', 'Ejercicio Terapéutico'),
        ('DESCANSO', 'Descanso Laboral'),
        ('ADAPTACION', 'Adaptación Laboral'),
        ('REMISION', 'Remisión Especialista'),
    ]
    
    evaluacion_osteomuscular = models.ForeignKey(EvaluacionOsteomuscular, on_delete=models.CASCADE, related_name='recomendaciones_osteomusculares')
    recomendacion = models.TextField(verbose_name="Recomendación")
    tipo = models.CharField(max_length=20, choices=TIPO_RECOMENDACION_CHOICES, verbose_name="Tipo")
    fecha = models.DateField(auto_now_add=True, verbose_name="Fecha")
    
    class Meta:
        verbose_name = "Recomendación Osteomuscular"
        verbose_name_plural = "Recomendaciones Osteomusculares"


class HistoriaClinicaGeneral(models.Model):
    """Historia Clínica General completa con todos los componentes médicos"""
    
    TIPO_EVALUACION_CHOICES = [
        ('PREOCUPACIONAL', 'Pre-ocupacional'),
        ('OCUPACIONAL', 'Ocupacional'),
        ('POSTOCUPACIONAL', 'Post-ocupacional'),
        ('CONSULTA_EXTERNA', 'Consulta Externa'),
        ('URGENCIAS', 'Urgencias'),
    ]
    
    ESTADO_CIVIL_CHOICES = [
        ('SOLTERO', 'Soltero/a'),
        ('CASADO', 'Casado/a'),
        ('UNION_LIBRE', 'Unión Libre'),
        ('SEPARADO', 'Separado/a'),
        ('DIVORCIADO', 'Divorciado/a'),
        ('VIUDO', 'Viudo/a'),
    ]
    
    NIVEL_EDUCATIVO_CHOICES = [
        ('PRIMARIA', 'Primaria'),
        ('SECUNDARIA', 'Secundaria'),
        ('TECNICO', 'Técnico'),
        ('TECNOLOGICO', 'Tecnológico'),
        ('UNIVERSITARIO', 'Universitario'),
        ('POSTGRADO', 'Postgrado'),
    ]
    
    LATERALIDAD_CHOICES = [
        ('DIESTRO', 'Diestro'),
        ('ZURDO', 'Zurdo'),
        ('AMBIDIESTRO', 'Ambidiestro'),
    ]
    
    CLASIFICACION_TA_CHOICES = [
        ('NORMAL', 'Normal'),
        ('PREHIPERTENSION', 'Prehipertensión'),
        ('HTA_GRADO_1', 'HTA Grado 1'),
        ('HTA_GRADO_2', 'HTA Grado 2'),
        ('CRISIS_HIPERTENSIVA', 'Crisis Hipertensiva'),
    ]
    
    # Relación con ficha clínica base
    ficha_clinica = models.OneToOneField(FichaClinica, on_delete=models.CASCADE, related_name='historia_clinica_general')
    
    # Información básica adicional
    tipo_evaluacion_medica = models.CharField(max_length=20, choices=TIPO_EVALUACION_CHOICES, default='CONSULTA_EXTERNA')
    estado_civil = models.CharField(max_length=15, choices=ESTADO_CIVIL_CHOICES, blank=True)
    nivel_educativo = models.CharField(max_length=15, choices=NIVEL_EDUCATIVO_CHOICES, blank=True)
    eps = models.CharField(max_length=100, blank=True, verbose_name="EPS")
    afp = models.CharField(max_length=100, blank=True, verbose_name="AFP")
    arl = models.CharField(max_length=100, blank=True, verbose_name="ARL")
    funciones_cargo = models.TextField(blank=True, verbose_name="Funciones del Cargo")
    
    # Motivo de consulta y enfermedad actual
    motivo_consulta = models.TextField(blank=True, verbose_name="Motivo de Consulta")
    enfermedad_actual = models.TextField(blank=True, verbose_name="Enfermedad Actual")
    
    # Signos Vitales
    tension_sistolica = models.PositiveIntegerField(null=True, blank=True, verbose_name="Tensión Sistólica (mmHg)")
    tension_diastolica = models.PositiveIntegerField(null=True, blank=True, verbose_name="Tensión Diastólica (mmHg)")
    clasificacion_ta = models.CharField(max_length=20, choices=CLASIFICACION_TA_CHOICES, blank=True, verbose_name="Clasificación TA")
    frecuencia_cardiaca = models.PositiveIntegerField(null=True, blank=True, verbose_name="Frecuencia Cardíaca (x min)")
    frecuencia_respiratoria = models.PositiveIntegerField(null=True, blank=True, verbose_name="Frecuencia Respiratoria (x min)")
    pulsioximetria = models.PositiveIntegerField(null=True, blank=True, verbose_name="Pulsioximetría (%)")
    temperatura = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name="Temperatura (°C)")
    lateralidad_dominante = models.CharField(max_length=12, choices=LATERALIDAD_CHOICES, default='DIESTRO', verbose_name="Lateralidad Dominante")
    
    # Antropometría
    peso_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Peso (kg)")
    talla_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Talla (cm)")
    imc = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="IMC")
    perimetro_abdominal = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Perímetro Abdominal (cm)")
    interpretacion_perimetro = models.CharField(max_length=100, blank=True, verbose_name="Interpretación Perímetro Abdominal")
    
    # Revisión por Sistemas - JSON para flexibilidad
    revision_sistemas = models.JSONField(default=dict, blank=True, verbose_name="Revisión por Sistemas")
    
    # Examen Físico por Segmentos - JSON para flexibilidad  
    examen_fisico = models.JSONField(default=dict, blank=True, verbose_name="Examen Físico")
    
    # Paraclínicos
    observaciones_paraclinicos = models.TextField(blank=True, verbose_name="Observaciones Paraclínicos")
    
    # Campos para RIPS
    via_ingreso = models.CharField(max_length=10, default='01', verbose_name="Vía de Ingreso")
    finalidad_consulta = models.CharField(max_length=10, default='10', verbose_name="Finalidad de la Consulta")
    causa_externa = models.CharField(max_length=10, default='15', verbose_name="Causa Externa")
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Historia Clínica General"
        verbose_name_plural = "Historias Clínicas Generales"
    
    def __str__(self):
        return f"Historia Clínica General - {self.ficha_clinica.nombre_trabajador}"
    
    def calcular_imc(self):
        """Calcular IMC automáticamente"""
        if self.peso_kg and self.talla_cm:
            talla_m = float(self.talla_cm) / 100
            imc = float(self.peso_kg) / (talla_m ** 2)
            return round(imc, 2)
        return None
    
    def clasificar_tension_arterial(self):
        """Clasificar tensión arterial según guías"""
        if not self.tension_sistolica or not self.tension_diastolica:
            return None
        
        sistolica = self.tension_sistolica
        diastolica = self.tension_diastolica
        
        if sistolica < 120 and diastolica < 80:
            return 'NORMAL'
        elif sistolica < 140 or diastolica < 90:
            return 'PREHIPERTENSION'
        elif sistolica < 160 or diastolica < 100:
            return 'HTA_GRADO_1'
        elif sistolica < 180 or diastolica < 110:
            return 'HTA_GRADO_2'
        else:
            return 'CRISIS_HIPERTENSIVA'
    
    def interpretar_perimetro_abdominal(self):
        """Interpretar perímetro abdominal según género"""
        if not self.perimetro_abdominal:
            return None
        
        perimetro = float(self.perimetro_abdominal)
        genero = self.ficha_clinica.genero
        
        if genero == 'M':  # Masculino
            if perimetro < 94:
                return 'Normal'
            elif perimetro < 102:
                return 'Riesgo aumentado'
            else:
                return 'Riesgo muy aumentado'
        elif genero == 'F':  # Femenino
            if perimetro < 80:
                return 'Normal'
            elif perimetro < 88:
                return 'Riesgo aumentado'
            else:
                return 'Riesgo muy aumentado'
        
        return 'No determinado'
    
    def get_revision_sistemas_defaults(self):
        """Obtener valores por defecto para revisión por sistemas"""
        return {
            'epilepsia_convulsiones': False,
            'deformidades_amputaciones': False,
            'cardiovascular': 'ASINTOMÁTICO',
            'dermatologico': 'ASINTOMÁTICO',
            'digestivo': 'ASINTOMÁTICO',
            'genitourinario': 'ASINTOMÁTICO',
            'neurologico': 'ASINTOMÁTICO',
            'ocular': 'ASINTOMÁTICO',
            'otorrinolaringologico': 'ASINTOMÁTICO',
            'osteomuscular': 'ASINTOMÁTICO',
            'respiratorio': 'ASINTOMÁTICO',
            'otros_sistemas': '',
            'observaciones': ''
        }
    
    def get_examen_fisico_defaults(self):
        """Obtener valores por defecto para examen físico"""
        return {
            'tegumentario': {'atrofia': 'NORMAL', 'otro': ''},
            'cabeza': {'cuero_cabelludo': 'NORMAL', 'otro': ''},
            'ojos': {
                'escleras_color': 'ANICTERICAS',
                'estrabismo': False,
                'hiperemia_conjuntival': False,
                'pupilas_normorreactivas': True,
                'otro': ''
            },
            'oidos': {
                'pabellon': 'NORMAL',
                'audicion': 'NORMAL',
                'otoscopia': 'NORMAL',
                'otro': ''
            },
            'nariz': {
                'tabique': 'NORMAL',
                'rinorrea': False,
                'sangrado_epistaxis': False,
                'otro': ''
            },
            'boca': {
                'mucosa_oral': 'HÚMEDA',
                'dentadura': 'COMPLETA',
                'otro': ''
            },
            'cuello': {
                'movilidad': 'NORMAL',
                'masas': False,
                'adenopatias': False,
                'ingurgitacion_yugular': False,
                'otro': ''
            },
            'torax': {
                'expansion_toracica': 'SIMÉTRICA NORMAL',
                'ganglios_axilares': 'NEGATIVO',
                'mamas_pezon': 'NORMALES',
                'otro': ''
            },
            'cardio_pulmonar': {
                'ruidos_cardiacos': 'RÍTMICOS, BIEN TIMBRADOS, SIN SOPLOS',
                'auscultacion_pulmonar': 'RUIDOS RESPIRATORIOS NORMALES SIN AGREGADOS',
                'otro': ''
            },
            'abdomen': {
                'inspeccion': 'NORMAL',
                'palpacion': 'BLANDO, NO DOLOROSO, NO MASAS, NO MEGALIAS',
                'auscultacion': 'RUIDOS INTESTINALES PRESENTES NORMALES',
                'otro': ''
            },
            'genitales': {
                'genitales_externos': 'NORMAL',
                'otro': ''
            },
            'neurologico': {
                'fuerza_muscular': 'NORMAL',
                'sensibilidad': 'CONSERVADA NORMAL',
                'otro': ''
            },
            'extremidades': {
                'inspeccion': 'SIMÉTRICAS, EUTRÓFICAS',
                'deformidad': False,
                'edemas': False,
                'otro': ''
            },
            'osteomuscular': {
                'articulaciones': 'NORMAL',
                'otro': ''
            },
            'otros_hallazgos': {
                'observaciones': '',
                'otro': ''
            }
        }
    
    def save(self, *args, **kwargs):
        # Auto-calcular IMC
        if not self.imc:
            calculated_imc = self.calcular_imc()
            if calculated_imc:
                self.imc = calculated_imc
        
        # Auto-clasificar tensión arterial
        if not self.clasificacion_ta:
            clasificacion = self.clasificar_tension_arterial()
            if clasificacion:
                self.clasificacion_ta = clasificacion
        
        # Auto-interpretar perímetro abdominal
        if not self.interpretacion_perimetro:
            interpretacion = self.interpretar_perimetro_abdominal()
            if interpretacion:
                self.interpretacion_perimetro = interpretacion
        
        # Inicializar JSON fields si están vacíos
        if not self.revision_sistemas:
            self.revision_sistemas = self.get_revision_sistemas_defaults()
        
        if not self.examen_fisico:
            self.examen_fisico = self.get_examen_fisico_defaults()
        
        super().save(*args, **kwargs)


class AntecedenteFamiliarGeneral(models.Model):
    """Antecedentes familiares para historia clínica general"""
    
    TIPO_ANTECEDENTE_CHOICES = [
        ('HIPERTENSION_ARTERIAL', 'Hipertensión Arterial'),
        ('DIABETES', 'Diabetes'),
        ('CANCER', 'Cáncer'),
        ('OTROS', 'Otros'),
    ]
    
    historia_clinica = models.ForeignKey(HistoriaClinicaGeneral, on_delete=models.CASCADE, related_name='antecedentes_familiares')
    tipo_antecedente = models.CharField(max_length=30, choices=TIPO_ANTECEDENTE_CHOICES, verbose_name="Antecedente")
    observacion = models.TextField(default='NO REFIERE', verbose_name="Observación")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha")
    
    class Meta:
        verbose_name = "Antecedente Familiar General"
        verbose_name_plural = "Antecedentes Familiares Generales"


class AntecedentePersonalGeneral(models.Model):
    """Antecedentes personales para historia clínica general"""
    
    TIPO_ANTECEDENTE_CHOICES = [
        ('HTA', 'Hipertensión Arterial'),
        ('DIABETES', 'Diabetes'),
        ('ENF_RENAL', 'Enfermedad Renal'),
        ('ENF_ARTICULAR', 'Enfermedad Articular'),
        ('TBC', 'Tuberculosis'),
        ('VENEREAS', 'Enfermedades Venéreas'),
        ('SIND_CONVULSIVO', 'Síndrome Convulsivo'),
        ('INMUNOLOGICOS', 'Inmunológicos'),
        ('HOSPITALIZACIONES', 'Hospitalizaciones'),
        ('TOXICOS_ALERGICOS', 'Tóxicos Alérgicos'),
        ('TRAUMATICO', 'Traumático'),
        ('QUIRURGICOS', 'Quirúrgicos'),
        ('OTRO', 'Otro'),
    ]
    
    historia_clinica = models.ForeignKey(HistoriaClinicaGeneral, on_delete=models.CASCADE, related_name='antecedentes_personales')
    tipo_antecedente = models.CharField(max_length=20, choices=TIPO_ANTECEDENTE_CHOICES, verbose_name="Antecedente")
    observacion = models.TextField(default='NO REFIERE', verbose_name="Observación")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha")
    
    class Meta:
        verbose_name = "Antecedente Personal General"
        verbose_name_plural = "Antecedentes Personales Generales"


class DocumentoClinico(models.Model):
    """Documentos externos y paraclínicos"""
    
    historia_clinica = models.ForeignKey(HistoriaClinicaGeneral, on_delete=models.CASCADE, related_name='documentos_clinicos')
    nombre_documento = models.CharField(max_length=200, verbose_name="Nombre del Documento")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    archivo = models.FileField(upload_to='documentos_clinicos/', blank=True, null=True, verbose_name="Archivo")
    usuario_creacion = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Documento Clínico"
        verbose_name_plural = "Documentos Clínicos"


class DiagnosticoGeneral(models.Model):
    """Diagnósticos para historia clínica general"""
    
    TIPO_DIAGNOSTICO_CHOICES = [
        ('PRINCIPAL', 'Principal'),
        ('RELACIONADO_1', 'Relacionado 1'),
        ('RELACIONADO_2', 'Relacionado 2'),
        ('RELACIONADO_3', 'Relacionado 3'),
    ]
    
    TIPO_IMPRESION_CHOICES = [
        ('CONFIRMADO', 'Confirmado'),
        ('IMPRESION_DIAGNOSTICA', 'Impresión Diagnóstica'),
        ('REPETICION', 'Repetición'),
    ]
    
    historia_clinica = models.ForeignKey(HistoriaClinicaGeneral, on_delete=models.CASCADE, related_name='diagnosticos')
    tipo_diagnostico = models.CharField(max_length=15, choices=TIPO_DIAGNOSTICO_CHOICES, verbose_name="Tipo Diagnóstico")
    codigo_cie10 = models.CharField(max_length=10, blank=True, verbose_name="Código CIE-10")
    nombre_diagnostico = models.CharField(max_length=500, verbose_name="Nombre del Diagnóstico")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    tipo_impresion = models.CharField(max_length=25, choices=TIPO_IMPRESION_CHOICES, default='IMPRESION_DIAGNOSTICA', verbose_name="Tipo de Impresión")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha")
    profesional = models.ForeignKey(Prestador, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = "Diagnóstico General"
        verbose_name_plural = "Diagnósticos Generales"


class OrdenMedicamento(models.Model):
    """Órdenes de medicamentos"""
    
    historia_clinica = models.ForeignKey(HistoriaClinicaGeneral, on_delete=models.CASCADE, related_name='ordenes_medicamentos')
    numero_orden = models.PositiveIntegerField(default=1, verbose_name="Número de Orden")
    nombre_medicamento = models.CharField(max_length=200, verbose_name="Nombre del Medicamento")
    cantidad = models.CharField(max_length=50, verbose_name="Cantidad")
    posologia = models.CharField(max_length=200, verbose_name="Posología")
    frecuencia = models.CharField(max_length=100, blank=True, verbose_name="Frecuencia")
    dias = models.PositiveIntegerField(null=True, blank=True, verbose_name="Días")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Orden de Medicamento"
        verbose_name_plural = "Órdenes de Medicamentos"


class OrdenServicioGeneral(models.Model):
    """Órdenes de servicios para historia clínica"""
    
    historia_clinica = models.ForeignKey(HistoriaClinicaGeneral, on_delete=models.CASCADE, related_name='ordenes_servicios')
    numero_orden = models.PositiveIntegerField(default=1, verbose_name="Número de Orden")
    nombre_servicio = models.CharField(max_length=200, verbose_name="Nombre del Servicio")
    cantidad = models.PositiveIntegerField(default=1, verbose_name="Cantidad")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Orden de Servicio General"
        verbose_name_plural = "Órdenes de Servicios Generales"


class OrdenRemision(models.Model):
    """Órdenes de remisión a especialista"""
    
    historia_clinica = models.ForeignKey(HistoriaClinicaGeneral, on_delete=models.CASCADE, related_name='ordenes_remisiones')
    numero_orden = models.PositiveIntegerField(default=1, verbose_name="Número de Orden")
    nombre_especialidad = models.CharField(max_length=100, verbose_name="Nombre de la Especialidad")
    motivo_remision = models.TextField(verbose_name="Motivo de la Remisión")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Orden de Remisión"
        verbose_name_plural = "Órdenes de Remisiones"


class OrdenIncapacidad(models.Model):
    """Órdenes de incapacidad"""
    
    TIPO_INCAPACIDAD_CHOICES = [
        ('ENFERMEDAD_GENERAL', 'Enfermedad General'),
        ('ACCIDENTE_TRABAJO', 'Accidente de Trabajo'),
        ('ENFERMEDAD_LABORAL', 'Enfermedad Laboral'),
        ('LICENCIA_MATERNIDAD', 'Licencia de Maternidad'),
        ('LICENCIA_PATERNIDAD', 'Licencia de Paternidad'),
    ]
    
    historia_clinica = models.ForeignKey(HistoriaClinicaGeneral, on_delete=models.CASCADE, related_name='ordenes_incapacidades')
    numero_orden = models.PositiveIntegerField(default=1, verbose_name="Número de Orden")
    motivo_incapacidad = models.TextField(verbose_name="Motivo de la Incapacidad")
    dias = models.PositiveIntegerField(verbose_name="Días")
    tipo = models.CharField(max_length=20, choices=TIPO_INCAPACIDAD_CHOICES, default='ENFERMEDAD_GENERAL', verbose_name="Tipo")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Orden de Incapacidad"
        verbose_name_plural = "Órdenes de Incapacidades"


class CertificadoMedico(models.Model):
    """Certificados médicos"""
    
    historia_clinica = models.ForeignKey(HistoriaClinicaGeneral, on_delete=models.CASCADE, related_name='certificados_medicos')
    numero_certificado = models.PositiveIntegerField(default=1, verbose_name="Número de Certificado")
    descripcion_certificado = models.TextField(verbose_name="Descripción del Certificado")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Certificado Médico"
        verbose_name_plural = "Certificados Médicos"


class EvolucionGeneral(models.Model):
    """Evoluciones para historia clínica general"""
    
    historia_clinica = models.ForeignKey(HistoriaClinicaGeneral, on_delete=models.CASCADE, related_name='evoluciones')
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha")
    profesional_asistencial = models.ForeignKey(Prestador, on_delete=models.SET_NULL, null=True, verbose_name="Profesional Asistencial")
    evolucion = models.TextField(verbose_name="Evolución")
    
    class Meta:
        verbose_name = "Evolución General"
        verbose_name_plural = "Evoluciones Generales"
        ordering = ['-fecha']