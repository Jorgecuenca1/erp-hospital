from django.urls import path
from . import views

app_name = 'quality_management'

urlpatterns = [
    # URLs para Incidente
    path('incidentes/', views.IncidenteListView.as_view(), name='incidente_list'),
    path('incidentes/add/', views.IncidenteCreateView.as_view(), name='incidente_create'),
    path('incidentes/<int:pk>/', views.IncidenteDetailView.as_view(), name='incidente_detail'),
    path('incidentes/<int:pk>/edit/', views.IncidenteUpdateView.as_view(), name='incidente_edit'),
    path('incidentes/<int:pk>/delete/', views.IncidenteDeleteView.as_view(), name='incidente_delete'),

    # URLs para Auditoria
    path('auditorias/', views.AuditoriaListView.as_view(), name='auditoria_list'),
    path('auditorias/add/', views.AuditoriaCreateView.as_view(), name='auditoria_create'),
    path('auditorias/<int:pk>/', views.AuditoriaDetailView.as_view(), name='auditoria_detail'),
    path('auditorias/<int:pk>/edit/', views.AuditoriaUpdateView.as_view(), name='auditoria_edit'),
    path('auditorias/<int:pk>/delete/', views.AuditoriaDeleteView.as_view(), name='auditoria_delete'),

    # URLs para HallazgoAuditoria
    path('hallazgos_auditoria/', views.HallazgoAuditoriaListView.as_view(), name='hallazgoauditoria_list'),
    path('auditorias/<int:auditoria_pk>/hallazgos/add/', views.HallazgoAuditoriaCreateView.as_view(), name='hallazgoauditoria_create'),
    path('hallazgos_auditoria/<int:pk>/', views.HallazgoAuditoriaDetailView.as_view(), name='hallazgoauditoria_detail'),
    path('hallazgos_auditoria/<int:pk>/edit/', views.HallazgoAuditoriaUpdateView.as_view(), name='hallazgoauditoria_edit'),
    path('hallazgos_auditoria/<int:pk>/delete/', views.HallazgoAuditoriaDeleteView.as_view(), name='hallazgoauditoria_delete'),

    # URLs para PlanMejora
    path('planes_mejora/', views.PlanMejoraListView.as_view(), name='planmejora_list'),
    path('hallazgos/<int:hallazgo_pk>/planes_mejora/add/', views.PlanMejoraCreateView.as_view(), name='planmejora_create'),
    path('planes_mejora/<int:pk>/', views.PlanMejoraDetailView.as_view(), name='planmejora_detail'),
    path('planes_mejora/<int:pk>/edit/', views.PlanMejoraUpdateView.as_view(), name='planmejora_edit'),
    path('planes_mejora/<int:pk>/delete/', views.PlanMejoraDeleteView.as_view(), name='planmejora_delete'),

    # URLs para DocumentoCalidad
    path('documentos_calidad/', views.DocumentoCalidadListView.as_view(), name='documentocalidad_list'),
    path('documentos_calidad/add/', views.DocumentoCalidadCreateView.as_view(), name='documentocalidad_create'),
    path('documentos_calidad/<int:pk>/', views.DocumentoCalidadDetailView.as_view(), name='documentocalidad_detail'),
    path('documentos_calidad/<int:pk>/edit/', views.DocumentoCalidadUpdateView.as_view(), name='documentocalidad_edit'),
    path('documentos_calidad/<int:pk>/delete/', views.DocumentoCalidadDeleteView.as_view(), name='documentocalidad_delete'),
] 