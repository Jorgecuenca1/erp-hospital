from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.urls import reverse_lazy
from django.db.models import Q, Sum, Count, Avg
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.db import transaction
from decimal import Decimal

from .models import (
    WaitingScreen, WaitingQueue, ScreenAnnouncement, HealthTip, ScreenConfiguration
)
from .forms import (
    WaitingScreenForm, WaitingQueueForm, ScreenAnnouncementForm,
    HealthTipForm, ScreenConfigurationForm, WaitingScreenSearchForm
)

class WaitingScreenDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'waiting_screen/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Dashboard statistics
        context['total_screens'] = WaitingScreen.objects.count()
        context['active_screens'] = WaitingScreen.objects.filter(is_active=True).count()
        context['total_queues'] = WaitingQueue.objects.count()
        context['waiting_patients'] = WaitingQueue.objects.filter(status='waiting').count()
        context['total_announcements'] = ScreenAnnouncement.objects.count()
        context['active_announcements'] = ScreenAnnouncement.objects.filter(is_active=True).count()
        context['total_health_tips'] = HealthTip.objects.count()
        context['active_health_tips'] = HealthTip.objects.filter(is_active=True).count()
        
        # Recent activities
        context['recent_queues'] = WaitingQueue.objects.order_by('-created_at')[:5]
        context['recent_announcements'] = ScreenAnnouncement.objects.order_by('-created_at')[:5]
        context['recent_health_tips'] = HealthTip.objects.order_by('-created_at')[:5]
        
        # Queue statistics
        context['queue_stats'] = WaitingQueue.objects.values('status').annotate(
            count=Count('id')
        )
        
        # Current waiting times
        context['avg_wait_time'] = WaitingQueue.objects.filter(
            status='waiting'
        ).aggregate(avg_wait=Avg('estimated_wait_minutes'))['avg_wait'] or 0
        
        return context

