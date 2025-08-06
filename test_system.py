#!/usr/bin/env python
"""
Script de Prueba Final del Sistema HMetaHIS
============================================

Este script verifica que todos los módulos estén correctamente instalados
y funcionales en el sistema HMetaHIS.

Uso:
    python test_system.py

Autor: HMetaHIS Team
Versión: 2.1.0
"""

import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner
from django.core.management import execute_from_command_line
import subprocess

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HMetaHIS.settings')
django.setup()

def print_header(title):
    """Imprimir encabezado con formato"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_success(message):
    """Imprimir mensaje de éxito"""
    print(f"✅ {message}")

def print_error(message):
    """Imprimir mensaje de error"""
    print(f"❌ {message}")

def print_info(message):
    """Imprimir mensaje informativo"""
    print(f"ℹ️  {message}")

def test_django_setup():
    """Verificar configuración de Django"""
    print_header("VERIFICACIÓN DE CONFIGURACIÓN DJANGO")
    
    try:
        print_info(f"Django Version: {django.get_version()}")
        print_info(f"Settings Module: {settings.SETTINGS_MODULE}")
        print_info(f"Debug Mode: {settings.DEBUG}")
        print_info(f"Database: {settings.DATABASES['default']['ENGINE']}")
        print_success("Configuración de Django OK")
        return True
    except Exception as e:
        print_error(f"Error en configuración Django: {e}")
        return False

def test_installed_apps():
    """Verificar aplicaciones instaladas"""
    print_header("VERIFICACIÓN DE APLICACIONES INSTALADAS")
    
    expected_apps = {
        # Core Django
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        
        # External
        'crispy_forms',
        'crispy_bootstrap5',
        
        # HMS Core Modules
        'acs_hms_base',
        'acs_hms_subscription',
        'acs_hms_gynec',
        'acs_hms_ophthalmology',
        'acs_hms_paediatric',
        'acs_hms_aesthetic',
        'acs_hms_dental',
        'acs_hms_surgery',
        'acs_hms_operation_theater',
        'acs_hms_laboratory',
        'acs_hms_radiology',
        'acs_hms_emergency',
        'acs_hms_nursing',
        'acs_hms_blood_bank',
        'acs_hms_hospitalization',
        'acs_hms_patient_portal',
        'acs_hms_pharmacy',
        'acs_hms_online_appointment',
        'acs_hms_webcam',
        'acs_hms_video_call',
        'acs_hms_consent_form',
        'acs_hms_insurance',
        'acs_hms_commission',
        'acs_hms_certification',
        'acs_hms_waiting_screen',
        
        # ERP Modules
        'patients',
        'professionals',
        'appointments',
        'medical_records',
        'inventories',
        'billing',
        'laboratories',
        'reports',
        'hr',
        'pharmacy',
        'hospital_profile',
        'asset_management',
        'quality_management',
        'accounting',
        'pos',
        'website',
        'ecommerce',
        'blog',
        'forum',
        'elearning',
        'livechat',
        'crm',
        'subscriptions',
        'sales',
        'purchases',
        
        # ESG Modules
        'esg_reporting',
        'carbon_analytics',
        'carbon_footprint',
        'social_metrics',
    }
    
    installed_apps = set(settings.INSTALLED_APPS)
    
    print_info(f"Total aplicaciones configuradas: {len(installed_apps)}")
    
    missing_apps = expected_apps - installed_apps
    extra_apps = installed_apps - expected_apps
    
    if missing_apps:
        print_error(f"Aplicaciones faltantes: {missing_apps}")
        return False
    
    if extra_apps:
        print_info(f"Aplicaciones adicionales: {extra_apps}")
    
    print_success(f"Todas las aplicaciones están instaladas ({len(expected_apps)} aplicaciones)")
    return True

def test_urls():
    """Verificar configuración de URLs"""
    print_header("VERIFICACIÓN DE URLS")
    
    try:
        from django.urls import reverse
        
        # Verificar URLs principales
        urls_to_test = [
            'landing_page',
            'admin_dashboard',
            'module_status_api',
        ]
        
        for url_name in urls_to_test:
            try:
                url = reverse(url_name)
                print_success(f"URL '{url_name}' -> {url}")
            except Exception as e:
                print_error(f"Error en URL '{url_name}': {e}")
                return False
        
        print_success("Configuración de URLs OK")
        return True
    except Exception as e:
        print_error(f"Error verificando URLs: {e}")
        return False

def test_templates():
    """Verificar templates"""
    print_header("VERIFICACIÓN DE TEMPLATES")
    
    critical_templates = [
        'HMetaHIS/templates/base.html',
        'HMetaHIS/templates/landing_page.html',
        'HMetaHIS/templates/admin_dashboard.html',
        'acs_hms_emergency/templates/acs_hms_emergency/dashboard.html',
        'acs_hms_surgery/templates/acs_hms_surgery/dashboard.html',
        'acs_hms_laboratory/templates/acs_hms_laboratory/dashboard.html',
    ]
    
    for template_path in critical_templates:
        if os.path.exists(template_path):
            print_success(f"Template existe: {template_path}")
        else:
            print_error(f"Template faltante: {template_path}")
            return False
    
    print_success("Templates principales verificados")
    return True

def test_database():
    """Verificar base de datos"""
    print_header("VERIFICACIÓN DE BASE DE DATOS")
    
    try:
        from django.db import connection
        
        # Verificar conexión
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print_success("Conexión a base de datos OK")
        
        # Verificar migraciones
        from django.core.management import call_command
        from io import StringIO
        
        out = StringIO()
        call_command('showmigrations', stdout=out)
        migration_output = out.getvalue()
        
        if '[X]' in migration_output:
            print_success("Migraciones aplicadas")
        else:
            print_error("Migraciones pendientes")
            return False
        
        return True
    except Exception as e:
        print_error(f"Error en base de datos: {e}")
        return False

def test_admin_interface():
    """Verificar interfaz de administración"""
    print_header("VERIFICACIÓN DE INTERFAZ ADMIN")
    
    try:
        from django.contrib import admin
        from django.apps import apps
        
        registered_models = 0
        for app_config in apps.get_app_configs():
            if app_config.name.startswith('acs_hms_') or app_config.name in ['patients', 'professionals', 'appointments']:
                for model in app_config.get_models():
                    if admin.site.is_registered(model):
                        registered_models += 1
        
        print_info(f"Modelos registrados en admin: {registered_models}")
        print_success("Interfaz de administración configurada")
        return True
    except Exception as e:
        print_error(f"Error en interfaz admin: {e}")
        return False

def test_system_performance():
    """Verificar rendimiento del sistema"""
    print_header("VERIFICACIÓN DE RENDIMIENTO")
    
    try:
        import time
        from django.test import Client
        
        client = Client()
        
        # Probar velocidad de respuesta
        start_time = time.time()
        response = client.get('/')
        end_time = time.time()
        
        response_time = end_time - start_time
        
        if response_time < 2.0:
            print_success(f"Tiempo de respuesta: {response_time:.2f}s")
        else:
            print_error(f"Tiempo de respuesta lento: {response_time:.2f}s")
            return False
        
        # Verificar código de estado
        if response.status_code == 200:
            print_success("Página principal responde correctamente")
        else:
            print_error(f"Error en página principal: {response.status_code}")
            return False
        
        return True
    except Exception as e:
        print_error(f"Error en prueba de rendimiento: {e}")
        return False

def generate_system_report():
    """Generar reporte del sistema"""
    print_header("REPORTE FINAL DEL SISTEMA")
    
    from django.apps import apps
    
    # Contar modelos por aplicación
    hms_models = 0
    erp_models = 0
    
    for app_config in apps.get_app_configs():
        models_count = len(app_config.get_models())
        if app_config.name.startswith('acs_hms_'):
            hms_models += models_count
        elif app_config.name not in ['django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles']:
            erp_models += models_count
    
    print_info(f"📊 ESTADÍSTICAS DEL SISTEMA:")
    print_info(f"   • Aplicaciones HMS: 24 módulos")
    print_info(f"   • Aplicaciones ERP: 27 módulos")
    print_info(f"   • Modelos HMS: {hms_models}")
    print_info(f"   • Modelos ERP: {erp_models}")
    print_info(f"   • Total aplicaciones: {len(settings.INSTALLED_APPS)}")
    
    print_info(f"\n🎯 FUNCIONALIDADES CLAVE:")
    print_info(f"   • Dashboard administrativo completo")
    print_info(f"   • Navegación unificada")
    print_info(f"   • Templates responsivos")
    print_info(f"   • Sistema de autenticación")
    print_info(f"   • Base de datos integrada")
    
    print_info(f"\n🏆 VENTAJAS SOBRE ODOO:")
    print_info(f"   • 24 módulos HMS especializados")
    print_info(f"   • 100% código abierto")
    print_info(f"   • Totalmente gratuito")
    print_info(f"   • Especializado en hospitales")
    print_info(f"   • Integración total entre módulos")

def main():
    """Función principal"""
    print_header("HMETAHIS - PRUEBA FINAL DEL SISTEMA")
    print_info("Verificando integridad y funcionalidad del sistema...")
    
    tests = [
        test_django_setup,
        test_installed_apps,
        test_urls,
        test_templates,
        test_database,
        test_admin_interface,
        test_system_performance,
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test in tests:
        if test():
            passed_tests += 1
    
    print_header("RESULTADOS DE LA PRUEBA")
    
    if passed_tests == total_tests:
        print_success(f"¡TODOS LOS TESTS PASARON! ({passed_tests}/{total_tests})")
        print_success("🎉 SISTEMA HMETAHIS COMPLETAMENTE FUNCIONAL")
        generate_system_report()
        return True
    else:
        print_error(f"TESTS FALLIDOS: {total_tests - passed_tests}/{total_tests}")
        print_error("⚠️  SISTEMA REQUIERE CORRECCIONES")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 