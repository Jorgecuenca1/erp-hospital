#!/usr/bin/env python3

import os

# Crear directorio si no existe
template_dir = "/home/jorge/erp-hospital/acs_hms_gynec/templates/acs_hms_gynec"
os.makedirs(template_dir, exist_ok=True)

# Template base
def crear_template(nombre_archivo, titulo, icono, color, list_url, descripcion):
    contenido = f'''{% extends 'base.html' %}
{% load static %}

{% block title %}Ginecología - {titulo}{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="row">
        <div class="col-12">
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">
                        <i class="{icono} {color}"></i>
                        {titulo}
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
                        {descripcion}
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
                                    <label for="{{{{ field.id_for_label }}}}">{{{{ field.label }}}}</label>
                                    {{{{ field }}}}
                                    {% if field.errors %}
                                        <div class="text-danger">{{{{ field.errors.0 }}}}</div>
                                    {% endif %}
                                    {% if field.help_text %}
                                        <small class="form-text text-muted">{{{{ field.help_text }}}}</small>
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

{% block extra_js %}
<script>
$(document).ready(function() {{
    // Agregar clases de Bootstrap a los campos del formulario
    $('input, select, textarea').addClass('form-control');
    $('input[type="checkbox"], input[type="radio"]').removeClass('form-control').addClass('form-check-input');
    
    // Validación de formularios
    $('form').on('submit', function(e) {{
        var requiredFields = $(this).find('[required]');
        var isValid = true;
        
        requiredFields.each(function() {{
            if (!$(this).val()) {{
                $(this).addClass('is-invalid');
                isValid = false;
            }} else {{
                $(this).removeClass('is-invalid');
            }}
        }});
        
        if (!isValid) {{
            e.preventDefault();
            alert('Por favor complete todos los campos requeridos.');
        }}
    }});
}});
</script>
{% endblock %}'''
    
    filepath = os.path.join(template_dir, nombre_archivo)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(contenido)
    print(f"✅ Creado: {nombre_archivo}")

# Crear templates
crear_template('procedure_create.html', 'Nuevo Procedimiento Ginecológico', 'fas fa-procedures', 'text-success', 'gynec:procedure_list', 'Registro de procedimientos ginecológicos realizados')

crear_template('antenatal_create.html', 'Nueva Visita Prenatal', 'fas fa-calendar-check', 'text-info', 'gynec:antenatal_list', 'Registro de visitas de control prenatal')

crear_template('contraceptive_create.html', 'Nueva Consulta de Anticoncepción', 'fas fa-pills', 'text-warning', 'gynec:contraceptive_list', 'Registro de consultas sobre métodos anticonceptivos')

crear_template('menopause_create.html', 'Nueva Evaluación de Menopausia', 'fas fa-thermometer-half', 'text-danger', 'gynec:menopause_list', 'Evaluación y manejo de la menopausia')

crear_template('medical_record_create.html', 'Nuevo Registro Médico Ginecológico', 'fas fa-file-medical', 'text-primary', 'gynec:medical_record_list', 'Registro médico especializado en ginecología')

print("\n🎉 ¡Todos los templates han sido creados exitosamente!")



