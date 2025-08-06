from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class OperationTheaterDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_operation_theater/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Operation Theater'
        context['module_type'] = 'hms'
        return context

class OperationTheaterListView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_operation_theater/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Operation Theater'
        return context

class OperationTheaterCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_operation_theater/create.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Operation Theater'
        return context

class OperationTheaterDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_operation_theater/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Operation Theater'
        return context

class OperationTheaterUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_operation_theater/update.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Operation Theater'
        return context

class OperationTheaterDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_operation_theater/delete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Operation Theater'
        return context

class OperationTheaterReportsView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_operation_theater/reports.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Operation Theater'
        return context
