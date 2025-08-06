from django.urls import path
from . import views

app_name = 'ecommerce'

urlpatterns = [
    # CategoriaProducto
    path('categorias/', views.CategoriaProductoListView.as_view(), name='categoriaproducto_list'),
    path('categorias/<int:pk>/', views.CategoriaProductoDetailView.as_view(), name='categoriaproducto_detail'),
    path('categorias/crear/', views.CategoriaProductoCreateView.as_view(), name='categoriaproducto_create'),
    path('categorias/<int:pk>/editar/', views.CategoriaProductoUpdateView.as_view(), name='categoriaproducto_update'),
    path('categorias/<int:pk>/eliminar/', views.CategoriaProductoDeleteView.as_view(), name='categoriaproducto_delete'),
    # Producto
    path('productos/', views.ProductoListView.as_view(), name='producto_list'),
    path('productos/<int:pk>/', views.ProductoDetailView.as_view(), name='producto_detail'),
    path('productos/crear/', views.ProductoCreateView.as_view(), name='producto_create'),
    path('productos/<int:pk>/editar/', views.ProductoUpdateView.as_view(), name='producto_update'),
    path('productos/<int:pk>/eliminar/', views.ProductoDeleteView.as_view(), name='producto_delete'),
    # Cliente
    path('clientes/', views.ClienteListView.as_view(), name='cliente_list'),
    path('clientes/<int:pk>/', views.ClienteDetailView.as_view(), name='cliente_detail'),
    path('clientes/crear/', views.ClienteCreateView.as_view(), name='cliente_create'),
    path('clientes/<int:pk>/editar/', views.ClienteUpdateView.as_view(), name='cliente_update'),
    path('clientes/<int:pk>/eliminar/', views.ClienteDeleteView.as_view(), name='cliente_delete'),
    # Carrito
    path('carritos/', views.CarritoListView.as_view(), name='carrito_list'),
    path('carritos/<int:pk>/', views.CarritoDetailView.as_view(), name='carrito_detail'),
    path('carritos/crear/', views.CarritoCreateView.as_view(), name='carrito_create'),
    path('carritos/<int:pk>/editar/', views.CarritoUpdateView.as_view(), name='carrito_update'),
    path('carritos/<int:pk>/eliminar/', views.CarritoDeleteView.as_view(), name='carrito_delete'),
    # LineaCarrito
    path('lineas_carrito/', views.LineaCarritoListView.as_view(), name='lineacarrito_list'),
    path('lineas_carrito/<int:pk>/', views.LineaCarritoDetailView.as_view(), name='lineacarrito_detail'),
    path('lineas_carrito/crear/', views.LineaCarritoCreateView.as_view(), name='lineacarrito_create'),
    path('lineas_carrito/<int:pk>/editar/', views.LineaCarritoUpdateView.as_view(), name='lineacarrito_update'),
    path('lineas_carrito/<int:pk>/eliminar/', views.LineaCarritoDeleteView.as_view(), name='lineacarrito_delete'),
    # Pedido
    path('pedidos/', views.PedidoListView.as_view(), name='pedido_list'),
    path('pedidos/<int:pk>/', views.PedidoDetailView.as_view(), name='pedido_detail'),
    path('pedidos/crear/', views.PedidoCreateView.as_view(), name='pedido_create'),
    path('pedidos/<int:pk>/editar/', views.PedidoUpdateView.as_view(), name='pedido_update'),
    path('pedidos/<int:pk>/eliminar/', views.PedidoDeleteView.as_view(), name='pedido_delete'),
    # LineaPedido
    path('lineas_pedido/', views.LineaPedidoListView.as_view(), name='lineapedido_list'),
    path('lineas_pedido/<int:pk>/', views.LineaPedidoDetailView.as_view(), name='lineapedido_detail'),
    path('lineas_pedido/crear/', views.LineaPedidoCreateView.as_view(), name='lineapedido_create'),
    path('lineas_pedido/<int:pk>/editar/', views.LineaPedidoUpdateView.as_view(), name='lineapedido_update'),
    path('lineas_pedido/<int:pk>/eliminar/', views.LineaPedidoDeleteView.as_view(), name='lineapedido_delete'),
    # Pago
    path('pagos/', views.PagoListView.as_view(), name='pago_list'),
    path('pagos/<int:pk>/', views.PagoDetailView.as_view(), name='pago_detail'),
    path('pagos/crear/', views.PagoCreateView.as_view(), name='pago_create'),
    path('pagos/<int:pk>/editar/', views.PagoUpdateView.as_view(), name='pago_update'),
    path('pagos/<int:pk>/eliminar/', views.PagoDeleteView.as_view(), name='pago_delete'),
] 