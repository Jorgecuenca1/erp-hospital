from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from .models import (
    PatientPortalUser, PatientAppointment, PatientDocument, 
    PatientMessage, PatientBilling, PatientFeedback, PatientNotification
)
from .forms import (
    PatientPortalUserRegistrationForm, PatientAppointmentForm,
    PatientDocumentForm, PatientMessageForm, PatientFeedbackForm,
    PatientProfileForm, AppointmentReschedulingForm
)


class PatientPortalMixin:
    """Mixin to ensure user has patient portal access"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        try:
            self.patient_user = PatientPortalUser.objects.get(user=request.user)
            if not self.patient_user.is_active:
                messages.error(request, "Your account is not active")
                return redirect('login')
        except PatientPortalUser.DoesNotExist:
            messages.error(request, "Access denied. Patient portal account required.")
            return redirect('login')
        
        return super().dispatch(request, *args, **kwargs)


def patient_portal_register(request):
    """Patient portal registration view"""
    if request.method == 'POST':
        form = PatientPortalUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! Welcome to the patient portal.")
            return redirect('patient_portal_dashboard')
    else:
        form = PatientPortalUserRegistrationForm()
    
    return render(request, 'patient_portal/register.html', {'form': form})


class PatientPortalDashboard(PatientPortalMixin, ListView):
    """Patient portal dashboard"""
    template_name = 'patient_portal/dashboard.html'
    context_object_name = 'recent_appointments'
    
    def get_queryset(self):
        return PatientAppointment.objects.filter(
            portal_user=self.patient_user
        ).order_by('-appointment_date')[:5]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient_user'] = self.patient_user
        context['unread_messages'] = PatientMessage.objects.filter(
            portal_user=self.patient_user,
            is_read=False
        ).count()
        context['pending_bills'] = PatientBilling.objects.filter(
            portal_user=self.patient_user,
            status='pending'
        ).count()
        context['unread_notifications'] = PatientNotification.objects.filter(
            portal_user=self.patient_user,
            is_read=False
        ).count()
        return context


class PatientAppointmentListView(PatientPortalMixin, ListView):
    """Patient appointments list"""
    model = PatientAppointment
    template_name = 'patient_portal/appointments.html'
    context_object_name = 'appointments'
    paginate_by = 10
    
    def get_queryset(self):
        return PatientAppointment.objects.filter(
            portal_user=self.patient_user
        ).order_by('-appointment_date')


class PatientAppointmentCreateView(PatientPortalMixin, CreateView):
    """Book new appointment"""
    model = PatientAppointment
    form_class = PatientAppointmentForm
    template_name = 'patient_portal/appointment_form.html'
    success_url = reverse_lazy('patient_appointments')
    
    def form_valid(self, form):
        form.instance.portal_user = self.patient_user
        messages.success(self.request, "Appointment booked successfully!")
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['patient_user'] = self.patient_user
        return kwargs


class PatientAppointmentDetailView(PatientPortalMixin, DetailView):
    """Appointment details"""
    model = PatientAppointment
    template_name = 'patient_portal/appointment_detail.html'
    context_object_name = 'appointment'
    
    def get_queryset(self):
        return PatientAppointment.objects.filter(portal_user=self.patient_user)


@login_required
def reschedule_appointment(request, pk):
    """Reschedule appointment"""
    try:
        patient_user = PatientPortalUser.objects.get(user=request.user)
        appointment = get_object_or_404(PatientAppointment, pk=pk, portal_user=patient_user)
    except PatientPortalUser.DoesNotExist:
        raise PermissionDenied("Access denied")
    
    if appointment.status not in ['scheduled', 'confirmed']:
        messages.error(request, "This appointment cannot be rescheduled")
        return redirect('patient_appointment_detail', pk=pk)
    
    if request.method == 'POST':
        form = AppointmentReschedulingForm(request.POST)
        if form.is_valid():
            appointment.appointment_date = form.cleaned_data['new_date']
            appointment.appointment_time = form.cleaned_data['new_time']
            appointment.status = 'scheduled'
            appointment.save()
            
            messages.success(request, "Appointment rescheduled successfully!")
            return redirect('patient_appointment_detail', pk=pk)
    else:
        form = AppointmentReschedulingForm()
    
    return render(request, 'patient_portal/reschedule_appointment.html', {
        'form': form,
        'appointment': appointment
    })


@login_required
def cancel_appointment(request, pk):
    """Cancel appointment"""
    try:
        patient_user = PatientPortalUser.objects.get(user=request.user)
        appointment = get_object_or_404(PatientAppointment, pk=pk, portal_user=patient_user)
    except PatientPortalUser.DoesNotExist:
        raise PermissionDenied("Access denied")
    
    if appointment.status not in ['scheduled', 'confirmed']:
        messages.error(request, "This appointment cannot be cancelled")
        return redirect('patient_appointment_detail', pk=pk)
    
    if request.method == 'POST':
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, "Appointment cancelled successfully!")
        return redirect('patient_appointments')
    
    return render(request, 'patient_portal/cancel_appointment.html', {
        'appointment': appointment
    })


class PatientDocumentListView(PatientPortalMixin, ListView):
    """Patient documents list"""
    model = PatientDocument
    template_name = 'patient_portal/documents.html'
    context_object_name = 'documents'
    paginate_by = 10
    
    def get_queryset(self):
        return PatientDocument.objects.filter(
            portal_user=self.patient_user,
            is_visible_to_patient=True
        ).order_by('-uploaded_at')


class PatientDocumentUploadView(PatientPortalMixin, CreateView):
    """Upload document"""
    model = PatientDocument
    form_class = PatientDocumentForm
    template_name = 'patient_portal/document_form.html'
    success_url = reverse_lazy('patient_documents')
    
    def form_valid(self, form):
        form.instance.portal_user = self.patient_user
        form.instance.uploaded_by = self.request.user
        messages.success(self.request, "Document uploaded successfully!")
        return super().form_valid(form)


class PatientMessageListView(PatientPortalMixin, ListView):
    """Patient messages list"""
    model = PatientMessage
    template_name = 'patient_portal/messages.html'
    context_object_name = 'messages'
    paginate_by = 10
    
    def get_queryset(self):
        return PatientMessage.objects.filter(
            portal_user=self.patient_user
        ).order_by('-created_at')


class PatientMessageCreateView(PatientPortalMixin, CreateView):
    """Send message"""
    model = PatientMessage
    form_class = PatientMessageForm
    template_name = 'patient_portal/message_form.html'
    success_url = reverse_lazy('patient_messages')
    
    def form_valid(self, form):
        form.instance.portal_user = self.patient_user
        messages.success(self.request, "Message sent successfully!")
        return super().form_valid(form)


class PatientMessageDetailView(PatientPortalMixin, DetailView):
    """Message details"""
    model = PatientMessage
    template_name = 'patient_portal/message_detail.html'
    context_object_name = 'message'
    
    def get_queryset(self):
        return PatientMessage.objects.filter(portal_user=self.patient_user)
    
    def get_object(self):
        message = super().get_object()
        # Mark as read
        if not message.is_read:
            message.is_read = True
            message.save()
        return message


class PatientBillingListView(PatientPortalMixin, ListView):
    """Patient billing list"""
    model = PatientBilling
    template_name = 'patient_portal/billing.html'
    context_object_name = 'bills'
    paginate_by = 10
    
    def get_queryset(self):
        return PatientBilling.objects.filter(
            portal_user=self.patient_user
        ).order_by('-created_at')


class PatientBillingDetailView(PatientPortalMixin, DetailView):
    """Billing details"""
    model = PatientBilling
    template_name = 'patient_portal/billing_detail.html'
    context_object_name = 'bill'
    
    def get_queryset(self):
        return PatientBilling.objects.filter(portal_user=self.patient_user)


class PatientFeedbackListView(PatientPortalMixin, ListView):
    """Patient feedback list"""
    model = PatientFeedback
    template_name = 'patient_portal/feedback.html'
    context_object_name = 'feedback_list'
    paginate_by = 10
    
    def get_queryset(self):
        return PatientFeedback.objects.filter(
            portal_user=self.patient_user
        ).order_by('-created_at')


class PatientFeedbackCreateView(PatientPortalMixin, CreateView):
    """Submit feedback"""
    model = PatientFeedback
    form_class = PatientFeedbackForm
    template_name = 'patient_portal/feedback_form.html'
    success_url = reverse_lazy('patient_feedback')
    
    def form_valid(self, form):
        form.instance.portal_user = self.patient_user
        messages.success(self.request, "Feedback submitted successfully!")
        return super().form_valid(form)


class PatientProfileView(PatientPortalMixin, UpdateView):
    """Patient profile"""
    model = PatientPortalUser
    form_class = PatientProfileForm
    template_name = 'patient_portal/profile.html'
    success_url = reverse_lazy('patient_profile')
    
    def get_object(self):
        return self.patient_user
    
    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully!")
        return super().form_valid(form)


class PatientNotificationListView(PatientPortalMixin, ListView):
    """Patient notifications"""
    model = PatientNotification
    template_name = 'patient_portal/notifications.html'
    context_object_name = 'notifications'
    paginate_by = 20
    
    def get_queryset(self):
        return PatientNotification.objects.filter(
            portal_user=self.patient_user
        ).order_by('-created_at')


@login_required
def mark_notification_read(request, pk):
    """Mark notification as read"""
    try:
        patient_user = PatientPortalUser.objects.get(user=request.user)
        notification = get_object_or_404(PatientNotification, pk=pk, portal_user=patient_user)
    except PatientPortalUser.DoesNotExist:
        raise PermissionDenied("Access denied")
    
    notification.is_read = True
    notification.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    
    return redirect('patient_notifications')


@login_required
def mark_all_notifications_read(request):
    """Mark all notifications as read"""
    try:
        patient_user = PatientPortalUser.objects.get(user=request.user)
    except PatientPortalUser.DoesNotExist:
        raise PermissionDenied("Access denied")
    
    PatientNotification.objects.filter(
        portal_user=patient_user,
        is_read=False
    ).update(is_read=True)
    
    messages.success(request, "All notifications marked as read")
    return redirect('patient_notifications')


@login_required
def download_document(request, pk):
    """Download patient document"""
    try:
        patient_user = PatientPortalUser.objects.get(user=request.user)
        document = get_object_or_404(PatientDocument, pk=pk, portal_user=patient_user)
    except PatientPortalUser.DoesNotExist:
        raise PermissionDenied("Access denied")
    
    if not document.is_visible_to_patient:
        raise PermissionDenied("Document not accessible")
    
    response = HttpResponse(document.file.read(), content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{document.title}"'
    return response


@login_required
def get_appointment_slots(request):
    """Get available appointment slots (AJAX)"""
    doctor_id = request.GET.get('doctor_id')
    date = request.GET.get('date')
    
    if not doctor_id or not date:
        return JsonResponse({'error': 'Doctor and date required'}, status=400)
    
    # Get booked appointments for the doctor on the specified date
    booked_appointments = PatientAppointment.objects.filter(
        doctor_id=doctor_id,
        appointment_date=date,
        status__in=['scheduled', 'confirmed']
    ).values_list('appointment_time', flat=True)
    
    # Generate available time slots (example: 9 AM to 5 PM, 30-minute slots)
    available_slots = []
    start_time = timezone.datetime.strptime('09:00', '%H:%M').time()
    end_time = timezone.datetime.strptime('17:00', '%H:%M').time()
    
    current_time = start_time
    while current_time < end_time:
        if current_time not in booked_appointments:
            available_slots.append(current_time.strftime('%H:%M'))
        
        # Add 30 minutes
        current_datetime = timezone.datetime.combine(timezone.now().date(), current_time)
        current_datetime += timezone.timedelta(minutes=30)
        current_time = current_datetime.time()
    
    return JsonResponse({'slots': available_slots})


@login_required
def patient_portal_search(request):
    """Search functionality for patient portal"""
    try:
        patient_user = PatientPortalUser.objects.get(user=request.user)
    except PatientPortalUser.DoesNotExist:
        raise PermissionDenied("Access denied")
    
    query = request.GET.get('q', '')
    results = {}
    
    if query:
        # Search appointments
        appointments = PatientAppointment.objects.filter(
            Q(portal_user=patient_user) &
            (Q(doctor__nombre__icontains=query) |
             Q(reason__icontains=query))
        )[:5]
        
        # Search documents
        documents = PatientDocument.objects.filter(
            Q(portal_user=patient_user) &
            Q(is_visible_to_patient=True) &
            (Q(title__icontains=query) |
             Q(description__icontains=query))
        )[:5]
        
        # Search messages
        messages = PatientMessage.objects.filter(
            Q(portal_user=patient_user) &
            (Q(subject__icontains=query) |
             Q(message__icontains=query))
        )[:5]
        
        results = {
            'appointments': appointments,
            'documents': documents,
            'messages': messages,
            'query': query
        }
    
    return render(request, 'patient_portal/search_results.html', results) 