from django.urls import path
from . import views

urlpatterns = [
    path('pacientes/', views.PacienteListView.as_view(), name='paciente_list'),
    path('pacientes/new/', views.PacienteCreateView.as_view(), name='paciente_create'),
    path('pacientes/<int:pk>/', views.PacienteDetailView.as_view(), name='paciente_detail'),
    path('pacientes/<int:pk>/edit/', views.PacienteUpdateView.as_view(), name='paciente_edit'),
    path('pacientes/<int:pk>/delete/', views.PacienteDeleteView.as_view(), name='paciente_delete'),
] 