from django.contrib import admin
from .models import CategoriaProducto, Producto, Cliente, Carrito, LineaCarrito, Pedido, LineaPedido, Pago

admin.site.register(CategoriaProducto)
admin.site.register(Producto)
admin.site.register(Cliente)
admin.site.register(Carrito)
admin.site.register(LineaCarrito)
admin.site.register(Pedido)
admin.site.register(LineaPedido)
admin.site.register(Pago)
