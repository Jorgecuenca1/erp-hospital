from django.urls import path
from django.views.generic import TemplateView

app_name = 'pharmacy'

urlpatterns = [
    # Dashboard placeholder
    path('', TemplateView.as_view(template_name='pharmacy/dashboard.html'), name='dashboard'),
] 