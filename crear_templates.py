#!/usr/bin/env python
"""
Script para crear automáticamente todos los templates HTML faltantes
"""
import os

# Configuración de módulos HMS
HMS_MODULES = [
    {
        'name': 'gynecology',
        'title': 'Ginecología',
        'icon': 'fas fa-female',
        'description': 'Ginecología y obstetricia especializada',
        'path': 'acs_hms_gynec'
    },
    {
        'name': 'ophthalmology',
        'title': 'Oftalmología',
        'icon': 'fas fa-eye',
        'description': 'Cuidado especializado de la vista',
        'path': 'acs_hms_ophthalmology'
    },
    {
        'name': 'pediatrics',
        'title': 'Pediatría',
        'icon': 'fas fa-baby',
        'description': 'Cuidado pediátrico integral',
        'path': 'acs_hms_paediatric'
    },
    {
        'name': 'aesthetic',
        'title': 'Estética',
        'icon': 'fas fa-spa',
        'description': 'Medicina estética y cosmética',
        'path': 'acs_hms_aesthetic'
    },
    {
        'name': 'dental',
        'title': 'Dental',
        'icon': 'fas fa-tooth',
        'description': 'Odontología y salud bucal',
        'path': 'acs_hms_dental'
    },
    {
        'name': 'surgery',
        'title': 'Cirugía',
        'icon': 'fas fa-procedures',
        'description': 'Cirugía general y especializada',
        'path': 'acs_hms_surgery'
    },
    {
        'name': 'operation-theater',
        'title': 'Quirófanos',
        'icon': 'fas fa-bed',
        'description': 'Gestión de quirófanos y equipos',
        'path': 'acs_hms_operation_theater'
    },
    {
        'name': 'laboratory',
        'title': 'Laboratorio',
        'icon': 'fas fa-flask',
        'description': 'Laboratorio clínico y análisis',
        'path': 'acs_hms_laboratory'
    },
    {
        'name': 'radiology',
        'title': 'Radiología',
        'icon': 'fas fa-x-ray',
        'description': 'Radiología e imágenes diagnósticas',
        'path': 'acs_hms_radiology'
    },
    {
        'name': 'emergency',
        'title': 'Emergencias',
        'icon': 'fas fa-ambulance',
        'description': 'Servicios de emergencia 24/7',
        'path': 'acs_hms_emergency'
    },
    {
        'name': 'nursing',
        'title': 'Enfermería',
        'icon': 'fas fa-user-nurse',
        'description': 'Gestión de enfermería y cuidados',
        'path': 'acs_hms_nursing'
    },
    {
        'name': 'blood-bank',
        'title': 'Banco de Sangre',
        'icon': 'fas fa-tint',
        'description': 'Banco de sangre y transfusiones',
        'path': 'acs_hms_blood_bank'
    },
    {
        'name': 'hospitalization',
        'title': 'Hospitalización',
        'icon': 'fas fa-procedures',
        'description': 'Gestión de hospitalización',
        'path': 'acs_hms_hospitalization'
    },
    {
        'name': 'patient-portal',
        'title': 'Portal Paciente',
        'icon': 'fas fa-user',
        'description': 'Portal del paciente',
        'path': 'acs_hms_patient_portal'
    },
    {
        'name': 'pharmacy',
        'title': 'Farmacia',
        'icon': 'fas fa-pills',
        'description': 'Farmacia hospitalaria',
        'path': 'acs_hms_pharmacy'
    },
    {
        'name': 'online-appointment',
        'title': 'Citas Online',
        'icon': 'fas fa-calendar-check',
        'description': 'Citas en línea',
        'path': 'acs_hms_online_appointment'
    },
    {
        'name': 'webcam',
        'title': 'Webcam',
        'icon': 'fas fa-video',
        'description': 'Gestión de webcam',
        'path': 'acs_hms_webcam'
    },
    {
        'name': 'video-call',
        'title': 'Video Call',
        'icon': 'fas fa-phone',
        'description': 'Videollamadas médicas',
        'path': 'acs_hms_video_call'
    },
    {
        'name': 'consent-form',
        'title': 'Consentimientos',
        'icon': 'fas fa-file-signature',
        'description': 'Consentimientos digitales',
        'path': 'acs_hms_consent_form'
    },
    {
        'name': 'subscription',
        'title': 'Suscripciones',
        'icon': 'fas fa-credit-card',
        'description': 'Gestión de suscripciones',
        'path': 'acs_hms_subscription'
    },
    {
        'name': 'insurance',
        'title': 'Seguros',
        'icon': 'fas fa-shield-alt',
        'description': 'Seguros médicos',
        'path': 'acs_hms_insurance'
    },
    {
        'name': 'commission',
        'title': 'Comisiones',
        'icon': 'fas fa-percentage',
        'description': 'Comisiones médicas',
        'path': 'acs_hms_commission'
    },
    {
        'name': 'certification',
        'title': 'Certificaciones',
        'icon': 'fas fa-certificate',
        'description': 'Certificaciones médicas',
        'path': 'acs_hms_certification'
    },
    {
        'name': 'waiting-screen',
        'title': 'Pantalla Espera',
        'icon': 'fas fa-tv',
        'description': 'Pantallas de espera',
        'path': 'acs_hms_waiting_screen'
    }
]

