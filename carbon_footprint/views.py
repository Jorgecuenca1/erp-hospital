from django.shortcuts import render
from django.views.generic import TemplateView

class CarbonFootprintDashboardView(TemplateView):
    template_name = 'carbon_footprint/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Carbon Footprint Dashboard'
        return context

class CalculateFootprintView(TemplateView):
    template_name = 'carbon_footprint/calculate.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Calculate Carbon Footprint'
        return context

class FootprintReportsView(TemplateView):
    template_name = 'carbon_footprint/reports.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Carbon Footprint Reports'
        return context 