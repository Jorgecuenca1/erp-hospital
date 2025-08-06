from django.shortcuts import render
from django.views.generic import TemplateView

class SocialMetricsDashboardView(TemplateView):
    template_name = 'social_metrics/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Social Metrics Dashboard'
        return context

class MetricsListView(TemplateView):
    template_name = 'social_metrics/metrics_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Social Metrics List'
        return context

class SocialReportsView(TemplateView):
    template_name = 'social_metrics/reports.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Social Reports'
        return context 