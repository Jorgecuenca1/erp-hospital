from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class VideoCallDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_video_call/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Video Call'
        context['module_type'] = 'hms'
        return context

class VideoCallListView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_video_call/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Video Call'
        return context

class VideoCallCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_video_call/create.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Video Call'
        return context

class VideoCallDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_video_call/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Video Call'
        return context

class VideoCallUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_video_call/update.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Video Call'
        return context

class VideoCallDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_video_call/delete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Video Call'
        return context

class VideoCallReportsView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_video_call/reports.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Video Call'
        return context
