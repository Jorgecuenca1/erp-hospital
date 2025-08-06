from django.contrib import admin
from .models import ESGReport, EnvironmentalMetric, SocialMetric, GovernanceMetric, ESGGoal


@admin.register(ESGReport)
class ESGReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'report_type', 'period', 'start_date', 'end_date', 'overall_esg_score', 'is_published', 'created_at']
    list_filter = ['report_type', 'period', 'is_published', 'created_at']
    search_fields = ['title', 'executive_summary']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'report_type', 'period', 'start_date', 'end_date')
        }),
        ('ESG Scores', {
            'fields': ('environmental_score', 'social_score', 'governance_score', 'overall_esg_score')
        }),
        ('Content', {
            'fields': ('executive_summary',)
        }),
        ('Publishing', {
            'fields': ('is_published',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


class EnvironmentalMetricInline(admin.TabularInline):
    model = EnvironmentalMetric
    extra = 1
    fields = ['metric_type', 'value', 'unit', 'target_value', 'beds_count', 'patient_days']


class SocialMetricInline(admin.TabularInline):
    model = SocialMetric
    extra = 1
    fields = ['metric_type', 'value', 'unit', 'target_value']


class GovernanceMetricInline(admin.TabularInline):
    model = GovernanceMetric
    extra = 1
    fields = ['metric_type', 'value', 'unit', 'target_value', 'certification_status']


@admin.register(EnvironmentalMetric)
class EnvironmentalMetricAdmin(admin.ModelAdmin):
    list_display = ['report', 'metric_type', 'value', 'unit', 'target_value', 'achievement_rate', 'created_at']
    list_filter = ['metric_type', 'report__report_type', 'created_at']
    search_fields = ['report__title', 'metric_type']
    date_hierarchy = 'created_at'
    
    def achievement_rate(self, obj):
        rate = obj.achievement_rate()
        if rate:
            return f"{rate:.1f}%"
        return "N/A"
    achievement_rate.short_description = 'Achievement Rate'


@admin.register(SocialMetric)
class SocialMetricAdmin(admin.ModelAdmin):
    list_display = ['report', 'metric_type', 'value', 'unit', 'target_value', 'created_at']
    list_filter = ['metric_type', 'report__report_type', 'created_at']
    search_fields = ['report__title', 'metric_type']
    date_hierarchy = 'created_at'


@admin.register(GovernanceMetric)
class GovernanceMetricAdmin(admin.ModelAdmin):
    list_display = ['report', 'metric_type', 'value', 'unit', 'target_value', 'certification_status', 'created_at']
    list_filter = ['metric_type', 'report__report_type', 'created_at']
    search_fields = ['report__title', 'metric_type', 'certification_status']
    date_hierarchy = 'created_at'


@admin.register(ESGGoal)
class ESGGoalAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'priority', 'progress_percentage', 'target_date', 'is_achieved', 'responsible_person']
    list_filter = ['category', 'priority', 'is_active', 'is_achieved', 'target_date']
    search_fields = ['title', 'description', 'responsible_person__username']
    date_hierarchy = 'target_date'
    readonly_fields = ['created_at', 'updated_at', 'progress_percentage', 'days_remaining']
    
    fieldsets = (
        ('Goal Information', {
            'fields': ('title', 'description', 'category', 'priority')
        }),
        ('Target & Progress', {
            'fields': ('target_value', 'current_value', 'unit', 'progress_percentage')
        }),
        ('Timeline', {
            'fields': ('start_date', 'target_date', 'days_remaining')
        }),
        ('Status', {
            'fields': ('is_active', 'is_achieved', 'achievement_date')
        }),
        ('Responsibility', {
            'fields': ('responsible_person', 'department')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def progress_percentage(self, obj):
        return f"{obj.progress_percentage():.1f}%"
    progress_percentage.short_description = 'Progress'
    
    def days_remaining(self, obj):
        days = obj.days_remaining()
        if days > 0:
            return f"{days} days"
        elif days == 0:
            return "Due today"
        else:
            return "Overdue"
    days_remaining.short_description = 'Days Remaining' 