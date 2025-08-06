from django.urls import path
from . import views

urlpatterns = [
    # Registration and Authentication
    path('register/', views.patient_portal_register, name='patient_portal_register'),
    
    # Dashboard
    path('', views.PatientPortalDashboard.as_view(), name='patient_portal_dashboard'),
    
    # Appointments
    path('appointments/', views.PatientAppointmentListView.as_view(), name='patient_appointments'),
    path('appointments/book/', views.PatientAppointmentCreateView.as_view(), name='patient_appointment_create'),
    path('appointments/<int:pk>/', views.PatientAppointmentDetailView.as_view(), name='patient_appointment_detail'),
    path('appointments/<int:pk>/reschedule/', views.reschedule_appointment, name='patient_appointment_reschedule'),
    path('appointments/<int:pk>/cancel/', views.cancel_appointment, name='patient_appointment_cancel'),
    
    # Documents
    path('documents/', views.PatientDocumentListView.as_view(), name='patient_documents'),
    path('documents/upload/', views.PatientDocumentUploadView.as_view(), name='patient_document_upload'),
    path('documents/<int:pk>/download/', views.download_document, name='patient_document_download'),
    
    # Messages
    path('messages/', views.PatientMessageListView.as_view(), name='patient_messages'),
    path('messages/send/', views.PatientMessageCreateView.as_view(), name='patient_message_create'),
    path('messages/<int:pk>/', views.PatientMessageDetailView.as_view(), name='patient_message_detail'),
    
    # Billing
    path('billing/', views.PatientBillingListView.as_view(), name='patient_billing'),
    path('billing/<int:pk>/', views.PatientBillingDetailView.as_view(), name='patient_billing_detail'),
    
    # Feedback
    path('feedback/', views.PatientFeedbackListView.as_view(), name='patient_feedback'),
    path('feedback/submit/', views.PatientFeedbackCreateView.as_view(), name='patient_feedback_create'),
    
    # Profile
    path('profile/', views.PatientProfileView.as_view(), name='patient_profile'),
    
    # Notifications
    path('notifications/', views.PatientNotificationListView.as_view(), name='patient_notifications'),
    path('notifications/<int:pk>/read/', views.mark_notification_read, name='patient_notification_read'),
    path('notifications/read-all/', views.mark_all_notifications_read, name='patient_notifications_read_all'),
    
    # AJAX endpoints
    path('ajax/appointment-slots/', views.get_appointment_slots, name='patient_appointment_slots'),
    
    # Search
    path('search/', views.patient_portal_search, name='patient_portal_search'),
] 