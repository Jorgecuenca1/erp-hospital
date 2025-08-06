from django.urls import path
from django.views.generic import TemplateView

app_name = 'aesthetic'

urlpatterns = [
    # Dashboard placeholder
    path('', TemplateView.as_view(template_name='aesthetic/dashboard.html'), name='dashboard'),
] 