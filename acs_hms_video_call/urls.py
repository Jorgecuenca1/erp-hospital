from django.urls import path
from django.views.generic import TemplateView

app_name = 'video_call'

urlpatterns = [
    # Dashboard placeholder
    path('', TemplateView.as_view(template_name='video_call/dashboard.html'), name='dashboard'),
] 