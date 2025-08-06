from django import forms
from django.forms import ModelForm
from .models import (
    Cliente, ProductoServicio, OrdenVenta, DetalleOrdenVenta,
    FacturaVenta, DetalleFacturaVenta, PagoVenta, DevolucionVenta
)

class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_cliente': forms.Select(attrs={'class': 'form-control'}),
            'identificacion': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contacto_principal': forms.TextInput(attrs={'class': 'form-control'}),
            'limite_credito': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'saldo_actual': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ProductoServicioForm(ModelForm):
    class Meta:
        model = ProductoServicio
        fields = '__all__'
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'precio_especial': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'impuesto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'requiere_autorizacion': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'stock_disponible': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock_minimo': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class OrdenVentaForm(ModelForm):
    class Meta:
        model = OrdenVenta
        fields = ['cliente', 'fecha_entrega_esperada', 'estado', 'descuento', 'notas']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'fecha_entrega_esperada': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'descuento': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class DetalleOrdenVentaForm(ModelForm):
    class Meta:
        model = DetalleOrdenVenta
        fields = ['producto_servicio', 'cantidad', 'precio_unitario', 'descuento', 'notas']
        widgets = {
            'producto_servicio': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'descuento': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class FacturaVentaForm(ModelForm):
    class Meta:
        model = FacturaVenta
        fields = ['cliente', 'orden_venta', 'fecha_vencimiento', 'estado', 'descuento', 'notas']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'orden_venta': forms.Select(attrs={'class': 'form-control'}),
            'fecha_vencimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'descuento': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class DetalleFacturaVentaForm(ModelForm):
    class Meta:
        model = DetalleFacturaVenta
        fields = ['producto_servicio', 'cantidad', 'precio_unitario', 'descuento']
        widgets = {
            'producto_servicio': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'descuento': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
        }

class PagoVentaForm(ModelForm):
    class Meta:
        model = PagoVenta
        fields = ['factura', 'fecha_pago', 'monto', 'metodo_pago', 'referencia', 'notas']
        widgets = {
            'factura': forms.Select(attrs={'class': 'form-control'}),
            'fecha_pago': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'metodo_pago': forms.Select(attrs={'class': 'form-control'}),
            'referencia': forms.TextInput(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class DevolucionVentaForm(ModelForm):
    class Meta:
        model = DevolucionVenta
        fields = ['factura', 'fecha_procesamiento', 'estado', 'motivo', 'monto_total', 'notas']
        widgets = {
            'factura': forms.Select(attrs={'class': 'form-control'}),
            'fecha_procesamiento': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'monto_total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# Formularios de búsqueda y filtros
class SalesSearchForm(forms.Form):
    '''Formulario de búsqueda para Sales'''
    
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
            ('BORRADOR', 'Borrador'),
            ('EMITIDA', 'Emitida'),
            ('PAGADA', 'Pagada'),
            ('ANULADA', 'Anulada'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Estado',
        required=False
    )

class SalesFilterForm(forms.Form):
    '''Formulario de filtros para Sales'''
    
    ordenar_por = forms.ChoiceField(
        choices=[
            ('fecha', 'Fecha'),
            ('cliente', 'Cliente'),
            ('total', 'Total'),
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