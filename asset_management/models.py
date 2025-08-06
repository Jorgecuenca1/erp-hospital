from django.db import models
from django.conf import settings # Para vincular con el usuario que registra o aprueba

class CategoriaActivo(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Categoría de Activo"
        verbose_name_plural = "Categorías de Activos"

    def __str__(self):
        return self.nombre

class ActivoFijo(models.Model):
    ESTADO_ACTIVO_CHOICES = [
        ('OPERATIVO', 'Operativo'),
        ('MANTENIMIENTO', 'En Mantenimiento'),
        ('BAJA', 'Dado de Baja'),
        ('OBSOLETO', 'Obsoleto'),
    ]

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    codigo_activo = models.CharField(max_length=50, unique=True, blank=True, null=True, help_text="Código interno del activo")
    numero_serie = models.CharField(max_length=100, blank=True, null=True, unique=True)
    categoria = models.ForeignKey(CategoriaActivo, on_delete=models.SET_NULL, null=True, blank=True, related_name='activos')
    fecha_adquisicion = models.DateField()
    valor_adquisicion = models.DecimalField(max_digits=12, decimal_places=2)
    vida_util_anios = models.IntegerField(blank=True, null=True, help_text="Vida útil esperada en años")
    ubicacion_actual = models.CharField(max_length=255, blank=True, null=True, help_text="Ej: Área de Radiología, Oficina 305")
    estado = models.CharField(max_length=20, choices=ESTADO_ACTIVO_CHOICES, default='OPERATIVO')
    responsable = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='activos_a_cargo', help_text="Usuario responsable del activo")
    observaciones = models.TextField(blank=True, null=True)
    fecha_ultimo_mantenimiento = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "Activo Fijo"
        verbose_name_plural = "Activos Fijos"

    def __str__(self):
        return f"{self.nombre} ({self.codigo_activo or self.numero_serie})"

class Mantenimiento(models.Model):
    TIPO_MANTENIMIENTO_CHOICES = [
        ('PREVENTIVO', 'Preventivo'),
        ('CORRECTIVO', 'Correctivo'),
        ('PREDICTIVO', 'Predictivo'),
    ]

    activo = models.ForeignKey(ActivoFijo, on_delete=models.CASCADE, related_name='mantenimientos')
    tipo_mantenimiento = models.CharField(max_length=20, choices=TIPO_MANTENIMIENTO_CHOICES)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField(blank=True, null=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    descripcion_problema = models.TextField(blank=True, null=True)
    acciones_realizadas = models.TextField()
    responsable_mantenimiento = models.CharField(max_length=100, blank=True, null=True, help_text="Persona o empresa que realizó el mantenimiento")
    proximo_mantenimiento_sugerido = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "Mantenimiento"
        verbose_name_plural = "Mantenimientos"
        ordering = ['fecha_inicio']

    def __str__(self):
        return f"Mantenimiento {self.tipo_mantenimiento} para {self.activo.nombre} el {self.fecha_inicio.strftime('%Y-%m-%d')}"

class BajaActivo(models.Model):
    activo = models.OneToOneField(ActivoFijo, on_delete=models.CASCADE, related_name='baja')
    fecha_baja = models.DateField(auto_now_add=True)
    razon_baja = models.TextField()
    valor_residual = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    aprobado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='bajas_aprobadas')

    class Meta:
        verbose_name = "Baja de Activo"
        verbose_name_plural = "Bajas de Activos"

    def __str__(self):
        return f"Baja de {self.activo.nombre} el {self.fecha_baja.strftime('%Y-%m-%d')}"
