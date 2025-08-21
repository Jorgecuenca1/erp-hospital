from django.urls import path
from . import views

app_name = 'hr'

urlpatterns = [
    # Dashboard principal
    path('', views.HRDashboardView.as_view(), name='dashboard'),
    # URLs para Cargo
    path('cargos/', views.CargoListView.as_view(), name='cargo_list'),
    path('cargos/new/', views.CargoCreateView.as_view(), name='cargo_create'),
    path('cargos/<int:pk>/', views.CargoDetailView.as_view(), name='cargo_detail'),
    path('cargos/<int:pk>/edit/', views.CargoUpdateView.as_view(), name='cargo_edit'),
    path('cargos/<int:pk>/delete/', views.CargoDeleteView.as_view(), name='cargo_delete'),

    # URLs para Empleado
    path('empleados/', views.EmpleadoListView.as_view(), name='empleado_list'),
    path('empleados/new/', views.EmpleadoCreateView.as_view(), name='empleado_create'),
    path('empleados/<int:pk>/', views.EmpleadoDetailView.as_view(), name='empleado_detail'),
    path('empleados/<int:pk>/edit/', views.EmpleadoUpdateView.as_view(), name='empleado_edit'),
    path('empleados/<int:pk>/delete/', views.EmpleadoDeleteView.as_view(), name='empleado_delete'),

    # URLs para Contrato
    path('contratos/', views.ContratoListView.as_view(), name='contrato_list'),
    path('contratos/new/', views.ContratoCreateView.as_view(), name='contrato_create'),
    path('contratos/<int:pk>/', views.ContratoDetailView.as_view(), name='contrato_detail'),
    path('contratos/<int:pk>/edit/', views.ContratoUpdateView.as_view(), name='contrato_edit'),
    path('contratos/<int:pk>/delete/', views.ContratoDeleteView.as_view(), name='contrato_delete'),

    # URLs para Nomina
    path('nominas/', views.NominaListView.as_view(), name='nomina_list'),
    path('nominas/new/', views.NominaCreateView.as_view(), name='nomina_create'),
    path('nominas/<int:pk>/', views.NominaDetailView.as_view(), name='nomina_detail'),
    path('nominas/<int:pk>/edit/', views.NominaUpdateView.as_view(), name='nomina_edit'),
    path('nominas/<int:pk>/delete/', views.NominaDeleteView.as_view(), name='nomina_delete'),
] 