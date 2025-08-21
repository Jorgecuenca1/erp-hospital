from django.urls import path
from . import views

app_name = 'medical_records'

urlpatterns = [
    # Dashboard principal
    path('', views.MedicalRecordsDashboardView.as_view(), name='dashboard'),
    # URLs para Consultas
    path('historias/<int:historia_clinica_id>/consultas/', views.ConsultaListView.as_view(), name='consulta_list'),
    path('historias/<int:historia_clinica_id>/consultas/new/', views.ConsultaCreateView.as_view(), name='consulta_create'),
    path('consultas/<int:pk>/', views.ConsultaDetailView.as_view(), name='consulta_detail'),
    path('consultas/<int:pk>/edit/', views.ConsultaUpdateView.as_view(), name='consulta_edit'),
    path('consultas/<int:pk>/delete/', views.ConsultaDeleteView.as_view(), name='consulta_delete'),

    # URLs para añadir sub-registros desde el detalle de la Consulta
    path('consultas/<int:pk>/add_diagnostico/', views.AddDiagnosticoView.as_view(), name='add_diagnostico'),
    path('consultas/<int:pk>/add_procedimiento/', views.AddProcedimientoView.as_view(), name='add_procedimiento'),
    path('consultas/<int:pk>/add_signos_vitales/', views.AddSignosVitalesView.as_view(), name='add_signos_vitales'),
    path('consultas/<int:pk>/add_nota_evolucion/', views.AddNotaEvolucionView.as_view(), name='add_nota_evolucion'),
    path('consultas/<int:pk>/add_documento_adjunto/', views.AddDocumentoAdjuntoView.as_view(), name='add_documento_adjunto'),
] 