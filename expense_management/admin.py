from django.contrib import admin
from .models import ExpenseCategory, ExpenseReport, ExpenseItem, ExpensePolicy, ExpenseApproval


@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'parent', 'is_active')
    list_filter = ('is_active', 'parent')
    search_fields = ('name', 'code', 'description')


@admin.register(ExpenseReport)
class ExpenseReportAdmin(admin.ModelAdmin):
    list_display = ('report_number', 'employee', 'title', 'total_amount', 'status', 'submit_date')
    list_filter = ('status', 'submit_date', 'currency')
    search_fields = ('report_number', 'employee__username', 'title')
    readonly_fields = ('created_at',)


@admin.register(ExpenseItem)
class ExpenseItemAdmin(admin.ModelAdmin):
    list_display = ('report', 'category', 'description', 'amount', 'expense_date', 'payment_method')
    list_filter = ('category', 'payment_method', 'is_billable')
    search_fields = ('description', 'vendor', 'receipt_number')


@admin.register(ExpensePolicy)
class ExpensePolicyAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'daily_limit', 'monthly_limit', 'requires_receipt', 'is_active')
    list_filter = ('requires_receipt', 'requires_approval', 'is_active')
    search_fields = ('name', 'description')


@admin.register(ExpenseApproval)
class ExpenseApprovalAdmin(admin.ModelAdmin):
    list_display = ('report', 'approver', 'approval_level', 'status', 'approved_amount', 'approval_date')
    list_filter = ('status', 'approval_level')
    search_fields = ('report__report_number', 'approver__username') 