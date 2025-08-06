from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class EmergencyDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_emergency/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Emergency'
        context['module_type'] = 'hms'
        return context

class EmergencyListView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_emergency/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Emergency'
        return context

class EmergencyCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_emergency/create.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Emergency'
        return context

class EmergencyDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_emergency/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Emergency'
        return context

class EmergencyUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_emergency/update.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Emergency'
        return context

class EmergencyDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_emergency/delete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Emergency'
        return context

class EmergencyReportsView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_emergency/reports.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Emergency'
        return context
