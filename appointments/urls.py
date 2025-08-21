from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    # Dashboard principal
    path('', views.AppointmentsDashboardView.as_view(), name='dashboard'),
    path('citas/', views.CitaListView.as_view(), name='cita_list'),
    path('citas/new/', views.CitaCreateView.as_view(), name='cita_create'),
    path('citas/<int:pk>/', views.CitaDetailView.as_view(), name='cita_detail'),
    path('citas/<int:pk>/edit/', views.CitaUpdateView.as_view(), name='cita_edit'),
    path('citas/<int:pk>/delete/', views.CitaDeleteView.as_view(), name='cita_delete'),
] 