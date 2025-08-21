from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    # Dashboard principal
    path('', views.PacienteDashboardView.as_view(), name='dashboard'),
    
    # Gestión de pacientes
    path('lista/', views.PacienteListView.as_view(), name='paciente_list'),
    path('crear/', views.PacienteCreateView.as_view(), name='paciente_create'),
    path('<int:pk>/', views.PacienteDetailView.as_view(), name='paciente_detail'),
    path('<int:pk>/editar/', views.PacienteUpdateView.as_view(), name='paciente_update'),
    path('<int:pk>/eliminar/', views.PacienteDeleteView.as_view(), name='paciente_delete'),
    
    # Funcionalidades adicionales
    path('historias/', views.HistoriasClinicasView.as_view(), name='historias'),
    path('citas/', views.CitasPacientesView.as_view(), name='citas'),
    path('ingresos/', views.IngresosPacientesView.as_view(), name='ingresos'),
    path('emergencias/', views.EmergenciasPacientesView.as_view(), name='emergencias'),
    path('reportes/', views.ReportesPacientesView.as_view(), name='reportes'),
] 