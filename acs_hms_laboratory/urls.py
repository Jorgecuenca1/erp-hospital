from django.urls import path
from django.views.generic import TemplateView

app_name = 'laboratory'

urlpatterns = [
    # Dashboard placeholder
    path('', TemplateView.as_view(template_name='laboratory/dashboard.html'), name='dashboard'),
] 