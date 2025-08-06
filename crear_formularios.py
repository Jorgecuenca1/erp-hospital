#!/usr/bin/env python
"""
Script para crear formularios básicos para todos los módulos
"""
import os

# Configuración de módulos HMS
HMS_MODULES = [
    'acs_hms_gynec', 'acs_hms_ophthalmology', 'acs_hms_paediatric', 'acs_hms_aesthetic',
    'acs_hms_dental', 'acs_hms_surgery', 'acs_hms_operation_theater', 'acs_hms_laboratory',
    'acs_hms_radiology', 'acs_hms_emergency', 'acs_hms_nursing', 'acs_hms_blood_bank',
    'acs_hms_hospitalization', 'acs_hms_patient_portal', 'acs_hms_pharmacy',
    'acs_hms_online_appointment', 'acs_hms_webcam', 'acs_hms_video_call',
    'acs_hms_consent_form', 'acs_hms_subscription', 'acs_hms_insurance',
    'acs_hms_commission', 'acs_hms_certification', 'acs_hms_waiting_screen'
]

# Configuración de módulos ERP
ERP_MODULES = [
    'professionals', 'appointments', 'medical_records', 'hospital_profile',
    'billing', 'sales', 'purchases', 'inventories', 'pharmacy', 'laboratories',
    'asset_management', 'hr', 'quality_management', 'reports', 'pos',
    'ecommerce', 'crm', 'subscriptions', 'website', 'blog', 'forum',
    'elearning', 'livechat'
]

def create_forms_content(module_name, module_type):
    """Genera el contenido de los formularios para un módulo"""
    
    if module_type == 'hms':
        title = module_name.replace('acs_hms_', '').replace('_', ' ').title()
    else:
        title = module_name.replace('_', ' ').title()
    
    return f"""from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User

class {title.replace(' ', '')}Form(forms.Form):
    '''Formulario básico para {title}'''
    
    nombre = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={{
            'class': 'form-control',
            'placeholder': 'Ingrese el nombre'
        }}),
        label='Nombre'
    )
    
    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={{
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Ingrese una descripción'
        }}),
        label='Descripción',
        required=False
    )
    
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={{
            'class': 'form-control',
            'type': 'date'
        }}),
        label='Fecha'
    )
    
    estado = forms.ChoiceField(
        choices=[
            ('ACTIVO', 'Activo'),
            ('INACTIVO', 'Inactivo'),
            ('PENDIENTE', 'Pendiente'),
        ],
        widget=forms.Select(attrs={{
            'class': 'form-control'
        }}),
        label='Estado'
    )
    
    observaciones = forms.CharField(
        widget=forms.Textarea(attrs={{
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Ingrese observaciones adicionales'
        }}),
        label='Observaciones',
        required=False
    )

class {title.replace(' ', '')}SearchForm(forms.Form):
    '''Formulario de búsqueda para {title}'''
    
    q = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={{
            'class': 'form-control',
            'placeholder': 'Buscar...'
        }}),
        label='Búsqueda',
        required=False
    )
    
    fecha_inicio = forms.DateField(
        widget=forms.DateInput(attrs={{
            'class': 'form-control',
            'type': 'date'
        }}),
        label='Fecha Inicio',
        required=False
    )
    
    fecha_fin = forms.DateField(
        widget=forms.DateInput(attrs={{
            'class': 'form-control',
            'type': 'date'
        }}),
        label='Fecha Fin',
        required=False
    )
    
    estado = forms.ChoiceField(
        choices=[
            ('', 'Todos los estados'),
            ('ACTIVO', 'Activo'),
            ('INACTIVO', 'Inactivo'),
            ('PENDIENTE', 'Pendiente'),
        ],
        widget=forms.Select(attrs={{
            'class': 'form-control'
        }}),
        label='Estado',
        required=False
    )

class {title.replace(' ', '')}FilterForm(forms.Form):
    '''Formulario de filtros para {title}'''
    
    ordenar_por = forms.ChoiceField(
        choices=[
            ('nombre', 'Nombre'),
            ('fecha', 'Fecha'),
            ('estado', 'Estado'),
        ],
        widget=forms.Select(attrs={{
            'class': 'form-control'
        }}),
        label='Ordenar por',
        required=False
    )
    
    orden = forms.ChoiceField(
        choices=[
            ('asc', 'Ascendente'),
            ('desc', 'Descendente'),
        ],
        widget=forms.Select(attrs={{
            'class': 'form-control'
        }}),
        label='Orden',
        required=False
    )
    
    por_pagina = forms.ChoiceField(
        choices=[
            ('10', '10 por página'),
            ('25', '25 por página'),
            ('50', '50 por página'),
            ('100', '100 por página'),
        ],
        widget=forms.Select(attrs={{
            'class': 'form-control'
        }}),
        label='Por página',
        required=False
    )
"""

