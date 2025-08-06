from django import forms
from .models import MedicalDevice, ProductionOrder, QualityCheck, BillOfMaterials


class MedicalDeviceForm(forms.ModelForm):
    """Form for medical device creation and editing"""
    class Meta:
        model = MedicalDevice
        fields = ['name', 'device_type', 'model_number', 'manufacturer', 'serial_number', 
                 'manufacturing_date', 'expiry_date', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Device Name'}),
            'device_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Device Type'}),
            'model_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Model Number'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Manufacturer'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Serial Number'}),
            'manufacturing_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'})
        }


class ProductionOrderForm(forms.ModelForm):
    """Form for production order creation and editing"""
    class Meta:
        model = ProductionOrder
        fields = ['order_number', 'device', 'quantity', 'priority', 'status', 
                 'assigned_to', 'start_date', 'end_date']
        widgets = {
            'order_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Order Number'}),
            'device': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'})
        }


class QualityCheckForm(forms.ModelForm):
    """Form for quality check creation and editing"""
    class Meta:
        model = QualityCheck
        fields = ['production_order', 'check_type', 'result', 'inspector', 'notes']
        widgets = {
            'production_order': forms.Select(attrs={'class': 'form-control'}),
            'check_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Check Type'}),
            'result': forms.Select(attrs={'class': 'form-control'}),
            'inspector': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Quality check notes'})
        }


class BillOfMaterialsForm(forms.ModelForm):
    """Form for bill of materials creation and editing"""
    class Meta:
        model = BillOfMaterials
        fields = ['device', 'component_name', 'quantity_required', 'unit_cost', 
                 'supplier', 'is_critical']
        widgets = {
            'device': forms.Select(attrs={'class': 'form-control'}),
            'component_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Component Name'}),
            'quantity_required': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'unit_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'supplier': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Supplier'}),
            'is_critical': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        } 