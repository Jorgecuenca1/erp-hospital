from django.urls import path
from . import views

app_name = 'accounting'

urlpatterns = [
    # Dashboard
    path('', views.AccountingDashboardView.as_view(), name='dashboard'),
    # PeriodoContable
    path('periodos/', views.PeriodoContableListView.as_view(), name='periodocontable_list'),
    path('periodos/<int:pk>/', views.PeriodoContableDetailView.as_view(), name='periodocontable_detail'),
    path('periodos/crear/', views.PeriodoContableCreateView.as_view(), name='periodocontable_create'),
    path('periodos/<int:pk>/editar/', views.PeriodoContableUpdateView.as_view(), name='periodocontable_update'),
    path('periodos/<int:pk>/eliminar/', views.PeriodoContableDeleteView.as_view(), name='periodocontable_delete'),
    # CuentaContable
    path('cuentas/', views.CuentaContableListView.as_view(), name='cuentacontable_list'),
    path('cuentas/<int:pk>/', views.CuentaContableDetailView.as_view(), name='cuentacontable_detail'),
    path('cuentas/crear/', views.CuentaContableCreateView.as_view(), name='cuentacontable_create'),
    path('cuentas/<int:pk>/editar/', views.CuentaContableUpdateView.as_view(), name='cuentacontable_update'),
    path('cuentas/<int:pk>/eliminar/', views.CuentaContableDeleteView.as_view(), name='cuentacontable_delete'),
    # Tercero
    path('terceros/', views.TerceroListView.as_view(), name='tercero_list'),
    path('terceros/<int:pk>/', views.TerceroDetailView.as_view(), name='tercero_detail'),
    path('terceros/crear/', views.TerceroCreateView.as_view(), name='tercero_create'),
    path('terceros/<int:pk>/editar/', views.TerceroUpdateView.as_view(), name='tercero_update'),
    path('terceros/<int:pk>/eliminar/', views.TerceroDeleteView.as_view(), name='tercero_delete'),
    # Diario
    path('diarios/', views.DiarioListView.as_view(), name='diario_list'),
    path('diarios/<int:pk>/', views.DiarioDetailView.as_view(), name='diario_detail'),
    path('diarios/crear/', views.DiarioCreateView.as_view(), name='diario_create'),
    path('diarios/<int:pk>/editar/', views.DiarioUpdateView.as_view(), name='diario_update'),
    path('diarios/<int:pk>/eliminar/', views.DiarioDeleteView.as_view(), name='diario_delete'),
    # Impuesto
    path('impuestos/', views.ImpuestoListView.as_view(), name='impuesto_list'),
    path('impuestos/<int:pk>/', views.ImpuestoDetailView.as_view(), name='impuesto_detail'),
    path('impuestos/crear/', views.ImpuestoCreateView.as_view(), name='impuesto_create'),
    path('impuestos/<int:pk>/editar/', views.ImpuestoUpdateView.as_view(), name='impuesto_update'),
    path('impuestos/<int:pk>/eliminar/', views.ImpuestoDeleteView.as_view(), name='impuesto_delete'),
    # AsientoContable
    path('asientos/', views.AsientoContableListView.as_view(), name='asientocontable_list'),
    path('asientos/<int:pk>/', views.AsientoContableDetailView.as_view(), name='asientocontable_detail'),
    path('asientos/crear/', views.AsientoContableCreateView.as_view(), name='asientocontable_create'),
    path('asientos/<int:pk>/editar/', views.AsientoContableUpdateView.as_view(), name='asientocontable_update'),
    path('asientos/<int:pk>/eliminar/', views.AsientoContableDeleteView.as_view(), name='asientocontable_delete'),
    # LineaAsiento
    path('lineas/', views.LineaAsientoListView.as_view(), name='lineaasiento_list'),
    path('lineas/<int:pk>/', views.LineaAsientoDetailView.as_view(), name='lineaasiento_detail'),
    path('lineas/crear/', views.LineaAsientoCreateView.as_view(), name='lineaasiento_create'),
    path('lineas/<int:pk>/editar/', views.LineaAsientoUpdateView.as_view(), name='lineaasiento_update'),
    path('lineas/<int:pk>/eliminar/', views.LineaAsientoDeleteView.as_view(), name='lineaasiento_delete'),
    
    # DatosEmpresa
    path('empresa/', views.DatosEmpresaListView.as_view(), name='datosempresa_list'),
    path('empresa/<int:pk>/', views.DatosEmpresaDetailView.as_view(), name='datosempresa_detail'),
    path('empresa/crear/', views.DatosEmpresaCreateView.as_view(), name='datosempresa_create'),
    path('empresa/<int:pk>/editar/', views.DatosEmpresaUpdateView.as_view(), name='datosempresa_update'),
    path('empresa/<int:pk>/eliminar/', views.DatosEmpresaDeleteView.as_view(), name='datosempresa_delete'),
    
    # CentroCosto
    path('centros-costo/', views.CentroCostoListView.as_view(), name='centrocosto_list'),
    path('centros-costo/<int:pk>/', views.CentroCostoDetailView.as_view(), name='centrocosto_detail'),
    path('centros-costo/crear/', views.CentroCostoCreateView.as_view(), name='centrocosto_create'),
    path('centros-costo/<int:pk>/editar/', views.CentroCostoUpdateView.as_view(), name='centrocosto_update'),
    path('centros-costo/<int:pk>/eliminar/', views.CentroCostoDeleteView.as_view(), name='centrocosto_delete'),
    
    # ComprobanteContable
    path('comprobantes/', views.ComprobanteContableListView.as_view(), name='comprobantecontable_list'),
    path('comprobantes/<int:pk>/', views.ComprobanteContableDetailView.as_view(), name='comprobantecontable_detail'),
    path('comprobantes/crear/', views.ComprobanteContableCreateView.as_view(), name='comprobantecontable_create'),
    path('comprobantes/<int:pk>/editar/', views.ComprobanteContableUpdateView.as_view(), name='comprobantecontable_update'),
    path('comprobantes/<int:pk>/eliminar/', views.ComprobanteContableDeleteView.as_view(), name='comprobantecontable_delete'),
    
    # CertificadoRetencion
    path('certificados/', views.CertificadoRetencionListView.as_view(), name='certificadoretencion_list'),
    path('certificados/<int:pk>/', views.CertificadoRetencionDetailView.as_view(), name='certificadoretencion_detail'),
    path('certificados/crear/', views.CertificadoRetencionCreateView.as_view(), name='certificadoretencion_create'),
    path('certificados/<int:pk>/editar/', views.CertificadoRetencionUpdateView.as_view(), name='certificadoretencion_update'),
    path('certificados/<int:pk>/eliminar/', views.CertificadoRetencionDeleteView.as_view(), name='certificadoretencion_delete'),
    
    # MovimientoBancario
    path('movimientos-bancarios/', views.MovimientoBancarioListView.as_view(), name='movimientobancario_list'),
    path('movimientos-bancarios/<int:pk>/', views.MovimientoBancarioDetailView.as_view(), name='movimientobancario_detail'),
    path('movimientos-bancarios/crear/', views.MovimientoBancarioCreateView.as_view(), name='movimientobancario_create'),
    path('movimientos-bancarios/<int:pk>/editar/', views.MovimientoBancarioUpdateView.as_view(), name='movimientobancario_update'),
    path('movimientos-bancarios/<int:pk>/eliminar/', views.MovimientoBancarioDeleteView.as_view(), name='movimientobancario_delete'),
    
    # CierreContable
    path('cierres/', views.CierreContableListView.as_view(), name='cierrecontable_list'),
    path('cierres/<int:pk>/', views.CierreContableDetailView.as_view(), name='cierrecontable_detail'),
    path('cierres/crear/', views.CierreContableCreateView.as_view(), name='cierrecontable_create'),
    path('cierres/<int:pk>/editar/', views.CierreContableUpdateView.as_view(), name='cierrecontable_update'),
    path('cierres/<int:pk>/eliminar/', views.CierreContableDeleteView.as_view(), name='cierrecontable_delete'),
    
    # Presupuesto
    path('presupuestos/', views.PresupuestoListView.as_view(), name='presupuesto_list'),
    path('presupuestos/<int:pk>/', views.PresupuestoDetailView.as_view(), name='presupuesto_detail'),
    path('presupuestos/crear/', views.PresupuestoCreateView.as_view(), name='presupuesto_create'),
    path('presupuestos/<int:pk>/editar/', views.PresupuestoUpdateView.as_view(), name='presupuesto_update'),
    path('presupuestos/<int:pk>/eliminar/', views.PresupuestoDeleteView.as_view(), name='presupuesto_delete'),
    
    # Reportes
    path('reportes/', views.ReportesView.as_view(), name='reportes'),

    # Reportes Fiscales
    path('reportes-fiscales/', views.ReporteFiscalListView.as_view(), name='reportefiscal_list'),
    path('reportes-fiscales/generar/', views.GenerarReporteFiscalView.as_view(), name='reportefiscal_create'),
    path('reportes-fiscales/<int:pk>/', views.ReporteFiscalDetailView.as_view(), name='reportefiscal_detail'),
    path('reportes-fiscales/<int:pk>/editar/', views.ReporteFiscalUpdateView.as_view(), name='reportefiscal_update'),
    path('reportes-fiscales/<int:pk>/eliminar/', views.ReporteFiscalDeleteView.as_view(), name='reportefiscal_delete'),
    
    # Gestión Geográfica
    # País
    path('paises/', views.PaisListView.as_view(), name='pais_list'),
    path('paises/crear/', views.PaisCreateView.as_view(), name='pais_create'),
    path('paises/<int:pk>/editar/', views.PaisUpdateView.as_view(), name='pais_edit'),
    path('paises/<int:pk>/eliminar/', views.PaisDeleteView.as_view(), name='pais_delete'),
    
    # Departamento
    path('departamentos/', views.DepartamentoListView.as_view(), name='departamento_list'),
    path('departamentos/crear/', views.DepartamentoCreateView.as_view(), name='departamento_create'),
    path('departamentos/<int:pk>/editar/', views.DepartamentoUpdateView.as_view(), name='departamento_edit'),
    path('departamentos/<int:pk>/eliminar/', views.DepartamentoDeleteView.as_view(), name='departamento_delete'),
    
    # Ciudad
    path('ciudades/', views.CiudadListView.as_view(), name='ciudad_list'),
    path('ciudades/crear/', views.CiudadCreateView.as_view(), name='ciudad_create'),
    path('ciudades/<int:pk>/editar/', views.CiudadUpdateView.as_view(), name='ciudad_edit'),
    path('ciudades/<int:pk>/eliminar/', views.CiudadDeleteView.as_view(), name='ciudad_delete'),
    
    # Reportes Avanzados
    path('reportes/balance-general/', views.BalanceGeneralView.as_view(), name='balance_general'),
    path('reportes/estado-resultados/', views.EstadoResultadosView.as_view(), name='estado_resultados'),
    path('reportes/flujo-efectivo/', views.FlujoEfectivoView.as_view(), name='flujo_efectivo'),
    path('reportes/analisis-financiero/', views.AnalisisFinancieroView.as_view(), name='analisis_financiero'),
] 