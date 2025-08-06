from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.urls import reverse_lazy
from django.db.models import Q, Sum, Count
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.db import transaction
from decimal import Decimal

from .models import (
    CommissionStructure, CommissionAgent, CommissionRecord,
    CommissionPayment, CommissionReport, CommissionConfiguration
)
from .forms import (
    CommissionStructureForm, CommissionAgentForm, CommissionRecordForm,
    CommissionPaymentForm, CommissionReportForm, CommissionConfigurationForm,
    CommissionSearchForm
)

class CommissionDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'commission/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Dashboard statistics
        context['total_structures'] = CommissionStructure.objects.count()
        context['active_structures'] = CommissionStructure.objects.filter(is_active=True).count()
        context['total_agents'] = CommissionAgent.objects.count()
        context['active_agents'] = CommissionAgent.objects.filter(is_active=True).count()
        context['total_records'] = CommissionRecord.objects.count()
        context['pending_records'] = CommissionRecord.objects.filter(status='pending').count()
        context['total_payments'] = CommissionPayment.objects.count()
        context['pending_payments'] = CommissionPayment.objects.filter(status='pending').count()
        
        # Recent activities
        context['recent_records'] = CommissionRecord.objects.order_by('-created_at')[:5]
        context['recent_payments'] = CommissionPayment.objects.order_by('-created_at')[:5]
        
        # Monthly statistics
        current_month = timezone.now().replace(day=1)
        context['monthly_records'] = CommissionRecord.objects.filter(
            created_at__gte=current_month
        ).count()
        context['monthly_payments'] = CommissionPayment.objects.filter(
            created_at__gte=current_month
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        return context

# Commission Structure Views
class CommissionStructureListView(LoginRequiredMixin, ListView):
    model = CommissionStructure
    template_name = 'commission/structure_list.html'
    context_object_name = 'structures'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = CommissionStructure.objects.all()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(service_type__icontains=search)
            )
        return queryset.order_by('-created_at')

class CommissionStructureDetailView(LoginRequiredMixin, DetailView):
    model = CommissionStructure
    template_name = 'commission/structure_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['records'] = CommissionRecord.objects.filter(structure=self.object)[:10]
        return context

class CommissionStructureCreateView(LoginRequiredMixin, CreateView):
    model = CommissionStructure
    form_class = CommissionStructureForm
    template_name = 'commission/structure_form.html'
    success_url = reverse_lazy('commission:structure_list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Commission structure created successfully.')
        return super().form_valid(form)

class CommissionStructureUpdateView(LoginRequiredMixin, UpdateView):
    model = CommissionStructure
    form_class = CommissionStructureForm
    template_name = 'commission/structure_form.html'
    
    def get_success_url(self):
        return reverse_lazy('commission:structure_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Commission structure updated successfully.')
        return super().form_valid(form)

class CommissionStructureDeleteView(LoginRequiredMixin, DeleteView):
    model = CommissionStructure
    template_name = 'commission/structure_confirm_delete.html'
    success_url = reverse_lazy('commission:structure_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Commission structure deleted successfully.')
        return super().delete(request, *args, **kwargs)

# Commission Agent Views
class CommissionAgentListView(LoginRequiredMixin, ListView):
    model = CommissionAgent
    template_name = 'commission/agent_list.html'
    context_object_name = 'agents'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = CommissionAgent.objects.select_related('user')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(agent_code__icontains=search) |
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search)
            )
        return queryset.order_by('-created_at')

class CommissionAgentDetailView(LoginRequiredMixin, DetailView):
    model = CommissionAgent
    template_name = 'commission/agent_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['records'] = CommissionRecord.objects.filter(agent=self.object)[:10]
        context['payments'] = CommissionPayment.objects.filter(agent=self.object)[:10]
        return context

class CommissionAgentCreateView(LoginRequiredMixin, CreateView):
    model = CommissionAgent
    form_class = CommissionAgentForm
    template_name = 'commission/agent_form.html'
    success_url = reverse_lazy('commission:agent_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Commission agent created successfully.')
        return super().form_valid(form)

class CommissionAgentUpdateView(LoginRequiredMixin, UpdateView):
    model = CommissionAgent
    form_class = CommissionAgentForm
    template_name = 'commission/agent_form.html'
    
    def get_success_url(self):
        return reverse_lazy('commission:agent_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Commission agent updated successfully.')
        return super().form_valid(form)

# Commission Record Views
class CommissionRecordListView(LoginRequiredMixin, ListView):
    model = CommissionRecord
    template_name = 'commission/record_list.html'
    context_object_name = 'records'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = CommissionRecord.objects.select_related('agent', 'structure', 'patient')
        
        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(agent__agent_code__icontains=search) |
                Q(patient__first_name__icontains=search) |
                Q(patient__last_name__icontains=search) |
                Q(service_description__icontains=search)
            )
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = CommissionSearchForm(self.request.GET)
        return context

class CommissionRecordDetailView(LoginRequiredMixin, DetailView):
    model = CommissionRecord
    template_name = 'commission/record_detail.html'

