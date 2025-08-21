#!/usr/bin/env python3
"""
Script para crear templates dashboard.html faltantes para módulos HMS
"""

import os

# Módulos que necesitan templates dashboard.html (basado en los errores del terminal)
modulos_faltantes = [
    {'nombre': 'ophthalmology', 'titulo': 'Oftalmología', 'icono': 'fas fa-eye', 'color': 'primary'},
    {'nombre': 'paediatric', 'titulo': 'Pediatría', 'icono': 'fas fa-baby', 'color': 'info'},
    {'nombre': 'aesthetic', 'titulo': 'Estética', 'icono': 'fas fa-spa', 'color': 'pink'},
    {'nombre': 'dental', 'titulo': 'Dental', 'icono': 'fas fa-tooth', 'color': 'success'},
    {'nombre': 'surgery', 'titulo': 'Cirugía', 'icono': 'fas fa-user-md', 'color': 'danger'},
    {'nombre': 'operation_theater', 'titulo': 'Quirófano', 'icono': 'fas fa-procedures', 'color': 'warning'},
    {'nombre': 'laboratory', 'titulo': 'Laboratorio', 'icono': 'fas fa-flask', 'color': 'secondary'},
    {'nombre': 'radiology', 'titulo': 'Radiología', 'icono': 'fas fa-x-ray', 'color': 'dark'},
]

