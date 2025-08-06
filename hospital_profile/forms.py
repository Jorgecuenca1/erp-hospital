from django import forms
from .models import HospitalProfile

class HospitalProfileForm(forms.ModelForm):
    class Meta:
        model = HospitalProfile
        fields = '__all__'
        widgets = {
            'fecha_habilitacion': forms.DateInput(attrs={'type': 'date'}),
        } 