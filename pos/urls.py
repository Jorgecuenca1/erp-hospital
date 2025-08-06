from django.urls import path
from . import views

app_name = 'pos'

urlpatterns = [
    path('', views.PuntoVentaListView.as_view(), name='dashboard'),
    
    # PuntoVenta
    path('puntoventa/', views.PuntoVentaListView.as_view(), name='puntoventa_list'),
    path('puntoventa/new/', views.PuntoVentaCreateView.as_view(), name='puntoventa_create'),
    path('puntoventa/<int:pk>/', views.PuntoVentaDetailView.as_view(), name='puntoventa_detail'),
    path('puntoventa/<int:pk>/edit/', views.PuntoVentaUpdateView.as_view(), name='puntoventa_update'),
    path('puntoventa/<int:pk>/delete/', views.PuntoVentaDeleteView.as_view(), name='puntoventa_delete'),
    
    # Caja
    path('caja/', views.CajaListView.as_view(), name='caja_list'),
    path('caja/new/', views.CajaCreateView.as_view(), name='caja_create'),
    path('caja/<int:pk>/', views.CajaDetailView.as_view(), name='caja_detail'),
    path('caja/<int:pk>/edit/', views.CajaUpdateView.as_view(), name='caja_update'),
    path('caja/<int:pk>/delete/', views.CajaDeleteView.as_view(), name='caja_delete'),
    
    # SesionCaja
    path('sesioncaja/', views.SesionCajaListView.as_view(), name='sesioncaja_list'),
    path('sesioncaja/new/', views.SesionCajaCreateView.as_view(), name='sesioncaja_create'),
    path('sesioncaja/<int:pk>/', views.SesionCajaDetailView.as_view(), name='sesioncaja_detail'),
    path('sesioncaja/<int:pk>/edit/', views.SesionCajaUpdateView.as_view(), name='sesioncaja_update'),
    path('sesioncaja/<int:pk>/delete/', views.SesionCajaDeleteView.as_view(), name='sesioncaja_delete'),
    
    # MetodoPagoPOS
    path('metodopago/', views.MetodoPagoPOSListView.as_view(), name='metodopagopos_list'),
    path('metodopago/new/', views.MetodoPagoPOSCreateView.as_view(), name='metodopagopos_create'),
    path('metodopago/<int:pk>/', views.MetodoPagoPOSDetailView.as_view(), name='metodopagopos_detail'),
    path('metodopago/<int:pk>/edit/', views.MetodoPagoPOSUpdateView.as_view(), name='metodopagopos_update'),
    path('metodopago/<int:pk>/delete/', views.MetodoPagoPOSDeleteView.as_view(), name='metodopagopos_delete'),
    
    # VentaPOS
    path('venta/', views.VentaPOSListView.as_view(), name='ventapos_list'),
    path('venta/new/', views.VentaPOSCreateView.as_view(), name='ventapos_create'),
    path('venta/<int:pk>/', views.VentaPOSDetailView.as_view(), name='ventapos_detail'),
    path('venta/<int:pk>/edit/', views.VentaPOSUpdateView.as_view(), name='ventapos_update'),
    path('venta/<int:pk>/delete/', views.VentaPOSDeleteView.as_view(), name='ventapos_delete'),
    
    # LineaVentaPOS
    path('lineaventa/', views.LineaVentaPOSListView.as_view(), name='lineaventapos_list'),
    path('lineaventa/new/', views.LineaVentaPOSCreateView.as_view(), name='lineaventapos_create'),
    path('lineaventa/<int:pk>/', views.LineaVentaPOSDetailView.as_view(), name='lineaventapos_detail'),
    path('lineaventa/<int:pk>/edit/', views.LineaVentaPOSUpdateView.as_view(), name='lineaventapos_update'),
    path('lineaventa/<int:pk>/delete/', views.LineaVentaPOSDeleteView.as_view(), name='lineaventapos_delete'),
] 