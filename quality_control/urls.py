from django.urls import path
from . import views

app_name = 'quality_control'

urlpatterns = [
    path('', views.quality_dashboard, name='dashboard'),
    path('standards/', views.quality_standards, name='standards'),
    path('audits/', views.quality_audits, name='audits'),
    path('metrics/', views.quality_metrics, name='metrics'),
    path('incidents/', views.incident_reports, name='incidents'),
    path('improvements/', views.quality_improvements, name='improvements'),
    path('compliance/', views.compliance_report, name='compliance'),
] 