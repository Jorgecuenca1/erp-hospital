from django import forms
from .models import MedicalEquipment, MaintenanceSchedule, MaintenanceRecord, MaintenanceAlert


class MedicalEquipmentForm(forms.ModelForm):
    """Form for medical equipment creation and editing"""
    class Meta:
        model = MedicalEquipment
        fields = ['name', 'equipment_type', 'model_number', 'serial_number', 'manufacturer',
                 'purchase_date', 'warranty_expiry', 'location', 'department', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Equipment Name'}),
            'equipment_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Equipment Type'}),
            'model_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Model Number'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Serial Number'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Manufacturer'}),
            'purchase_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'warranty_expiry': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department'}),
            'status': forms.Select(attrs={'class': 'form-control'})
        }


class MaintenanceScheduleForm(forms.ModelForm):
    """Form for maintenance schedule creation and editing"""
    class Meta:
        model = MaintenanceSchedule
        fields = ['equipment', 'maintenance_type', 'frequency', 'next_maintenance',
                 'assigned_technician', 'estimated_duration', 'priority', 'status']
        widgets = {
            'equipment': forms.Select(attrs={'class': 'form-control'}),
            'maintenance_type': forms.Select(attrs={'class': 'form-control'}),
            'frequency': forms.Select(attrs={'class': 'form-control'}),
            'next_maintenance': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'assigned_technician': forms.Select(attrs={'class': 'form-control'}),
            'estimated_duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 2:30:00'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'})
        }


class MaintenanceRecordForm(forms.ModelForm):
    """Form for maintenance record creation and editing"""
    class Meta:
        model = MaintenanceRecord
        fields = ['equipment', 'maintenance_date', 'technician', 'maintenance_type',
                 'description', 'parts_used', 'cost', 'downtime_hours', 'issues_found',
                 'recommendations', 'next_maintenance_due']
        widgets = {
            'equipment': forms.Select(attrs={'class': 'form-control'}),
            'maintenance_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'technician': forms.Select(attrs={'class': 'form-control'}),
            'maintenance_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Maintenance Type'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'parts_used': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'downtime_hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'issues_found': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'recommendations': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'next_maintenance_due': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        }


class MaintenanceAlertForm(forms.ModelForm):
    """Form for maintenance alert creation and editing"""
    class Meta:
        model = MaintenanceAlert
        fields = ['equipment', 'alert_type', 'message', 'priority']
        widgets = {
            'equipment': forms.Select(attrs={'class': 'form-control'}),
            'alert_type': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'priority': forms.Select(attrs={'class': 'form-control'})
        } 