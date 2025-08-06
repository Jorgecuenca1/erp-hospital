from django.urls import path
from django.views.generic import TemplateView

app_name = 'blood_bank'

urlpatterns = [
    # Dashboard placeholder
    path('', TemplateView.as_view(template_name='blood_bank/dashboard.html'), name='dashboard'),
] 