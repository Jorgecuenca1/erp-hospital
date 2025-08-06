from django.urls import path
from . import views

app_name = 'rental_management'

urlpatterns = [
    path('', views.rental_dashboard, name='dashboard'),
    path('equipment/', views.rental_equipment, name='equipment'),
    path('agreements/', views.rental_agreements, name='agreements'),
    path('payments/', views.rental_payments, name='payments'),
] 