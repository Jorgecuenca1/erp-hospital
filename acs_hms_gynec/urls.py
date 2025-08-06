from django.urls import path
from . import views

app_name = 'gynec'

urlpatterns = [
    # Dashboard principal
    path('', views.GynecDashboardView.as_view(), name='dashboard'),
    
    # Gestión de pacientes ginecológicos
    path('patients/', views.GynecPatientListView.as_view(), name='patient_list'),
    path('patients/create/', views.GynecPatientCreateView.as_view(), name='patient_create'),
    path('patients/<int:pk>/', views.GynecPatientDetailView.as_view(), name='patient_detail'),
    path('patients/<int:pk>/update/', views.GynecPatientUpdateView.as_view(), name='patient_update'),
    path('patients/<int:pk>/delete/', views.GynecPatientDeleteView.as_view(), name='patient_delete'),
    
    # Gestión de embarazos
    path('pregnancies/', views.PregnancyListView.as_view(), name='pregnancy_list'),
    path('pregnancies/create/', views.PregnancyCreateView.as_view(), name='pregnancy_create'),
    path('pregnancies/<int:pk>/', views.PregnancyDetailView.as_view(), name='pregnancy_detail'),
    path('pregnancies/<int:pk>/update/', views.PregnancyUpdateView.as_view(), name='pregnancy_update'),
    path('pregnancies/<int:pk>/delete/', views.PregnancyDeleteView.as_view(), name='pregnancy_delete'),
    
    # Visitas prenatales
    path('antenatal-visits/', views.AntenatalVisitListView.as_view(), name='antenatal_list'),
    path('antenatal-visits/create/', views.AntenatalVisitCreateView.as_view(), name='antenatal_create'),
    path('antenatal-visits/<int:pk>/', views.AntenatalVisitDetailView.as_view(), name='antenatal_detail'),
    path('antenatal-visits/<int:pk>/update/', views.AntenatalVisitUpdateView.as_view(), name='antenatal_update'),
    path('antenatal-visits/<int:pk>/delete/', views.AntenatalVisitDeleteView.as_view(), name='antenatal_delete'),
    
    # Procedimientos ginecológicos
    path('procedures/', views.GynecologyProcedureListView.as_view(), name='procedure_list'),
    path('procedures/create/', views.GynecologyProcedureCreateView.as_view(), name='procedure_create'),
    path('procedures/<int:pk>/', views.GynecologyProcedureDetailView.as_view(), name='procedure_detail'),
    path('procedures/<int:pk>/update/', views.GynecologyProcedureUpdateView.as_view(), name='procedure_update'),
    path('procedures/<int:pk>/delete/', views.GynecologyProcedureDeleteView.as_view(), name='procedure_delete'),
    
    # Consultas de anticoncepción
    path('contraceptive/', views.ContraceptiveConsultationListView.as_view(), name='contraceptive_list'),
    path('contraceptive/create/', views.ContraceptiveConsultationCreateView.as_view(), name='contraceptive_create'),
    path('contraceptive/<int:pk>/', views.ContraceptiveConsultationDetailView.as_view(), name='contraceptive_detail'),
    path('contraceptive/<int:pk>/update/', views.ContraceptiveConsultationUpdateView.as_view(), name='contraceptive_update'),
    path('contraceptive/<int:pk>/delete/', views.ContraceptiveConsultationDeleteView.as_view(), name='contraceptive_delete'),
    
    # Gestión de menopausia
    path('menopause/', views.MenopauseManagementListView.as_view(), name='menopause_list'),
    path('menopause/create/', views.MenopauseManagementCreateView.as_view(), name='menopause_create'),
    path('menopause/<int:pk>/', views.MenopauseManagementDetailView.as_view(), name='menopause_detail'),
    path('menopause/<int:pk>/update/', views.MenopauseManagementUpdateView.as_view(), name='menopause_update'),
    path('menopause/<int:pk>/delete/', views.MenopauseManagementDeleteView.as_view(), name='menopause_delete'),
    
    # Registros médicos ginecológicos
    path('medical-records/', views.GynecologyMedicalRecordListView.as_view(), name='medical_record_list'),
    path('medical-records/create/', views.GynecologyMedicalRecordCreateView.as_view(), name='medical_record_create'),
    path('medical-records/<int:pk>/', views.GynecologyMedicalRecordDetailView.as_view(), name='medical_record_detail'),
    path('medical-records/<int:pk>/update/', views.GynecologyMedicalRecordUpdateView.as_view(), name='medical_record_update'),
    path('medical-records/<int:pk>/delete/', views.GynecologyMedicalRecordDeleteView.as_view(), name='medical_record_delete'),
    
    # Reportes y estadísticas
    path('reports/', views.GynecReportsView.as_view(), name='reports'),
] 