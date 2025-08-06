from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Sum, Count, Q
from django.utils import timezone
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import ESGReport, EnvironmentalMetric, SocialMetric, GovernanceMetric, ESGGoal
from .forms import ESGReportForm, ESGGoalForm
import json
from datetime import datetime, timedelta


@login_required
def esg_dashboard(request):
    """ESG Dashboard with key metrics and charts"""
    
    # Get latest reports
    recent_reports = ESGReport.objects.filter(is_published=True)[:5]
    
    # Calculate average ESG scores
    avg_scores = ESGReport.objects.filter(is_published=True).aggregate(
        avg_environmental=Avg('environmental_score'),
        avg_social=Avg('social_score'),
        avg_governance=Avg('governance_score'),
        avg_overall=Avg('overall_esg_score')
    )
    
    # Active goals by category
    goals_by_category = ESGGoal.objects.filter(is_active=True).values('category').annotate(
        total=Count('id'),
        achieved=Count('id', filter=Q(is_achieved=True))
    )
    
    # Environmental metrics summary
    env_metrics = EnvironmentalMetric.objects.filter(
        report__is_published=True,
        created_at__gte=timezone.now() - timedelta(days=90)
    ).values('metric_type').annotate(
        avg_value=Avg('value'),
        total_count=Count('id')
    )
    
    # Goals progress
    active_goals = ESGGoal.objects.filter(is_active=True)[:10]
    
    context = {
        'recent_reports': recent_reports,
        'avg_scores': avg_scores,
        'goals_by_category': goals_by_category,
        'env_metrics': env_metrics,
        'active_goals': active_goals,
        'total_reports': ESGReport.objects.count(),
        'published_reports': ESGReport.objects.filter(is_published=True).count(),
        'active_goals_count': ESGGoal.objects.filter(is_active=True).count(),
    }
    
    return render(request, 'esg_reporting/dashboard.html', context)


