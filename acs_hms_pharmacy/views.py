from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class PharmacyDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_pharmacy/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Pharmacy'
        context['module_type'] = 'hms'
        return context

class PharmacyListView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_pharmacy/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Pharmacy'
        return context

class PharmacyCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_pharmacy/create.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Pharmacy'
        return context

class PharmacyDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_pharmacy/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Pharmacy'
        return context

class PharmacyUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_pharmacy/update.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Pharmacy'
        return context

class PharmacyDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_pharmacy/delete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Pharmacy'
        return context

class PharmacyReportsView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_pharmacy/reports.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Pharmacy'
        return context
