from django.contrib import admin
from .models import Curso, Modulo, Leccion, Inscripcion, ProgresoLeccion

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'instructor', 'fecha_creacion', 'activo')
    list_filter = ('activo', 'fecha_creacion', 'instructor')
    search_fields = ('titulo', 'descripcion')
    raw_id_fields = ('instructor',)

@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'curso', 'orden')
    list_filter = ('curso',)
    search_fields = ('titulo', 'descripcion')
    ordering = ('curso', 'orden')

@admin.register(Leccion)
class LeccionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'modulo', 'tipo_contenido', 'orden', 'url_video')
    list_filter = ('modulo__curso', 'modulo', 'tipo_contenido')
    search_fields = ('titulo', 'contenido')
    ordering = ('modulo__curso', 'modulo', 'orden')

@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'curso', 'fecha_inscripcion', 'completado')
    list_filter = ('completado', 'fecha_inscripcion', 'estudiante', 'curso')
    search_fields = ('estudiante__username', 'curso__titulo')
    raw_id_fields = ('estudiante', 'curso')

@admin.register(ProgresoLeccion)
class ProgresoLeccionAdmin(admin.ModelAdmin):
    list_display = ('inscripcion', 'leccion', 'completado', 'fecha_completado')
    list_filter = ('completado', 'inscripcion__estudiante', 'leccion__modulo__curso')
    raw_id_fields = ('inscripcion', 'leccion')