# Waiting Screen Views
class WaitingScreenListView(LoginRequiredMixin, ListView):
    model = WaitingScreen
    template_name = 'waiting_screen/screen_list.html'
    context_object_name = 'screens'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = WaitingScreen.objects.all()
        
        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(location__icontains=search) |
                Q(screen_type__icontains=search)
            )
        
        # Filter by status
        is_active = self.request.GET.get('is_active')
        if is_active:
            queryset = queryset.filter(is_active=True)
        
        return queryset.order_by('name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = WaitingScreenSearchForm(self.request.GET)
        return context

class WaitingScreenDetailView(LoginRequiredMixin, DetailView):
    model = WaitingScreen
    template_name = 'waiting_screen/screen_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['queue_data'] = WaitingQueue.objects.filter(screen=self.object)
        context['announcements'] = ScreenAnnouncement.objects.filter(
            screens=self.object, is_active=True
        )
        return context

class WaitingScreenCreateView(LoginRequiredMixin, CreateView):
    model = WaitingScreen
    form_class = WaitingScreenForm
    template_name = 'waiting_screen/screen_form.html'
    success_url = reverse_lazy('waiting_screen:screen_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Waiting screen created successfully.')
        return super().form_valid(form)

class WaitingScreenUpdateView(LoginRequiredMixin, UpdateView):
    model = WaitingScreen
    form_class = WaitingScreenForm
    template_name = 'waiting_screen/screen_form.html'
    
    def get_success_url(self):
        return reverse_lazy('waiting_screen:screen_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Waiting screen updated successfully.')
        return super().form_valid(form)

class WaitingScreenDeleteView(LoginRequiredMixin, DeleteView):
    model = WaitingScreen
    template_name = 'waiting_screen/screen_confirm_delete.html'
    success_url = reverse_lazy('waiting_screen:screen_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Waiting screen deleted successfully.')
        return super().delete(request, *args, **kwargs)

# Waiting Queue Views
class WaitingQueueListView(LoginRequiredMixin, ListView):
    model = WaitingQueue
    template_name = 'waiting_screen/queue_list.html'
    context_object_name = 'queues'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = WaitingQueue.objects.select_related('patient', 'doctor', 'screen')
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by screen
        screen_id = self.request.GET.get('screen')
        if screen_id:
            queryset = queryset.filter(screen_id=screen_id)
            
        return queryset.order_by('arrival_time')

class WaitingQueueDetailView(LoginRequiredMixin, DetailView):
    model = WaitingQueue
    template_name = 'waiting_screen/queue_detail.html'

class WaitingQueueCreateView(LoginRequiredMixin, CreateView):
    model = WaitingQueue
    form_class = WaitingQueueForm
    template_name = 'waiting_screen/queue_form.html'
    success_url = reverse_lazy('waiting_screen:queue_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Queue entry created successfully.')
        return super().form_valid(form)

class WaitingQueueUpdateView(LoginRequiredMixin, UpdateView):
    model = WaitingQueue
    form_class = WaitingQueueForm
    template_name = 'waiting_screen/queue_form.html'
    
    def get_success_url(self):
        return reverse_lazy('waiting_screen:queue_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Queue entry updated successfully.')
        return super().form_valid(form)

# Screen Announcement Views
class ScreenAnnouncementListView(LoginRequiredMixin, ListView):
    model = ScreenAnnouncement
    template_name = 'waiting_screen/announcement_list.html'
    context_object_name = 'announcements'
    paginate_by = 20
    
    def get_queryset(self):
        return ScreenAnnouncement.objects.order_by('-priority', '-created_at')

class ScreenAnnouncementDetailView(LoginRequiredMixin, DetailView):
    model = ScreenAnnouncement
    template_name = 'waiting_screen/announcement_detail.html'

class ScreenAnnouncementCreateView(LoginRequiredMixin, CreateView):
    model = ScreenAnnouncement
    form_class = ScreenAnnouncementForm
    template_name = 'waiting_screen/announcement_form.html'
    success_url = reverse_lazy('waiting_screen:announcement_list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Announcement created successfully.')
        return super().form_valid(form)

class ScreenAnnouncementUpdateView(LoginRequiredMixin, UpdateView):
    model = ScreenAnnouncement
    form_class = ScreenAnnouncementForm
    template_name = 'waiting_screen/announcement_form.html'
    
    def get_success_url(self):
        return reverse_lazy('waiting_screen:announcement_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Announcement updated successfully.')
        return super().form_valid(form)

# Health Tips Views
class HealthTipListView(LoginRequiredMixin, ListView):
    model = HealthTip
    template_name = 'waiting_screen/health_tip_list.html'
    context_object_name = 'health_tips'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = HealthTip.objects.all()
        
        # Filter by category
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
            
        return queryset.order_by('-created_at')

class HealthTipDetailView(LoginRequiredMixin, DetailView):
    model = HealthTip
    template_name = 'waiting_screen/health_tip_detail.html'

class HealthTipCreateView(LoginRequiredMixin, CreateView):
    model = HealthTip
    form_class = HealthTipForm
    template_name = 'waiting_screen/health_tip_form.html'
    success_url = reverse_lazy('waiting_screen:health_tip_list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Health tip created successfully.')
        return super().form_valid(form)

class HealthTipUpdateView(LoginRequiredMixin, UpdateView):
    model = HealthTip
    form_class = HealthTipForm
    template_name = 'waiting_screen/health_tip_form.html'
    
    def get_success_url(self):
        return reverse_lazy('waiting_screen:health_tip_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Health tip updated successfully.')
        return super().form_valid(form)

# Configuration Views
class ScreenConfigurationView(LoginRequiredMixin, UpdateView):
    model = ScreenConfiguration
    form_class = ScreenConfigurationForm
    template_name = 'waiting_screen/configuration.html'
    success_url = reverse_lazy('waiting_screen:configuration')
    
    def get_object(self):
        config, created = ScreenConfiguration.objects.get_or_create(
            defaults={'updated_by': self.request.user}
        )
        return config
    
    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        messages.success(self.request, 'Screen configuration updated successfully.')
        return super().form_valid(form)

# AJAX Views
@login_required
def get_queue_status(request):
    """Get current queue status"""
    screen_id = request.GET.get('screen_id')
    
    if screen_id:
        queues = WaitingQueue.objects.filter(
            screen_id=screen_id,
            status='waiting'
        ).order_by('arrival_time')
    else:
        queues = WaitingQueue.objects.filter(
            status='waiting'
        ).order_by('arrival_time')
    
    queue_data = []
    for queue in queues:
        queue_data.append({
            'id': queue.id,
            'queue_number': queue.queue_number,
            'patient_name': queue.patient.first_name + ' ' + queue.patient.last_name,
            'doctor_name': queue.doctor.user.get_full_name(),
            'wait_time': queue.wait_time_minutes,
            'estimated_wait': queue.estimated_wait_minutes,
            'status': queue.status,
        })
    
    return JsonResponse({'queues': queue_data})

@login_required
def update_queue_status(request):
    """Update queue status"""
    if request.method == 'POST':
        queue_id = request.POST.get('queue_id')
        new_status = request.POST.get('status')
        
        try:
            queue = WaitingQueue.objects.get(id=queue_id)
            queue.status = new_status
            
            if new_status == 'called':
                queue.called_time = timezone.now()
            elif new_status == 'in_progress':
                queue.start_time = timezone.now()
            elif new_status == 'completed':
                queue.end_time = timezone.now()
            
            queue.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Queue status updated successfully'
            })
        except WaitingQueue.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Queue not found'
            }, status=404)
    
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

@login_required
def get_announcements(request):
    """Get active announcements"""
    screen_id = request.GET.get('screen_id')
    
    if screen_id:
        announcements = ScreenAnnouncement.objects.filter(
            screens__id=screen_id,
            is_active=True
        )
    else:
        announcements = ScreenAnnouncement.objects.filter(is_active=True)
    
    announcement_data = []
    for announcement in announcements:
        announcement_data.append({
            'id': announcement.id,
            'title': announcement.title,
            'content': announcement.content,
            'type': announcement.announcement_type,
            'priority': announcement.priority,
        })
    
    return JsonResponse({'announcements': announcement_data})

@login_required
def get_health_tips(request):
    """Get random health tips"""
    tips = HealthTip.objects.filter(is_active=True).order_by('?')[:5]
    
    tip_data = []
    for tip in tips:
        tip_data.append({
            'id': tip.id,
            'title': tip.title,
            'content': tip.content,
            'category': tip.category,
        })
    
    return JsonResponse({'health_tips': tip_data})

@login_required
def export_queue_data(request):
    """Export queue data to CSV"""
    import csv
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="queue_data.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Queue Number', 'Patient', 'Doctor', 'Status', 'Arrival Time', 'Wait Time (min)'])
    
    queues = WaitingQueue.objects.select_related('patient', 'doctor', 'doctor__user').all()
    for queue in queues:
        writer.writerow([
            queue.queue_number,
            queue.patient.first_name + ' ' + queue.patient.last_name,
            queue.doctor.user.get_full_name(),
            queue.status,
            queue.arrival_time,
            queue.wait_time_minutes
        ])
    
    return response 