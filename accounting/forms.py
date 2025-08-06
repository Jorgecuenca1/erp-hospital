from django import forms
from django.forms import inlineformset_factory
from .models import (
    PeriodoContable, CuentaContable, Tercero, Diario, Impuesto, 
    AsientoContable, LineaAsiento, DatosEmpresa, CentroCosto, 
    ComprobanteContable, CertificadoRetencion, MovimientoBancario, CierreContable, Presupuesto,
    ReporteFiscal, DetalleFiscal
)

class PeriodoContableForm(forms.ModelForm):
    class Meta:
        model = PeriodoContable
        fields = '__all__'
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
        }

class CuentaContableForm(forms.ModelForm):
    class Meta:
        model = CuentaContable
        fields = '__all__'
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'nivel': forms.NumberInput(attrs={'class': 'form-control'}),
            'padre': forms.Select(attrs={'class': 'form-control'}),
        }

class TerceroForm(forms.ModelForm):
    class Meta:
        model = Tercero
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'nit': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DiarioForm(forms.ModelForm):
    class Meta:
        model = Diario
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
        }

class ImpuestoForm(forms.ModelForm):
    class Meta:
        model = Impuesto
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'porcentaje': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
        }

class AsientoContableForm(forms.ModelForm):
    class Meta:
        model = AsientoContable
        fields = ['fecha', 'descripcion', 'diario', 'periodo', 'tercero', 'referencia']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'diario': forms.Select(attrs={'class': 'form-control'}),
            'periodo': forms.Select(attrs={'class': 'form-control'}),
            'tercero': forms.Select(attrs={'class': 'form-control'}),
            'referencia': forms.TextInput(attrs={'class': 'form-control'}),
        }

class LineaAsientoForm(forms.ModelForm):
    class Meta:
        model = LineaAsiento
        fields = ['cuenta', 'descripcion', 'debito', 'credito', 'impuesto', 'tercero']
        widgets = {
            'cuenta': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'debito': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'credito': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'impuesto': forms.Select(attrs={'class': 'form-control'}),
            'tercero': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        debito = cleaned_data.get('debito', 0)
        credito = cleaned_data.get('credito', 0)
        
        if debito > 0 and credito > 0:
            raise forms.ValidationError("Una línea no puede tener débito y crédito simultáneamente.")
        
        if debito == 0 and credito == 0:
            raise forms.ValidationError("Una línea debe tener débito o crédito.")
        
        return cleaned_data

# Formset para las líneas de asiento
LineaAsientoFormSet = inlineformset_factory(
    AsientoContable, 
    LineaAsiento, 
    form=LineaAsientoForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True
)

# Nuevos formularios
class DatosEmpresaForm(forms.ModelForm):
    class Meta:
        model = DatosEmpresa
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'nit': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'representante_legal': forms.TextInput(attrs={'class': 'form-control'}),
            'cargo_representante': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CentroCostoForm(forms.ModelForm):
    class Meta:
        model = CentroCosto
        fields = '__all__'
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'contrato': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class ComprobanteContableForm(forms.ModelForm):
    class Meta:
        model = ComprobanteContable
        fields = ['tipo', 'numero', 'fecha', 'tercero', 'centro_costo', 'descripcion', 'valor', 'estado']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tercero': forms.Select(attrs={'class': 'form-control'}),
            'centro_costo': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }

class CertificadoRetencionForm(forms.ModelForm):
    class Meta:
        model = CertificadoRetencion
        fields = ['tipo', 'numero', 'fecha', 'tercero', 'base_gravable', 'porcentaje_retencion', 'valor_retenido', 'concepto']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tercero': forms.Select(attrs={'class': 'form-control'}),
            'base_gravable': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'porcentaje_retencion': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
            'valor_retenido': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'concepto': forms.TextInput(attrs={'class': 'form-control'}),
        } 

# Nuevos formularios para funcionalidades agregadas
class MovimientoBancarioForm(forms.ModelForm):
    class Meta:
        model = MovimientoBancario
        fields = ['banco', 'cuenta_bancaria', 'fecha', 'descripcion', 'valor', 'tipo', 'referencia']
        widgets = {
            'banco': forms.TextInput(attrs={'class': 'form-control'}),
            'cuenta_bancaria': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'referencia': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CierreContableForm(forms.ModelForm):
    class Meta:
        model = CierreContable
        fields = ['periodo', 'observaciones']
        widgets = {
            'periodo': forms.Select(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = Presupuesto
        fields = ['periodo', 'cuenta', 'centro_costo', 'monto_presupuestado']
        widgets = {
            'periodo': forms.Select(attrs={'class': 'form-control'}),
            'cuenta': forms.Select(attrs={'class': 'form-control'}),
            'centro_costo': forms.Select(attrs={'class': 'form-control'}),
            'monto_presupuestado': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        } 

class ReporteFiscalForm(forms.ModelForm):
    """Formulario para reportes fiscales"""
    class Meta:
        model = ReporteFiscal
        fields = ['tipo', 'periodo', 'fecha_inicio', 'fecha_fin', 'observaciones']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        
        if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
            raise forms.ValidationError('La fecha de inicio no puede ser mayor a la fecha fin.')
        
        return cleaned_data

class DetalleFiscalForm(forms.ModelForm):
    """Formulario para detalles fiscales"""
    class Meta:
        model = DetalleFiscal
        fields = ['fecha', 'tercero', 'concepto', 'base_gravable', 'porcentaje_impuesto', 'valor_impuesto', 'asiento']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'concepto': forms.TextInput(attrs={'class': 'form-control'}),
            'base_gravable': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'porcentaje_impuesto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'valor_impuesto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        } 