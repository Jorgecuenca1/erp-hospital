from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .models import Categoria, Post, Comentario
from .forms import CategoriaForm, PostForm, ComentarioForm

# Create your views here.

# Vistas para Categoria
class CategoriaListView(ListView):
    model = Categoria
    template_name = 'blog/categoria_list.html'
    context_object_name = 'categorias'

class CategoriaDetailView(DetailView):
    model = Categoria
    template_name = 'blog/categoria_detail.html'
    context_object_name = 'categoria'

class CategoriaCreateView(CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'blog/categoria_form.html'
    success_url = reverse_lazy('categoria_list')

class CategoriaUpdateView(UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'blog/categoria_form.html'
    success_url = reverse_lazy('categoria_list')

class CategoriaDeleteView(DeleteView):
    model = Categoria
    template_name = 'blog/categoria_confirm_delete.html'
    success_url = reverse_lazy('categoria_list')

# Vistas para Post
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ComentarioForm()
        context['categorias'] = Categoria.objects.all()
        return context

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post_list')

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post_list')

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

# Vistas para Comentario
class ComentarioListView(ListView):
    model = Comentario
    template_name = 'blog/comentario_list.html'
    context_object_name = 'comentarios'

class ComentarioDetailView(DetailView):
    model = Comentario
    template_name = 'blog/comentario_detail.html'
    context_object_name = 'comentario'

class ComentarioCreateView(CreateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'blog/comentario_form.html'

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.request.GET.get('post'))
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.post.pk})

class ComentarioUpdateView(UpdateView):
    model = Comentario
    form_class = ComentarioForm
    template_name = 'blog/comentario_form.html'
    
    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.post.pk})

class ComentarioDeleteView(DeleteView):
    model = Comentario
    template_name = 'blog/comentario_confirm_delete.html'
    
    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.post.pk})