@login_required
def esg_report_list(request):
    """List all ESG reports with filtering"""
    
    reports = ESGReport.objects.all()
    
    # Filtering
    report_type = request.GET.get('type')
    period = request.GET.get('period')
    year = request.GET.get('year')
    
    if report_type:
        reports = reports.filter(report_type=report_type)
    if period:
        reports = reports.filter(period=period)
    if year:
        reports = reports.filter(start_date__year=year)
    
    # Pagination
    paginator = Paginator(reports, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get available years for filter
    years = ESGReport.objects.dates('start_date', 'year', order='DESC')
    
    context = {
        'page_obj': page_obj,
        'report_types': ESGReport.REPORT_TYPES,
        'periods': ESGReport.REPORT_PERIODS,
        'years': years,
        'current_filters': {
            'type': report_type,
            'period': period,
            'year': year,
        }
    }
    
    return render(request, 'esg_reporting/report_list.html', context)


@login_required
def esg_report_detail(request, report_id):
    """Display detailed ESG report"""
    
    report = get_object_or_404(ESGReport, id=report_id)
    
    # Get all metrics for this report
    environmental_metrics = report.environmental_metrics.all()
    social_metrics = report.social_metrics.all()
    governance_metrics = report.governance_metrics.all()
    
    context = {
        'report': report,
        'environmental_metrics': environmental_metrics,
        'social_metrics': social_metrics,
        'governance_metrics': governance_metrics,
    }
    
    return render(request, 'esg_reporting/report_detail.html', context)


@login_required
def create_esg_report(request):
    """Create new ESG report"""
    
    if request.method == 'POST':
        form = ESGReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.created_by = request.user
            report.save()
            messages.success(request, 'ESG Report created successfully!')
            return redirect('esg_report_detail', report_id=report.id)
    else:
        form = ESGReportForm()
    
    context = {
        'form': form,
        'title': 'Create ESG Report'
    }
    
    return render(request, 'esg_reporting/report_form.html', context)


@login_required
def esg_goals_list(request):
    """List ESG goals with progress tracking"""
    
    goals = ESGGoal.objects.filter(is_active=True)
    
    # Filtering
    category = request.GET.get('category')
    priority = request.GET.get('priority')
    
    if category:
        goals = goals.filter(category=category)
    if priority:
        goals = goals.filter(priority=priority)
    
    # Pagination
    paginator = Paginator(goals, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    stats = {
        'total_goals': ESGGoal.objects.filter(is_active=True).count(),
        'achieved_goals': ESGGoal.objects.filter(is_active=True, is_achieved=True).count(),
        'overdue_goals': ESGGoal.objects.filter(
            is_active=True, 
            is_achieved=False, 
            target_date__lt=timezone.now().date()
        ).count(),
    }
    
    context = {
        'page_obj': page_obj,
        'categories': ESGGoal.GOAL_CATEGORIES,
        'priorities': ESGGoal.PRIORITY_LEVELS,
        'stats': stats,
        'current_filters': {
            'category': category,
            'priority': priority,
        }
    }
    
    return render(request, 'esg_reporting/goals_list.html', context)


@login_required
def create_esg_goal(request):
    """Create new ESG goal"""
    
    if request.method == 'POST':
        form = ESGGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.responsible_person = request.user
            goal.save()
            messages.success(request, 'ESG Goal created successfully!')
            return redirect('esg_goals_list')
    else:
        form = ESGGoalForm()
    
    context = {
        'form': form,
        'title': 'Create ESG Goal'
    }
    
    return render(request, 'esg_reporting/goal_form.html', context)


@login_required
def esg_analytics_api(request):
    """API endpoint for ESG analytics data"""
    
    # Environmental metrics trends
    env_trends = EnvironmentalMetric.objects.filter(
        created_at__gte=timezone.now() - timedelta(days=365)
    ).values('metric_type', 'created_at__month').annotate(
        avg_value=Avg('value')
    ).order_by('created_at__month')
    
    # ESG scores over time
    score_trends = ESGReport.objects.filter(
        is_published=True,
        created_at__gte=timezone.now() - timedelta(days=365)
    ).values('created_at__month').annotate(
        avg_environmental=Avg('environmental_score'),
        avg_social=Avg('social_score'),
        avg_governance=Avg('governance_score'),
        avg_overall=Avg('overall_esg_score')
    ).order_by('created_at__month')
    
    # Goals achievement rate by category
    goals_achievement = ESGGoal.objects.values('category').annotate(
        total=Count('id'),
        achieved=Count('id', filter=Q(is_achieved=True))
    )
    
    data = {
        'env_trends': list(env_trends),
        'score_trends': list(score_trends),
        'goals_achievement': list(goals_achievement),
        'generated_at': timezone.now().isoformat()
    }
    
    return JsonResponse(data)


@login_required
def sustainability_metrics(request):
    """Sustainability metrics overview"""
    
    # Latest environmental metrics
    latest_env_metrics = EnvironmentalMetric.objects.filter(
        created_at__gte=timezone.now() - timedelta(days=30)
    ).values('metric_type').annotate(
        latest_value=Avg('value'),
        total_measurements=Count('id')
    )
    
    # Carbon footprint calculation
    carbon_metrics = EnvironmentalMetric.objects.filter(
        metric_type='carbon_emissions',
        created_at__gte=timezone.now() - timedelta(days=365)
    ).aggregate(
        total_emissions=Sum('value'),
        avg_monthly=Avg('value')
    )
    
    # Energy efficiency
    energy_metrics = EnvironmentalMetric.objects.filter(
        metric_type='energy_consumption',
        created_at__gte=timezone.now() - timedelta(days=365)
    ).aggregate(
        total_consumption=Sum('value'),
        avg_monthly=Avg('value')
    )
    
    context = {
        'latest_env_metrics': latest_env_metrics,
        'carbon_metrics': carbon_metrics,
        'energy_metrics': energy_metrics,
    }
    
    return render(request, 'esg_reporting/sustainability_metrics.html', context) 