from django.urls import path
from . import views

app_name = 'social_metrics'

urlpatterns = [
    path('', views.SocialMetricsDashboardView.as_view(), name='dashboard'),
    path('metrics/', views.MetricsListView.as_view(), name='metrics_list'),
    path('reports/', views.SocialReportsView.as_view(), name='reports'),
] 