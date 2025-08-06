from django.urls import path
from . import views

urlpatterns = [
    # URLs para TipoExamen
    path('tipos-examen/', views.TipoExamenListView.as_view(), name='tipo_examen_list'),
    path('tipos-examen/new/', views.TipoExamenCreateView.as_view(), name='tipo_examen_create'),
    path('tipos-examen/<int:pk>/', views.TipoExamenDetailView.as_view(), name='tipo_examen_detail'),
    path('tipos-examen/<int:pk>/edit/', views.TipoExamenUpdateView.as_view(), name='tipo_examen_edit'),
    path('tipos-examen/<int:pk>/delete/', views.TipoExamenDeleteView.as_view(), name='tipo_examen_delete'),

    # URLs para EquipoLaboratorio
    path('equipos-laboratorio/', views.EquipoLaboratorioListView.as_view(), name='equipo_list'),
    path('equipos-laboratorio/new/', views.EquipoLaboratorioCreateView.as_view(), name='equipo_create'),
    path('equipos-laboratorio/<int:pk>/', views.EquipoLaboratorioDetailView.as_view(), name='equipo_detail'),
    path('equipos-laboratorio/<int:pk>/edit/', views.EquipoLaboratorioUpdateView.as_view(), name='equipo_edit'),
    path('equipos-laboratorio/<int:pk>/delete/', views.EquipoLaboratorioDeleteView.as_view(), name='equipo_delete'),

    # URLs para OrdenExamen
    path('ordenes-examen/', views.OrdenExamenListView.as_view(), name='orden_examen_list'),
    path('ordenes-examen/new/', views.OrdenExamenCreateView.as_view(), name='orden_examen_create'),
    path('ordenes-examen/<int:pk>/', views.OrdenExamenDetailView.as_view(), name='orden_examen_detail'),
    path('ordenes-examen/<int:pk>/edit/', views.OrdenExamenUpdateView.as_view(), name='orden_examen_edit'),
    path('ordenes-examen/<int:pk>/delete/', views.OrdenExamenDeleteView.as_view(), name='orden_examen_delete'),

    # URLs para ResultadoExamen
    path('resultados-examen/', views.ResultadoExamenListView.as_view(), name='resultado_examen_list'),
    path('resultados-examen/new/', views.ResultadoExamenCreateView.as_view(), name='resultado_examen_create'),
    path('resultados-examen/<int:pk>/', views.ResultadoExamenDetailView.as_view(), name='resultado_examen_detail'),
    path('resultados-examen/<int:pk>/edit/', views.ResultadoExamenUpdateView.as_view(), name='resultado_examen_edit'),
    path('resultados-examen/<int:pk>/delete/', views.ResultadoExamenDeleteView.as_view(), name='resultado_examen_delete'),
] 