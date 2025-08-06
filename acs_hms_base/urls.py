from django.urls import path
from . import views

app_name = 'acs_hms_base'

urlpatterns = [
    # Dashboard
    path('', views.DashboardView.as_view(), name='dashboard'),
    
    # Hospital Management
    path('hospitals/', views.HospitalListView.as_view(), name='hospital_list'),
    path('hospitals/create/', views.HospitalCreateView.as_view(), name='hospital_create'),
    path('hospitals/<int:pk>/', views.HospitalDetailView.as_view(), name='hospital_detail'),
    path('hospitals/<int:pk>/edit/', views.HospitalUpdateView.as_view(), name='hospital_update'),
    path('hospitals/<int:pk>/delete/', views.HospitalDeleteView.as_view(), name='hospital_delete'),
    
    # Department Management
    path('departments/', views.DepartmentListView.as_view(), name='department_list'),
    path('departments/create/', views.DepartmentCreateView.as_view(), name='department_create'),
    path('departments/<int:pk>/', views.DepartmentDetailView.as_view(), name='department_detail'),
    path('departments/<int:pk>/edit/', views.DepartmentUpdateView.as_view(), name='department_update'),
    path('departments/<int:pk>/delete/', views.DepartmentDeleteView.as_view(), name='department_delete'),
    
    # Room Management
    path('rooms/', views.RoomListView.as_view(), name='room_list'),
    path('rooms/create/', views.RoomCreateView.as_view(), name='room_create'),
    path('rooms/<int:pk>/', views.RoomDetailView.as_view(), name='room_detail'),
    path('rooms/<int:pk>/edit/', views.RoomUpdateView.as_view(), name='room_update'),
    path('rooms/<int:pk>/delete/', views.RoomDeleteView.as_view(), name='room_delete'),
    
    # HMS User Management
    path('users/', views.HMSUserListView.as_view(), name='user_list'),
    path('users/create/', views.HMSUserCreateView.as_view(), name='user_create'),
    path('users/<int:pk>/', views.HMSUserDetailView.as_view(), name='user_detail'),
    path('users/<int:pk>/edit/', views.HMSUserUpdateView.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', views.HMSUserDeleteView.as_view(), name='user_delete'),
    
    # Patient Management
    path('patients/', views.PatientListView.as_view(), name='patient_list'),
    path('patients/create/', views.PatientCreateView.as_view(), name='patient_create'),
    path('patients/<int:pk>/', views.PatientDetailView.as_view(), name='patient_detail'),
    path('patients/<int:pk>/edit/', views.PatientUpdateView.as_view(), name='patient_update'),
    path('patients/<int:pk>/delete/', views.PatientDeleteView.as_view(), name='patient_delete'),
    
    # Appointment Management
    path('appointments/', views.AppointmentListView.as_view(), name='appointment_list'),
    path('appointments/create/', views.AppointmentCreateView.as_view(), name='appointment_create'),
    path('appointments/<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment_detail'),
    path('appointments/<int:pk>/edit/', views.AppointmentUpdateView.as_view(), name='appointment_update'),
    path('appointments/<int:pk>/delete/', views.AppointmentDeleteView.as_view(), name='appointment_delete'),
    
    # Medical Record Management
    path('medical-records/', views.MedicalRecordListView.as_view(), name='medical_record_list'),
    path('medical-records/create/', views.MedicalRecordCreateView.as_view(), name='medical_record_create'),
    path('medical-records/<int:pk>/', views.MedicalRecordDetailView.as_view(), name='medical_record_detail'),
    path('medical-records/<int:pk>/edit/', views.MedicalRecordUpdateView.as_view(), name='medical_record_update'),
    path('medical-records/<int:pk>/delete/', views.MedicalRecordDeleteView.as_view(), name='medical_record_delete'),
    
    # Configuration
    path('configuration/', views.HospitalConfigurationView.as_view(), name='configuration'),
    
    # API endpoints
    path('api/patients/search/', views.PatientSearchAPIView.as_view(), name='patient_search_api'),
    path('api/doctors/search/', views.DoctorSearchAPIView.as_view(), name='doctor_search_api'),
    path('api/rooms/available/', views.AvailableRoomsAPIView.as_view(), name='available_rooms_api'),
] 