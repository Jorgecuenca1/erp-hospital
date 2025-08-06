from django.urls import path
from django.views.generic import TemplateView

app_name = 'certification'

urlpatterns = [
    # Dashboard placeholder
    path('', TemplateView.as_view(template_name='certification/dashboard.html'), name='dashboard'),
] 