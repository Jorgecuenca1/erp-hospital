from django import forms
from .models import PaginaWeb, Seccion, Menu, Banner

class PaginaWebForm(forms.ModelForm):
    class Meta:
        model = PaginaWeb
        fields = '__all__'

class SeccionForm(forms.ModelForm):
    class Meta:
        model = Seccion
        fields = '__all__'

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = '__all__'

class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = '__all__' 