def crear_dashboard_template(nombre_modulo, titulo, icono, color):
    """Crea template dashboard.html para un módulo específico"""
    
    template_content = f'''{% extends 'base.html' %}
{% load static %}

{% block title %}{titulo} - Dashboard{% endblock %}

{% block content %}
<div class="container-fluid">
    <!-- Header del Módulo -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="card bg-{color} text-white">
                <div class="card-body">
                    <div class="row align-items-center">
                        <div class="col">
                            <h1 class="card-title mb-1">
                                <i class="{icono} me-3"></i>
                                {titulo}
                            </h1>
                            <p class="card-text mb-0">Panel de control del módulo de {titulo.lower()}</p>
                        </div>
                        <div class="col-auto">
                            <div class="text-center">
                                <h4 class="mb-0">HMS</h4>
                                <small>Sistema Hospitalario</small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Estadísticas Rápidas -->
    <div class="row mb-4">
        <div class="col-xl-3 col-md-6">
            <div class="card">
                <div class="card-body">
                    <div class="d-flex">
                        <div class="flex-shrink-0">
                            <div class="avatar-sm rounded-circle bg-{color} bg-opacity-10">
                                <span class="avatar-title rounded-circle bg-{color} bg-opacity-20">
                                    <i class="{icono} text-{color}"></i>
                                </span>
                            </div>
                        </div>
                        <div class="flex-grow-1 ms-3">
                            <h5 class="fw-semibold">{{{{ total_records|default:"0" }}}}</h5>
                            <p class="text-muted mb-0">Total de Registros</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-xl-3 col-md-6">
            <div class="card">
                <div class="card-body">
                    <div class="d-flex">
                        <div class="flex-shrink-0">
                            <div class="avatar-sm rounded-circle bg-success bg-opacity-10">
                                <span class="avatar-title rounded-circle bg-success bg-opacity-20">
                                    <i class="fas fa-check text-success"></i>
                                </span>
                            </div>
                        </div>
                        <div class="flex-grow-1 ms-3">
                            <h5 class="fw-semibold">{{{{ today_records|default:"0" }}}}</h5>
                            <p class="text-muted mb-0">Hoy</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-xl-3 col-md-6">
            <div class="card">
                <div class="card-body">
                    <div class="d-flex">
                        <div class="flex-shrink-0">
                            <div class="avatar-sm rounded-circle bg-info bg-opacity-10">
                                <span class="avatar-title rounded-circle bg-info bg-opacity-20">
                                    <i class="fas fa-calendar text-info"></i>
                                </span>
                            </div>
                        </div>
                        <div class="flex-grow-1 ms-3">
                            <h5 class="fw-semibold">{{{{ month_records|default:"0" }}}}</h5>
                            <p class="text-muted mb-0">Este Mes</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-xl-3 col-md-6">
            <div class="card">
                <div class="card-body">
                    <div class="d-flex">
                        <div class="flex-shrink-0">
                            <div class="avatar-sm rounded-circle bg-warning bg-opacity-10">
                                <span class="avatar-title rounded-circle bg-warning bg-opacity-20">
                                    <i class="fas fa-clock text-warning"></i>
                                </span>
                            </div>
                        </div>
                        <div class="flex-grow-1 ms-3">
                            <h5 class="fw-semibold">{{{{ pending_records|default:"0" }}}}</h5>
                            <p class="text-muted mb-0">Pendientes</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Acciones Rápidas -->
    <div class="row mb-4">
        <div class="col-12">
            <div class="card">
                <div class="card-header">
                    <h5 class="card-title mb-0">
                        <i class="fas fa-bolt me-2"></i>
                        Acciones Rápidas
                    </h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-lg-3 col-md-6 mb-3">
                            <a href="#" class="btn btn-{color} w-100 d-flex align-items-center">
                                <i class="fas fa-plus me-2"></i>
                                Nuevo Registro
                            </a>
                        </div>
                        <div class="col-lg-3 col-md-6 mb-3">
                            <a href="#" class="btn btn-outline-{color} w-100 d-flex align-items-center">
                                <i class="fas fa-list me-2"></i>
                                Ver Todos
                            </a>
                        </div>
                        <div class="col-lg-3 col-md-6 mb-3">
                            <a href="#" class="btn btn-outline-info w-100 d-flex align-items-center">
                                <i class="fas fa-chart-bar me-2"></i>
                                Reportes
                            </a>
                        </div>
                        <div class="col-lg-3 col-md-6 mb-3">
                            <a href="#" class="btn btn-outline-secondary w-100 d-flex align-items-center">
                                <i class="fas fa-cog me-2"></i>
                                Configuración
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Contenido Principal -->
    <div class="row">
        <div class="col-lg-8">
            <div class="card">
                <div class="card-header">
                    <h5 class="card-title mb-0">
                        <i class="fas fa-clock me-2"></i>
                        Actividad Reciente
                    </h5>
                </div>
                <div class="card-body">
                    <div class="text-center py-4">
                        <i class="{icono} fa-3x text-muted mb-3"></i>
                        <h5 class="text-muted">Módulo {titulo}</h5>
                        <p class="text-muted">Este módulo está configurado y listo para usar.</p>
                        <div class="alert alert-info">
                            <i class="fas fa-info-circle me-2"></i>
                            <strong>Próximamente:</strong> Funcionalidades específicas del módulo de {titulo.lower()}.
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-lg-4">
            <div class="card">
                <div class="card-header">
                    <h5 class="card-title mb-0">
                        <i class="fas fa-info-circle me-2"></i>
                        Información del Módulo
                    </h5>
                </div>
                <div class="card-body">
                    <ul class="list-unstyled mb-0">
                        <li class="py-2 border-bottom">
                            <i class="{icono} text-{color} me-2"></i>
                            <strong>Módulo:</strong> {titulo}
                        </li>
                        <li class="py-2 border-bottom">
                            <i class="fas fa-hospital text-success me-2"></i>
                            <strong>Sistema:</strong> HMS
                        </li>
                        <li class="py-2 border-bottom">
                            <i class="fas fa-check-circle text-success me-2"></i>
                            <strong>Estado:</strong> Activo
                        </li>
                        <li class="py-2">
                            <i class="fas fa-calendar text-info me-2"></i>
                            <strong>Última actualización:</strong> Hoy
                        </li>
                    </ul>
                </div>
            </div>
            
            <div class="card mt-3">
                <div class="card-header">
                    <h5 class="card-title mb-0">
                        <i class="fas fa-link me-2"></i>
                        Enlaces Rápidos
                    </h5>
                </div>
                <div class="card-body">
                    <div class="d-grid gap-2">
                        <a href="/dashboard/" class="btn btn-outline-primary btn-sm">
                            <i class="fas fa-home me-2"></i>
                            Dashboard Principal
                        </a>
                        <a href="/hms/" class="btn btn-outline-info btn-sm">
                            <i class="fas fa-hospital me-2"></i>
                            Módulos HMS
                        </a>
                        <a href="/patients/" class="btn btn-outline-success btn-sm">
                            <i class="fas fa-users me-2"></i>
                            Pacientes
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
$(document).ready(function() {{
    console.log('Dashboard {titulo} cargado exitosamente');
    
    // Inicializar tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {{
        return new bootstrap.Tooltip(tooltipTriggerEl);
    }});
}});
</script>
{% endblock %}'''

    # Crear directorio si no existe
    template_dir = f"/home/jorge/erp-hospital/{nombre_modulo}/templates/{nombre_modulo}"
    os.makedirs(template_dir, exist_ok=True)
    
    # Escribir archivo
    filepath = os.path.join(template_dir, "dashboard.html")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(template_content)
    
    print(f"✅ Creado: {nombre_modulo}/templates/{nombre_modulo}/dashboard.html")

def main():
    print("🚀 CREANDO TEMPLATES DASHBOARD.HTML PARA MÓDULOS HMS")
    print("=" * 60)
    
    for modulo in modulos_faltantes:
        crear_dashboard_template(
            modulo['nombre'], 
            modulo['titulo'], 
            modulo['icono'], 
            modulo['color']
        )
    
    print("\n🎉 ¡Todos los templates dashboard.html han sido creados!")
    print(f"📊 Total de templates creados: {len(modulos_faltantes)}")
    print("\n📋 Templates creados:")
    for modulo in modulos_faltantes:
        print(f"   - {modulo['nombre']}/dashboard.html")
    
    print("\n🔧 Próximos pasos:")
    print("   1. Reiniciar el servidor Django")
    print("   2. Probar cada módulo HMS")
    print("   3. Verificar que no hay más errores TemplateDoesNotExist")

if __name__ == '__main__':
    main()



