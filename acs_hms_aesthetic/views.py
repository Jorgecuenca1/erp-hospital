from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class AestheticDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_aesthetic/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Aesthetic'
        context['module_type'] = 'hms'
        return context

class AestheticListView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_aesthetic/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Aesthetic'
        return context

class AestheticCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_aesthetic/create.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Aesthetic'
        return context

class AestheticDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_aesthetic/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Aesthetic'
        return context

class AestheticUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_aesthetic/update.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Aesthetic'
        return context

class AestheticDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_aesthetic/delete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Aesthetic'
        return context

class AestheticReportsView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_aesthetic/reports.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Aesthetic'
        return context
