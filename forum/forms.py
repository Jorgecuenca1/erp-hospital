from django import forms
from .models import Tema, Pregunta, Respuesta

class TemaForm(forms.ModelForm):
    class Meta:
        model = Tema
        fields = '__all__'

class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ['tema', 'titulo', 'contenido', 'autor']
        # Optional: widgets for better UI, e.g., making 'autor' hidden if set automatically
        # widgets = {
        #     'autor': forms.HiddenInput(),
        # }

class RespuestaForm(forms.ModelForm):
    class Meta:
        model = Respuesta
        fields = ['pregunta', 'contenido', 'autor']
        # widgets = {
        #     'pregunta': forms.HiddenInput(),
        #     'autor': forms.HiddenInput(),
        # }
