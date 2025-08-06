from django.contrib import admin
from .models import ResourceType, ResourceAllocation, StaffSchedule, CapacityPlanning


@admin.register(ResourceType)
class ResourceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'unit', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')


@admin.register(ResourceAllocation)
class ResourceAllocationAdmin(admin.ModelAdmin):
    list_display = ('resource_type', 'department', 'planned_quantity', 'allocated_quantity', 'status', 'priority')
    list_filter = ('status', 'priority', 'department')
    search_fields = ('resource_type__name', 'department')


@admin.register(StaffSchedule)
class StaffScheduleAdmin(admin.ModelAdmin):
    list_display = ('staff_member', 'department', 'shift_type', 'start_datetime', 'end_datetime', 'status')
    list_filter = ('shift_type', 'status', 'department')
    search_fields = ('staff_member__username', 'department', 'role')


@admin.register(CapacityPlanning)
class CapacityPlanningAdmin(admin.ModelAdmin):
    list_display = ('department', 'resource_type', 'planning_period', 'current_capacity', 'planned_capacity', 'utilization_rate')
    list_filter = ('planning_period', 'department')
    search_fields = ('department', 'resource_type__name') 