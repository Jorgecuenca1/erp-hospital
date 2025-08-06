from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class CertificationDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_certification/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Certification'
        context['module_type'] = 'hms'
        return context

class CertificationListView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_certification/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Certification'
        return context

class CertificationCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_certification/create.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Certification'
        return context

class CertificationDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_certification/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Certification'
        return context

class CertificationUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_certification/update.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Certification'
        return context

class CertificationDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_certification/delete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Certification'
        return context

class CertificationReportsView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_certification/reports.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Certification'
        return context
