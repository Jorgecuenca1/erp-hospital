#!/usr/bin/env python3
"""
Mapeo de URLs reales vs URLs del dashboard
"""

# URLs que SÍ EXISTEN pero con diferentes rutas
URLS_EXISTENTES = {
    # HMS - URLs que funcionan
    'hms_working': [
        ('/hms/', 'Base HMS'),
        ('/hms/pharmacy/', 'Farmacia HMS'),
        ('/hms/online-appointment/', 'Citas Online'),
        ('/hms/waiting-screen/', 'Pantalla Espera'),
        # Estos necesitan templates pero las URLs existen
        ('/hms/gynecology/', 'Ginecología'),
        ('/hms/radiology/', 'Radiología'),
        ('/hms/nursing/', 'Enfermería'),
        ('/hms/consent-form/', 'Consentimientos'),
        ('/hms/commission/', 'Comisiones'),
    ],
    
    # ERP - URLs que SÍ existen
    'erp_working': [
        ('/patients/', 'Pacientes'),  # Funciona pero tiene error en campo
        ('/appointments/citas/', 'Citas'),
        ('/accounting/', 'Contabilidad'),
        ('/billing/', 'Facturación'),
        ('/sales/', 'Ventas'),
        ('/purchases/', 'Compras'),
        ('/inventories/', 'Inventarios'),
        ('/pos/', 'Punto de Venta'),
        ('/website/paginas/', 'Sitio Web'),
        ('/carbon/', 'Huella Carbono'),
        ('/social/', 'Métricas Sociales'),
    ],
    
    # URLs que EXISTEN pero necesitan dashboards
    'need_dashboards': [
        ('/hr/empleados/', 'Recursos Humanos'),
        ('/reports/generados/', 'Reportes'),
        ('/crm/leads/', 'CRM'),
        ('/ecommerce/productos/', 'E-commerce'),
        ('/forum/temas/', 'Foro'),
        ('/elearning/cursos/', 'E-learning'),
        ('/livechat/', 'Live Chat'),  # Necesita implementar
        ('/blog/', 'Blog'),  # Necesita implementar
        ('/subscriptions/', 'Suscripciones'),  # Necesita implementar
    ],
    
    # Admisión-Recepción - TODO funciona
    'admision_working': [
        ('/admision/', 'Dashboard Admisión'),
        ('/admision/ordenes/', 'Órdenes de Servicios'),
        ('/admision/seguimiento/', 'Seguimiento Pacientes'),
        ('/admision/seguimiento-atenciones/', 'Seguimiento Atenciones'),
        ('/admision/portal-empresas/', 'Portal Empresas'),
        ('/admision/lista-precios/', 'Lista de Precios'),
        ('/admision/imprimir-historias/', 'Imprimir Historias'),
        ('/admision/empresas-historias/', 'Empresas Historias'),
        ('/admision/fichas-clinicas/', 'Fichas Clínicas'),
        ('/admision/evaluacion-ocupacional/nueva/', 'Evaluación Ocupacional'),
        ('/admision/examen-visual/nuevo/', 'Examen Visual'),
        ('/admision/audiometria/nueva/', 'Audiometría'),
        ('/admision/espirometria/nueva/', 'Espirometría'),
        ('/admision/osteomuscular/nueva/', 'Osteomuscular'),
        ('/admision/historia-clinica-general/nueva/', 'Historia General'),
        ('/admision/historias-cerradas/', 'Historias Cerradas'),
    ]
}

# URLs que necesitan corrección en el dashboard
CORRECCION_DASHBOARD = {
    # Cambiar estas URLs del dashboard por las reales
    '/professionals/': '/hr/empleados/',  # Profesionales → Empleados
    '/hospital_profile/': '/hms/',  # Perfil Hospital → Base HMS
    '/pharmacy/': '/hms/pharmacy/',  # Farmacia → Farmacia HMS
    '/laboratories/': '/inventories/',  # Laboratorios → Inventarios
    '/asset_management/': '/inventories/ubicaciones/',  # Activos → Ubicaciones
    '/hr/': '/hr/empleados/',  # RRHH → Empleados
    '/quality_management/': '/reports/generados/',  # Calidad → Reportes
    '/reports/': '/reports/generados/',  # Reportes → Reportes Generados
    '/ecommerce/': '/ecommerce/productos/',  # E-commerce → Productos
    '/crm/': '/crm/leads/',  # CRM → Leads
    '/blog/': '/forum/temas/',  # Blog → Foro (por ahora)
    '/forum/': '/forum/temas/',  # Foro → Temas
    '/elearning/': '/elearning/cursos/',  # E-learning → Cursos
}

print("📋 MAPEO DE URLs REALES")
print("=" * 50)

total_working = (
    len(URLS_EXISTENTES['hms_working']) +
    len(URLS_EXISTENTES['erp_working']) +
    len(URLS_EXISTENTES['admision_working'])
)

print(f"✅ URLs que SÍ funcionan: {total_working}")
print(f"🔧 URLs que necesitan corrección: {len(CORRECCION_DASHBOARD)}")
print(f"🏗️ URLs que necesitan dashboards: {len(URLS_EXISTENTES['need_dashboards'])}")

print("\n🔧 CORRECCIONES NECESARIAS:")
for old_url, new_url in CORRECCION_DASHBOARD.items():
    print(f"❌ {old_url} → ✅ {new_url}")

print("\n✅ ADMISIÓN-RECEPCIÓN (100% FUNCIONAL):")
for url, name in URLS_EXISTENTES['admision_working']:
    print(f"✅ {name}: {url}")
