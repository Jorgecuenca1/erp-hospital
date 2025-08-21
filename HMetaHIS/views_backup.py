from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count


class LandingPageView(TemplateView):
    template_name = 'landing_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'HMetaHIS - Sistema ERP Hospitalario'
        return context


class AdminDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'admin_dashboard.html'
    login_url = '/admin/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Módulos HMS organizados por categorías
        context['hms_modules'] = {
            'core': [
                {'name': 'Base HMS', 'url': '/hms/', 'icon': 'fa-hospital', 'description': 'Sistema base hospitalario'},
                {'name': 'Suscripciones', 'url': '/hms/subscription/', 'icon': 'fa-credit-card', 'description': 'Gestión de suscripciones'},
            ],
            'specialties': [
                {'name': 'Ginecología', 'url': '/hms/gynecology/', 'icon': 'fa-female', 'description': 'Ginecología y obstetricia'},
                {'name': 'Oftalmología', 'url': '/hms/ophthalmology/', 'icon': 'fa-eye', 'description': 'Cuidado de la vista'},
                {'name': 'Pediatría', 'url': '/hms/pediatrics/', 'icon': 'fa-child', 'description': 'Cuidado pediátrico'},
                {'name': 'Estética', 'url': '/hms/aesthetic/', 'icon': 'fa-star', 'description': 'Medicina estética'},
                {'name': 'Dental', 'url': '/hms/dental/', 'icon': 'fa-tooth', 'description': 'Odontología'},
            ],
            'surgery': [
                {'name': 'Cirugía', 'url': '/hms/surgery/', 'icon': 'fa-cut', 'description': 'Cirugía general'},
                {'name': 'Quirófanos', 'url': '/hms/operation-theater/', 'icon': 'fa-procedures', 'description': 'Gestión de quirófanos'},
            ],
            'diagnostics': [
                {'name': 'Laboratorio', 'url': '/hms/laboratory/', 'icon': 'fa-flask', 'description': 'Laboratorio clínico'},
                {'name': 'Radiología', 'url': '/hms/radiology/', 'icon': 'fa-x-ray', 'description': 'Radiología e imágenes'},
            ],
            'emergency': [
                {'name': 'Emergencias', 'url': '/hms/emergency/', 'icon': 'fa-ambulance', 'description': 'Servicios de emergencia'},
                {'name': 'Enfermería', 'url': '/hms/nursing/', 'icon': 'fa-user-nurse', 'description': 'Gestión de enfermería'},
            ],
            'patient_services': [
                {'name': 'Banco de Sangre', 'url': '/hms/blood-bank/', 'icon': 'fa-tint', 'description': 'Banco de sangre'},
                {'name': 'Hospitalización', 'url': '/hms/hospitalization/', 'icon': 'fa-bed', 'description': 'Gestión de hospitalización'},
                {'name': 'Portal Paciente', 'url': '/hms/patient-portal/', 'icon': 'fa-user-circle', 'description': 'Portal del paciente'},
                {'name': 'Farmacia HMS', 'url': '/hms/pharmacy/', 'icon': 'fa-pills', 'description': 'Farmacia hospitalaria'},
            ],
            'digital_health': [
                {'name': 'Citas Online', 'url': '/hms/online-appointment/', 'icon': 'fa-calendar-plus', 'description': 'Citas en línea'},
                {'name': 'Webcam', 'url': '/hms/webcam/', 'icon': 'fa-video', 'description': 'Gestión de webcam'},
                {'name': 'Video Call', 'url': '/hms/video-call/', 'icon': 'fa-video', 'description': 'Videollamadas médicas'},
                {'name': 'Consentimientos', 'url': '/hms/consent-form/', 'icon': 'fa-file-signature', 'description': 'Consentimientos digitales'},
            ],
            'business': [
                {'name': 'Seguros', 'url': '/hms/insurance/', 'icon': 'fa-shield-alt', 'description': 'Seguros médicos'},
                {'name': 'Comisiones', 'url': '/hms/commission/', 'icon': 'fa-percentage', 'description': 'Comisiones médicas'},
                {'name': 'Certificaciones', 'url': '/hms/certification/', 'icon': 'fa-certificate', 'description': 'Certificaciones médicas'},
            ],
            'user_experience': [
                {'name': 'Pantalla Espera', 'url': '/hms/waiting-screen/', 'icon': 'fa-tv', 'description': 'Pantallas de espera'},
            ]
        }

        # Módulos ERP organizados por categorías
        context['erp_modules'] = {
            'core_business': [
                {'name': 'Pacientes', 'url': '/patients/', 'icon': 'fa-users', 'description': 'Gestión de pacientes'},
                {'name': 'Profesionales', 'url': '/professionals/', 'icon': 'fa-user-md', 'description': 'Gestión de profesionales'},
                {'name': 'Citas', 'url': '/appointments/citas/', 'icon': 'fa-calendar', 'description': 'Gestión de citas'},
                {'name': 'Historias Clínicas', 'url': '/patients/historias/', 'icon': 'fa-notes-medical', 'description': 'Historias médicas'},
                {'name': 'Perfil Hospital', 'url': '/hospital_profile/', 'icon': 'fa-hospital', 'description': 'Perfil del hospital'},
            ],
            'admision_recepcion': [
                {'name': 'Admisión - Recepción', 'url': '/admision/', 'icon': 'fa-clipboard-check', 'description': 'Dashboard principal de admisión'},
                {'name': 'Órdenes de Servicios', 'url': '/admision/ordenes-servicios/', 'icon': 'fa-file-medical', 'description': 'Crear y gestionar órdenes de servicios médicos'},
                {'name': 'Seguimiento a Pacientes', 'url': '/admision/seguimiento-pacientes/', 'icon': 'fa-user-clock', 'description': 'Seguimiento en tiempo real del estado de pacientes'},
                {'name': 'Seguimiento a Atenciones', 'url': '/admision/seguimiento-atenciones/', 'icon': 'fa-stethoscope', 'description': 'Seguimiento de atenciones médicas por día o paciente'},
                {'name': 'Portal Empresas', 'url': '/admision/portal-empresas/', 'icon': 'fa-building', 'description': 'Servicios solicitados por empresas'},
                {'name': 'Lista de Precios', 'url': '/admision/lista-precios/', 'icon': 'fa-dollar-sign', 'description': 'Precios por convenios y contratos'},
                {'name': 'Imprimir Historias', 'url': '/admision/imprimir-historias/', 'icon': 'fa-print', 'description': 'Impresión de historias clínicas'},
                {'name': 'Empresas Historias', 'url': '/admision/empresas-historias/', 'icon': 'fa-briefcase-medical', 'description': 'Historias clínicas por empresa'},
            ],
            'fichas_clinicas': [
                {'name': 'Fichas Clínicas', 'url': '/admision/fichas-clinicas/', 'icon': 'fa-notes-medical', 'description': 'Dashboard de fichas clínicas'},
                {'name': 'Evaluación Ocupacional', 'url': '/admision/evaluacion-ocupacional/nueva/', 'icon': 'fa-hard-hat', 'description': 'Evaluaciones médicas ocupacionales completas'},
                {'name': 'Examen Visual', 'url': '/admision/examen-visual/nueva/', 'icon': 'fa-eye', 'description': 'Exámenes oftalmológicos detallados'},
                {'name': 'Audiometría', 'url': '/admision/audiometria/nueva/', 'icon': 'fa-volume-up', 'description': 'Evaluaciones auditivas con clasificación CAOHC'},
                {'name': 'Espirometría', 'url': '/admision/espirometria/nueva/', 'icon': 'fa-lungs', 'description': 'Pruebas de función pulmonar'},
                {'name': 'Osteomuscular', 'url': '/admision/osteomuscular/nueva/', 'icon': 'fa-bone', 'description': 'Evaluaciones osteomusculares y posturales'},
                {'name': 'Historia Clínica General', 'url': '/admision/historia-clinica-general/nueva/', 'icon': 'fa-file-medical-alt', 'description': 'Historias clínicas generales completas'},
                {'name': 'Historias Cerradas', 'url': '/admision/historias-cerradas/', 'icon': 'fa-archive', 'description': 'Consulta de historias clínicas completadas'},
            ],
            'financial': [
                {'name': 'Contabilidad', 'url': '/accounting/', 'icon': 'fa-calculator', 'description': 'Sistema contable'},
                {'name': 'Facturación', 'url': '/billing/', 'icon': 'fa-file-invoice', 'description': 'Facturación médica'},
                {'name': 'Ventas', 'url': '/sales/', 'icon': 'fa-chart-line', 'description': 'Gestión de ventas'},
                {'name': 'Compras', 'url': '/purchases/', 'icon': 'fa-shopping-cart', 'description': 'Gestión de compras'},
            ],
            'inventory': [
                {'name': 'Inventarios', 'url': '/inventories/', 'icon': 'fa-boxes', 'description': 'Control de inventarios'},
                {'name': 'Farmacia', 'url': '/pharmacy/', 'icon': 'fa-pills', 'description': 'Farmacia del hospital'},
                {'name': 'Laboratorio', 'url': '/laboratories/', 'icon': 'fa-flask', 'description': 'Laboratorio clínico'},
                {'name': 'Activos', 'url': '/asset_management/', 'icon': 'fa-tools', 'description': 'Gestión de activos'},
            ],
            'hr_quality': [
                {'name': 'Recursos Humanos', 'url': '/hr/', 'icon': 'fa-users', 'description': 'Gestión de RRHH'},
                {'name': 'Calidad', 'url': '/quality_management/', 'icon': 'fa-award', 'description': 'Gestión de calidad'},
                {'name': 'Reportes', 'url': '/reports/', 'icon': 'fa-chart-bar', 'description': 'Reportes y análisis'},
            ],
            'commerce': [
                {'name': 'Punto de Venta', 'url': '/pos/', 'icon': 'fa-cash-register', 'description': 'Punto de venta'},
                {'name': 'E-commerce', 'url': '/ecommerce/', 'icon': 'fa-shopping-bag', 'description': 'Comercio electrónico'},
                {'name': 'CRM', 'url': '/crm/', 'icon': 'fa-handshake', 'description': 'Gestión de relaciones'},
                {'name': 'Suscripciones', 'url': '/subscriptions/', 'icon': 'fa-sync', 'description': 'Gestión de suscripciones'},
            ],
            'digital': [
                {'name': 'Sitio Web', 'url': '/website/paginas/', 'icon': 'fa-globe', 'description': 'Gestión del sitio web'},
                {'name': 'Blog', 'url': '/blog/', 'icon': 'fa-blog', 'description': 'Sistema de blog'},
                {'name': 'Foro', 'url': '/forum/', 'icon': 'fa-comments', 'description': 'Foro de discusión'},
                {'name': 'E-learning', 'url': '/elearning/', 'icon': 'fa-graduation-cap', 'description': 'Plataforma educativa'},
                {'name': 'Live Chat', 'url': '/livechat/', 'icon': 'fa-comment', 'description': 'Chat en vivo'},
            ]
        }

        # Módulos ESG (Sostenibilidad)
        context['esg_modules'] = [
            {'name': 'Reportes ESG', 'url': '/esg/', 'icon': 'fa-leaf', 'description': 'Reportes de sostenibilidad'},
            {'name': 'Huella Carbono', 'url': '/carbon/', 'icon': 'fa-tree', 'description': 'Análisis de huella de carbono'},
            {'name': 'Métricas Sociales', 'url': '/social/', 'icon': 'fa-heart', 'description': 'Métricas de impacto social'},
        ]

        # Estadísticas básicas
        context['stats'] = {
            'total_modules': 91,
            'hms_modules': 24,
            'erp_modules': 43,
            'esg_modules': 3,
            'completion_rate': 95
        }

        return context


@login_required
def module_status_api(request):
    """API para obtener el estado de los módulos"""
    try:
        # Aquí puedes agregar lógica para verificar el estado real de cada módulo
        # Por ejemplo, verificar si las tablas existen, si hay datos, etc.
        
        module_status = {
            'hms_modules': {
                'total': 24,
                'active': 24,
                'with_data': 12,
                'errors': 0
            },
            'erp_modules': {
                'total': 27,
                'active': 27,
                'with_data': 27,
                'errors': 0
            },
            'last_updated': '2024-01-15 10:30:00'
        }
        
        return JsonResponse(module_status)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500) 