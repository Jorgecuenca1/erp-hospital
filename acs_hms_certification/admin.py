from django.contrib import admin
from .models import (
    CertificationBody, CertificationType, DoctorCertification,
    CertificationRenewal, ContinuingEducation, CertificationAudit,
    CertificationNotification, CertificationStatistics
)


@admin.register(CertificationBody)
class CertificationBodyAdmin(admin.ModelAdmin):
    list_display = ['name', 'acronym', 'country', 'is_accredited', 'is_active']
    list_filter = ['is_accredited', 'is_active', 'country']
    search_fields = ['name', 'acronym', 'country']


@admin.register(CertificationType)
class CertificationTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'certification_body', 'is_mandatory', 'is_active']
    list_filter = ['category', 'is_mandatory', 'is_active']
    search_fields = ['name', 'certification_body__name']


@admin.register(DoctorCertification)
class DoctorCertificationAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'certification_type', 'certificate_number', 'status', 'expiry_date']
    list_filter = ['status', 'certification_type__category', 'is_verified']
    search_fields = ['doctor__nombre', 'certificate_number']
    date_hierarchy = 'expiry_date'


@admin.register(CertificationRenewal)
class CertificationRenewalAdmin(admin.ModelAdmin):
    list_display = ['renewal_id', 'doctor_certification', 'renewal_date', 'status', 'is_paid']
    list_filter = ['status', 'is_paid']
    search_fields = ['renewal_id', 'doctor_certification__doctor__nombre']


@admin.register(ContinuingEducation)
class ContinuingEducationAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'title', 'education_type', 'credit_hours', 'is_completed']
    list_filter = ['education_type', 'is_completed']
    search_fields = ['doctor__nombre', 'title', 'provider']


@admin.register(CertificationAudit)
class CertificationAuditAdmin(admin.ModelAdmin):
    list_display = ['doctor_certification', 'action', 'user', 'timestamp']
    list_filter = ['action', 'timestamp']
    readonly_fields = ['timestamp']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(CertificationNotification)
class CertificationNotificationAdmin(admin.ModelAdmin):
    list_display = ['doctor_certification', 'notification_type', 'is_sent', 'sent_at']
    list_filter = ['notification_type', 'is_sent']
    readonly_fields = ['sent_at']


@admin.register(CertificationStatistics)
class CertificationStatisticsAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_certifications', 'active_certifications', 'expired_certifications']
    list_filter = ['date']
    readonly_fields = ['created_at']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False 