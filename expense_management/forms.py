from django import forms
from .models import ExpenseCategory, ExpenseReport, ExpenseItem, ExpensePolicy, ExpenseApproval


class ExpenseCategoryForm(forms.ModelForm):
    """Form for expense category creation and editing"""
    class Meta:
        model = ExpenseCategory
        fields = ['name', 'code', 'parent', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category Name'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category Code'}),
            'parent': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }


class ExpenseReportForm(forms.ModelForm):
    """Form for expense report creation and editing"""
    class Meta:
        model = ExpenseReport
        fields = ['employee', 'report_number', 'title', 'description', 'submit_date',
                 'currency', 'status']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'report_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Report Number'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Report Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'submit_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'currency': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Currency Code'}),
            'status': forms.Select(attrs={'class': 'form-control'})
        }


class ExpenseItemForm(forms.ModelForm):
    """Form for expense item creation and editing"""
    class Meta:
        model = ExpenseItem
        fields = ['report', 'category', 'description', 'expense_date', 'amount',
                 'currency', 'receipt_number', 'vendor', 'payment_method',
                 'is_billable', 'client_reference', 'mileage']
        widgets = {
            'report': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Expense Description'}),
            'expense_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'currency': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Currency'}),
            'receipt_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Receipt Number'}),
            'vendor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Vendor/Supplier'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'is_billable': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'client_reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Client Reference'}),
            'mileage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
        }


class ExpensePolicyForm(forms.ModelForm):
    """Form for expense policy creation and editing"""
    class Meta:
        model = ExpensePolicy
        fields = ['name', 'category', 'daily_limit', 'monthly_limit', 'requires_receipt',
                 'requires_approval', 'approval_threshold', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Policy Name'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'daily_limit': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'monthly_limit': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'requires_receipt': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'requires_approval': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'approval_threshold': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }


class ExpenseApprovalForm(forms.ModelForm):
    """Form for expense approval creation and editing"""
    class Meta:
        model = ExpenseApproval
        fields = ['report', 'approver', 'approval_level', 'status', 'approved_amount', 'comments']
        widgets = {
            'report': forms.Select(attrs={'class': 'form-control'}),
            'approver': forms.Select(attrs={'class': 'form-control'}),
            'approval_level': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'approved_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
        } 