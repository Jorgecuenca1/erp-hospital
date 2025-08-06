from django.urls import path
from . import views

app_name = 'inventories'

urlpatterns = [
    # Dashboard principal
    path('', views.InventoryDashboardView.as_view(), name='dashboard'),
    
    # URLs para Ubicaciones de Almacén
    path('ubicaciones/', views.UbicacionAlmacenListView.as_view(), name='ubicacion_list'),
    path('ubicaciones/new/', views.UbicacionAlmacenCreateView.as_view(), name='ubicacion_create'),
    path('ubicaciones/<int:pk>/', views.UbicacionAlmacenDetailView.as_view(), name='ubicacion_detail'),
    path('ubicaciones/<int:pk>/edit/', views.UbicacionAlmacenUpdateView.as_view(), name='ubicacion_edit'),
    path('ubicaciones/<int:pk>/delete/', views.UbicacionAlmacenDeleteView.as_view(), name='ubicacion_delete'),

    # URLs para Categorías de Producto
    path('categorias/', views.CategoriaProductoListView.as_view(), name='categoria_list'),
    path('categorias/new/', views.CategoriaProductoCreateView.as_view(), name='categoria_create'),
    path('categorias/<int:pk>/', views.CategoriaProductoDetailView.as_view(), name='categoria_detail'),
    path('categorias/<int:pk>/edit/', views.CategoriaProductoUpdateView.as_view(), name='categoria_edit'),
    path('categorias/<int:pk>/delete/', views.CategoriaProductoDeleteView.as_view(), name='categoria_delete'),

    # URLs para Productos
    path('productos/', views.ProductoListView.as_view(), name='producto_list'),
    path('productos/new/', views.ProductoCreateView.as_view(), name='producto_create'),
    path('productos/<int:pk>/', views.ProductoDetailView.as_view(), name='producto_detail'),
    path('productos/<int:pk>/edit/', views.ProductoUpdateView.as_view(), name='producto_edit'),
    path('productos/<int:pk>/delete/', views.ProductoDeleteView.as_view(), name='producto_delete'),

    # URLs para Movimientos de Inventario
    path('movimientos/', views.MovimientoInventarioListView.as_view(), name='movimiento_list'),
    path('movimientos/new/', views.MovimientoInventarioCreateView.as_view(), name='movimiento_create'),
    path('movimientos/<int:pk>/', views.MovimientoInventarioDetailView.as_view(), name='movimiento_detail'),
    path('movimientos/<int:pk>/edit/', views.MovimientoInventarioUpdateView.as_view(), name='movimiento_edit'),
    path('movimientos/<int:pk>/delete/', views.MovimientoInventarioDeleteView.as_view(), name='movimiento_delete'),

    # URLs para Órdenes de Dispensación
    path('ordenes-dispensacion/', views.OrdenDispensacionListView.as_view(), name='orden_list'),
    path('ordenes-dispensacion/new/', views.OrdenDispensacionCreateView.as_view(), name='orden_create'),
    path('ordenes-dispensacion/<int:pk>/', views.OrdenDispensacionDetailView.as_view(), name='orden_detail'),
    path('ordenes-dispensacion/<int:pk>/edit/', views.OrdenDispensacionUpdateView.as_view(), name='orden_edit'),
    path('ordenes-dispensacion/<int:pk>/delete/', views.OrdenDispensacionDeleteView.as_view(), name='orden_delete'),
    
    # URLs para Reportes
    path('reportes/', views.InventoryReportsView.as_view(), name='reports'),
    path('stock-bajo/', views.LowStockView.as_view(), name='low_stock'),
    path('productos-caducados/', views.ExpiredProductsView.as_view(), name='expired_products'),
    path('movimientos-resumen/', views.MovementsSummaryView.as_view(), name='movements_summary'),
] 