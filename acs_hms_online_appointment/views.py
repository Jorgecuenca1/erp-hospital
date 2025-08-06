from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class OnlineAppointmentDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_online_appointment/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Online Appointment'
        context['module_type'] = 'hms'
        return context

class OnlineAppointmentListView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_online_appointment/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Online Appointment'
        return context

class OnlineAppointmentCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_online_appointment/create.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Online Appointment'
        return context

class OnlineAppointmentDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_online_appointment/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Online Appointment'
        return context

class OnlineAppointmentUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_online_appointment/update.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Online Appointment'
        return context

class OnlineAppointmentDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_online_appointment/delete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Online Appointment'
        return context

class OnlineAppointmentReportsView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_online_appointment/reports.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Online Appointment'
        return context
