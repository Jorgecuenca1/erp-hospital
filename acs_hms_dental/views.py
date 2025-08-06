from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class DentalDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_dental/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Dental'
        context['module_type'] = 'hms'
        return context

class DentalListView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_dental/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Dental'
        return context

class DentalCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_dental/create.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Dental'
        return context

class DentalDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_dental/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Dental'
        return context

class DentalUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_dental/update.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Dental'
        return context

class DentalDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_dental/delete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Dental'
        return context

class DentalReportsView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_dental/reports.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Dental'
        return context
