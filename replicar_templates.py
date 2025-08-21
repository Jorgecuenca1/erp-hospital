#!/usr/bin/env python3

import os
import shutil

# Leer el template base
with open('/home/jorge/erp-hospital/ophthalmology/templates/ophthalmology/dashboard.html', 'r') as f:
    template_base = f.read()

# Configuraciones para cada módulo
modulos = [
    {'nombre': 'paediatric', 'titulo': 'Pediatría', 'icono': 'fas fa-baby', 'color': 'info', 'descripcion': 'pacientes pediátricos'},
    {'nombre': 'aesthetic', 'titulo': 'Estética', 'icono': 'fas fa-spa', 'color': 'success', 'descripcion': 'tratamientos estéticos'},
    {'nombre': 'dental', 'titulo': 'Dental', 'icono': 'fas fa-tooth', 'color': 'primary', 'descripcion': 'pacientes dentales'},
    {'nombre': 'surgery', 'titulo': 'Cirugía', 'icono': 'fas fa-user-md', 'color': 'danger', 'descripcion': 'procedimientos quirúrgicos'},
    {'nombre': 'operation_theater', 'titulo': 'Quirófano', 'icono': 'fas fa-procedures', 'color': 'warning', 'descripcion': 'salas de operaciones'},
    {'nombre': 'laboratory', 'titulo': 'Laboratorio', 'icono': 'fas fa-flask', 'color': 'secondary', 'descripcion': 'pruebas de laboratorio'},
    {'nombre': 'radiology', 'titulo': 'Radiología', 'icono': 'fas fa-x-ray', 'color': 'dark', 'descripcion': 'estudios radiológicos'},
]

for modulo in modulos:
    # Adaptar template para cada módulo
    contenido = template_base.replace('Oftalmología', modulo['titulo'])
    contenido = contenido.replace('oftalmología', modulo['titulo'].lower())
    contenido = contenido.replace('fas fa-eye', modulo['icono'])
    contenido = contenido.replace('bg-primary', f"bg-{modulo['color']}")
    contenido = contenido.replace('text-primary', f"text-{modulo['color']}")
    contenido = contenido.replace('btn-primary', f"btn-{modulo['color']}")
    contenido = contenido.replace('btn-outline-primary', f"btn-outline-{modulo['color']}")
    contenido = contenido.replace('pacientes oftalmológicos', modulo['descripcion'])
    
    # Escribir archivo
    filepath = f"/home/jorge/erp-hospital/{modulo['nombre']}/templates/{modulo['nombre']}/dashboard.html"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(contenido)
    
    print(f"✅ Creado: {modulo['nombre']}/dashboard.html")

print("\n🎉 Todos los templates han sido creados exitosamente!")



