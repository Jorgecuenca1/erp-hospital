from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import (
    ConsentFormTemplate, ConsentForm, ConsentFormAudit, 
    ConsentFormNotification, ConsentFormDocument, ConsentFormConfiguration
)
from .forms import (
    ConsentFormTemplateForm, ConsentFormCreateForm, ConsentFormSignatureForm,
    ConsentFormRevokeForm, ConsentFormNotificationForm, ConsentFormSearchForm,
    ConsentFormBulkActionForm, ConsentFormConfigurationForm
)


class ConsentFormTemplateListView(LoginRequiredMixin, ListView):
    """List all consent form templates"""
    model = ConsentFormTemplate
    template_name = 'consent_form/template_list.html'
    context_object_name = 'templates'
    paginate_by = 20
    
    def get_queryset(self):
        return ConsentFormTemplate.objects.filter(is_active=True)


class ConsentFormTemplateDetailView(LoginRequiredMixin, DetailView):
    """View consent form template details"""
    model = ConsentFormTemplate
    template_name = 'consent_form/template_detail.html'
    context_object_name = 'template'


class ConsentFormTemplateCreateView(LoginRequiredMixin, CreateView):
    """Create new consent form template"""
    model = ConsentFormTemplate
    form_class = ConsentFormTemplateForm
    template_name = 'consent_form/template_form.html'
    success_url = reverse_lazy('consent_template_list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "Consent form template created successfully!")
        return super().form_valid(form)


class ConsentFormTemplateUpdateView(LoginRequiredMixin, UpdateView):
    """Update consent form template"""
    model = ConsentFormTemplate
    form_class = ConsentFormTemplateForm
    template_name = 'consent_form/template_form.html'
    success_url = reverse_lazy('consent_template_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Consent form template updated successfully!")
        return super().form_valid(form)


class ConsentFormListView(LoginRequiredMixin, ListView):
    """List all consent forms"""
    model = ConsentForm
    template_name = 'consent_form/consent_list.html'
    context_object_name = 'consents'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = ConsentForm.objects.select_related('template', 'patient', 'doctor')
        
        # Apply search filters
        form = ConsentFormSearchForm(self.request.GET)
        if form.is_valid():
            query = form.cleaned_data.get('search_query')
            search_type = form.cleaned_data.get('search_type')
            status = form.cleaned_data.get('status')
            date_from = form.cleaned_data.get('date_from')
            date_to = form.cleaned_data.get('date_to')
            
            if query:
                if search_type == 'consent_id':
                    queryset = queryset.filter(consent_id__icontains=query)
                elif search_type == 'patient_name':
                    queryset = queryset.filter(patient__nombre__icontains=query)
                elif search_type == 'doctor_name':
                    queryset = queryset.filter(doctor__nombre__icontains=query)
                elif search_type == 'procedure_name':
                    queryset = queryset.filter(procedure_name__icontains=query)
                else:
                    queryset = queryset.filter(
                        Q(consent_id__icontains=query) |
                        Q(patient__nombre__icontains=query) |
                        Q(doctor__nombre__icontains=query) |
                        Q(procedure_name__icontains=query)
                    )
            
            if status:
                queryset = queryset.filter(status=status)
            
            if date_from:
                queryset = queryset.filter(created_at__date__gte=date_from)
            
            if date_to:
                queryset = queryset.filter(created_at__date__lte=date_to)
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = ConsentFormSearchForm(self.request.GET)
        return context


class ConsentFormDetailView(LoginRequiredMixin, DetailView):
    """View consent form details"""
    model = ConsentForm
    template_name = 'consent_form/consent_detail.html'
    context_object_name = 'consent'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['audit_logs'] = self.object.audit_logs.all()[:10]
        return context


class ConsentFormCreateView(LoginRequiredMixin, CreateView):
    """Create new consent form"""
    model = ConsentForm
    form_class = ConsentFormCreateForm
    template_name = 'consent_form/consent_form.html'
    success_url = reverse_lazy('consent_form_list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.status = 'draft'
        messages.success(self.request, "Consent form created successfully!")
        
        # Create audit log
        consent_form = form.save()
        ConsentFormAudit.objects.create(
            consent_form=consent_form,
            action='created',
            user=self.request.user,
            ip_address=self.get_client_ip(),
            user_agent=self.request.META.get('HTTP_USER_AGENT', ''),
            details={'message': 'Consent form created'}
        )
        
        return super().form_valid(form)
    
    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip


@login_required
def consent_form_sign(request, pk):
    """Sign consent form"""
    consent_form = get_object_or_404(ConsentForm, pk=pk)
    
    if consent_form.status not in ['draft', 'pending']:
        messages.error(request, "This consent form cannot be signed")
        return redirect('consent_form_detail', pk=pk)
    
    # Determine signature type
    signature_type = request.GET.get('type', 'patient')
    
    if request.method == 'POST':
        form = ConsentFormSignatureForm(
            request.POST,
            consent_form=consent_form,
            signature_type=signature_type
        )
        
        if form.is_valid():
            signature_data = form.cleaned_data['signature_data']
            ip_address = get_client_ip(request)
            
            if signature_type == 'patient':
                consent_form.sign_patient(signature_data, ip_address)
            elif signature_type == 'guardian':
                consent_form.sign_guardian(signature_data, ip_address)
            elif signature_type == 'witness':
                witness_name = form.cleaned_data['witness_name']
                witness_relationship = form.cleaned_data['witness_relationship']
                consent_form.sign_witness(signature_data, witness_name, witness_relationship)
            elif signature_type == 'doctor':
                consent_form.sign_doctor(signature_data)
            
            # Create audit log
            ConsentFormAudit.objects.create(
                consent_form=consent_form,
                action='signed',
                user=request.user,
                ip_address=ip_address,
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                details={'signature_type': signature_type}
            )
            
            messages.success(request, f"Consent form signed successfully as {signature_type}")
            return redirect('consent_form_detail', pk=pk)
    else:
        form = ConsentFormSignatureForm(
            consent_form=consent_form,
            signature_type=signature_type
        )
    
    return render(request, 'consent_form/consent_sign.html', {
        'form': form,
        'consent_form': consent_form,
        'signature_type': signature_type
    })


@login_required
def consent_form_revoke(request, pk):
    """Revoke consent form"""
    consent_form = get_object_or_404(ConsentForm, pk=pk)
    
    if consent_form.status != 'signed':
        messages.error(request, "Only signed consent forms can be revoked")
        return redirect('consent_form_detail', pk=pk)
    
    if request.method == 'POST':
        form = ConsentFormRevokeForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data['reason']
            consent_form.revoke(reason, request.user)
            
            # Create audit log
            ConsentFormAudit.objects.create(
                consent_form=consent_form,
                action='revoked',
                user=request.user,
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                details={'reason': reason}
            )
            
            messages.success(request, "Consent form revoked successfully")
            return redirect('consent_form_detail', pk=pk)
    else:
        form = ConsentFormRevokeForm()
    
    return render(request, 'consent_form/consent_revoke.html', {
        'form': form,
        'consent_form': consent_form
    })


@login_required
def consent_form_pdf(request, pk):
    """Generate PDF for consent form"""
    consent_form = get_object_or_404(ConsentForm, pk=pk)
    
    # Create audit log
    ConsentFormAudit.objects.create(
        consent_form=consent_form,
        action='printed',
        user=request.user,
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
        details={'format': 'pdf'}
    )
    
    # Generate PDF (simplified - would need proper PDF generation)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="consent_{consent_form.consent_id}.pdf"'
    
    # Here you would implement actual PDF generation
    response.write(b'PDF content would go here')
    
    return response


@login_required
def consent_form_send_notification(request, pk):
    """Send notification for consent form"""
    consent_form = get_object_or_404(ConsentForm, pk=pk)
    
    if request.method == 'POST':
        form = ConsentFormNotificationForm(request.POST)
        if form.is_valid():
            notification = form.save(commit=False)
            notification.consent_form = consent_form
            notification.save()
            
            messages.success(request, "Notification sent successfully")
            return redirect('consent_form_detail', pk=pk)
    else:
        form = ConsentFormNotificationForm()
    
    return render(request, 'consent_form/send_notification.html', {
        'form': form,
        'consent_form': consent_form
    })


@login_required
def consent_form_bulk_action(request):
    """Handle bulk actions on consent forms"""
    if request.method == 'POST':
        form = ConsentFormBulkActionForm(request.POST)
        if form.is_valid():
            action = form.cleaned_data['action']
            selected_ids = form.cleaned_data['selected_items'].split(',')
            
            consent_forms = ConsentForm.objects.filter(id__in=selected_ids)
            
            if action == 'send_reminders':
                # Send reminder notifications
                for consent_form in consent_forms:
                    if consent_form.status == 'pending':
                        ConsentFormNotification.objects.create(
                            consent_form=consent_form,
                            notification_type='signature_required',
                            recipient_email=consent_form.patient.email,
                            recipient_name=consent_form.patient.nombre,
                            subject=f'Signature Required: {consent_form.template.title}',
                            message=f'Please sign the consent form: {consent_form.consent_id}'
                        )
                messages.success(request, f"Reminders sent for {consent_forms.count()} consent forms")
            
            elif action == 'mark_expired':
                # Mark as expired
                expired_count = consent_forms.filter(status='pending').update(status='expired')
                messages.success(request, f"{expired_count} consent forms marked as expired")
            
            elif action == 'export_pdf':
                # Export to PDF (simplified)
                messages.success(request, f"PDF export initiated for {consent_forms.count()} consent forms")
            
            return redirect('consent_form_list')
    
    return redirect('consent_form_list')


@login_required
def consent_form_dashboard(request):
    """Consent form dashboard with statistics"""
    from django.db.models import Count
    
    # Get statistics
    total_forms = ConsentForm.objects.count()
    signed_forms = ConsentForm.objects.filter(status='signed').count()
    pending_forms = ConsentForm.objects.filter(status='pending').count()
    expired_forms = ConsentForm.objects.filter(status='expired').count()
    
    # Forms by template
    forms_by_template = ConsentFormTemplate.objects.annotate(
        form_count=Count('forms')
    ).order_by('-form_count')[:10]
    
    # Recent forms
    recent_forms = ConsentForm.objects.select_related(
        'template', 'patient', 'doctor'
    ).order_by('-created_at')[:10]
    
    context = {
        'total_forms': total_forms,
        'signed_forms': signed_forms,
        'pending_forms': pending_forms,
        'expired_forms': expired_forms,
        'forms_by_template': forms_by_template,
        'recent_forms': recent_forms,
    }
    
    return render(request, 'consent_form/dashboard.html', context)


@login_required
def consent_form_configuration(request):
    """Configure consent form settings"""
    try:
        config = ConsentFormConfiguration.objects.get()
    except ConsentFormConfiguration.DoesNotExist:
        config = ConsentFormConfiguration()
    
    if request.method == 'POST':
        form = ConsentFormConfigurationForm(request.POST)
        if form.is_valid():
            # Update configuration
            for field, value in form.cleaned_data.items():
                setattr(config, field, value)
            
            config.updated_by = request.user
            config.save()
            
            messages.success(request, "Configuration updated successfully")
            return redirect('consent_form_configuration')
    else:
        # Initialize form with current configuration
        initial_data = {}
        if config.pk:
            for field in ConsentFormConfigurationForm.base_fields:
                initial_data[field] = getattr(config, field, None)
        
        form = ConsentFormConfigurationForm(initial=initial_data)
    
    return render(request, 'consent_form/configuration.html', {
        'form': form,
        'config': config
    })


def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@login_required
def consent_form_ajax_search(request):
    """AJAX search for consent forms"""
    query = request.GET.get('q', '')
    results = []
    
    if query:
        consent_forms = ConsentForm.objects.filter(
            Q(consent_id__icontains=query) |
            Q(patient__nombre__icontains=query) |
            Q(procedure_name__icontains=query)
        )[:10]
        
        for consent_form in consent_forms:
            results.append({
                'id': consent_form.id,
                'consent_id': consent_form.consent_id,
                'patient_name': consent_form.patient.nombre,
                'template_title': consent_form.template.title,
                'status': consent_form.status,
                'created_at': consent_form.created_at.strftime('%Y-%m-%d')
            })
    
    return JsonResponse({'results': results})


@login_required
def consent_form_statistics_api(request):
    """API endpoint for consent form statistics"""
    from django.db.models import Count
    from datetime import datetime, timedelta
    
    # Get date range
    days = int(request.GET.get('days', 30))
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=days)
    
    # Get daily statistics
    daily_stats = ConsentForm.objects.filter(
        created_at__date__gte=start_date,
        created_at__date__lte=end_date
    ).extra(
        select={'day': 'date(created_at)'}
    ).values('day').annotate(
        total=Count('id'),
        signed=Count('id', filter=Q(status='signed')),
        pending=Count('id', filter=Q(status='pending'))
    ).order_by('day')
    
    return JsonResponse({
        'daily_stats': list(daily_stats),
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat()
    }) 