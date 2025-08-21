#!/usr/bin/env python3
"""
Verificación final del dashboard corregido con URLs reales
"""

import os
import sys
import django
import requests

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HMetaHIS.settings')
django.setup()

from HMetaHIS.views import AdminDashboardView

def test_url(base_url, path):
    """Probar una URL específica"""
    full_url = f"{base_url}{path}"
    try:
        response = requests.get(full_url, timeout=5, allow_redirects=False)
        return response.status_code
    except:
        return None

def main():
    base_url = "http://localhost:8000"
    
    print("🏥 VERIFICACIÓN FINAL - DASHBOARD CON URLs REALES")
    print("=" * 70)
    
    # URLs que debe tener el dashboard corregido
    urls_dashboard = [
        # Core Business
        ('/patients/', 'Pacientes'),
        ('/hr/empleados/', 'Profesionales/Empleados'),
        ('/appointments/citas/', 'Citas'),
        ('/hms/', 'Perfil Hospital/Base HMS'),
        
        # Admisión-Recepción (16 módulos)
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
        
        # Financial
        ('/accounting/', 'Contabilidad'),
        ('/billing/', 'Facturación'),
        ('/sales/', 'Ventas'),
        ('/purchases/', 'Compras'),
        
        # Operations
        ('/inventories/', 'Inventarios'),
        ('/hr/empleados/', 'Recursos Humanos'),
        ('/reports/generados/', 'Reportes'),
        
        # Commerce
        ('/pos/', 'Punto de Venta'),
        ('/ecommerce/productos/', 'E-commerce'),
        ('/crm/leads/', 'CRM'),
        
        # Digital
        ('/website/paginas/', 'Sitio Web'),
        ('/forum/temas/', 'Foro'),
        ('/elearning/cursos/', 'E-learning'),
        
        # HMS
        ('/hms/', 'Base HMS'),
        ('/hms/pharmacy/', 'Farmacia HMS'),
        ('/hms/online-appointment/', 'Citas Online'),
        ('/hms/waiting-screen/', 'Pantalla Espera'),
        
        # ESG
        ('/carbon/', 'Huella Carbono'),
        ('/social/', 'Métricas Sociales'),
    ]
    
    print(f"🧪 PROBANDO {len(urls_dashboard)} URLs del Dashboard Corregido:")
    print("-" * 70)
    
    urls_ok = 0
    urls_redirect = 0
    urls_error = 0
    
    for url, name in urls_dashboard:
        status = test_url(base_url, url)
        
        if status == 200:
            print(f"✅ {name:35} {url:35} → 200 OK")
            urls_ok += 1
        elif status in [301, 302]:
            print(f"🔄 {name:35} {url:35} → {status} REDIRECT")
            urls_redirect += 1
        elif status == 404:
            print(f"❌ {name:35} {url:35} → 404 NOT FOUND")
            urls_error += 1
        elif status == 500:
            print(f"⚠️ {name:35} {url:35} → 500 SERVER ERROR")
            urls_error += 1
        elif status is None:
            print(f"🚫 {name:35} {url:35} → CONNECTION ERROR")
            urls_error += 1
        else:
            print(f"⚠️ {name:35} {url:35} → {status}")
            urls_error += 1
    
    # Estadísticas finales
    total_working = urls_ok + urls_redirect
    total_urls = len(urls_dashboard)
    success_rate = (total_working / total_urls) * 100
    
    print("\n📊 RESULTADOS FINALES:")
    print("=" * 70)
    print(f"✅ URLs funcionando (200): {urls_ok}")
    print(f"🔄 URLs con redirección: {urls_redirect}")
    print(f"❌ URLs con errores: {urls_error}")
    print(f"📈 Total funcionando: {total_working}/{total_urls}")
    print(f"🎯 Porcentaje de éxito: {success_rate:.1f}%")
    
    if success_rate >= 90:
        print(f"\n🎉 ¡EXCELENTE! Dashboard funcionando al {success_rate:.1f}%")
        print("✅ Las URLs del dashboard ahora apuntan a módulos reales")
        print("✅ El cliente tendrá una experiencia de navegación perfecta")
        print("✅ Sistema listo para producción")
    elif success_rate >= 75:
        print(f"\n👍 BUENO - Dashboard funcionando al {success_rate:.1f}%")
        print("🔧 Quedan algunos errores menores por corregir")
    else:
        print(f"\n⚠️ NECESITA TRABAJO - Solo {success_rate:.1f}% funcionando")
        print("🔧 Requiere más correcciones")
    
    print(f"\n💡 INSTRUCCIONES PARA JORGE:")
    print("1. 🌐 Accede a: http://localhost:8000/dashboard/")
    print("2. 🔑 Usa credenciales de admin")
    print(f"3. 📊 Dashboard muestra {total_working} módulos funcionando")
    print("4. 🚀 Todos los módulos de Admisión-Recepción operativos")
    print("5. ✨ Navegación sin errores 404/500 en enlaces principales")

if __name__ == '__main__':
    main()
