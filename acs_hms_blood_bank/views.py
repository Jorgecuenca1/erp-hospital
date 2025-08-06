from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class BloodBankDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_blood_bank/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Blood Bank'
        context['module_type'] = 'hms'
        return context

class BloodBankListView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_blood_bank/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Blood Bank'
        return context

class BloodBankCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_blood_bank/create.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Blood Bank'
        return context

class BloodBankDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_blood_bank/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Blood Bank'
        return context

class BloodBankUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_blood_bank/update.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Blood Bank'
        return context

class BloodBankDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_blood_bank/delete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Blood Bank'
        return context

class BloodBankReportsView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_blood_bank/reports.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Blood Bank'
        return context
