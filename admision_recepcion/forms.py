from django import forms
from django.forms import modelformset_factory, inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, HTML, Submit, Row, Column, Fieldset
from .models import (
    OrdenServicio, DetalleOrdenServicio, Municipio, Empresa, 
    Convenio, Servicio, Prestador, SeguimientoPaciente
)


class OrdenServicioForm(forms.ModelForm):
    """Formulario principal para Órdenes de Servicios"""
    
    class Meta:
        model = OrdenServicio
        fields = '__all__'
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_solicitud': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_orden': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'funciones_cargo': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'correo_electronico': forms.EmailInput(attrs={'class': 'form-control'}),
            'foto': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'huella': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'firma': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            # Campos de texto
            'numero_identificacion': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad_nacimiento': forms.TextInput(attrs={'class': 'form-control'}),
            'primer_apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'segundo_apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'primer_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'otros_nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'barrio': forms.TextInput(attrs={'class': 'form-control'}),
            'localidad': forms.TextInput(attrs={'class': 'form-control'}),
            'celulares': forms.TextInput(attrs={'class': 'form-control'}),
            'telefonos': forms.TextInput(attrs={'class': 'form-control'}),
            'profesion_cargo': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_evaluacion': forms.TextInput(attrs={'class': 'form-control'}),
            'eps': forms.TextInput(attrs={'class': 'form-control'}),
            'afp': forms.TextInput(attrs={'class': 'form-control'}),
            'arl': forms.TextInput(attrs={'class': 'form-control'}),
            # Campos de selección
            'tipo_documento': forms.Select(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'estado_civil': forms.Select(attrs={'class': 'form-control'}),
            'nivel_educativo': forms.Select(attrs={'class': 'form-control'}),
            'zona': forms.Select(attrs={'class': 'form-control'}),
            'sede': forms.Select(attrs={'class': 'form-control'}),
            'estrato': forms.Select(attrs={'class': 'form-control'}),
            'estado_orden': forms.Select(attrs={'class': 'form-control'}),
            'municipio': forms.Select(attrs={'class': 'form-control select2'}),
            'convenio': forms.Select(attrs={'class': 'form-control select2'}),
            'empresa_mision': forms.Select(attrs={'class': 'form-control select2'}),
            # Campos numéricos
            'total_orden': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'readonly': True}),
            'total_pagar': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'readonly': True}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            # Información de la Orden
            Fieldset(
                'Información de la Orden',
                Row(
                    Column('numero_orden', css_class='form-group col-md-4 mb-3'),
                    Column('fecha_orden', css_class='form-group col-md-4 mb-3'),
                    Column('estado_orden', css_class='form-group col-md-4 mb-3'),
                ),
                css_class='border rounded p-3 mb-4'
            ),
            
            # Datos Personales
            Fieldset(
                'Datos Personales',
                Row(
                    Column('tipo_documento', css_class='form-group col-md-3 mb-3'),
                    Column('numero_identificacion', css_class='form-group col-md-3 mb-3'),
                    Column('ciudad_nacimiento', css_class='form-group col-md-3 mb-3'),
                    Column('fecha_nacimiento', css_class='form-group col-md-3 mb-3'),
                ),
                Row(
                    Column('primer_apellido', css_class='form-group col-md-3 mb-3'),
                    Column('segundo_apellido', css_class='form-group col-md-3 mb-3'),
                    Column('primer_nombre', css_class='form-group col-md-3 mb-3'),
                    Column('otros_nombres', css_class='form-group col-md-3 mb-3'),
                ),
                Row(
                    Column('genero', css_class='form-group col-md-3 mb-3'),
                    Column('estado_civil', css_class='form-group col-md-3 mb-3'),
                    Column('nivel_educativo', css_class='form-group col-md-3 mb-3'),
                    Column('correo_electronico', css_class='form-group col-md-3 mb-3'),
                ),
                Row(
                    Column('foto', css_class='form-group col-md-4 mb-3'),
                    Column('huella', css_class='form-group col-md-4 mb-3'),
                    Column('firma', css_class='form-group col-md-4 mb-3'),
                ),
                css_class='border rounded p-3 mb-4'
            ),
            
            # Datos de Ubicación
            Fieldset(
                'Datos de Ubicación',
                Row(
                    Column('zona', css_class='form-group col-md-2 mb-3'),
                    Column('direccion', css_class='form-group col-md-4 mb-3'),
                    Column('barrio', css_class='form-group col-md-3 mb-3'),
                    Column('localidad', css_class='form-group col-md-3 mb-3'),
                ),
                Row(
                    Column('sede', css_class='form-group col-md-3 mb-3'),
                    Column('estrato', css_class='form-group col-md-2 mb-3'),
                    Column('municipio', css_class='form-group col-md-4 mb-3'),
                    Column('celulares', css_class='form-group col-md-3 mb-3'),
                ),
                Row(
                    Column('telefonos', css_class='form-group col-md-4 mb-3'),
                ),
                css_class='border rounded p-3 mb-4'
            ),
            
            # Datos de Trabajo
            Fieldset(
                'Datos de Trabajo',
                Row(
                    Column('profesion_cargo', css_class='form-group col-md-6 mb-3'),
                    Column('tipo_evaluacion', css_class='form-group col-md-6 mb-3'),
                ),
                Row(
                    Column('funciones_cargo', css_class='form-group col-md-12 mb-3'),
                ),
                Row(
                    Column('convenio', css_class='form-group col-md-6 mb-3'),
                    Column('empresa_mision', css_class='form-group col-md-6 mb-3'),
                ),
                Row(
                    Column('eps', css_class='form-group col-md-4 mb-3'),
                    Column('afp', css_class='form-group col-md-4 mb-3'),
                    Column('arl', css_class='form-group col-md-4 mb-3'),
                ),
                css_class='border rounded p-3 mb-4'
            ),
            
            # Observaciones
            Fieldset(
                'Observaciones y Solicitud',
                Row(
                    Column('observaciones', css_class='form-group col-md-8 mb-3'),
                    Column('fecha_solicitud', css_class='form-group col-md-4 mb-3'),
                ),
                css_class='border rounded p-3 mb-4'
            ),
            
            # Totales
            Fieldset(
                'Totales',
                Row(
                    Column('total_orden', css_class='form-group col-md-6 mb-3'),
                    Column('total_pagar', css_class='form-group col-md-6 mb-3'),
                ),
                css_class='border rounded p-3 mb-4'
            ),
            
            Submit('submit', 'Guardar Orden de Servicio', css_class='btn btn-primary btn-lg')
        )
        
        # Filtrar queryset para campos de relación
        self.fields['municipio'].queryset = Municipio.objects.filter(activo=True).order_by('departamento', 'nombre')
        self.fields['convenio'].queryset = Convenio.objects.filter(estado='ACTIVO').order_by('nombre')
        self.fields['empresa_mision'].queryset = Empresa.objects.filter(activo=True).order_by('razon_social')


