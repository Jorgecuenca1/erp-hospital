from django.db import models
from django.conf import settings
from professionals.models import ProfesionalSalud
from patients.models import Paciente

ESTADO_INCIDENTE_CHOICES = [
    ('REPORTADO', 'Reportado'),
    ('EN_INVESTIGACION', 'En Investigación'),
    ('RESUELTO', 'Resuelto'),
    ('CERRADO', 'Cerrado'),
]

class Incidente(models.Model):
    TIPO_INCIDENTE_CHOICES = [
        ('PACIENTE', 'Incidente con Paciente'),
        ('PERSONAL', 'Incidente con Personal'),
        ('INFRAESTRUCTURA', 'Incidente de Infraestructura'),
        ('EQUIPO', 'Incidente con Equipo'),
        ('SEGURIDAD', 'Incidente de Seguridad'),
        ('OTRO', 'Otro'),
    ]
    SEVERIDAD_CHOICES = [
        ('BAJA', 'Baja'),
        ('MEDIA', 'Media'),
        ('ALTA', 'Alta'),
        ('CRITICA', 'Crítica'),
    ]

    fecha_hora_incidente = models.DateTimeField()
    tipo_incidente = models.CharField(max_length=20, choices=TIPO_INCIDENTE_CHOICES)
    descripcion = models.TextField()
    severidad = models.CharField(max_length=10, choices=SEVERIDAD_CHOICES, default='MEDIA')
    estado = models.CharField(max_length=20, choices=ESTADO_INCIDENTE_CHOICES, default='REPORTADO')
    reportado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='incidentes_reportados')
    fecha_hora_reporte = models.DateTimeField(auto_now_add=True)
    investigador_asignado = models.ForeignKey(ProfesionalSalud, on_delete=models.SET_NULL, null=True, blank=True, related_name='incidentes_investigados')
    fecha_cierre = models.DateTimeField(blank=True, null=True)
    acciones_correctivas = models.TextField(blank=True, null=True)
    paciente_afectado = models.ForeignKey(Paciente, on_delete=models.SET_NULL, null=True, blank=True, related_name='incidentes_afectados')

    class Meta:
        verbose_name = "Incidente"
        verbose_name_plural = "Incidentes"
        ordering = ['fecha_hora_incidente']

    def __str__(self):
        return f"Incidente de {self.get_tipo_incidente_display()} - {self.fecha_hora_incidente.strftime('%Y-%m-%d %H:%M')}"

class Auditoria(models.Model):
    TIPO_AUDITORIA_CHOICES = [
        ('INTERNA', 'Interna'),
        ('EXTERNA', 'Externa'),
    ]
    ESTADO_AUDITORIA_CHOICES = [
        ('PLANIFICADA', 'Planificada'),
        ('EN_PROGRESO', 'En Progreso'),
        ('FINALIZADA', 'Finalizada'),
        ('CANCELADA', 'Cancelada'),
    ]

    nombre = models.CharField(max_length=255)
    tipo_auditoria = models.CharField(max_length=20, choices=TIPO_AUDITORIA_CHOICES)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(blank=True, null=True)
    alcance = models.TextField()
    equipo_auditor = models.ManyToManyField(ProfesionalSalud, related_name='auditorias_participadas')
    estado = models.CharField(max_length=20, choices=ESTADO_AUDITORIA_CHOICES, default='PLANIFICADA')
    documento_informe = models.FileField(upload_to='auditorias/informes/', blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Auditoría"
        verbose_name_plural = "Auditorías"
        ordering = ['fecha_inicio']

    def __str__(self):
        return f"Auditoría {self.nombre} ({self.get_tipo_auditoria_display()}) - {self.fecha_inicio.strftime('%Y-%m-%d')}"

class HallazgoAuditoria(models.Model):
    auditoria = models.ForeignKey(Auditoria, on_delete=models.CASCADE, related_name='hallazgos')
    descripcion = models.TextField()
    clasificacion = models.CharField(max_length=50, help_text="Ej: No Conformidad, Observación, Oportunidad de Mejora")
    evidencia = models.TextField(blank=True, null=True)
    responsable_correccion = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='hallazgos_asignados')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_limite_correccion = models.DateField(blank=True, null=True)
    cerrado = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Hallazgo de Auditoría"
        verbose_name_plural = "Hallazgos de Auditoría"

    def __str__(self):
        return f"Hallazgo en {self.auditoria.nombre} - {self.clasificacion}"

class PlanMejora(models.Model):
    hallazgo = models.OneToOneField(HallazgoAuditoria, on_delete=models.CASCADE, related_name='plan_mejora', null=True, blank=True) # Puede ser un plan de mejora general o vinculado a un hallazgo
    nombre_plan = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_limite = models.DateField()
    responsable = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='planes_mejora_responsable')
    estado = models.CharField(max_length=20, choices=ESTADO_INCIDENTE_CHOICES, default='REPORTADO') # Reutilizamos los estados de incidente para seguimiento
    acciones_implementadas = models.TextField(blank=True, null=True)
    fecha_cierre = models.DateField(blank=True, null=True)
    efectividad = models.CharField(max_length=50, blank=True, null=True, help_text="Ej: Efectivo, Parcialmente Efectivo, No Efectivo")

    class Meta:
        verbose_name = "Plan de Mejora"
        verbose_name_plural = "Planes de Mejora"

    def __str__(self):
        return self.nombre_plan

class DocumentoCalidad(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('MANUAL', 'Manual'),
        ('PROCEDIMIENTO', 'Procedimiento'),
        ('POLITICA', 'Política'),
        ('FORMATO', 'Formato'),
        ('GUIA', 'Guía'),
        ('REGISTRO', 'Registro'),
        ('OTRO', 'Otro'),
    ]

    nombre = models.CharField(max_length=255)
    codigo = models.CharField(max_length=50, unique=True, blank=True, null=True)
    tipo_documento = models.CharField(max_length=20, choices=TIPO_DOCUMENTO_CHOICES)
    version = models.CharField(max_length=10, default='1.0')
    fecha_emision = models.DateField(auto_now_add=True)
    fecha_revision = models.DateField(blank=True, null=True)
    archivo = models.FileField(upload_to='documentos_calidad/')
    aprobado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='documentos_aprobados')
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Documento de Calidad"
        verbose_name_plural = "Documentos de Calidad"
        ordering = ['-fecha_emision']

    def __str__(self):
        return f"{self.nombre} (v{self.version})"
