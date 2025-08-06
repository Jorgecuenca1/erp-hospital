from django.urls import path
from . import views

app_name = 'esg_reporting'

urlpatterns = [
    # Dashboard
    path('', views.esg_dashboard, name='dashboard'),
    
    # ESG Reports
    path('reports/', views.esg_report_list, name='report_list'),
    path('reports/create/', views.create_esg_report, name='create_report'),
    path('reports/<int:report_id>/', views.esg_report_detail, name='report_detail'),
    
    # ESG Goals
    path('goals/', views.esg_goals_list, name='goals_list'),
    path('goals/create/', views.create_esg_goal, name='create_goal'),
    
    # Analytics & Metrics
    path('sustainability/', views.sustainability_metrics, name='sustainability_metrics'),
    path('api/analytics/', views.esg_analytics_api, name='analytics_api'),
] 