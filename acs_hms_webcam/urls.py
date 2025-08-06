from django.urls import path
from django.views.generic import TemplateView

app_name = 'webcam'

urlpatterns = [
    # Dashboard placeholder
    path('', TemplateView.as_view(template_name='webcam/dashboard.html'), name='dashboard'),
] 