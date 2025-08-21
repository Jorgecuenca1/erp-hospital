"""
URL configuration for HMetaHIS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from HMetaHIS.views import LandingPageView, AdminDashboardView, module_status_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name='landing_page'),
    path('dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('api/module-status/', module_status_api, name='module_status_api'),
    
    # ========== ORIGINAL HOSPITAL MODULES ==========
    path('patients/', include('patients.urls')),
    path('professionals/', include('professionals.urls')),
    path('appointments/', include('appointments.urls')),
    path('medical_records/', include('medical_records.urls')),
    path('inventories/', include('inventories.urls')),
    path('billing/', include('billing.urls')),
    path('laboratories/', include('laboratories.urls')),
    path('reports/', include('reports.urls')),
    path('hr/', include('hr.urls')),
    path('pharmacy/', include('pharmacy.urls')),
    path('hospital_profile/', include('hospital_profile.urls')),
    path('asset_management/', include('asset_management.urls')),
    path('quality_management/', include('quality_management.urls')),
    path('accounting/', include('accounting.urls')),
    path('website/', include('website.urls')),
    path('ecommerce/', include('ecommerce.urls')),
    path('blog/', include('blog.urls')),
    path('forum/', include('forum.urls')),
    path('elearning/', include('elearning.urls')),
    path('livechat/', include('livechat.urls')),
    path('subscriptions/', include('subscriptions.urls')),
    path('crm/', include('crm.urls')),
    path('sales/', include('sales.urls')),
    path('purchases/', include('purchases.urls')),
    path('pos/', include('pos.urls')),
    
    # ========== HMS CORE MODULES ==========
    # Base and Foundation
    path('hms/', include('acs_hms_base.urls')),
    
    # ========== ADMISSION AND RECEPTION ==========
    path('admision/', include('admision_recepcion.urls')),
    
    # Medical Specialties
    path('hms/gynecology/', include('acs_hms_gynec.urls')),
    path('hms/ophthalmology/', include('acs_hms_ophthalmology.urls')),
    path('hms/pediatrics/', include('acs_hms_paediatric.urls')),
    path('hms/aesthetic/', include('acs_hms_aesthetic.urls')),
    path('hms/dental/', include('acs_hms_dental.urls')),
    
    # Surgery and Operations
    path('hms/surgery/', include('acs_hms_surgery.urls')),
    path('hms/operation-theater/', include('acs_hms_operation_theater.urls')),
    
    # Laboratory and Diagnostics
    path('hms/laboratory/', include('acs_hms_laboratory.urls')),
    path('hms/radiology/', include('acs_hms_radiology.urls')),
    
    # Emergency and Critical Care
    path('hms/emergency/', include('acs_hms_emergency.urls')),
    path('hms/nursing/', include('acs_hms_nursing.urls')),
    
    # Blood Bank Management
    path('hms/blood-bank/', include('acs_hms_blood_bank.urls')),
    
    # Patient Services
    path('hms/hospitalization/', include('acs_hms_hospitalization.urls')),
    path('hms/patient-portal/', include('acs_hms_patient_portal.urls')),
    
    # Pharmacy and Medications
    path('hms/pharmacy/', include('acs_hms_pharmacy.urls')),
    
    # Digital Health
    path('hms/online-appointment/', include('acs_hms_online_appointment.urls')),
    path('hms/webcam/', include('acs_hms_webcam.urls')),
    path('hms/video-call/', include('acs_hms_video_call.urls')),
    path('hms/consent-form/', include('acs_hms_consent_form.urls')),
    
    # Business and Administration
    path('hms/subscription/', include('acs_hms_subscription.urls')),
    path('hms/insurance/', include('acs_hms_insurance.urls')),
    path('hms/commission/', include('acs_hms_commission.urls')),
    path('hms/certification/', include('acs_hms_certification.urls')),
    
    # User Experience
    path('hms/waiting-screen/', include('acs_hms_waiting_screen.urls')),
    
    # ========== NEW MODULES FOR 100% PARITY ==========
    path('manufacturing/', include('manufacturing.urls')),
    path('maintenance/', include('maintenance.urls')),
    path('quality-control/', include('quality_control.urls')),
    path('planning/', include('planning.urls')),
    path('expenses/', include('expense_management.urls')),
    path('rental/', include('rental_management.urls')),
    path('esg/', include('esg_reporting.urls')),
    path('carbon/', include('carbon_footprint.urls')),
    path('social/', include('social_metrics.urls')),
]
