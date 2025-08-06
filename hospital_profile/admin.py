from django.contrib import admin
from .models import HospitalProfile

@admin.register(HospitalProfile)
class HospitalProfileAdmin(admin.ModelAdmin):
    list_display = ('nombre_hospital', 'nit', 'telefono', 'email')
    search_fields = ('nombre_hospital', 'nit')
    list_filter = ('fecha_habilitacion',)
