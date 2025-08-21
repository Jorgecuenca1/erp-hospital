from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class SubscriptionsDashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard principal de suscripciones"""
    template_name = 'subscriptions/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Suscripciones'
        context['suscripciones_total'] = 0  # Placeholder
        return context

# Planes de suscripción - Vistas placeholder
class PlanSuscripcionListView(LoginRequiredMixin, TemplateView):
    template_name = 'subscriptions/plan_list.html'

class PlanSuscripcionCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'subscriptions/plan_create.html'

# Suscripciones - Vistas placeholder
class SuscripcionListView(LoginRequiredMixin, TemplateView):
    template_name = 'subscriptions/suscripcion_list.html'

class SuscripcionCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'subscriptions/suscripcion_create.html'