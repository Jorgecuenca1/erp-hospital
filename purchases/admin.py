from django.contrib import admin
from .models import (
    Proveedor, ProductoCompra, OrdenCompra, DetalleOrdenCompra,
    FacturaCompra, DetalleFacturaCompra, PagoCompra, RecepcionCompra,
    DetalleRecepcionCompra, CotizacionCompra, DetalleCotizacionCompra
)

# Register your models here.
admin.site.register(Proveedor)
admin.site.register(ProductoCompra)
admin.site.register(OrdenCompra)
admin.site.register(DetalleOrdenCompra)
admin.site.register(FacturaCompra)
admin.site.register(DetalleFacturaCompra)
admin.site.register(PagoCompra)
admin.site.register(RecepcionCompra)
admin.site.register(DetalleRecepcionCompra)
admin.site.register(CotizacionCompra)
admin.site.register(DetalleCotizacionCompra)
