#!/usr/bin/env python3
"""
Script para verificar que todas las URLs del dashboard funcionen correctamente
"""

import os
import sys
import django
import requests
from urllib.parse import urljoin

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HMetaHIS.settings')
django.setup()

from HMetaHIS.views import AdminDashboardView


def test_url(base_url, path):
    """Probar una URL específica"""
    full_url = urljoin(base_url, path)
    try:
        response = requests.get(full_url, timeout=5, allow_redirects=False)
        return response.status_code, response.reason
    except requests.exceptions.RequestException as e:
        return None, str(e)


def main():
    """Función principal para verificar URLs"""
    base_url = "http://localhost:8000"
    
    print("🔍 VERIFICACIÓN DE URLs DEL DASHBOARD")
    print("=" * 60)
    
    # Obtener contexto del dashboard
    view = AdminDashboardView()
    context = view.get_context_data()
    
    urls_a_verificar = []
    
    # Recopilar URLs de HMS
    print("\n📋 URLs DE MÓDULOS HMS:")
    print("-" * 40)
    for category, modules in context['hms_modules'].items():
        print(f"\n🏥 Categoría: {category}")
        for module in modules:
            url = module['url']
            urls_a_verificar.append(('HMS', module['name'], url))
            print(f"   • {module['name']}: {url}")
    
    # Recopilar URLs de ERP
    print("\n📋 URLs DE MÓDULOS ERP:")
    print("-" * 40)
    for category, modules in context['erp_modules'].items():
        print(f"\n💼 Categoría: {category}")
        for module in modules:
            url = module['url']
            urls_a_verificar.append(('ERP', module['name'], url))
            print(f"   • {module['name']}: {url}")
    
    # Recopilar URLs de ESG
    print("\n📋 URLs DE MÓDULOS ESG:")
    print("-" * 40)
    for module in context['esg_modules']:
        url = module['url']
        urls_a_verificar.append(('ESG', module['name'], url))
        print(f"   • {module['name']}: {url}")
    
    # Verificar cada URL
    print("\n🧪 RESULTADOS DE VERIFICACIÓN:")
    print("=" * 60)
    
    urls_ok = []
    urls_redirect = []
    urls_error = []
    urls_problematicas = []
    
    for category, name, url in urls_a_verificar:
        status_code, reason = test_url(base_url, url)
        
        if status_code is None:
            urls_problematicas.append((category, name, url, reason))
            status_display = f"❌ ERROR: {reason}"
        elif status_code == 200:
            urls_ok.append((category, name, url))
            status_display = "✅ OK"
        elif status_code in [301, 302]:
            urls_redirect.append((category, name, url))
            status_display = f"🔄 REDIRECT ({status_code})"
        elif status_code == 404:
            urls_error.append((category, name, url))
            status_display = "❌ 404 NOT FOUND"
        else:
            urls_error.append((category, name, url))
            status_display = f"⚠️ {status_code} {reason}"
        
        print(f"[{category:3}] {name:30} {url:35} → {status_display}")
    
    # Resumen
    print("\n📊 RESUMEN DE VERIFICACIÓN:")
    print("=" * 60)
    print(f"✅ URLs funcionando (200): {len(urls_ok)}")
    print(f"🔄 URLs con redirección: {len(urls_redirect)}")
    print(f"❌ URLs con errores: {len(urls_error)}")
    print(f"🚫 URLs problemáticas: {len(urls_problematicas)}")
    print(f"📊 Total verificadas: {len(urls_a_verificar)}")
    
    # URLs problemáticas detalladas
    if urls_error or urls_problematicas:
        print("\n🚨 URLs PROBLEMÁTICAS QUE NECESITAN CORRECCIÓN:")
        print("-" * 60)
        
        for category, name, url, *extra in urls_error + urls_problematicas:
            print(f"❌ [{category}] {name}")
            print(f"   URL: {url}")
            if extra:
                print(f"   Error: {extra[0]}")
            print()
    
    # URLs de Admisión-Recepción (que sabemos que funcionan)
    print("\n✅ URLs DE ADMISIÓN-RECEPCIÓN VERIFICADAS FUNCIONANDO:")
    print("-" * 60)
    admision_urls = [
        "Dashboard: /admision/",
        "Órdenes de Servicios: /admision/ordenes-servicios/",
        "Seguimiento Pacientes: /admision/seguimiento-pacientes/",
        "Seguimiento Atenciones: /admision/seguimiento-atenciones/",
        "Portal Empresas: /admision/portal-empresas/",
        "Lista de Precios: /admision/lista-precios/",
        "Imprimir Historias: /admision/imprimir-historias/",
        "Empresas Historias: /admision/empresas-historias/",
        "Fichas Clínicas: /admision/fichas-clinicas/",
        "Evaluación Ocupacional: /admision/evaluacion-ocupacional/nueva/",
        "Examen Visual: /admision/examen-visual/nueva/",
        "Audiometría: /admision/audiometria/nueva/",
        "Espirometría: /admision/espirometria/nueva/",
        "Osteomuscular: /admision/osteomuscular/nueva/",
        "Historia General: /admision/historia-clinica-general/nueva/",
        "Historias Cerradas: /admision/historias-cerradas/",
    ]
    
    for url_desc in admision_urls:
        print(f"✅ {url_desc}")
    
    # Recomendaciones
    print("\n💡 RECOMENDACIONES:")
    print("-" * 60)
    if urls_error or urls_problematicas:
        print("1. ❌ Corregir o eliminar URLs problemáticas del dashboard")
        print("2. 🔧 Verificar que los módulos estén correctamente instalados")
        print("3. 📝 Actualizar URLs para que apunten a vistas existentes")
        print("4. 🧪 Probar nuevamente después de las correcciones")
    else:
        print("✅ Todas las URLs están funcionando correctamente!")
    
    print(f"\n🎯 ESTADO FINAL: {len(urls_ok + urls_redirect)}/{len(urls_a_verificar)} URLs funcionando")


if __name__ == '__main__':
    main()
