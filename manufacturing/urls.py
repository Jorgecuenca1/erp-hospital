from django.urls import path
from . import views

app_name = 'manufacturing'

urlpatterns = [
    path('', views.manufacturing_dashboard, name='dashboard'),
    path('devices/', views.device_list, name='device_list'),
    path('orders/', views.production_orders, name='production_orders'),
    path('quality/', views.quality_control, name='quality_control'),
    path('bom/', views.bill_of_materials, name='bill_of_materials'),
] 