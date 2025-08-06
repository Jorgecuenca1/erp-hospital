from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, 
    TemplateView, FormView
)
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.db.models import Q, Count, Avg, Sum
from django.utils import timezone
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
import json
import csv
from datetime import datetime, timedelta
from decimal import Decimal

from .models import (
    RadiologyModality, RadiologyExam, RadiologyOrder, RadiologyStudy,
    RadiologyImage, RadiologyReport, RadiologyProtocol, RadiologySettings
)

class RadiologyDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'radiology/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Dashboard statistics
        context['total_modalities'] = RadiologyModality.objects.count()
        context['active_modalities'] = RadiologyModality.objects.filter(is_active=True).count()
        context['total_exams'] = RadiologyExam.objects.count()
        context['active_exams'] = RadiologyExam.objects.filter(is_active=True).count()
        context['total_orders'] = RadiologyOrder.objects.count()
        context['pending_orders'] = RadiologyOrder.objects.filter(status='ordered').count()
        context['total_studies'] = RadiologyStudy.objects.count()
        context['completed_studies'] = RadiologyStudy.objects.filter(status='completed').count()
        context['total_reports'] = RadiologyReport.objects.count()
        context['pending_reports'] = RadiologyReport.objects.filter(status='pending').count()
        
        # Recent activities
        context['recent_orders'] = RadiologyOrder.objects.order_by('-ordered_date')[:5]
        context['recent_studies'] = RadiologyStudy.objects.order_by('-study_date')[:5]
        context['recent_reports'] = RadiologyReport.objects.order_by('-created_at')[:5]
        
        # Today's schedule
        today = timezone.now().date()
        context['todays_studies'] = RadiologyStudy.objects.filter(study_date__date=today)
        context['todays_orders'] = RadiologyOrder.objects.filter(ordered_date__date=today)
        
        return context

# Radiology Modality Views
class RadiologyModalityListView(LoginRequiredMixin, ListView):
    model = RadiologyModality
    template_name = 'radiology/modality_list.html'
    context_object_name = 'modalities'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = RadiologyModality.objects.all()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(modality_code__icontains=search)
            )
        return queryset.order_by('modality_code')

class RadiologyModalityDetailView(LoginRequiredMixin, DetailView):
    model = RadiologyModality
    template_name = 'radiology/modality_detail.html'

# Radiology Exam Views
class RadiologyExamListView(LoginRequiredMixin, ListView):
    model = RadiologyExam
    template_name = 'radiology/exam_list.html'
    context_object_name = 'exams'
    paginate_by = 20
    
    def get_queryset(self):
        return RadiologyExam.objects.select_related('modality').order_by('exam_name')

class RadiologyExamDetailView(LoginRequiredMixin, DetailView):
    model = RadiologyExam
    template_name = 'radiology/exam_detail.html'

# Radiology Order Views
class RadiologyOrderListView(LoginRequiredMixin, ListView):
    model = RadiologyOrder
    template_name = 'radiology/order_list.html'
    context_object_name = 'orders'
    paginate_by = 20
    
    def get_queryset(self):
        return RadiologyOrder.objects.select_related('patient', 'exam', 'ordering_physician').order_by('-ordered_date')

class RadiologyOrderDetailView(LoginRequiredMixin, DetailView):
    model = RadiologyOrder
    template_name = 'radiology/order_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['study'] = self.object.study
        except RadiologyStudy.DoesNotExist:
            context['study'] = None
        return context

# Radiology Study Views
class RadiologyStudyListView(LoginRequiredMixin, ListView):
    model = RadiologyStudy
    template_name = 'radiology/study_list.html'
    context_object_name = 'studies'
    paginate_by = 20
    
    def get_queryset(self):
        return RadiologyStudy.objects.select_related('order', 'order__patient', 'technologist', 'modality').order_by('-study_date')

class RadiologyStudyDetailView(LoginRequiredMixin, DetailView):
    model = RadiologyStudy
    template_name = 'radiology/study_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = RadiologyImage.objects.filter(study=self.object)
        try:
            context['report'] = self.object.report
        except RadiologyReport.DoesNotExist:
            context['report'] = None
        return context

# Radiology Image Views
class RadiologyImageListView(LoginRequiredMixin, ListView):
    model = RadiologyImage
    template_name = 'radiology/image_list.html'
    context_object_name = 'images'
    paginate_by = 20
    
    def get_queryset(self):
        return RadiologyImage.objects.select_related('study', 'study__order__patient').order_by('-created_at')

class RadiologyImageDetailView(LoginRequiredMixin, DetailView):
    model = RadiologyImage
    template_name = 'radiology/image_detail.html'

# Radiology Report Views
class RadiologyReportListView(LoginRequiredMixin, ListView):
    model = RadiologyReport
    template_name = 'radiology/report_list.html'
    context_object_name = 'reports'
    paginate_by = 20
    
    def get_queryset(self):
        return RadiologyReport.objects.select_related('study', 'study__order__patient', 'radiologist').order_by('-created_at')

class RadiologyReportDetailView(LoginRequiredMixin, DetailView):
    model = RadiologyReport
    template_name = 'radiology/report_detail.html'

# Radiology Protocol Views
class RadiologyProtocolListView(LoginRequiredMixin, ListView):
    model = RadiologyProtocol
    template_name = 'radiology/protocol_list.html'
    context_object_name = 'protocols'
    paginate_by = 20
    
    def get_queryset(self):
        return RadiologyProtocol.objects.select_related('exam').order_by('name')

class RadiologyProtocolDetailView(LoginRequiredMixin, DetailView):
    model = RadiologyProtocol
    template_name = 'radiology/protocol_detail.html'

# Export Views
@login_required
def export_radiology_data(request):
    """Export radiology data to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="radiology_data.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Patient', 'Exam', 'Date', 'Status', 'Technologist'])
    
    orders = RadiologyOrder.objects.select_related('patient', 'exam')
    for order in orders:
        writer.writerow([
            f"{order.patient.first_name} {order.patient.last_name}",
            order.exam.exam_name,
            order.ordered_date.strftime('%Y-%m-%d'),
            order.status,
            ''  # Technologist would be from study
        ])
    
    return response

# AJAX Views
@login_required
def get_patient_radiology_history(request):
    """Get patient's radiology history for AJAX requests"""
    patient_id = request.GET.get('patient_id')
    if not patient_id:
        return JsonResponse({'error': 'Patient ID required'}, status=400)
    
    orders = RadiologyOrder.objects.filter(patient_id=patient_id).order_by('-ordered_date')
    data = []
    for order in orders:
        data.append({
            'id': order.id,
            'exam': order.exam.exam_name,
            'date': order.ordered_date.strftime('%Y-%m-%d'),
            'status': order.status,
        })
    
    return JsonResponse({'orders': data})

@login_required
def update_order_status(request):
    """Update order status via AJAX"""
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        status = request.POST.get('status')
        
        if not order_id or not status:
            return JsonResponse({'error': 'Order ID and status required'}, status=400)
        
        try:
            order = RadiologyOrder.objects.get(id=order_id)
            order.status = status
            if status == 'scheduled':
                order.scheduled_date = timezone.now()
            order.save()
            
            return JsonResponse({'success': True, 'message': 'Order status updated successfully'})
        except RadiologyOrder.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400) 