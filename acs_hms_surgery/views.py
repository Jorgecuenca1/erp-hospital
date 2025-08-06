from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class SurgeryDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_surgery/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Surgery'
        context['module_type'] = 'hms'
        return context

class SurgeryListView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_surgery/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Surgery'
        return context

class SurgeryCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_surgery/create.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Surgery'
        return context

class SurgeryDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_surgery/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Surgery'
        return context

class SurgeryUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_surgery/update.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Surgery'
        return context

class SurgeryDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_surgery/delete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Surgery'
        return context

class SurgeryReportsView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_surgery/reports.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Surgery'
        return context
