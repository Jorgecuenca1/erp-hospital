from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class BlogDashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard principal de blog"""
    template_name = 'blog/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Blog'
        context['articulos_total'] = 0  # Placeholder
        return context

# Artículos - Vistas placeholder
class ArticuloListView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/articulo_list.html'

class ArticuloCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/articulo_create.html'

class ArticuloDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/articulo_detail.html'

class ArticuloUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/articulo_update.html'

class ArticuloDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/articulo_delete.html'