from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    # Dashboard principal
    path('', views.ReportsDashboardView.as_view(), name='dashboard'),
    # URLs para ReporteGenerado
    path('generados/', views.ReporteGeneradoListView.as_view(), name='reporte_list'),
    path('generados/new/', views.ReporteGeneradoCreateView.as_view(), name='reporte_create'),
    path('generados/<int:pk>/', views.ReporteGeneradoDetailView.as_view(), name='reporte_detail'),
    path('generados/<int:pk>/edit/', views.ReporteGeneradoUpdateView.as_view(), name='reporte_edit'),
    path('generados/<int:pk>/delete/', views.ReporteGeneradoDeleteView.as_view(), name='reporte_delete'),
] 