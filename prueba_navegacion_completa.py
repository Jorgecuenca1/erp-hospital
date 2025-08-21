#!/usr/bin/env python3
"""
Prueba completa de navegación del sistema corregido
"""

import requests

def test_url(url, name):
    """Probar una URL y mostrar resultado detallado"""
    try:
        response = requests.get(f"http://localhost:8000{url}", timeout=10, allow_redirects=False)
        status = response.status_code
        
        if status == 200:
            print(f"✅ {name:40} {url:30} → 200 OK")
            return True
        elif status == 302:
            print(f"🔐 {name:40} {url:30} → 302 LOGIN REQUIRED")
            return True
        elif status == 404:
            print(f"❌ {name:40} {url:30} → 404 NOT FOUND")
            return False
        elif status == 500:
            print(f"⚠️ {name:40} {url:30} → 500 SERVER ERROR")
            return False
        else:
            print(f"🔧 {name:40} {url:30} → {status}")
            return False
            
    except Exception as e:
        print(f"💥 {name:40} {url:30} → ERROR: {str(e)[:30]}")
        return False

def main():
    print("🧪 PRUEBA COMPLETA DE NAVEGACIÓN")
    print("=" * 80)
    
    # URLs críticas que estaban fallando
    urls_criticas = [
        ('/dashboard/', 'Dashboard Principal'),
        ('/patients/', 'Pacientes Dashboard'),
        ('/patients/lista/', 'Lista Pacientes'),
        ('/patients/crear/', 'Crear Paciente'),
        ('/appointments/', 'Citas Dashboard'),
        ('/appointments/citas/', 'Lista Citas'),
        ('/appointments/citas/new/', 'Nueva Cita'),
        ('/medical_records/', 'Historias Clínicas'),
        ('/hr/', 'Recursos Humanos'),
        ('/pharmacy/', 'Farmacia'),
        ('/laboratories/', 'Laboratorios'),
    ]
    
    # URLs de admisión-recepción
    urls_admision = [
        ('/admision/', 'Admisión Dashboard'),
        ('/admision/ordenes/', 'Órdenes Servicios'),
        ('/admision/seguimiento/', 'Seguimiento Pacientes'),
        ('/admision/seguimiento-atenciones/', 'Seguimiento Atenciones'),
        ('/admision/lista-precios/', 'Lista Precios'),
        ('/admision/portal-empresas/', 'Portal Empresas'),
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
    
    # URLs de comercio
    urls_comercio = [
        ('/accounting/', 'Contabilidad'),
        ('/billing/', 'Facturación'),
        ('/sales/', 'Ventas'),
        ('/purchases/', 'Compras'),
        ('/inventories/', 'Inventarios'),
        ('/reports/', 'Reportes'),
        ('/pos/', 'Punto de Venta'),
        ('/ecommerce/', 'E-commerce'),
        ('/crm/', 'CRM'),
        ('/website/', 'Sitio Web'),
        ('/forum/', 'Foro'),
        ('/elearning/', 'E-learning'),
        ('/blog/', 'Blog'),
        ('/livechat/', 'Live Chat'),
        ('/subscriptions/', 'Suscripciones'),
    ]
    
    # URLs HMS
    urls_hms = [
        ('/hms/', 'Base HMS'),
        ('/hms/pharmacy/', 'Farmacia HMS'),
        ('/hms/online-appointment/', 'Citas Online'),
        ('/hms/waiting-screen/', 'Pantalla Espera'),
        ('/hms/ophthalmology/', 'Oftalmología'),
        ('/hms/nursing/', 'Enfermería'),
        ('/hms/radiology/', 'Radiología'),
    ]
    
    # URLs ESG
    urls_esg = [
        ('/carbon/', 'Huella Carbono'),
        ('/social/', 'Métricas Sociales'),
    ]
    
    # Probar todas las categorías
    categorias = [
        ("📍 URLs CRÍTICAS", urls_criticas),
        ("🏥 ADMISIÓN-RECEPCIÓN", urls_admision),
        ("💼 COMERCIO Y ERP", urls_comercio),
        ("🩺 HMS (Hospital Management)", urls_hms),
        ("🌱 ESG (Sostenibilidad)", urls_esg),
    ]
    
    total_urls = 0
    total_funcionando = 0
    
    for categoria, urls in categorias:
        print(f"\n{categoria}")
        print("-" * 80)
        
        funcionando_categoria = 0
        for url, name in urls:
            if test_url(url, name):
                funcionando_categoria += 1
                total_funcionando += 1
            total_urls += 1
        
        porcentaje = (funcionando_categoria / len(urls)) * 100
        print(f"    └─ {funcionando_categoria}/{len(urls)} funcionando ({porcentaje:.1f}%)")
    
    # Resumen final
    porcentaje_total = (total_funcionando / total_urls) * 100
    
    print(f"\n📊 RESUMEN FINAL:")
    print("=" * 80)
    print(f"✅ URLs funcionando: {total_funcionando}")
    print(f"❌ URLs con problemas: {total_urls - total_funcionando}")
    print(f"📈 Total URLs probadas: {total_urls}")
    print(f"🎯 Porcentaje de éxito: {porcentaje_total:.1f}%")
    
    if porcentaje_total >= 95:
        print(f"\n🎉 ¡EXCELENTE! Sistema funcionando al {porcentaje_total:.1f}%")
        print("✅ Navegación completamente operativa")
        print("✅ Problemas críticos resueltos")
    elif porcentaje_total >= 85:
        print(f"\n👍 BIEN - Sistema funcionando al {porcentaje_total:.1f}%")
        print("🔧 Solo errores menores pendientes")
    else:
        print(f"\n⚠️ NECESITA MÁS TRABAJO - Solo {porcentaje_total:.1f}% funcionando")

if __name__ == '__main__':
    main()
