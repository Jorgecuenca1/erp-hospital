from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

# Create your views here.

class LiveChatDashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard principal de live chat"""
    template_name = 'livechat/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Live Chat'
        context['conversaciones_total'] = 0  # Placeholder
        return context

# Conversaciones - Vistas placeholder
class ConversacionListView(LoginRequiredMixin, TemplateView):
    template_name = 'livechat/conversacion_list.html'

class ConversacionDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'livechat/conversacion_detail.html'

# API para mensajes
class MessageAPIView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({'messages': []})
    
    def post(self, request, *args, **kwargs):
        return JsonResponse({'status': 'ok'})