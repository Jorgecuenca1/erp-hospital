from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class WebcamDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_webcam/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Webcam'
        context['module_type'] = 'hms'
        return context

class WebcamListView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_webcam/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Webcam'
        return context

class WebcamCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_webcam/create.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Webcam'
        return context

class WebcamDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_webcam/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Webcam'
        return context

class WebcamUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_webcam/update.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Webcam'
        return context

class WebcamDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_webcam/delete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Webcam'
        return context

class WebcamReportsView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_webcam/reports.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Webcam'
        return context
