from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Curso(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cursos_impartidos')
    fecha_creacion = models.DateTimeField(default=timezone.now)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Cursos"

    def __str__(self):
        return self.titulo

class Modulo(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='modulos')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    orden = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ['orden']
        verbose_name_plural = "Modulos"

    def __str__(self):
        return f'{self.orden}. {self.titulo}'

class Leccion(models.Model):
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, related_name='lecciones')
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    tipo_contenido = models.CharField(max_length=50, choices=(
        ('texto', 'Texto'),
        ('video', 'Video'),
        ('quiz', 'Cuestionario'),
    ), default='texto')
    url_video = models.URLField(blank=True, null=True)
    orden = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ['orden']
        verbose_name_plural = "Lecciones"

    def __str__(self):
        return f'{self.modulo.curso.titulo} - {self.modulo.titulo} - {self.orden}. {self.titulo}'

class Inscripcion(models.Model):
    estudiante = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inscripciones')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='inscripciones')
    fecha_inscripcion = models.DateTimeField(default=timezone.now)
    completado = models.BooleanField(default=False)

    class Meta:
        unique_together = ('estudiante', 'curso')
        verbose_name_plural = "Inscripciones"

    def __str__(self):
        return f'{self.estudiante.username} inscrito en {self.curso.titulo}'

class ProgresoLeccion(models.Model):
    inscripcion = models.ForeignKey(Inscripcion, on_delete=models.CASCADE, related_name='progreso_lecciones')
    leccion = models.ForeignKey(Leccion, on_delete=models.CASCADE)
    completado = models.BooleanField(default=False)
    fecha_completado = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ('inscripcion', 'leccion')
        verbose_name_plural = "Progreso de Lecciones"

    def __str__(self):
        return f'{self.inscripcion.estudiante.username} - {self.leccion.titulo} ({ "Completado" if self.completado else "Pendiente"})'