def create_models_content(module_name, module_type):
    """Genera el contenido de los modelos básicos para un módulo"""
    
    if module_type == 'hms':
        title = module_name.replace('acs_hms_', '').replace('_', ' ').title()
    else:
        title = module_name.replace('_', ' ').title()
    
    return f"""from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class {title.replace(' ', '')}(models.Model):
    '''Modelo básico para {title}'''
    
    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
        ('PENDIENTE', 'Pendiente'),
    ]
    
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.DateField(default=timezone.now)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='ACTIVO')
    observaciones = models.TextField(blank=True, null=True)
    
    # Campos de auditoría
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '{title}'
        verbose_name_plural = '{title}s'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return self.nombre
    
    def get_absolute_url(self):
        return f'/{{self._meta.app_label}}/{{self.pk}}/'
"""

def create_admin_content(module_name, module_type):
    """Genera el contenido del admin para un módulo"""
    
    if module_type == 'hms':
        title = module_name.replace('acs_hms_', '').replace('_', ' ').title()
    else:
        title = module_name.replace('_', ' ').title()
    
    return f"""from django.contrib import admin
from django.utils.html import format_html
from .models import {title.replace(' ', '')}

@admin.register({title.replace(' ', '')})
class {title.replace(' ', '')}Admin(admin.ModelAdmin):
    list_display = ['nombre', 'fecha', 'estado', 'creado_por', 'fecha_creacion', 'estado_color']
    list_filter = ['estado', 'fecha', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    date_hierarchy = 'fecha_creacion'
    readonly_fields = ['fecha_creacion', 'fecha_modificacion']
    
    fieldsets = (
        ('Información Básica', {{
            'fields': ('nombre', 'descripcion', 'fecha', 'estado')
        }}),
        ('Detalles', {{
            'fields': ('observaciones',),
            'classes': ('collapse',)
        }}),
        ('Auditoría', {{
            'fields': ('creado_por', 'fecha_creacion', 'fecha_modificacion'),
            'classes': ('collapse',)
        }}),
    )
    
    def estado_color(self, obj):
        if obj.estado == 'ACTIVO':
            return format_html('<span style="color: green;">✅ {{}}</span>', obj.estado)
        elif obj.estado == 'INACTIVO':
            return format_html('<span style="color: red;">❌ {{}}</span>', obj.estado)
        else:
            return format_html('<span style="color: orange;">⏳ {{}}</span>', obj.estado)
    estado_color.short_description = 'Estado'
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es un nuevo objeto
            obj.creado_por = request.user
        super().save_model(request, obj, form, change)
"""

def create_file_if_not_exists(file_path, content):
    """Crea el archivo si no existe"""
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Archivo creado: {file_path}")
    else:
        print(f"⚠️  Archivo ya existe: {file_path}")

def create_module_files(module_name, module_type):
    """Crea los archivos necesarios para un módulo"""
    
    # Crear forms.py
    forms_content = create_forms_content(module_name, module_type)
    forms_path = f"{module_name}/forms.py"
    create_file_if_not_exists(forms_path, forms_content)
    
    # Crear models.py (solo si no existe)
    models_content = create_models_content(module_name, module_type)
    models_path = f"{module_name}/models.py"
    create_file_if_not_exists(models_path, models_content)
    
    # Crear admin.py (solo si no existe)
    admin_content = create_admin_content(module_name, module_type)
    admin_path = f"{module_name}/admin.py"
    create_file_if_not_exists(admin_path, admin_content)

def main():
    """Función principal"""
    print("🏥 Creando formularios y modelos para HMetaHIS...")
    print("=" * 50)
    
    # Crear archivos para módulos HMS
    print("\n📋 Creando archivos para módulos HMS...")
    for module in HMS_MODULES:
        create_module_files(module, 'hms')
    
    # Crear archivos para módulos ERP
    print("\n🏢 Creando archivos para módulos ERP...")
    for module in ERP_MODULES:
        create_module_files(module, 'erp')
    
    print("\n🎉 ¡Todos los archivos han sido creados exitosamente!")
    print(f"📊 Total de módulos procesados: {len(HMS_MODULES) + len(ERP_MODULES)}")
    print("\n🚀 Los módulos están listos para usar.")

if __name__ == '__main__':
    main() 