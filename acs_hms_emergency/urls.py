from django.urls import path
from django.views.generic import TemplateView

app_name = 'emergency'

urlpatterns = [
    # Dashboard placeholder
    path('', TemplateView.as_view(template_name='emergency/dashboard.html'), name='dashboard'),
] 