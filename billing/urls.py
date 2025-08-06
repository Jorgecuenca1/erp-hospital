from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    # Dashboard principal
    path('', views.BillingDashboardView.as_view(), name='dashboard'),
    
    # URLs para Facturas
    path('facturas/', views.FacturaListView.as_view(), name='factura_list'),
    path('facturas/new/', views.FacturaCreateView.as_view(), name='factura_create'),
    path('facturas/<int:pk>/', views.FacturaDetailView.as_view(), name='factura_detail'),
    path('facturas/<int:pk>/edit/', views.FacturaUpdateView.as_view(), name='factura_edit'),
    path('facturas/<int:pk>/delete/', views.FacturaDeleteView.as_view(), name='factura_delete'),
    
    # URLs para DetalleFactura
    path('detalles/', views.DetalleFacturaListView.as_view(), name='detalle_factura_list'),
    path('detalles/new/', views.DetalleFacturaCreateView.as_view(), name='detalle_factura_create'),
    path('detalles/<int:pk>/', views.DetalleFacturaDetailView.as_view(), name='detalle_factura_detail'),
    path('detalles/<int:pk>/edit/', views.DetalleFacturaUpdateView.as_view(), name='detalle_factura_edit'),
    path('detalles/<int:pk>/delete/', views.DetalleFacturaDeleteView.as_view(), name='detalle_factura_delete'),
    
    # URLs para TransaccionDIAN
    path('transacciones-dian/', views.TransaccionDIANListView.as_view(), name='transaccion_dian_list'),
    path('transacciones-dian/new/', views.TransaccionDIANCreateView.as_view(), name='transaccion_dian_create'),
    path('transacciones-dian/<int:pk>/', views.TransaccionDIANDetailView.as_view(), name='transaccion_dian_detail'),
    path('transacciones-dian/<int:pk>/edit/', views.TransaccionDIANUpdateView.as_view(), name='transaccion_dian_edit'),
    path('transacciones-dian/<int:pk>/delete/', views.TransaccionDIANDeleteView.as_view(), name='transaccion_dian_delete'),
    
    # URLs para Reportes
    path('reportes/', views.BillingReportsView.as_view(), name='reports'),
    path('facturas-pendientes/', views.FacturasPendientesView.as_view(), name='facturas_pendientes'),
    path('facturas-vencidas/', views.FacturasVencidasView.as_view(), name='facturas_vencidas'),
] 