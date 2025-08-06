#!/usr/bin/env python
"""
Script para crear vistas básicas para todos los módulos
"""
import os

# Configuración de módulos HMS
HMS_MODULES = [
    'acs_hms_gynec', 'acs_hms_ophthalmology', 'acs_hms_paediatric', 'acs_hms_aesthetic',
    'acs_hms_dental', 'acs_hms_surgery', 'acs_hms_operation_theater', 'acs_hms_laboratory',
    'acs_hms_radiology', 'acs_hms_emergency', 'acs_hms_nursing', 'acs_hms_blood_bank',
    'acs_hms_hospitalization', 'acs_hms_patient_portal', 'acs_hms_pharmacy',
    'acs_hms_online_appointment', 'acs_hms_webcam', 'acs_hms_video_call',
    'acs_hms_consent_form', 'acs_hms_subscription', 'acs_hms_insurance',
    'acs_hms_commission', 'acs_hms_certification', 'acs_hms_waiting_screen'
]

# Configuración de módulos ERP
ERP_MODULES = [
    'professionals', 'appointments', 'medical_records', 'hospital_profile',
    'billing', 'sales', 'purchases', 'inventories', 'pharmacy', 'laboratories',
    'asset_management', 'hr', 'quality_management', 'reports', 'pos',
    'ecommerce', 'crm', 'subscriptions', 'website', 'blog', 'forum',
    'elearning', 'livechat'
]

def create_views_content(module_name, module_type):
    """Genera el contenido de las vistas para un módulo"""
    
    if module_type == 'hms':
        app_name = module_name
        title = module_name.replace('acs_hms_', '').replace('_', ' ').title()
    else:
        app_name = module_name
        title = module_name.replace('_', ' ').title()
    
    return f"""from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class {title.replace(' ', '')}DashboardView(LoginRequiredMixin, TemplateView):
    template_name = '{app_name}/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = '{title}'
        context['module_type'] = '{module_type}'
        return context

class {title.replace(' ', '')}ListView(LoginRequiredMixin, TemplateView):
    template_name = '{app_name}/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = '{title}'
        return context

class {title.replace(' ', '')}CreateView(LoginRequiredMixin, TemplateView):
    template_name = '{app_name}/create.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = '{title}'
        return context

class {title.replace(' ', '')}DetailView(LoginRequiredMixin, TemplateView):
    template_name = '{app_name}/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = '{title}'
        return context

class {title.replace(' ', '')}UpdateView(LoginRequiredMixin, TemplateView):
    template_name = '{app_name}/update.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = '{title}'
        return context

class {title.replace(' ', '')}DeleteView(LoginRequiredMixin, TemplateView):
    template_name = '{app_name}/delete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = '{title}'
        return context

class {title.replace(' ', '')}ReportsView(LoginRequiredMixin, TemplateView):
    template_name = '{app_name}/reports.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = '{title}'
        return context
"""

def create_urls_content(module_name, module_type):
    """Genera el contenido de las URLs para un módulo"""
    
    if module_type == 'hms':
        app_name = module_name
        title = module_name.replace('acs_hms_', '').replace('_', ' ').title()
    else:
        app_name = module_name
        title = module_name.replace('_', ' ').title()
    
    return f"""from django.urls import path
from . import views

app_name = '{app_name}'

urlpatterns = [
    path('', views.{title.replace(' ', '')}DashboardView.as_view(), name='dashboard'),
    path('lista/', views.{title.replace(' ', '')}ListView.as_view(), name='list'),
    path('crear/', views.{title.replace(' ', '')}CreateView.as_view(), name='create'),
    path('<int:pk>/', views.{title.replace(' ', '')}DetailView.as_view(), name='detail'),
    path('<int:pk>/editar/', views.{title.replace(' ', '')}UpdateView.as_view(), name='update'),
    path('<int:pk>/eliminar/', views.{title.replace(' ', '')}DeleteView.as_view(), name='delete'),
    path('reportes/', views.{title.replace(' ', '')}ReportsView.as_view(), name='reports'),
]
"""

def create_file_if_not_exists(file_path, content):
    """Crea el archivo si no existe"""
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Archivo creado: {file_path}")
    else:
        print(f"⚠️  Archivo ya existe: {file_path}")

def create_module_files(module_name, module_type):
    """Crea los archivos necesarios para un módulo"""
    
    # Crear views.py
    views_content = create_views_content(module_name, module_type)
    views_path = f"{module_name}/views.py"
    create_file_if_not_exists(views_path, views_content)
    
    # Crear urls.py
    urls_content = create_urls_content(module_name, module_type)
    urls_path = f"{module_name}/urls.py"
    create_file_if_not_exists(urls_path, urls_content)

def main():
    """Función principal"""
    print("🏥 Creando vistas y URLs para HMetaHIS...")
    print("=" * 50)
    
    # Crear archivos para módulos HMS
    print("\n📋 Creando archivos para módulos HMS...")
    for module in HMS_MODULES:
        create_module_files(module, 'hms')
    
    # Crear archivos para módulos ERP
    print("\n🏢 Creando archivos para módulos ERP...")
    for module in ERP_MODULES:
        create_module_files(module, 'erp')
    
    print("\n🎉 ¡Todos los archivos han sido creados exitosamente!")
    print(f"📊 Total de módulos procesados: {len(HMS_MODULES) + len(ERP_MODULES)}")
    print("\n🚀 Los módulos están listos para usar.")

if __name__ == '__main__':
    main() 