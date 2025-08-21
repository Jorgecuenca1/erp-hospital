from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Dashboard principal
    path('', views.BlogDashboardView.as_view(), name='dashboard'),
    # Artículos
    path('articulos/', views.ArticuloListView.as_view(), name='articulo_list'),
    path('articulos/crear/', views.ArticuloCreateView.as_view(), name='articulo_create'),
    path('articulos/<int:pk>/', views.ArticuloDetailView.as_view(), name='articulo_detail'),
    path('articulos/<int:pk>/editar/', views.ArticuloUpdateView.as_view(), name='articulo_edit'),
    path('articulos/<int:pk>/eliminar/', views.ArticuloDeleteView.as_view(), name='articulo_delete'),
]