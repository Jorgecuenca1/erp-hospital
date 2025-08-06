from django.urls import path
from django.views.generic import TemplateView

app_name = 'dental'

urlpatterns = [
    # Dashboard placeholder
    path('', TemplateView.as_view(template_name='dental/dashboard.html'), name='dashboard'),
] 