from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'acs_hms_online_appointment'

urlpatterns = [
    # Dashboard principal
    path('', views.OnlineAppointmentDashboardView.as_view(), name='dashboard'),
    
    # Gestión básica de citas online
    path('appointments/', views.OnlineAppointmentListView.as_view(), name='appointment_list'),
    path('appointments/create/', views.OnlineAppointmentCreateView.as_view(), name='appointment_create'),
    path('appointments/<int:pk>/', views.OnlineAppointmentDetailView.as_view(), name='appointment_detail'),
    path('appointments/<int:pk>/update/', views.OnlineAppointmentUpdateView.as_view(), name='appointment_update'),
    path('appointments/<int:pk>/delete/', views.OnlineAppointmentDeleteView.as_view(), name='appointment_delete'),
    path('reports/', views.OnlineAppointmentReportsView.as_view(), name='reports'),
    
    # === AGENDA ELECTRÓNICA ===
    path('agenda/', views.AgendaElectronicaListView.as_view(), name='agenda_list'),
    path('agenda/crear/', views.AgendaElectronicaCreateView.as_view(), name='agenda_create'),
    path('agenda/<int:pk>/', views.AgendaElectronicaDetailView.as_view(), name='agenda_detail'),
    path('agenda/<int:pk>/editar/', views.AgendaElectronicaUpdateView.as_view(), name='agenda_update'),
    path('agenda/<int:pk>/eliminar/', views.AgendaElectronicaDeleteView.as_view(), name='agenda_delete'),
    path('agenda/<int:pk>/tabla/', views.AgendaDisponibilidadTableView.as_view(), name='agenda_table'),
    
    # === GESTIÓN DE DISPONIBILIDAD INDIVIDUAL ===
    path('availability/', views.DoctorAvailabilityListView.as_view(), name='availability_list'),
    path('availability/create/', views.DoctorAvailabilityCreateView.as_view(), name='availability_create'),
] 