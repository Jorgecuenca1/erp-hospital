from django.urls import path
from . import views

app_name = 'hospital_profile'

urlpatterns = [
    path('', views.HospitalProfileDetailView.as_view(), name='detail'),
    path('edit/', views.HospitalProfileUpdateView.as_view(), name='edit'),
] 