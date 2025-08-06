from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    # Dashboard principal
    path('', views.SalesDashboardView.as_view(), name='dashboard'),
    
    # URLs para Clientes
    path('clientes/', views.ClienteListView.as_view(), name='cliente_list'),
    path('clientes/new/', views.ClienteCreateView.as_view(), name='cliente_create'),
    path('clientes/<int:pk>/', views.ClienteDetailView.as_view(), name='cliente_detail'),
    path('clientes/<int:pk>/edit/', views.ClienteUpdateView.as_view(), name='cliente_edit'),
    path('clientes/<int:pk>/delete/', views.ClienteDeleteView.as_view(), name='cliente_delete'),
    
    # URLs para Productos/Servicios
    path('productos/', views.ProductoServicioListView.as_view(), name='productoservicio_list'),
    path('productos/new/', views.ProductoServicioCreateView.as_view(), name='productoservicio_create'),
    path('productos/<int:pk>/', views.ProductoServicioDetailView.as_view(), name='productoservicio_detail'),
    path('productos/<int:pk>/edit/', views.ProductoServicioUpdateView.as_view(), name='productoservicio_edit'),
    path('productos/<int:pk>/delete/', views.ProductoServicioDeleteView.as_view(), name='productoservicio_delete'),
    
    # URLs para Órdenes de Venta
    path('ordenes/', views.OrdenVentaListView.as_view(), name='ordenventa_list'),
    path('ordenes/new/', views.OrdenVentaCreateView.as_view(), name='ordenventa_create'),
    path('ordenes/<int:pk>/', views.OrdenVentaDetailView.as_view(), name='ordenventa_detail'),
    path('ordenes/<int:pk>/edit/', views.OrdenVentaUpdateView.as_view(), name='ordenventa_edit'),
    path('ordenes/<int:pk>/delete/', views.OrdenVentaDeleteView.as_view(), name='ordenventa_delete'),
    
    # URLs para Facturas de Venta
    path('facturas/', views.FacturaVentaListView.as_view(), name='facturaventa_list'),
    path('facturas/new/', views.FacturaVentaCreateView.as_view(), name='facturaventa_create'),
    path('facturas/<int:pk>/', views.FacturaVentaDetailView.as_view(), name='facturaventa_detail'),
    path('facturas/<int:pk>/edit/', views.FacturaVentaUpdateView.as_view(), name='facturaventa_edit'),
    path('facturas/<int:pk>/delete/', views.FacturaVentaDeleteView.as_view(), name='facturaventa_delete'),
    
    # URLs para Pagos de Venta
    path('pagos/', views.PagoVentaListView.as_view(), name='pagoventa_list'),
    path('pagos/new/', views.PagoVentaCreateView.as_view(), name='pagoventa_create'),
    path('pagos/<int:pk>/', views.PagoVentaDetailView.as_view(), name='pagoventa_detail'),
    path('pagos/<int:pk>/edit/', views.PagoVentaUpdateView.as_view(), name='pagoventa_edit'),
    path('pagos/<int:pk>/delete/', views.PagoVentaDeleteView.as_view(), name='pagoventa_delete'),
    
    # URLs para Devoluciones de Venta
    path('devoluciones/', views.DevolucionVentaListView.as_view(), name='devolucionventa_list'),
    path('devoluciones/new/', views.DevolucionVentaCreateView.as_view(), name='devolucionventa_create'),
    path('devoluciones/<int:pk>/', views.DevolucionVentaDetailView.as_view(), name='devolucionventa_detail'),
    path('devoluciones/<int:pk>/edit/', views.DevolucionVentaUpdateView.as_view(), name='devolucionventa_edit'),
    path('devoluciones/<int:pk>/delete/', views.DevolucionVentaDeleteView.as_view(), name='devolucionventa_delete'),
    
    # URLs para Reportes
    path('reportes/', views.SalesReportsView.as_view(), name='reports'),
    path('facturas-pendientes/', views.FacturasPendientesView.as_view(), name='facturas_pendientes'),
    path('facturas-vencidas/', views.FacturasVencidasView.as_view(), name='facturas_vencidas'),
] 