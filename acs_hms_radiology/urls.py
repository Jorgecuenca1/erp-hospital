from django.urls import path
from . import views

app_name = 'radiology'

urlpatterns = [
    # Dashboard
    path('', views.RadiologyDashboardView.as_view(), name='dashboard'),
    
    # Radiology Modality URLs
    path('modalities/', views.RadiologyModalityListView.as_view(), name='modality_list'),
    path('modalities/<int:pk>/', views.RadiologyModalityDetailView.as_view(), name='modality_detail'),
    
    # Radiology Exam URLs
    path('exams/', views.RadiologyExamListView.as_view(), name='exam_list'),
    path('exams/<int:pk>/', views.RadiologyExamDetailView.as_view(), name='exam_detail'),
    
    # Radiology Order URLs
    path('orders/', views.RadiologyOrderListView.as_view(), name='order_list'),
    path('orders/<int:pk>/', views.RadiologyOrderDetailView.as_view(), name='order_detail'),
    
    # Radiology Study URLs
    path('studies/', views.RadiologyStudyListView.as_view(), name='study_list'),
    path('studies/<int:pk>/', views.RadiologyStudyDetailView.as_view(), name='study_detail'),
    
    # Radiology Image URLs
    path('images/', views.RadiologyImageListView.as_view(), name='image_list'),
    path('images/<int:pk>/', views.RadiologyImageDetailView.as_view(), name='image_detail'),
    
    # Radiology Report URLs
    path('reports/', views.RadiologyReportListView.as_view(), name='report_list'),
    path('reports/<int:pk>/', views.RadiologyReportDetailView.as_view(), name='report_detail'),
    
    # Radiology Protocol URLs
    path('protocols/', views.RadiologyProtocolListView.as_view(), name='protocol_list'),
    path('protocols/<int:pk>/', views.RadiologyProtocolDetailView.as_view(), name='protocol_detail'),
    
    # Export URLs
    path('export/', views.export_radiology_data, name='export_data'),
    
    # AJAX URLs
    path('api/patient-history/', views.get_patient_radiology_history, name='patient_history'),
    path('api/update-status/', views.update_order_status, name='update_status'),
] 