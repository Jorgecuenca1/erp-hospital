from django.urls import path
from django.views.generic import TemplateView

app_name = 'operation_theater'

urlpatterns = [
    # Dashboard placeholder
    path('', TemplateView.as_view(template_name='operation_theater/dashboard.html'), name='dashboard'),
] 