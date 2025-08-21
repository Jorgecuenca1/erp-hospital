#!/usr/bin/env python3
"""
Auditoría completa de TODO el sistema HMetaHIS
Revisa URLs, templates, vistas y errores comunes
"""

import os
import re
import requests
from pathlib import Path

def find_all_urls():
    """Encontrar todas las URLs definidas en el sistema"""
    urls_encontradas = []
    
    # Buscar todos los archivos urls.py
    for root, dirs, files in os.walk('/home/jorge/erp-hospital'):
        if 'venv' in root or '__pycache__' in root:
            continue
        for file in files:
            if file == 'urls.py':
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r') as f:
                        content = f.read()
                        # Buscar patrones de path()
                        patterns = re.findall(r"path\(['\"]([^'\"]*)['\"]", content)
                        app_name = re.search(r"app_name\s*=\s*['\"]([^'\"]*)['\"]", content)
                        app_name = app_name.group(1) if app_name else os.path.basename(os.path.dirname(filepath))
                        
                        for pattern in patterns:
                            if pattern and not pattern.startswith('<'):
                                urls_encontradas.append({
                                    'app': app_name,
                                    'pattern': pattern,
                                    'file': filepath,
                                    'full_url': f"/{pattern}" if not pattern.startswith('/') else pattern
                                })
                except:
                    continue
    
    return urls_encontradas

def find_all_templates():
    """Encontrar todos los templates en el sistema"""
    templates_encontrados = []
    
    for root, dirs, files in os.walk('/home/jorge/erp-hospital'):
        if 'venv' in root or '__pycache__' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                templates_encontrados.append({
                    'file': file,
                    'path': filepath,
                    'app': os.path.basename(os.path.dirname(os.path.dirname(filepath)))
                })
    
    return templates_encontrados

def check_template_errors(template_path):
    """Verificar errores comunes en templates"""
    errores = []
    try:
        with open(template_path, 'r') as f:
            content = f.read()
            lines = content.split('\n')
            
            for i, line in enumerate(lines, 1):
                # Buscar bloques for sin endfor
                if '{% for ' in line and '{% endfor %}' not in content:
                    errores.append(f"Línea {i}: Posible for sin endfor")
                
                # Buscar bloques if sin endif
                if '{% if ' in line and line.count('{% if') > content.count('{% endif %}'):
                    errores.append(f"Línea {i}: Posible if sin endif")
                
                # Buscar comparaciones problemáticas
                if "request.GET." in line and "==" in line:
                    errores.append(f"Línea {i}: Sintaxis problemática en comparación")
                
                # Buscar URLs problemáticas
                url_patterns = re.findall(r"{% url ['\"]([^'\"]*)['\"]", line)
                for url in url_patterns:
                    if not url or url.startswith('admin:'):
                        continue
                    errores.append(f"Línea {i}: Verificar URL '{url}'")
    
    except Exception as e:
        errores.append(f"Error leyendo archivo: {e}")
    
    return errores

def test_url_response(url):
    """Probar respuesta de una URL"""
    try:
        response = requests.get(f"http://localhost:8000{url}", timeout=5, allow_redirects=False)
        return response.status_code
    except:
        return None

def main():
    print("🔍 AUDITORÍA COMPLETA DEL SISTEMA HMetaHIS")
    print("=" * 80)
    
    # 1. Encontrar todas las URLs
    print("\n📍 1. ANALIZANDO URLs DEL SISTEMA...")
    urls = find_all_urls()
    print(f"   Encontradas {len(urls)} URLs en {len(set(u['app'] for u in urls))} aplicaciones")
    
    # 2. Encontrar todos los templates
    print("\n📄 2. ANALIZANDO TEMPLATES DEL SISTEMA...")
    templates = find_all_templates()
    print(f"   Encontrados {len(templates)} templates")
    
    # 3. Verificar errores en templates
    print("\n🐛 3. VERIFICANDO ERRORES EN TEMPLATES...")
    templates_con_errores = 0
    total_errores = 0
    
    for template in templates:
        errores = check_template_errors(template['path'])
        if errores:
            templates_con_errores += 1
            total_errores += len(errores)
            print(f"   ❌ {template['file']}: {len(errores)} errores")
            for error in errores[:3]:  # Solo mostrar primeros 3
                print(f"      • {error}")
            if len(errores) > 3:
                print(f"      • ... y {len(errores) - 3} errores más")
    
    # 4. Probar URLs principales
    print("\n🌐 4. PROBANDO URLs PRINCIPALES...")
    urls_principales = [
        '/dashboard/',
        '/patients/',
        '/appointments/',
        '/medical_records/',
        '/hr/',
        '/admision/',
        '/admision/ordenes/',
        '/admision/seguimiento/',
    ]
    
    urls_funcionando = 0
    for url in urls_principales:
        status = test_url_response(url)
        if status in [200, 302]:
            print(f"   ✅ {url}: {status}")
            urls_funcionando += 1
        else:
            print(f"   ❌ {url}: {status or 'ERROR'}")
    
    # 5. Resumen final
    print("\n📊 RESUMEN DE LA AUDITORÍA:")
    print("=" * 80)
    print(f"📍 URLs encontradas: {len(urls)}")
    print(f"📄 Templates encontrados: {len(templates)}")
    print(f"🐛 Templates con errores: {templates_con_errores}")
    print(f"⚠️  Total errores detectados: {total_errores}")
    print(f"🌐 URLs principales funcionando: {urls_funcionando}/{len(urls_principales)}")
    
    # 6. Prioridades de corrección
    print(f"\n🎯 PRIORIDADES DE CORRECCIÓN:")
    print("1. Corregir errores de sintaxis en templates")
    print("2. Verificar URLs faltantes en views.py")
    print("3. Crear templates faltantes")
    print("4. Corregir FieldErrors en formularios")
    print("5. Probar navegación completa")

if __name__ == '__main__':
    main()
