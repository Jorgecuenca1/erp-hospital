from django.urls import path
from django.views.generic import TemplateView

app_name = 'hospitalization'

urlpatterns = [
    # Dashboard placeholder
    path('', TemplateView.as_view(template_name='hospitalization/dashboard.html'), name='dashboard'),
] 