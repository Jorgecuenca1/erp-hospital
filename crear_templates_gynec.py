#!/usr/bin/env python3
"""
Script para crear templates específicos para el módulo de ginecología
"""

templates = {
    'procedure_create.html': {
        'title': 'Nuevo Procedimiento Ginecológico',
        'icon': 'fas fa-procedures',
        'color': 'text-success',
        'list_url': 'gynec:procedure_list',
        'description': 'Registro de procedimientos ginecológicos realizados'
    },
    'antenatal_create.html': {
        'title': 'Nueva Visita Prenatal',
        'icon': 'fas fa-calendar-check',
        'color': 'text-info',
        'list_url': 'gynec:antenatal_list',
        'description': 'Registro de visitas de control prenatal'
    },
    'contraceptive_create.html': {
        'title': 'Nueva Consulta de Anticoncepción',
        'icon': 'fas fa-pills',
        'color': 'text-warning',
        'list_url': 'gynec:contraceptive_list',
        'description': 'Registro de consultas sobre métodos anticonceptivos'
    },
    'menopause_create.html': {
        'title': 'Nueva Evaluación de Menopausia',
        'icon': 'fas fa-thermometer-half',
        'color': 'text-danger',
        'list_url': 'gynec:menopause_list',
        'description': 'Evaluación y manejo de la menopausia'
    },
    'medical_record_create.html': {
        'title': 'Nuevo Registro Médico Ginecológico',
        'icon': 'fas fa-file-medical',
        'color': 'text-primary',
        'list_url': 'gynec:medical_record_list',
        'description': 'Registro médico especializado en ginecología'
    }
}

base_template = """{% extends 'base.html' %}
{% load static %}

{% block title %}Ginecología - {title}{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="row">
        <div class="col-12">
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">
                        <i class="{icon} {color}"></i>
                        {title}
                    </h3>
                    <div class="card-tools">
                        <a href="{% url '{list_url}' %}" class="btn btn-secondary btn-sm">
                            <i class="fas fa-arrow-left"></i> Volver a Lista
                        </a>
                    </div>
                </div>
                <div class="card-body">
                    <div class="alert alert-info">
                        <i class="fas fa-info-circle"></i>
                        {description}
                    </div>
                    
                    <form method="post" class="row">
                        {% csrf_token %}
                        
                        <div class="col-12">
                            <h5 class="{color}">
                                <i class="fas fa-edit"></i> Información del Formulario
                            </h5>
                            
                            <!-- Renderizado automático de todos los campos del formulario -->
                            {% for field in form %}
                                <div class="form-group">
                                    <label for="{{ field.id_for_label }}">{{ field.label }}</label>
                                    {{ field }}
                                    {% if field.errors %}
                                        <div class="text-danger">{{ field.errors.0 }}</div>
                                    {% endif %}
                                    {% if field.help_text %}
                                        <small class="form-text text-muted">{{ field.help_text }}</small>
                                    {% endif %}
                                </div>
                            {% endfor %}
                        </div>
                        
                        <div class="col-12 text-center mt-4">
                            <button type="submit" class="btn btn-success btn-lg">
                                <i class="fas fa-save"></i> Guardar Registro
                            </button>
                            <a href="{% url '{list_url}' %}" class="btn btn-secondary btn-lg">
                                <i class="fas fa-times"></i> Cancelar
                            </a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

""" + """{% block extra_js %}
<script>
$(document).ready(function() {
    // Agregar clases de Bootstrap a los campos del formulario
    $('input, select, textarea').addClass('form-control');
    $('input[type="checkbox"], input[type="radio"]').removeClass('form-control').addClass('form-check-input');
    
    // Validación de formularios
    $('form').on('submit', function(e) {
        var requiredFields = $(this).find('[required]');
        var isValid = true;
        
        requiredFields.each(function() {
            if (!$(this).val()) {
                $(this).addClass('is-invalid');
                isValid = false;
            } else {
                $(this).removeClass('is-invalid');
            }
        });
        
        if (!isValid) {
            e.preventDefault();
            alert('Por favor complete todos los campos requeridos.');
        }
    });
    
    // Mejorar la apariencia de campos de fecha
    $('input[type="date"], input[type="datetime-local"]').addClass('form-control');
    
    // Mejorar la apariencia de textareas
    $('textarea').attr('rows', 3);
});
</script>
{% endblock %}""""""

import os

# Crear directorio si no existe
template_dir = "/home/jorge/erp-hospital/acs_hms_gynec/templates/acs_hms_gynec"
os.makedirs(template_dir, exist_ok=True)

# Crear cada template
for filename, config in templates.items():
    template_content = base_template.format(
        title=config['title'],
        icon=config['icon'],
        color=config['color'],
        list_url=config['list_url'],
        description=config['description']
    )
    
    filepath = os.path.join(template_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(template_content)
    
    print(f"✅ Creado: {filename}")

print(f"\n🎉 ¡Todos los templates han sido creados exitosamente!")
print(f"📁 Ubicación: {template_dir}")
print(f"\n📋 Templates creados:")
for filename in templates.keys():
    print(f"   - {filename}")
