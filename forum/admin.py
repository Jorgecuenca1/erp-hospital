from django.contrib import admin
from .models import Tema, Pregunta, Respuesta

@admin.register(Tema)
class TemaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_creacion')
    search_fields = ('nombre',)

@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tema', 'autor', 'fecha_creacion', 'ultima_actualizacion')
    list_filter = ('tema', 'autor', 'fecha_creacion')
    search_fields = ('titulo', 'contenido')
    raw_id_fields = ('autor',)
    date_hierarchy = 'fecha_creacion'
    ordering = ('-fecha_creacion',)

@admin.register(Respuesta)
class RespuestaAdmin(admin.ModelAdmin):
    list_display = ('pregunta', 'autor', 'fecha_creacion')
    list_filter = ('autor', 'fecha_creacion')
    search_fields = ('contenido',)
    raw_id_fields = ('autor', 'pregunta')
    date_hierarchy = 'fecha_creacion'
    ordering = ('fecha_creacion',)
