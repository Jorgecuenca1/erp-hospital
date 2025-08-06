from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class PaediatricDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_paediatric/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Paediatric'
        context['module_type'] = 'hms'
        return context

class PaediatricListView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_paediatric/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Paediatric'
        return context

class PaediatricCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_paediatric/create.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Paediatric'
        return context

class PaediatricDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_paediatric/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Paediatric'
        return context

class PaediatricUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_paediatric/update.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Paediatric'
        return context

class PaediatricDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_paediatric/delete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Paediatric'
        return context

class PaediatricReportsView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_paediatric/reports.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Paediatric'
        return context
