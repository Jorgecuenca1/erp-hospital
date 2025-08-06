from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    # PaginaWeb
    path('paginas/', views.PaginaWebListView.as_view(), name='paginaweb_list'),
    path('paginas/<int:pk>/', views.PaginaWebDetailView.as_view(), name='paginaweb_detail'),
    path('paginas/crear/', views.PaginaWebCreateView.as_view(), name='paginaweb_create'),
    path('paginas/<int:pk>/editar/', views.PaginaWebUpdateView.as_view(), name='paginaweb_update'),
    path('paginas/<int:pk>/eliminar/', views.PaginaWebDeleteView.as_view(), name='paginaweb_delete'),
    # Seccion
    path('secciones/', views.SeccionListView.as_view(), name='seccion_list'),
    path('secciones/<int:pk>/', views.SeccionDetailView.as_view(), name='seccion_detail'),
    path('secciones/crear/', views.SeccionCreateView.as_view(), name='seccion_create'),
    path('secciones/<int:pk>/editar/', views.SeccionUpdateView.as_view(), name='seccion_update'),
    path('secciones/<int:pk>/eliminar/', views.SeccionDeleteView.as_view(), name='seccion_delete'),
    # Menu
    path('menus/', views.MenuListView.as_view(), name='menu_list'),
    path('menus/<int:pk>/', views.MenuDetailView.as_view(), name='menu_detail'),
    path('menus/crear/', views.MenuCreateView.as_view(), name='menu_create'),
    path('menus/<int:pk>/editar/', views.MenuUpdateView.as_view(), name='menu_update'),
    path('menus/<int:pk>/eliminar/', views.MenuDeleteView.as_view(), name='menu_delete'),
    # Banner
    path('banners/', views.BannerListView.as_view(), name='banner_list'),
    path('banners/<int:pk>/', views.BannerDetailView.as_view(), name='banner_detail'),
    path('banners/crear/', views.BannerCreateView.as_view(), name='banner_create'),
    path('banners/<int:pk>/editar/', views.BannerUpdateView.as_view(), name='banner_update'),
    path('banners/<int:pk>/eliminar/', views.BannerDeleteView.as_view(), name='banner_delete'),
] 