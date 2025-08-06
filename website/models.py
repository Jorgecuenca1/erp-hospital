from django.db import models

# Create your models here.

class PaginaWeb(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    contenido = models.TextField(blank=True, null=True)
    publicada = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.titulo

class Seccion(models.Model):
    pagina = models.ForeignKey(PaginaWeb, on_delete=models.CASCADE, related_name='secciones')
    titulo = models.CharField(max_length=200)
    contenido = models.TextField(blank=True, null=True)
    orden = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.titulo} ({self.pagina})"

class Menu(models.Model):
    nombre = models.CharField(max_length=100)
    url = models.CharField(max_length=255)
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre

class Banner(models.Model):
    titulo = models.CharField(max_length=200)
    imagen = models.ImageField(upload_to='banners/')
    url = models.CharField(max_length=255, blank=True, null=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.titulo
