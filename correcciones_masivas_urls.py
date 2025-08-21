#!/usr/bin/env python3
"""
Script para corregir masivamente URLs problemáticas encontradas en la auditoría
"""

import os
import re

def corregir_urls_en_archivo(filepath):
    """Corregir URLs problemáticas en un archivo específico"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Correcciones más comunes
        correcciones = [
            # Sintaxis de comparación en templates
            (r"request\.GET\.(\w+)==['\"](\w+)['\"]", r'request.GET.\1 == "\2"'),
            
            # URLs de appointments
            (r"{% url 'cita_", r"{% url 'appointments:cita_"),
            
            # URLs de patients
            (r"{% url 'paciente_", r"{% url 'patients:paciente_"),
            
            # URLs de professionals
            (r"{% url 'profesional_", r"{% url 'professionals:profesional_"),
            
            # URLs de admision_recepcion
            (r"{% url 'orden_", r"{% url 'admision_recepcion:orden_"),
            
            # Comillas simples a dobles en comparaciones
            (r"{% if ([^}]+)==[']([^']+)['] %}", r'{% if \1 == "\2" %}'),
        ]
        
        content_modificado = content
        cambios = 0
        
        for patron, reemplazo in correcciones:
            matches = re.findall(patron, content_modificado)
            if matches:
                content_modificado = re.sub(patron, reemplazo, content_modificado)
                cambios += len(matches)
        
        if cambios > 0:
            with open(filepath, 'w') as f:
                f.write(content_modificado)
            return cambios
        
        return 0
        
    except Exception as e:
        print(f"Error procesando {filepath}: {e}")
        return 0

def main():
    print("🔧 CORRECCIONES MASIVAS DE URLs")
    print("=" * 50)
    
    archivos_procesados = 0
    total_cambios = 0
    
    # Buscar todos los templates
    for root, dirs, files in os.walk('/home/jorge/erp-hospital'):
        if 'venv' in root or '__pycache__' in root:
            continue
        
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                cambios = corregir_urls_en_archivo(filepath)
                if cambios > 0:
                    print(f"✅ {file}: {cambios} correcciones")
                    archivos_procesados += 1
                    total_cambios += cambios
    
    print(f"\n📊 RESUMEN:")
    print(f"Archivos corregidos: {archivos_procesados}")
    print(f"Total correcciones: {total_cambios}")

if __name__ == '__main__':
    main()