class DetalleOrdenServicioForm(forms.ModelForm):
    """Formulario para detalles de servicios"""
    
    class Meta:
        model = DetalleOrdenServicio
        fields = ['cantidad', 'servicio', 'prestador', 'valor_unitario', 'forma_pago', 'valor_pagar', 'observaciones']
        widgets = {
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'value': '1'}),
            'servicio': forms.Select(attrs={'class': 'form-control select2'}),
            'prestador': forms.Select(attrs={'class': 'form-control select2'}),
            'valor_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'forma_pago': forms.Select(attrs={'class': 'form-control'}),
            'valor_pagar': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['servicio'].queryset = Servicio.objects.filter(activo=True).order_by('nombre')
        self.fields['prestador'].queryset = Prestador.objects.filter(activo=True).order_by('nombre')


# Formset para manejar múltiples detalles de servicios
DetalleOrdenServicioFormSet = inlineformset_factory(
    OrdenServicio,
    DetalleOrdenServicio,
    form=DetalleOrdenServicioForm,
    extra=1,
    can_delete=True,
    fields=['cantidad', 'servicio', 'prestador', 'valor_unitario', 'forma_pago', 'valor_pagar', 'observaciones']
)


class SeguimientoPacienteForm(forms.ModelForm):
    """Formulario para seguimiento de pacientes"""
    
    class Meta:
        model = SeguimientoPaciente
        fields = ['estado', 'observaciones']
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class OrdenServicioBusquedaForm(forms.Form):
    """Formulario de búsqueda para órdenes de servicios"""
    
    numero_orden = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Número de orden...'
        }),
        label='N°. O.S.'
    )
    
    numero_identificacion = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Número de identificación...'
        }),
        label='Identificación'
    )
    
    nombre_paciente = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre del paciente...'
        }),
        label='Nombre'
    )
    
    fecha_desde = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='Desde'
    )
    
    fecha_hasta = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='Hasta'
    )
    
    estado_orden = forms.ChoiceField(
        required=False,
        choices=[('', 'Todos')] + OrdenServicio.ESTADO_ORDEN_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Estado'
    )
    
    sede = forms.ChoiceField(
        required=False,
        choices=[('', 'Todas')] + OrdenServicio.SEDE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Sede'
    )


# Formularios para modelos auxiliares

class EmpresaForm(forms.ModelForm):
    """Formulario para empresas"""
    
    class Meta:
        model = Empresa
        fields = '__all__'
        widgets = {
            'nit': forms.TextInput(attrs={'class': 'form-control'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_comercial': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_empresa': forms.Select(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contacto_principal': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ConvenioForm(forms.ModelForm):
    """Formulario para convenios"""
    
    class Meta:
        model = Convenio
        fields = '__all__'
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'empresa': forms.Select(attrs={'class': 'form-control select2'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'valor_contrato': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }


class ServicioForm(forms.ModelForm):
    """Formulario para servicios"""
    
    class Meta:
        model = Servicio
        fields = '__all__'
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'valor_base': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }


class PrestadorForm(forms.ModelForm):
    """Formulario para prestadores"""
    
    class Meta:
        model = Prestador
        fields = '__all__'
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control'}),
            'especialidad': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
