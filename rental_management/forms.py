from django import forms
from .models import RentalEquipment, RentalAgreement, RentalPayment, RentalInspection


class RentalEquipmentForm(forms.ModelForm):
    """Form for rental equipment creation and editing"""
    class Meta:
        model = RentalEquipment
        fields = ['name', 'category', 'model', 'manufacturer', 'serial_number',
                 'description', 'daily_rate', 'weekly_rate', 'monthly_rate',
                 'security_deposit', 'availability_status', 'location']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Equipment Name'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Model'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Manufacturer'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Serial Number'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'daily_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'weekly_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'monthly_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'security_deposit': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'availability_status': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'})
        }


class RentalAgreementForm(forms.ModelForm):
    """Form for rental agreement creation and editing"""
    class Meta:
        model = RentalAgreement
        fields = ['agreement_number', 'equipment', 'renter_name', 'renter_contact',
                 'renter_address', 'start_date', 'end_date', 'rental_period',
                 'rental_rate', 'total_amount', 'security_deposit', 'status', 'created_by']
        widgets = {
            'agreement_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Agreement Number'}),
            'equipment': forms.Select(attrs={'class': 'form-control'}),
            'renter_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Renter Name'}),
            'renter_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Information'}),
            'renter_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'rental_period': forms.Select(attrs={'class': 'form-control'}),
            'rental_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'total_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'security_deposit': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'created_by': forms.Select(attrs={'class': 'form-control'})
        }


class RentalPaymentForm(forms.ModelForm):
    """Form for rental payment creation and editing"""
    class Meta:
        model = RentalPayment
        fields = ['agreement', 'payment_date', 'amount', 'payment_method',
                 'transaction_id', 'payment_type']
        widgets = {
            'agreement': forms.Select(attrs={'class': 'form-control'}),
            'payment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'transaction_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Transaction ID'}),
            'payment_type': forms.Select(attrs={'class': 'form-control'})
        }


class RentalInspectionForm(forms.ModelForm):
    """Form for rental inspection creation and editing"""
    class Meta:
        model = RentalInspection
        fields = ['agreement', 'inspection_type', 'inspection_date', 'inspector',
                 'condition', 'notes', 'damage_cost']
        widgets = {
            'agreement': forms.Select(attrs={'class': 'form-control'}),
            'inspection_type': forms.Select(attrs={'class': 'form-control'}),
            'inspection_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'inspector': forms.Select(attrs={'class': 'form-control'}),
            'condition': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'damage_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
        } 