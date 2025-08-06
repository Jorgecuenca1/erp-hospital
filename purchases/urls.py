from django.urls import path
from . import views

app_name = 'purchases'

urlpatterns = [
    # Dashboard principal
    path('', views.PurchasesDashboardView.as_view(), name='dashboard'),
    
    # URLs para Proveedores
    path('proveedores/', views.ProveedorListView.as_view(), name='proveedor_list'),
    path('proveedores/new/', views.ProveedorCreateView.as_view(), name='proveedor_create'),
    path('proveedores/<int:pk>/', views.ProveedorDetailView.as_view(), name='proveedor_detail'),
    path('proveedores/<int:pk>/edit/', views.ProveedorUpdateView.as_view(), name='proveedor_edit'),
    path('proveedores/<int:pk>/delete/', views.ProveedorDeleteView.as_view(), name='proveedor_delete'),
    
    # URLs para Productos de Compra
    path('productos/', views.ProductoCompraListView.as_view(), name='productocompra_list'),
    path('productos/new/', views.ProductoCompraCreateView.as_view(), name='productocompra_create'),
    path('productos/<int:pk>/', views.ProductoCompraDetailView.as_view(), name='productocompra_detail'),
    path('productos/<int:pk>/edit/', views.ProductoCompraUpdateView.as_view(), name='productocompra_edit'),
    path('productos/<int:pk>/delete/', views.ProductoCompraDeleteView.as_view(), name='productocompra_delete'),
    
    # URLs para Órdenes de Compra
    path('ordenes/', views.OrdenCompraListView.as_view(), name='ordencompra_list'),
    path('ordenes/new/', views.OrdenCompraCreateView.as_view(), name='ordencompra_create'),
    path('ordenes/<int:pk>/', views.OrdenCompraDetailView.as_view(), name='ordencompra_detail'),
    path('ordenes/<int:pk>/edit/', views.OrdenCompraUpdateView.as_view(), name='ordencompra_edit'),
    path('ordenes/<int:pk>/delete/', views.OrdenCompraDeleteView.as_view(), name='ordencompra_delete'),
    
    # URLs para Facturas de Compra
    path('facturas/', views.FacturaCompraListView.as_view(), name='facturacompra_list'),
    path('facturas/new/', views.FacturaCompraCreateView.as_view(), name='facturacompra_create'),
    path('facturas/<int:pk>/', views.FacturaCompraDetailView.as_view(), name='facturacompra_detail'),
    path('facturas/<int:pk>/edit/', views.FacturaCompraUpdateView.as_view(), name='facturacompra_edit'),
    path('facturas/<int:pk>/delete/', views.FacturaCompraDeleteView.as_view(), name='facturacompra_delete'),
    
    # URLs para Pagos de Compra
    path('pagos/', views.PagoCompraListView.as_view(), name='pagocompra_list'),
    path('pagos/new/', views.PagoCompraCreateView.as_view(), name='pagocompra_create'),
    path('pagos/<int:pk>/', views.PagoCompraDetailView.as_view(), name='pagocompra_detail'),
    path('pagos/<int:pk>/edit/', views.PagoCompraUpdateView.as_view(), name='pagocompra_edit'),
    path('pagos/<int:pk>/delete/', views.PagoCompraDeleteView.as_view(), name='pagocompra_delete'),
    
    # URLs para Recepciones de Compra
    path('recepciones/', views.RecepcionCompraListView.as_view(), name='recepcioncompra_list'),
    path('recepciones/new/', views.RecepcionCompraCreateView.as_view(), name='recepcioncompra_create'),
    path('recepciones/<int:pk>/', views.RecepcionCompraDetailView.as_view(), name='recepcioncompra_detail'),
    path('recepciones/<int:pk>/edit/', views.RecepcionCompraUpdateView.as_view(), name='recepcioncompra_edit'),
    path('recepciones/<int:pk>/delete/', views.RecepcionCompraDeleteView.as_view(), name='recepcioncompra_delete'),
    
    # URLs para Cotizaciones de Compra
    path('cotizaciones/', views.CotizacionCompraListView.as_view(), name='cotizacioncompra_list'),
    path('cotizaciones/new/', views.CotizacionCompraCreateView.as_view(), name='cotizacioncompra_create'),
    path('cotizaciones/<int:pk>/', views.CotizacionCompraDetailView.as_view(), name='cotizacioncompra_detail'),
    path('cotizaciones/<int:pk>/edit/', views.CotizacionCompraUpdateView.as_view(), name='cotizacioncompra_edit'),
    path('cotizaciones/<int:pk>/delete/', views.CotizacionCompraDeleteView.as_view(), name='cotizacioncompra_delete'),
    
    # URLs para Reportes
    path('reportes/', views.PurchasesReportsView.as_view(), name='reports'),
    path('facturas-pendientes/', views.FacturasPendientesView.as_view(), name='facturas_pendientes'),
    path('facturas-vencidas/', views.FacturasVencidasView.as_view(), name='facturas_vencidas'),
    path('productos-necesitan-compra/', views.ProductosNecesitanCompraView.as_view(), name='productos_necesitan_compra'),
] 