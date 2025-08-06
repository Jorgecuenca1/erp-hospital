from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class SubscriptionDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_subscription/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Subscription'
        context['module_type'] = 'hms'
        return context

class SubscriptionListView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_subscription/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Subscription'
        return context

class SubscriptionCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_subscription/create.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Subscription'
        return context

class SubscriptionDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_subscription/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Subscription'
        return context

class SubscriptionUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_subscription/update.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Subscription'
        return context

class SubscriptionDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_subscription/delete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Subscription'
        return context

class SubscriptionReportsView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_subscription/reports.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Subscription'
        return context
