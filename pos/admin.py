from django.contrib import admin
from .models import PuntoVenta, Caja, SesionCaja, MetodoPagoPOS, VentaPOS, LineaVentaPOS

admin.site.register(PuntoVenta)
admin.site.register(Caja)
admin.site.register(SesionCaja)
admin.site.register(MetodoPagoPOS)
admin.site.register(VentaPOS)
admin.site.register(LineaVentaPOS)
