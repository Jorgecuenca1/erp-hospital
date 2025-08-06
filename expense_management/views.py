from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Avg
from .models import ExpenseCategory, ExpenseReport, ExpenseItem, ExpensePolicy, ExpenseApproval


@login_required
def expense_dashboard(request):
    """Expense management dashboard"""
    context = {
        'total_reports': ExpenseReport.objects.count(),
        'pending_approvals': ExpenseReport.objects.filter(status='submitted').count(),
        'approved_reports': ExpenseReport.objects.filter(status='approved').count(),
        'total_expenses': ExpenseItem.objects.aggregate(total=Sum('amount'))['total'] or 0,
        'recent_reports': ExpenseReport.objects.order_by('-created_at')[:5],
        'expense_by_category': ExpenseItem.objects.values('category__name').annotate(total=Sum('amount'))[:5],
        'avg_report_amount': ExpenseReport.objects.aggregate(avg=Avg('total_amount'))['avg'] or 0
    }
    return render(request, 'expense_management/dashboard.html', context)


@login_required
def expense_reports(request):
    """Expense reports view"""
    reports = ExpenseReport.objects.all().order_by('-created_at')
    return render(request, 'expense_management/reports.html', {'reports': reports})


@login_required
def expense_categories(request):
    """Expense categories management"""
    categories = ExpenseCategory.objects.filter(is_active=True).order_by('name')
    return render(request, 'expense_management/categories.html', {'categories': categories})


@login_required
def expense_policies(request):
    """Expense policies management"""
    policies = ExpensePolicy.objects.filter(is_active=True).order_by('name')
    return render(request, 'expense_management/policies.html', {'policies': policies}) 