#!/usr/bin/env python3
"""
Script para crear vistas de dashboard mínimas para todos los módulos
"""

# Vista de dashboard simple para appointments
APPOINTMENTS_DASHBOARD = '''
class AppointmentsDashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard principal de citas"""
    template_name = 'appointments/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Citas'
        context['citas_hoy'] = 0  # Placeholder
        context['citas_total'] = 0  # Placeholder
        return context
'''

# Vista de dashboard simple para medical_records
MEDICAL_RECORDS_DASHBOARD = '''
class MedicalRecordsDashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard principal de historias clínicas"""
    template_name = 'medical_records/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Historias Clínicas'
        context['historias_total'] = 0  # Placeholder
        return context
'''

# Vista de dashboard simple para pharmacy
PHARMACY_DASHBOARD = '''
class PharmacyDashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard principal de farmacia"""
    template_name = 'pharmacy/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Farmacia'
        context['medicamentos_total'] = 0  # Placeholder
        return context
'''

# Vista de dashboard simple para laboratories
LABORATORIES_DASHBOARD = '''
class LaboratoriesDashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard principal de laboratorios"""
    template_name = 'laboratories/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Laboratorios'
        context['examenes_total'] = 0  # Placeholder
        return context
'''

# Vista de dashboard simple para website
WEBSITE_DASHBOARD = '''
class WebsiteDashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard principal del sitio web"""
    template_name = 'website/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Sitio Web'
        context['paginas_total'] = 0  # Placeholder
        return context
'''

# Otros dashboards que necesitamos
BLOG_DASHBOARD = '''
class BlogDashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard principal del blog"""
    template_name = 'blog/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Blog'
        context['articulos_total'] = 0  # Placeholder
        return context
'''

LIVECHAT_DASHBOARD = '''
class LiveChatDashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard principal del chat en vivo"""
    template_name = 'livechat/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Live Chat'
        context['conversaciones_activas'] = 0  # Placeholder
        return context
'''

SUBSCRIPTIONS_DASHBOARD = '''
class SubscriptionsDashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard principal de suscripciones"""
    template_name = 'subscriptions/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Suscripciones'
        context['suscripciones_activas'] = 0  # Placeholder
        return context
'''

print("📋 VISTAS DE DASHBOARD NECESARIAS:")
print("=" * 50)

dashboards_needed = [
    ('appointments', 'AppointmentsDashboardView'),
    ('medical_records', 'MedicalRecordsDashboardView'),
    ('pharmacy', 'PharmacyDashboardView'),
    ('laboratories', 'LaboratoriesDashboardView'),
    ('website', 'WebsiteDashboardView'),
    ('blog', 'BlogDashboardView'),
    ('livechat', 'LiveChatDashboardView'),
    ('subscriptions', 'SubscriptionsDashboardView'),
]

for module, view_name in dashboards_needed:
    print(f"📝 {module}: {view_name}")

print(f"\n✅ {len(dashboards_needed)} vistas necesarias para completar dashboards")
print("🔧 Cada vista debe agregarse al archivo views.py del módulo correspondiente")
print("📁 Cada vista necesita un template dashboard.html en su directorio")
