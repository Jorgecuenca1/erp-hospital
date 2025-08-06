from django.contrib import admin
from .models import QualityStandard, QualityAudit, QualityMetric, IncidentReport, QualityImprovement


@admin.register(QualityStandard)
class QualityStandardAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'target_value', 'unit', 'frequency', 'is_active')
    list_filter = ('category', 'frequency', 'is_active')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(QualityAudit)
class QualityAuditAdmin(admin.ModelAdmin):
    list_display = ('audit_type', 'department', 'auditor', 'audit_date', 'compliance_score', 'status')
    list_filter = ('audit_type', 'status', 'department')
    search_fields = ('department', 'scope')
    readonly_fields = ('created_at',)


@admin.register(QualityMetric)
class QualityMetricAdmin(admin.ModelAdmin):
    list_display = ('standard', 'measurement_date', 'actual_value', 'variance', 'is_compliant')
    list_filter = ('is_compliant', 'standard__category')
    search_fields = ('standard__name',)
    readonly_fields = ('variance', 'is_compliant', 'created_at')


@admin.register(IncidentReport)
class IncidentReportAdmin(admin.ModelAdmin):
    list_display = ('incident_type', 'severity', 'department', 'reporter', 'incident_date', 'status')
    list_filter = ('incident_type', 'severity', 'status', 'department')
    search_fields = ('description', 'department')
    readonly_fields = ('created_at',)


@admin.register(QualityImprovement)
class QualityImprovementAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'responsible_person', 'start_date', 'target_completion', 'status')
    list_filter = ('status', 'department')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at',) 