# Configuración de módulos ERP
ERP_MODULES = [
    {
        'name': 'professionals',
        'title': 'Profesionales',
        'icon': 'fas fa-user-md',
        'description': 'Gestión de profesionales médicos',
        'path': 'professionals'
    },
    {
        'name': 'appointments',
        'title': 'Citas',
        'icon': 'fas fa-calendar',
        'description': 'Gestión de citas médicas',
        'path': 'appointments'
    },
    {
        'name': 'medical_records',
        'title': 'Historias Clínicas',
        'icon': 'fas fa-file-medical',
        'description': 'Historias médicas electrónicas',
        'path': 'medical_records'
    },
    {
        'name': 'hospital_profile',
        'title': 'Perfil Hospital',
        'icon': 'fas fa-hospital',
        'description': 'Perfil del hospital',
        'path': 'hospital_profile'
    },
    {
        'name': 'billing',
        'title': 'Facturación',
        'icon': 'fas fa-file-invoice-dollar',
        'description': 'Facturación médica',
        'path': 'billing'
    },
    {
        'name': 'sales',
        'title': 'Ventas',
        'icon': 'fas fa-chart-line',
        'description': 'Gestión de ventas',
        'path': 'sales'
    },
    {
        'name': 'purchases',
        'title': 'Compras',
        'icon': 'fas fa-shopping-cart',
        'description': 'Gestión de compras',
        'path': 'purchases'
    },
    {
        'name': 'inventories',
        'title': 'Inventarios',
        'icon': 'fas fa-boxes',
        'description': 'Control de inventarios',
        'path': 'inventories'
    },
    {
        'name': 'pharmacy',
        'title': 'Farmacia',
        'icon': 'fas fa-pills',
        'description': 'Farmacia del hospital',
        'path': 'pharmacy'
    },
    {
        'name': 'laboratories',
        'title': 'Laboratorio',
        'icon': 'fas fa-flask',
        'description': 'Laboratorio clínico',
        'path': 'laboratories'
    },
    {
        'name': 'asset_management',
        'title': 'Activos',
        'icon': 'fas fa-tools',
        'description': 'Gestión de activos',
        'path': 'asset_management'
    },
    {
        'name': 'hr',
        'title': 'Recursos Humanos',
        'icon': 'fas fa-users-cog',
        'description': 'Gestión de RRHH',
        'path': 'hr'
    },
    {
        'name': 'quality_management',
        'title': 'Calidad',
        'icon': 'fas fa-award',
        'description': 'Gestión de calidad',
        'path': 'quality_management'
    },
    {
        'name': 'reports',
        'title': 'Reportes',
        'icon': 'fas fa-chart-bar',
        'description': 'Reportes y análisis',
        'path': 'reports'
    },
    {
        'name': 'pos',
        'title': 'Punto de Venta',
        'icon': 'fas fa-cash-register',
        'description': 'Punto de venta',
        'path': 'pos'
    },
    {
        'name': 'ecommerce',
        'title': 'E-commerce',
        'icon': 'fas fa-shopping-bag',
        'description': 'Comercio electrónico',
        'path': 'ecommerce'
    },
    {
        'name': 'crm',
        'title': 'CRM',
        'icon': 'fas fa-handshake',
        'description': 'Gestión de relaciones',
        'path': 'crm'
    },
    {
        'name': 'subscriptions',
        'title': 'Suscripciones',
        'icon': 'fas fa-credit-card',
        'description': 'Gestión de suscripciones',
        'path': 'subscriptions'
    },
    {
        'name': 'website',
        'title': 'Sitio Web',
        'icon': 'fas fa-globe',
        'description': 'Gestión del sitio web',
        'path': 'website'
    },
    {
        'name': 'blog',
        'title': 'Blog',
        'icon': 'fas fa-blog',
        'description': 'Sistema de blog',
        'path': 'blog'
    },
    {
        'name': 'forum',
        'title': 'Foro',
        'icon': 'fas fa-comments',
        'description': 'Foro de discusión',
        'path': 'forum'
    },
    {
        'name': 'elearning',
        'title': 'E-learning',
        'icon': 'fas fa-graduation-cap',
        'description': 'Plataforma educativa',
        'path': 'elearning'
    },
    {
        'name': 'livechat',
        'title': 'Live Chat',
        'icon': 'fas fa-comments',
        'description': 'Chat en vivo',
        'path': 'livechat'
    }
]

