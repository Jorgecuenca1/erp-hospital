from django.urls import path
from django.views.generic import TemplateView

app_name = 'online_appointment'

urlpatterns = [
    # Dashboard placeholder
    path('', TemplateView.as_view(template_name='online_appointment/dashboard.html'), name='dashboard'),
] 