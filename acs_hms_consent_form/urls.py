from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.consent_form_dashboard, name='consent_form_dashboard'),
    
    # Templates
    path('templates/', views.ConsentFormTemplateListView.as_view(), name='consent_template_list'),
    path('templates/create/', views.ConsentFormTemplateCreateView.as_view(), name='consent_template_create'),
    path('templates/<int:pk>/', views.ConsentFormTemplateDetailView.as_view(), name='consent_template_detail'),
    path('templates/<int:pk>/edit/', views.ConsentFormTemplateUpdateView.as_view(), name='consent_template_edit'),
    
    # Consent Forms
    path('forms/', views.ConsentFormListView.as_view(), name='consent_form_list'),
    path('forms/create/', views.ConsentFormCreateView.as_view(), name='consent_form_create'),
    path('forms/<int:pk>/', views.ConsentFormDetailView.as_view(), name='consent_form_detail'),
    path('forms/<int:pk>/sign/', views.consent_form_sign, name='consent_form_sign'),
    path('forms/<int:pk>/revoke/', views.consent_form_revoke, name='consent_form_revoke'),
    path('forms/<int:pk>/pdf/', views.consent_form_pdf, name='consent_form_pdf'),
    path('forms/<int:pk>/notify/', views.consent_form_send_notification, name='consent_form_notify'),
    
    # Bulk Actions
    path('forms/bulk-action/', views.consent_form_bulk_action, name='consent_form_bulk_action'),
    
    # Configuration
    path('configuration/', views.consent_form_configuration, name='consent_form_configuration'),
    
    # AJAX endpoints
    path('ajax/search/', views.consent_form_ajax_search, name='consent_form_ajax_search'),
    path('ajax/statistics/', views.consent_form_statistics_api, name='consent_form_statistics_api'),
] 