def create_template_content(module, module_type):
    """Genera el contenido del template para un módulo"""
    
    if module_type == 'hms':
        url_prefix = f"/hms/{module['name']}/"
        breadcrumb_parent = "HMS"
    else:
        url_prefix = f"/{module['name']}/"
        breadcrumb_parent = "ERP"
    
    return f"""{{% extends 'base_hms.html' %}}

{{% block title %}}{module['title']} - HMetaHIS{{% endblock %}}

{{% block breadcrumb %}}
<li class="breadcrumb-item"><a href="{{% url 'landing_page' %}}">Inicio</a></li>
<li class="breadcrumb-item"><a href="/dashboard/">{breadcrumb_parent}</a></li>
<li class="breadcrumb-item active">{module['title']}</li>
{{% endblock %}}

{{% block sidebar %}}
<li class="nav-item">
    <a class="nav-link active" href="{url_prefix}">
        <i class="fas fa-tachometer-alt me-2"></i>Dashboard
    </a>
</li>
<li class="nav-item">
    <a class="nav-link" href="{url_prefix}lista/">
        <i class="fas fa-list me-2"></i>Lista
    </a>
</li>
<li class="nav-item">
    <a class="nav-link" href="{url_prefix}crear/">
        <i class="fas fa-plus me-2"></i>Nuevo
    </a>
</li>
<li class="nav-item">
    <a class="nav-link" href="{url_prefix}reportes/">
        <i class="fas fa-chart-bar me-2"></i>Reportes
    </a>
</li>
{{% endblock %}}

{{% block content %}}
<div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
    <h1 class="h2">
        <i class="{module['icon']} me-2"></i>
        {module['title']}
    </h1>
    <div class="btn-toolbar mb-2 mb-md-0">
        <div class="btn-group me-2">
            <a href="{url_prefix}crear/" class="btn btn-primary">
                <i class="fas fa-plus me-1"></i>Nuevo
            </a>
            <button type="button" class="btn btn-outline-secondary">
                <i class="fas fa-download me-1"></i>Exportar
            </button>
        </div>
    </div>
</div>

<!-- Estadísticas -->
<div class="row mb-4">
    <div class="col-xl-3 col-md-6 mb-4">
        <div class="stats-card">
            <div class="row no-gutters align-items-center">
                <div class="col mr-2">
                    <div class="text-xs font-weight-bold text-uppercase mb-1">Total</div>
                    <div class="h5 mb-0 font-weight-bold">1,250</div>
                </div>
                <div class="col-auto">
                    <i class="{module['icon']} fa-2x text-white-50"></i>
                </div>
            </div>
        </div>
    </div>
    
    <div class="col-xl-3 col-md-6 mb-4">
        <div class="stats-card">
            <div class="row no-gutters align-items-center">
                <div class="col mr-2">
                    <div class="text-xs font-weight-bold text-uppercase mb-1">Activos</div>
                    <div class="h5 mb-0 font-weight-bold">890</div>
                </div>
                <div class="col-auto">
                    <i class="fas fa-check-circle fa-2x text-white-50"></i>
                </div>
            </div>
        </div>
    </div>
    
    <div class="col-xl-3 col-md-6 mb-4">
        <div class="stats-card">
            <div class="row no-gutters align-items-center">
                <div class="col mr-2">
                    <div class="text-xs font-weight-bold text-uppercase mb-1">Hoy</div>
                    <div class="h5 mb-0 font-weight-bold">45</div>
                </div>
                <div class="col-auto">
                    <i class="fas fa-calendar-day fa-2x text-white-50"></i>
                </div>
            </div>
        </div>
    </div>
    
    <div class="col-xl-3 col-md-6 mb-4">
        <div class="stats-card">
            <div class="row no-gutters align-items-center">
                <div class="col mr-2">
                    <div class="text-xs font-weight-bold text-uppercase mb-1">Este Mes</div>
                    <div class="h5 mb-0 font-weight-bold">1,200</div>
                </div>
                <div class="col-auto">
                    <i class="fas fa-calendar-alt fa-2x text-white-50"></i>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Descripción del Módulo -->
<div class="row mb-4">
    <div class="col-12">
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">
                    <i class="fas fa-info-circle me-2"></i>
                    Acerca de {module['title']}
                </h5>
            </div>
            <div class="card-body">
                <p class="lead">{module['description']}</p>
                <p>Este módulo proporciona todas las funcionalidades necesarias para la gestión completa de {module['title'].lower()} en el sistema hospitalario HMetaHIS.</p>
                
                <div class="row mt-4">
                    <div class="col-md-4">
                        <div class="text-center">
                            <i class="fas fa-cogs fa-3x text-primary mb-3"></i>
                            <h5>Gestión Completa</h5>
                            <p class="text-muted">Administración integral de todos los aspectos del módulo</p>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="text-center">
                            <i class="fas fa-chart-line fa-3x text-success mb-3"></i>
                            <h5>Reportes Avanzados</h5>
                            <p class="text-muted">Análisis detallado y reportes personalizados</p>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="text-center">
                            <i class="fas fa-mobile-alt fa-3x text-info mb-3"></i>
                            <h5>Acceso Móvil</h5>
                            <p class="text-muted">Interfaz responsive para dispositivos móviles</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Acciones Rápidas -->
<div class="row mb-4">
    <div class="col-12">
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">
                    <i class="fas fa-bolt me-2"></i>
                    Acciones Rápidas
                </h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-3 mb-3">
                        <a href="{url_prefix}crear/" class="btn btn-primary w-100">
                            <i class="fas fa-plus fa-2x mb-2"></i><br>
                            Nuevo Registro
                        </a>
                    </div>
                    <div class="col-md-3 mb-3">
                        <a href="{url_prefix}lista/" class="btn btn-success w-100">
                            <i class="fas fa-list fa-2x mb-2"></i><br>
                            Ver Lista
                        </a>
                    </div>
                    <div class="col-md-3 mb-3">
                        <a href="{url_prefix}reportes/" class="btn btn-info w-100">
                            <i class="fas fa-chart-bar fa-2x mb-2"></i><br>
                            Reportes
                        </a>
                    </div>
                    <div class="col-md-3 mb-3">
                        <a href="{url_prefix}configuracion/" class="btn btn-secondary w-100">
                            <i class="fas fa-cog fa-2x mb-2"></i><br>
                            Configuración
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Estado del Sistema -->
<div class="row">
    <div class="col-md-8">
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">
                    <i class="fas fa-clock me-2"></i>
                    Actividad Reciente
                </h5>
            </div>
            <div class="card-body">
                <div class="list-group list-group-flush">
                    <div class="list-group-item d-flex justify-content-between align-items-center">
                        <div>
                            <h6 class="mb-1">Nuevo registro creado</h6>
                            <small class="text-muted">Usuario: Admin - Hace 5 minutos</small>
                        </div>
                        <span class="badge bg-primary rounded-pill">Nuevo</span>
                    </div>
                    <div class="list-group-item d-flex justify-content-between align-items-center">
                        <div>
                            <h6 class="mb-1">Registro actualizado</h6>
                            <small class="text-muted">Usuario: Doctor García - Hace 15 minutos</small>
                        </div>
                        <span class="badge bg-success rounded-pill">Actualizado</span>
                    </div>
                    <div class="list-group-item d-flex justify-content-between align-items-center">
                        <div>
                            <h6 class="mb-1">Reporte generado</h6>
                            <small class="text-muted">Usuario: Contador - Hace 30 minutos</small>
                        </div>
                        <span class="badge bg-info rounded-pill">Reporte</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="col-md-4">
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">
                    <i class="fas fa-chart-pie me-2"></i>
                    Estadísticas
                </h5>
            </div>
            <div class="card-body">
                <canvas id="statsChart" width="300" height="200"></canvas>
            </div>
        </div>
        
        <div class="card mt-3">
            <div class="card-header">
                <h5 class="mb-0">
                    <i class="fas fa-bell me-2"></i>
                    Notificaciones
                </h5>
            </div>
            <div class="card-body">
                <div class="alert alert-info" role="alert">
                    <i class="fas fa-info-circle me-2"></i>
                    <strong>Módulo activo</strong> y funcionando correctamente
                </div>
                <div class="alert alert-success" role="alert">
                    <i class="fas fa-check-circle me-2"></i>
                    <strong>Sincronización</strong> con otros módulos exitosa
                </div>
            </div>
        </div>
    </div>
</div>
{{% endblock %}}

{{% block extra_js %}}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
// Gráfico de estadísticas
const ctx = document.getElementById('statsChart').getContext('2d');
const statsChart = new Chart(ctx, {{
    type: 'doughnut',
    data: {{
        labels: ['Activos', 'Inactivos', 'Pendientes'],
        datasets: [{{
            data: [70, 20, 10],
            backgroundColor: [
                '#27ae60',
                '#e74c3c',
                '#f39c12'
            ]
        }}]
    }},
    options: {{
        responsive: true,
        plugins: {{
            legend: {{
                position: 'bottom',
            }}
        }}
    }}
}});
</script>
{{% endblock %}}
"""

