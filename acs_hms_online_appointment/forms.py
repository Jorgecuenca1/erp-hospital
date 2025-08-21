from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from acs_hms_base.models import HMSUser
from .models import DoctorAvailability, OnlineAppointmentSlot

class OnlineAppointmentForm(forms.Form):
    '''Formulario básico para Online Appointment'''
    
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

class OnlineAppointmentSearchForm(forms.Form):
    '''Formulario de búsqueda para Online Appointment'''
    
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

class OnlineAppointmentFilterForm(forms.Form):
    '''Formulario de filtros para Online Appointment'''
    
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


class AgendaElectronicaDisponibilidadForm(forms.Form):
    """Formulario para crear disponibilidad en la agenda electrónica"""
    
    # Nombre del profesional
    profesional = forms.ModelChoiceField(
        queryset=HMSUser.objects.filter(user_type='DOCTOR'),
        widget=forms.Select(attrs={
            'class': 'form-control select2',
            'placeholder': 'Escriba el nombre o apellido'
        }),
        label='Nombre del profesional que se le generará espacio en la agenda',
        help_text='Escriba el nombre o apellido y selecciónelo de la lista desplegable.',
        empty_label='Seleccione un profesional...'
    )
    
    # Rango de fechas
    fecha_desde = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'placeholder': 'dd/mm/aaaa'
        }),
        label='Desde el día',
        help_text='dd/mm/aaaa'
    )
    
    fecha_hasta = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'placeholder': 'dd/mm/aaaa'
        }),
        label='Hasta el día',
        help_text='dd/mm/aaaa'
    )
    
    # Horarios de mañana
    hora_inicio_am = forms.TimeField(
        initial='08:00',
        widget=forms.TimeInput(attrs={
            'class': 'form-control',
            'type': 'time',
            'value': '08:00'
        }),
        label='Hora inicio a.m.',
        help_text='08:00 a.m.'
    )
    
    hora_fin_am = forms.TimeField(
        initial='12:00',
        widget=forms.TimeInput(attrs={
            'class': 'form-control',
            'type': 'time',
            'value': '12:00'
        }),
        label='Hora fin a.m.',
        help_text='12:00 p.m.'
    )
    
    # Horarios de tarde
    hora_inicio_pm = forms.TimeField(
        initial='14:00',
        widget=forms.TimeInput(attrs={
            'class': 'form-control',
            'type': 'time',
            'value': '14:00'
        }),
        label='Hora inicio p.m.',
        help_text='02:00 p.m.'
    )
    
    hora_fin_pm = forms.TimeField(
        initial='18:00',
        widget=forms.TimeInput(attrs={
            'class': 'form-control',
            'type': 'time',
            'value': '18:00'
        }),
        label='Hora fin p.m.',
        help_text='06:00 p.m.'
    )
    
    # Dividir en intervalos
    DIVISION_CHOICES = [
        ('15', '15 minutos'),
        ('20', '20 minutos'),
        ('30', '30 minutos'),
        ('45', '45 minutos'),
        ('60', '60 minutos'),
    ]
    
    dividir_en = forms.ChoiceField(
        choices=DIVISION_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Dividir en',
        initial='30'
    )
    
    # Sede
    SEDE_CHOICES = [
        ('PRINCIPAL', 'PRINCIPAL'),
        ('SUCURSAL_1', 'SUCURSAL 1'),
        ('SUCURSAL_2', 'SUCURSAL 2'),
        ('CONSULTORIO_EXTERNO', 'CONSULTORIO EXTERNO'),
    ]
    
    sede = forms.ChoiceField(
        choices=SEDE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Sede donde se creará la disponibilidad',
        initial='PRINCIPAL'
    )
    
    # Días de la semana (campos de selección múltiple)
    lunes = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='LUNES'
    )
    
    martes = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='MARTES'
    )
    
    miercoles = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='MIÉRCOLES'
    )
    
    jueves = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='JUEVES'
    )
    
    viernes = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='VIERNES'
    )
    
    sabado = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='SÁBADO'
    )
    
    domingo = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='DOMINGO'
    )
    
    # Habilitar disponibilidad en Agenda tus citas
    habilitar_agenda_tus_citas = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Habilitar disponibilidad en Agenda tus citas'
    )
    
    # Habilitar disponibilidad en Doctoralia
    habilitar_doctoralia = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Habilitar disponibilidad en Doctoralia'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar queryset de profesionales
        self.fields['profesional'].queryset = HMSUser.objects.filter(
            user_type='DOCTOR',
            active=True
        ).select_related('user')
    
    def clean(self):
        cleaned_data = super().clean()
        fecha_desde = cleaned_data.get('fecha_desde')
        fecha_hasta = cleaned_data.get('fecha_hasta')
        
        # Validar que la fecha hasta sea posterior a la fecha desde
        if fecha_desde and fecha_hasta:
            if fecha_hasta < fecha_desde:
                raise forms.ValidationError('La fecha "hasta" debe ser posterior a la fecha "desde"')
        
        # Validar que al menos un día de la semana esté seleccionado
        dias_semana = [
            cleaned_data.get('lunes'),
            cleaned_data.get('martes'),
            cleaned_data.get('miercoles'),
            cleaned_data.get('jueves'),
            cleaned_data.get('viernes'),
            cleaned_data.get('sabado'),
            cleaned_data.get('domingo'),
        ]
        
        if not any(dias_semana):
            raise forms.ValidationError('Debe seleccionar al menos un día de la semana')
        
        # Validar horarios de mañana
        hora_inicio_am = cleaned_data.get('hora_inicio_am')
        hora_fin_am = cleaned_data.get('hora_fin_am')
        
        if hora_inicio_am and hora_fin_am:
            if hora_fin_am <= hora_inicio_am:
                raise forms.ValidationError('La hora fin a.m. debe ser posterior a la hora inicio a.m.')
        
        # Validar horarios de tarde
        hora_inicio_pm = cleaned_data.get('hora_inicio_pm')
        hora_fin_pm = cleaned_data.get('hora_fin_pm')
        
        if hora_inicio_pm and hora_fin_pm:
            if hora_fin_pm <= hora_inicio_pm:
                raise forms.ValidationError('La hora fin p.m. debe ser posterior a la hora inicio p.m.')
        
        # Validar que no se superpongan horarios de mañana y tarde
        if hora_fin_am and hora_inicio_pm:
            if hora_inicio_pm <= hora_fin_am:
                raise forms.ValidationError('El horario de la tarde no puede superponerse con el horario de la mañana')
        
        return cleaned_data
    
    def get_selected_days(self):
        """Retorna una lista de los días seleccionados"""
        cleaned_data = self.cleaned_data
        selected_days = []
        
        day_mapping = {
            'lunes': 'monday',
            'martes': 'tuesday',
            'miercoles': 'wednesday',
            'jueves': 'thursday',
            'viernes': 'friday',
            'sabado': 'saturday',
            'domingo': 'sunday',
        }
        
        for spanish_day, english_day in day_mapping.items():
            if cleaned_data.get(spanish_day):
                selected_days.append(english_day)
        
        return selected_days


class DoctorAvailabilityForm(forms.ModelForm):
    """Formulario para editar disponibilidad individual de doctor"""
    
    class Meta:
        model = DoctorAvailability
        fields = '__all__'
        widgets = {
            'doctor': forms.Select(attrs={'class': 'form-control select2'}),
            'day_of_week': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'slot_duration': forms.NumberInput(attrs={'class': 'form-control', 'min': '5', 'max': '180'}),
            'slot_type': forms.Select(attrs={'class': 'form-control'}),
            'max_appointments': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '10'}),
            'consultation_fee': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'special_instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = HMSUser.objects.filter(
            user_type='DOCTOR',
            active=True
        ).select_related('user')
