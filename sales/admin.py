from django.contrib import admin
from .models import (
    Cliente, ProductoServicio, OrdenVenta, DetalleOrdenVenta,
    FacturaVenta, DetalleFacturaVenta, PagoVenta, DevolucionVenta, DetalleDevolucionVenta
)

# Register your models here.
admin.site.register(Cliente)
admin.site.register(ProductoServicio)
admin.site.register(OrdenVenta)
admin.site.register(DetalleOrdenVenta)
admin.site.register(FacturaVenta)
admin.site.register(DetalleFacturaVenta)
admin.site.register(PagoVenta)
admin.site.register(DevolucionVenta)
admin.site.register(DetalleDevolucionVenta)
