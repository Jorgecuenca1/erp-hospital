from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class OphthalmologyDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_ophthalmology/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Ophthalmology'
        context['module_type'] = 'hms'
        return context

class OphthalmologyListView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_ophthalmology/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Ophthalmology'
        return context

class OphthalmologyCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_ophthalmology/create.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Ophthalmology'
        return context

class OphthalmologyDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_ophthalmology/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Ophthalmology'
        return context

class OphthalmologyUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_ophthalmology/update.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Ophthalmology'
        return context

class OphthalmologyDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_ophthalmology/delete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Ophthalmology'
        return context

class OphthalmologyReportsView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_ophthalmology/reports.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Ophthalmology'
        return context
