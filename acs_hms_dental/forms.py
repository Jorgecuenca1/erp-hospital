from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User

class DentalForm(forms.Form):
    '''Formulario básico para Dental'''
    
    nombre = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el nombre'
        }),
        label='Nombre'
    )
    
    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Ingrese una descripción'
        }),
        label='Descripción',
        required=False
    )
    
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='Fecha'
    )
    
    estado = forms.ChoiceField(
        choices=[
            ('ACTIVO', 'Activo'),
            ('INACTIVO', 'Inactivo'),
            ('PENDIENTE', 'Pendiente'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Estado'
    )
    
    observaciones = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Ingrese observaciones adicionales'
        }),
        label='Observaciones',
        required=False
    )

class DentalSearchForm(forms.Form):
    '''Formulario de búsqueda para Dental'''
    
    q = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar...'
        }),
        label='Búsqueda',
        required=False
    )
    
    fecha_inicio = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='Fecha Inicio',
        required=False
    )
    
    fecha_fin = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
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
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Estado',
        required=False
    )

class DentalFilterForm(forms.Form):
    '''Formulario de filtros para Dental'''
    
    ordenar_por = forms.ChoiceField(
        choices=[
            ('nombre', 'Nombre'),
            ('fecha', 'Fecha'),
            ('estado', 'Estado'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Ordenar por',
        required=False
    )
    
    orden = forms.ChoiceField(
        choices=[
            ('asc', 'Ascendente'),
            ('desc', 'Descendente'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
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
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Por página',
        required=False
    )
