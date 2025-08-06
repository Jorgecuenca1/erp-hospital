from django.urls import path
from . import views

app_name = 'nursing'

urlpatterns = [
    # Dashboard
    path('', views.NursingDashboardView.as_view(), name='dashboard'),
    
    # Nursing Unit URLs
    path('units/', views.NursingUnitListView.as_view(), name='unit_list'),
    path('units/<int:pk>/', views.NursingUnitDetailView.as_view(), name='unit_detail'),
    
    # Nursing Shift URLs
    path('shifts/', views.NursingShiftListView.as_view(), name='shift_list'),
    path('shifts/<int:pk>/', views.NursingShiftDetailView.as_view(), name='shift_detail'),
    
    # Nursing Assessment URLs
    path('assessments/', views.NursingAssessmentListView.as_view(), name='assessment_list'),
    path('assessments/<int:pk>/', views.NursingAssessmentDetailView.as_view(), name='assessment_detail'),
    
    # Nursing Care URLs
    path('care/', views.NursingCareListView.as_view(), name='care_list'),
    path('care/<int:pk>/', views.NursingCareDetailView.as_view(), name='care_detail'),
    
    # Medication Administration URLs
    path('medications/', views.MedicationAdministrationListView.as_view(), name='medication_list'),
    path('medications/<int:pk>/', views.MedicationAdministrationDetailView.as_view(), name='medication_detail'),
    
    # Nursing Handoff URLs
    path('handoffs/', views.NursingHandoffListView.as_view(), name='handoff_list'),
    path('handoffs/<int:pk>/', views.NursingHandoffDetailView.as_view(), name='handoff_detail'),
    
    # Nursing Incident URLs
    path('incidents/', views.NursingIncidentListView.as_view(), name='incident_list'),
    path('incidents/<int:pk>/', views.NursingIncidentDetailView.as_view(), name='incident_detail'),
    
    # Export URLs
    path('export/', views.export_nursing_data, name='export_data'),
    
    # AJAX URLs
    path('api/patient-data/', views.get_patient_nursing_data, name='patient_data'),
    path('api/update-medication/', views.update_medication_status, name='update_medication'),
    path('api/unit-census/', views.get_unit_census, name='unit_census'),
] 