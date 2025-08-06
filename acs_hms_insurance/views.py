from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class InsuranceDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_insurance/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Insurance'
        context['module_type'] = 'hms'
        return context

class InsuranceListView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_insurance/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Insurance'
        return context

class InsuranceCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_insurance/create.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Insurance'
        return context

class InsuranceDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_insurance/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Insurance'
        return context

class InsuranceUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_insurance/update.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Insurance'
        return context

class InsuranceDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_insurance/delete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Insurance'
        return context

class InsuranceReportsView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_insurance/reports.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Insurance'
        return context
