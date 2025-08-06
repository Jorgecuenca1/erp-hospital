from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import PaginaWeb, Seccion, Menu, Banner
from .forms import PaginaWebForm, SeccionForm, MenuForm, BannerForm

# Create your views here.

# PaginaWeb
class PaginaWebListView(ListView):
    model = PaginaWeb
class PaginaWebDetailView(DetailView):
    model = PaginaWeb
class PaginaWebCreateView(CreateView):
    model = PaginaWeb
    form_class = PaginaWebForm
    success_url = reverse_lazy('website:paginaweb_list')
class PaginaWebUpdateView(UpdateView):
    model = PaginaWeb
    form_class = PaginaWebForm
    success_url = reverse_lazy('website:paginaweb_list')
class PaginaWebDeleteView(DeleteView):
    model = PaginaWeb
    success_url = reverse_lazy('website:paginaweb_list')

# Seccion
class SeccionListView(ListView):
    model = Seccion
class SeccionDetailView(DetailView):
    model = Seccion
class SeccionCreateView(CreateView):
    model = Seccion
    form_class = SeccionForm
    success_url = reverse_lazy('website:seccion_list')
class SeccionUpdateView(UpdateView):
    model = Seccion
    form_class = SeccionForm
    success_url = reverse_lazy('website:seccion_list')
class SeccionDeleteView(DeleteView):
    model = Seccion
    success_url = reverse_lazy('website:seccion_list')

# Menu
class MenuListView(ListView):
    model = Menu
class MenuDetailView(DetailView):
    model = Menu
class MenuCreateView(CreateView):
    model = Menu
    form_class = MenuForm
    success_url = reverse_lazy('website:menu_list')
class MenuUpdateView(UpdateView):
    model = Menu
    form_class = MenuForm
    success_url = reverse_lazy('website:menu_list')
class MenuDeleteView(DeleteView):
    model = Menu
    success_url = reverse_lazy('website:menu_list')

# Banner
class BannerListView(ListView):
    model = Banner
class BannerDetailView(DetailView):
    model = Banner
class BannerCreateView(CreateView):
    model = Banner
    form_class = BannerForm
    success_url = reverse_lazy('website:banner_list')
class BannerUpdateView(UpdateView):
    model = Banner
    form_class = BannerForm
    success_url = reverse_lazy('website:banner_list')
class BannerDeleteView(DeleteView):
    model = Banner
    success_url = reverse_lazy('website:banner_list')
