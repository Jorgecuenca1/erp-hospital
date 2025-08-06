from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q, Avg, Sum
from django.utils import timezone
from datetime import datetime, timedelta
from .models import QualityStandard, QualityAudit, QualityMetric, IncidentReport, QualityImprovement


@login_required
def quality_dashboard(request):
    """Quality control dashboard view"""
    today = timezone.now().date()
    
    # Calculate compliance rates
    total_metrics = QualityMetric.objects.count()
    compliant_metrics = QualityMetric.objects.filter(is_compliant=True).count()
    compliance_rate = (compliant_metrics / total_metrics * 100) if total_metrics > 0 else 0
    
    context = {
        'total_standards': QualityStandard.objects.filter(is_active=True).count(),
        'total_audits': QualityAudit.objects.count(),
        'compliance_rate': compliance_rate,
        'open_incidents': IncidentReport.objects.filter(status__in=['reported', 'investigating']).count(),
        'critical_incidents': IncidentReport.objects.filter(severity='critical', status__in=['reported', 'investigating']).count(),
        'active_improvements': QualityImprovement.objects.filter(status='in_progress').count(),
        'recent_incidents': IncidentReport.objects.order_by('-incident_date')[:5],
        'recent_audits': QualityAudit.objects.order_by('-audit_date')[:5],
        'compliance_by_category': QualityMetric.objects.select_related('standard').values('standard__category').annotate(
            total=Count('id'),
            compliant=Count('id', filter=Q(is_compliant=True))
        ),
        'incidents_by_type': IncidentReport.objects.values('incident_type').annotate(count=Count('id'))[:5],
        'avg_audit_score': QualityAudit.objects.aggregate(avg_score=Avg('compliance_score'))['avg_score'] or 0
    }
    return render(request, 'quality_control/dashboard.html', context)


@login_required
def quality_standards(request):
    """Quality standards management"""
    standards = QualityStandard.objects.filter(is_active=True).order_by('category')
    return render(request, 'quality_control/standards.html', {'standards': standards})


@login_required
def quality_audits(request):
    """Quality audits management"""
    audits = QualityAudit.objects.all().order_by('-audit_date')
    return render(request, 'quality_control/audits.html', {'audits': audits})


@login_required
def quality_metrics(request):
    """Quality metrics tracking"""
    metrics = QualityMetric.objects.select_related('standard').order_by('-measurement_date')
    return render(request, 'quality_control/metrics.html', {'metrics': metrics})


@login_required
def incident_reports(request):
    """Incident reports management"""
    incidents = IncidentReport.objects.all().order_by('-incident_date')
    return render(request, 'quality_control/incidents.html', {'incidents': incidents})


@login_required
def quality_improvements(request):
    """Quality improvement initiatives"""
    improvements = QualityImprovement.objects.all().order_by('-start_date')
    return render(request, 'quality_control/improvements.html', {'improvements': improvements})


@login_required
def compliance_report(request):
    """Compliance reporting"""
    compliance_data = {
        'overall_compliance': 0,
        'category_compliance': {},
        'trend_data': []
    }
    
    # Calculate overall compliance
    total_metrics = QualityMetric.objects.count()
    compliant_metrics = QualityMetric.objects.filter(is_compliant=True).count()
    if total_metrics > 0:
        compliance_data['overall_compliance'] = (compliant_metrics / total_metrics * 100)
    
    # Category compliance
    categories = QualityStandard.objects.values_list('category', flat=True).distinct()
    for category in categories:
        category_metrics = QualityMetric.objects.filter(standard__category=category)
        category_compliant = category_metrics.filter(is_compliant=True).count()
        category_total = category_metrics.count()
        if category_total > 0:
            compliance_data['category_compliance'][category] = (category_compliant / category_total * 100)
    
    return render(request, 'quality_control/compliance_report.html', {'compliance_data': compliance_data}) 