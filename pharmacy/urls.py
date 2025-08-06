from django.urls import path
from . import views

app_name = 'pharmacy'

urlpatterns = [
    # URLs for Medicamento
    path('medicamentos/', views.MedicamentoListView.as_view(), name='medicamento_list'),
    path('medicamentos/add/', views.MedicamentoCreateView.as_view(), name='medicamento_create'),
    path('medicamentos/<int:pk>/', views.MedicamentoDetailView.as_view(), name='medicamento_detail'),
    path('medicamentos/<int:pk>/edit/', views.MedicamentoUpdateView.as_view(), name='medicamento_edit'),
    path('medicamentos/<int:pk>/delete/', views.MedicamentoDeleteView.as_view(), name='medicamento_delete'),

    # URLs for Receta
    path('recetas/', views.RecetaListView.as_view(), name='receta_list'),
    path('recetas/add/', views.RecetaCreateView.as_view(), name='receta_create'),
    path('recetas/<int:pk>/', views.RecetaDetailView.as_view(), name='receta_detail'),
    path('recetas/<int:pk>/edit/', views.RecetaUpdateView.as_view(), name='receta_edit'),
    path('recetas/<int:pk>/delete/', views.RecetaDeleteView.as_view(), name='receta_delete'),

] 