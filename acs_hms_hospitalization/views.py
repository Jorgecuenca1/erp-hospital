from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class HospitalizationDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_hospitalization/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Hospitalization'
        context['module_type'] = 'hms'
        return context

class HospitalizationListView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_hospitalization/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Hospitalization'
        return context

class HospitalizationCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_hospitalization/create.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Hospitalization'
        return context

class HospitalizationDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_hospitalization/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Hospitalization'
        return context

class HospitalizationUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_hospitalization/update.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Hospitalization'
        return context

class HospitalizationDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_hospitalization/delete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Hospitalization'
        return context

class HospitalizationReportsView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_hospitalization/reports.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Hospitalization'
        return context
