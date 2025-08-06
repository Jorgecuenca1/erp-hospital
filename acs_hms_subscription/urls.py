from django.urls import path
from django.views.generic import TemplateView

app_name = 'subscription'

urlpatterns = [
    # Dashboard placeholder
    path('', TemplateView.as_view(template_name='subscription/dashboard.html'), name='dashboard'),
] 