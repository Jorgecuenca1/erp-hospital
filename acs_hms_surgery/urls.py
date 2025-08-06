from django.urls import path
from django.views.generic import TemplateView

app_name = 'surgery'

urlpatterns = [
    # Dashboard placeholder
    path('', TemplateView.as_view(template_name='surgery/dashboard.html'), name='dashboard'),
] 