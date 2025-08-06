from django import forms
from .models import Curso, Modulo, Leccion, Inscripcion, ProgresoLeccion

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = '__all__'

class ModuloForm(forms.ModelForm):
    class Meta:
        model = Modulo
        fields = '__all__'

class LeccionForm(forms.ModelForm):
    class Meta:
        model = Leccion
        fields = '__all__'

class InscripcionForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = '__all__'

class ProgresoLeccionForm(forms.ModelForm):
    class Meta:
        model = ProgresoLeccion
        fields = '__all__'
