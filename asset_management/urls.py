from django.urls import path
from . import views

app_name = 'asset_management'

urlpatterns = [
    # URLs para CategoriaActivo
    path('categorias/', views.CategoriaActivoListView.as_view(), name='categoriaactivo_list'),
    path('categorias/add/', views.CategoriaActivoCreateView.as_view(), name='categoriaactivo_create'),
    path('categorias/<int:pk>/', views.CategoriaActivoDetailView.as_view(), name='categoriaactivo_detail'),
    path('categorias/<int:pk>/edit/', views.CategoriaActivoUpdateView.as_view(), name='categoriaactivo_edit'),
    path('categorias/<int:pk>/delete/', views.CategoriaActivoDeleteView.as_view(), name='categoriaactivo_delete'),

    # URLs para ActivoFijo
    path('activos/', views.ActivoFijoListView.as_view(), name='activofijo_list'),
    path('activos/add/', views.ActivoFijoCreateView.as_view(), name='activofijo_create'),
    path('activos/<int:pk>/', views.ActivoFijoDetailView.as_view(), name='activofijo_detail'),
    path('activos/<int:pk>/edit/', views.ActivoFijoUpdateView.as_view(), name='activofijo_edit'),
    path('activos/<int:pk>/delete/', views.ActivoFijoDeleteView.as_view(), name='activofijo_delete'),

    # URLs para Mantenimiento
    path('mantenimientos/', views.MantenimientoListView.as_view(), name='mantenimiento_list'),
    path('activos/<int:activo_pk>/mantenimientos/add/', views.MantenimientoCreateView.as_view(), name='mantenimiento_create'),
    path('mantenimientos/<int:pk>/', views.MantenimientoDetailView.as_view(), name='mantenimiento_detail'),
    path('mantenimientos/<int:pk>/edit/', views.MantenimientoUpdateView.as_view(), name='mantenimiento_edit'),
    path('mantenimientos/<int:pk>/delete/', views.MantenimientoDeleteView.as_view(), name='mantenimiento_delete'),

    # URLs para BajaActivo
    path('bajas/', views.BajaActivoListView.as_view(), name='bajaactivo_list'),
    path('activos/<int:activo_pk>/bajas/add/', views.BajaActivoCreateView.as_view(), name='bajaactivo_create'),
    path('bajas/<int:pk>/', views.BajaActivoDetailView.as_view(), name='bajaactivo_detail'),
    path('bajas/<int:pk>/edit/', views.BajaActivoUpdateView.as_view(), name='bajaactivo_edit'),
    path('bajas/<int:pk>/delete/', views.BajaActivoDeleteView.as_view(), name='bajaactivo_delete'),
] 