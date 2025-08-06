from django.urls import path
from . import views

urlpatterns = [
    # URLs para Especialidades
    path('especialidades/', views.EspecialidadListView.as_view(), name='especialidad_list'),
    path('especialidades/new/', views.EspecialidadCreateView.as_view(), name='especialidad_create'),
    path('especialidades/<int:pk>/', views.EspecialidadDetailView.as_view(), name='especialidad_detail'),
    path('especialidades/<int:pk>/edit/', views.EspecialidadUpdateView.as_view(), name='especialidad_edit'),
    path('especialidades/<int:pk>/delete/', views.EspecialidadDeleteView.as_view(), name='especialidad_delete'),

    # URLs para Profesionales de Salud
    path('profesionales/', views.ProfesionalSaludListView.as_view(), name='profesional_list'),
    path('profesionales/new/', views.ProfesionalSaludCreateView.as_view(), name='profesional_create'),
    path('profesionales/<int:pk>/', views.ProfesionalSaludDetailView.as_view(), name='profesional_detail'),
    path('profesionales/<int:pk>/edit/', views.ProfesionalSaludUpdateView.as_view(), name='profesional_edit'),
    path('profesionales/<int:pk>/delete/', views.ProfesionalSaludDeleteView.as_view(), name='profesional_delete'),
] 