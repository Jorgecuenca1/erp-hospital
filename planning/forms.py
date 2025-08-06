from django import forms
from .models import ResourceType, ResourceAllocation, StaffSchedule, CapacityPlanning


class ResourceTypeForm(forms.ModelForm):
    """Form for resource type creation and editing"""
    class Meta:
        model = ResourceType
        fields = ['name', 'category', 'description', 'unit', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Resource Name'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Unit (e.g., hours, pieces)'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }


class ResourceAllocationForm(forms.ModelForm):
    """Form for resource allocation creation and editing"""
    class Meta:
        model = ResourceAllocation
        fields = ['resource_type', 'department', 'planned_quantity', 'allocated_quantity',
                 'start_date', 'end_date', 'responsible_person', 'priority', 'status', 'notes']
        widgets = {
            'resource_type': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department'}),
            'planned_quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'allocated_quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'responsible_person': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }


class StaffScheduleForm(forms.ModelForm):
    """Form for staff schedule creation and editing"""
    class Meta:
        model = StaffSchedule
        fields = ['staff_member', 'department', 'shift_type', 'start_datetime',
                 'end_datetime', 'role', 'status']
        widgets = {
            'staff_member': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department'}),
            'shift_type': forms.Select(attrs={'class': 'form-control'}),
            'start_datetime': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_datetime': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'role': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Role/Position'}),
            'status': forms.Select(attrs={'class': 'form-control'})
        }


class CapacityPlanningForm(forms.ModelForm):
    """Form for capacity planning creation and editing"""
    class Meta:
        model = CapacityPlanning
        fields = ['department', 'planning_period', 'resource_type', 'current_capacity',
                 'planned_capacity', 'utilization_rate', 'forecasted_demand',
                 'gap_analysis', 'action_plan', 'created_by']
        widgets = {
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department'}),
            'planning_period': forms.Select(attrs={'class': 'form-control'}),
            'resource_type': forms.Select(attrs={'class': 'form-control'}),
            'current_capacity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'planned_capacity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'utilization_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'max': '100', 'min': '0'}),
            'forecasted_demand': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'gap_analysis': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'action_plan': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'created_by': forms.Select(attrs={'class': 'form-control'})
        } 