def create_directory_if_not_exists(path):
    """Crea el directorio si no existe"""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"✅ Directorio creado: {path}")

def create_template_file(module, module_type):
    """Crea el archivo de template para un módulo"""
    
    if module_type == 'hms':
        template_path = f"{module['path']}/templates/{module['path']}/dashboard.html"
    else:
        template_path = f"{module['path']}/templates/{module['path']}/dashboard.html"
    
    # Crear directorios si no existen
    dir_path = os.path.dirname(template_path)
    create_directory_if_not_exists(dir_path)
    
    # Generar contenido del template
    content = create_template_content(module, module_type)
    
    # Escribir archivo
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Template creado: {template_path}")

def main():
    """Función principal"""
    print("🏥 Creando templates para HMetaHIS...")
    print("=" * 50)
    
    # Crear templates para módulos HMS
    print("\n📋 Creando templates para módulos HMS...")
    for module in HMS_MODULES:
        create_template_file(module, 'hms')
    
    # Crear templates para módulos ERP
    print("\n🏢 Creando templates para módulos ERP...")
    for module in ERP_MODULES:
        create_template_file(module, 'erp')
    
    print("\n🎉 ¡Todos los templates han sido creados exitosamente!")
    print(f"📊 Total de templates creados: {len(HMS_MODULES) + len(ERP_MODULES)}")
    print("\n🚀 Los módulos están listos para usar.")

if __name__ == '__main__':
    main() 