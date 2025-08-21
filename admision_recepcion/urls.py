from django.urls import path
from . import views

app_name = 'admision_recepcion'

urlpatterns = [
    # Dashboard
    path('', views.AdmisionRecepcionDashboardView.as_view(), name='dashboard'),
    
    # Órdenes de Servicios
    path('ordenes/', views.OrdenServicioListView.as_view(), name='orden_list'),
    path('ordenes/crear/', views.OrdenServicioCreateView.as_view(), name='orden_create'),
    path('ordenes/<int:pk>/', views.OrdenServicioDetailView.as_view(), name='orden_detail'),
    path('ordenes/<int:pk>/editar/', views.OrdenServicioUpdateView.as_view(), name='orden_update'),
    path('ordenes/<int:pk>/eliminar/', views.OrdenServicioDeleteView.as_view(), name='orden_delete'),
    
    # Seguimiento
    path('seguimiento/', views.SeguimientoPacientesView.as_view(), name='seguimiento_pacientes'),
    path('seguimiento-atenciones/', views.SeguimientoAtencionesView.as_view(), name='seguimiento_atenciones'),
    
    # Portal de Empresas
    path('portal-empresas/', views.PortalEmpresasView.as_view(), name='portal_empresas'),
    
    # Lista de Precios
    path('lista-precios/', views.ListaPreciosView.as_view(), name='lista_precios'),
    
    # Historias Clínicas
    path('imprimir-historias/', views.ImprimirHistoriasClinicasView.as_view(), name='imprimir_historias'),
    path('empresas-historias/', views.EmpresasHistoriasClinicasView.as_view(), name='empresas_historias'),
    
    # Fichas Clínicas
    path('fichas-clinicas/', views.FichaClinicaListView.as_view(), name='fichas_clinicas'),
    path('evaluacion-ocupacional/nueva/', views.EvaluacionOcupacionalCreateView.as_view(), name='evaluacion_ocupacional_create'),
    path('evaluacion-ocupacional/<int:pk>/', views.EvaluacionOcupacionalDetailView.as_view(), name='evaluacion_ocupacional_detail'),
    path('examen-visual/nuevo/', views.ExamenVisualCreateView.as_view(), name='examen_visual_create'),
    path('examen-visual/<int:pk>/', views.ExamenVisualDetailView.as_view(), name='examen_visual_detail'),
    path('audiometria/nueva/', views.AudiometriaCreateView.as_view(), name='audiometria_create'),
    path('audiometria/<int:pk>/', views.AudiometriaDetailView.as_view(), name='audiometria_detail'),
    path('espirometria/nueva/', views.EspirometriaCreateView.as_view(), name='espirometria_create'),
    path('espirometria/<int:pk>/', views.EspirometriaDetailView.as_view(), name='espirometria_detail'),
    path('osteomuscular/nueva/', views.EvaluacionOsteomuscularCreateView.as_view(), name='osteomuscular_create'),
    path('osteomuscular/<int:pk>/', views.EvaluacionOsteomuscularDetailView.as_view(), name='osteomuscular_detail'),
    path('historia-clinica-general/nueva/', views.HistoriaClinicaGeneralCreateView.as_view(), name='historia_clinica_general_create'),
    path('historia-clinica-general/<int:pk>/', views.HistoriaClinicaGeneralDetailView.as_view(), name='historia_clinica_general_detail'),
    path('historias-cerradas/', views.HistoriasClinicasCerradasView.as_view(), name='historias_cerradas'),
    
    # AJAX
    path('ajax/seguimiento/<int:pk>/', views.agregar_seguimiento_ajax, name='ajax_seguimiento'),
    path('ajax/cambiar-estado/<int:pk>/', views.cambiar_estado_orden_ajax, name='ajax_cambiar_estado'),
    path('ajax/buscar-servicio/', views.buscar_servicio_ajax, name='ajax_buscar_servicio'),
    path('ajax/buscar-prestador/', views.buscar_prestador_ajax, name='ajax_buscar_prestador'),
    
    # AJAX Portal Empresas
    path('ajax/confirmar-cita/<int:pk>/', views.confirmar_cita_ajax, name='ajax_confirmar_cita'),
    path('ajax/cancelar-cita/<int:pk>/', views.cancelar_cita_ajax, name='ajax_cancelar_cita'),
    path('ajax/crear-orden-cita/<int:pk>/', views.crear_orden_desde_cita_ajax, name='ajax_crear_orden_cita'),
    path('ajax/buscar-empresa/', views.buscar_empresa_ajax, name='ajax_buscar_empresa'),
    path('ajax/buscar-trabajador/', views.buscar_trabajador_ajax, name='ajax_buscar_trabajador'),
    
    # Modelos auxiliares
    path('empresas/', views.EmpresaListView.as_view(), name='empresa_list'),
    path('empresas/crear/', views.EmpresaCreateView.as_view(), name='empresa_create'),
    
    path('convenios/', views.ConvenioListView.as_view(), name='convenio_list'),
    path('convenios/crear/', views.ConvenioCreateView.as_view(), name='convenio_create'),
    
    path('servicios/', views.ServicioListView.as_view(), name='servicio_list'),
    path('servicios/crear/', views.ServicioCreateView.as_view(), name='servicio_create'),
    
    path('prestadores/', views.PrestadorListView.as_view(), name='prestador_list'),
    path('prestadores/crear/', views.PrestadorCreateView.as_view(), name='prestador_create'),
]
