from django.urls import path
from . import views

app_name = 'maintenance'

urlpatterns = [
    path('', views.maintenance_dashboard, name='dashboard'),
    path('equipment/', views.equipment_list, name='equipment_list'),
    path('equipment/<int:equipment_id>/', views.equipment_detail, name='equipment_detail'),
    path('schedule/', views.maintenance_schedule, name='schedule'),
    path('records/', views.maintenance_records, name='records'),
    path('alerts/', views.maintenance_alerts, name='alerts'),
] 