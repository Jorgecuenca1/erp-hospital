from django.urls import path
from django.views.generic import TemplateView

app_name = 'insurance'

urlpatterns = [
    # Dashboard placeholder
    path('', TemplateView.as_view(template_name='insurance/dashboard.html'), name='dashboard'),
] 