from django.db import models

# Create your models here.

class HospitalProfile(models.Model):
    nombre_hospital = models.CharField(max_length=255, unique=True)
    nit = models.CharField(max_length=20, unique=True, verbose_name="NIT")
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    sitio_web = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='hospital_logos/', blank=True, null=True)
    mision = models.TextField(blank=True, null=True)
    vision = models.TextField(blank=True, null=True)
    valores = models.TextField(blank=True, null=True)
    descripcion_corta = models.TextField(blank=True, null=True)
    # Campos para cumplimiento normativo (ej. SGP, habilitacion)
    numero_habilitacion = models.CharField(max_length=50, blank=True, null=True)
    fecha_habilitacion = models.DateField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Perfil del Hospital"
        verbose_name_plural = "Perfiles del Hospital"

    def __str__(self):
        return self.nombre_hospital
