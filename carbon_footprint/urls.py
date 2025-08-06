from django.urls import path
from . import views

app_name = 'carbon_footprint'

urlpatterns = [
    path('', views.CarbonFootprintDashboardView.as_view(), name='dashboard'),
    path('calculate/', views.CalculateFootprintView.as_view(), name='calculate'),
    path('reports/', views.FootprintReportsView.as_view(), name='reports'),
] 