class CommissionRecordCreateView(LoginRequiredMixin, CreateView):
    model = CommissionRecord
    form_class = CommissionRecordForm
    template_name = 'commission/record_form.html'
    success_url = reverse_lazy('commission:record_list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Commission record created successfully.')
        return super().form_valid(form)

class CommissionRecordUpdateView(LoginRequiredMixin, UpdateView):
    model = CommissionRecord
    form_class = CommissionRecordForm
    template_name = 'commission/record_form.html'
    
    def get_success_url(self):
        return reverse_lazy('commission:record_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Commission record updated successfully.')
        return super().form_valid(form)

# Commission Payment Views
class CommissionPaymentListView(LoginRequiredMixin, ListView):
    model = CommissionPayment
    template_name = 'commission/payment_list.html'
    context_object_name = 'payments'
    paginate_by = 20
    
    def get_queryset(self):
        return CommissionPayment.objects.select_related('agent').order_by('-created_at')

class CommissionPaymentDetailView(LoginRequiredMixin, DetailView):
    model = CommissionPayment
    template_name = 'commission/payment_detail.html'

class CommissionPaymentCreateView(LoginRequiredMixin, CreateView):
    model = CommissionPayment
    form_class = CommissionPaymentForm
    template_name = 'commission/payment_form.html'
    success_url = reverse_lazy('commission:payment_list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Commission payment created successfully.')
        return super().form_valid(form)

# Commission Report Views
class CommissionReportListView(LoginRequiredMixin, ListView):
    model = CommissionReport
    template_name = 'commission/report_list.html'
    context_object_name = 'reports'
    paginate_by = 20
    
    def get_queryset(self):
        return CommissionReport.objects.order_by('-generated_at')

class CommissionReportCreateView(LoginRequiredMixin, CreateView):
    model = CommissionReport
    form_class = CommissionReportForm
    template_name = 'commission/report_form.html'
    success_url = reverse_lazy('commission:report_list')
    
    def form_valid(self, form):
        form.instance.generated_by = self.request.user
        messages.success(self.request, 'Commission report created successfully.')
        return super().form_valid(form)

# Configuration Views
class CommissionConfigurationView(LoginRequiredMixin, UpdateView):
    model = CommissionConfiguration
    form_class = CommissionConfigurationForm
    template_name = 'commission/configuration.html'
    success_url = reverse_lazy('commission:configuration')
    
    def get_object(self):
        config, created = CommissionConfiguration.objects.get_or_create(
            defaults={'updated_by': self.request.user}
        )
        return config
    
    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        messages.success(self.request, 'Commission configuration updated successfully.')
        return super().form_valid(form)

# API Views
@method_decorator(csrf_exempt, name='dispatch')
class CommissionAPIView(LoginRequiredMixin, TemplateView):
    
    def get(self, request):
        """Get commission data"""
        agent_id = request.GET.get('agent_id')
        structure_id = request.GET.get('structure_id')
        
        data = {}
        
        if agent_id:
            try:
                agent = CommissionAgent.objects.get(id=agent_id)
                data['agent'] = {
                    'id': agent.id,
                    'code': agent.agent_code,
                    'name': agent.user.get_full_name(),
                    'total_earned': agent.get_total_commission_earned(),
                    'total_paid': agent.get_total_commission_paid(),
                    'pending': agent.get_pending_commission(),
                }
            except CommissionAgent.DoesNotExist:
                return JsonResponse({'error': 'Agent not found'}, status=404)
        
        if structure_id:
            try:
                structure = CommissionStructure.objects.get(id=structure_id)
                data['structure'] = {
                    'id': structure.id,
                    'name': structure.name,
                    'service_type': structure.service_type,
                    'calculation_type': structure.calculation_type,
                    'percentage_rate': float(structure.percentage_rate),
                    'flat_fee_amount': float(structure.flat_fee_amount),
                }
            except CommissionStructure.DoesNotExist:
                return JsonResponse({'error': 'Structure not found'}, status=404)
        
        return JsonResponse(data)

@login_required
def export_commission_data(request):
    """Export commission data to CSV"""
    import csv
    from django.http import HttpResponse
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="commission_data.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Agent Code', 'Agent Name', 'Service Date', 'Service Amount', 'Commission Amount', 'Status'])
    
    records = CommissionRecord.objects.select_related('agent', 'agent__user').all()
    for record in records:
        writer.writerow([
            record.agent.agent_code,
            record.agent.user.get_full_name(),
            record.service_date,
            record.service_amount,
            record.commission_amount,
            record.status
        ])
    
    return response

@login_required
def calculate_commission(request):
    """Calculate commission for a given service amount"""
    if request.method == 'POST':
        structure_id = request.POST.get('structure_id')
        service_amount = request.POST.get('service_amount')
        
        try:
            structure = CommissionStructure.objects.get(id=structure_id)
            commission_amount = structure.calculate_commission(float(service_amount))
            
            return JsonResponse({
                'commission_amount': commission_amount,
                'service_amount': service_amount,
                'structure_name': structure.name
            })
        except CommissionStructure.DoesNotExist:
            return JsonResponse({'error': 'Structure not found'}, status=404)
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid service amount'}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405) 