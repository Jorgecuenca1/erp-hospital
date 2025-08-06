from django.contrib import admin
from .models import PlanSuscripcion, Suscripcion, PagoSuscripcion

admin.site.register(PlanSuscripcion)
admin.site.register(Suscripcion)
admin.site.register(PagoSuscripcion)
