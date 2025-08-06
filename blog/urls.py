from django.urls import path
from .views import (
    CategoriaListView, CategoriaDetailView, CategoriaCreateView, CategoriaUpdateView, CategoriaDeleteView,
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,
    ComentarioListView, ComentarioDetailView, ComentarioCreateView, ComentarioUpdateView, ComentarioDeleteView
)

urlpatterns = [
    # URLs para Categoria
    path('categorias/', CategoriaListView.as_view(), name='categoria_list'),
    path('categorias/<int:pk>/', CategoriaDetailView.as_view(), name='categoria_detail'),
    path('categorias/new/', CategoriaCreateView.as_view(), name='categoria_create'),
    path('categorias/<int:pk>/edit/', CategoriaUpdateView.as_view(), name='categoria_update'),
    path('categorias/<int:pk>/delete/', CategoriaDeleteView.as_view(), name='categoria_delete'),

    # URLs para Post
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/new/', PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),

    # URLs para Comentario
    path('comentarios/', ComentarioListView.as_view(), name='comentario_list'),
    path('comentarios/<int:pk>/', ComentarioDetailView.as_view(), name='comentario_detail'),
    path('comentarios/new/', ComentarioCreateView.as_view(), name='comentario_create'),
    path('comentarios/<int:pk>/edit/', ComentarioUpdateView.as_view(), name='comentario_update'),
    path('comentarios/<int:pk>/delete/', ComentarioDeleteView.as_view(), name='comentario_delete'),
]