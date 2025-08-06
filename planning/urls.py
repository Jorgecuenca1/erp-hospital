from django.urls import path
from . import views

app_name = 'planning'

urlpatterns = [
    path('', views.planning_dashboard, name='dashboard'),
    path('allocation/', views.resource_allocation, name='allocation'),
    path('scheduling/', views.staff_scheduling, name='scheduling'),
    path('capacity/', views.capacity_planning, name='capacity'),
] 