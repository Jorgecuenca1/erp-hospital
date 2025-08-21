from django.urls import path
from .views import (
    ForumDashboardView,
    TemaListView, TemaDetailView, TemaCreateView, TemaUpdateView, TemaDeleteView,
    PreguntaListView, PreguntaDetailView, PreguntaCreateView, PreguntaUpdateView, PreguntaDeleteView,
    RespuestaListView, RespuestaDetailView, RespuestaCreateView, RespuestaUpdateView, RespuestaDeleteView
)

app_name = 'forum'

urlpatterns = [
    # Dashboard principal
    path('', ForumDashboardView.as_view(), name='dashboard'),
    # URLs para Tema
    path('temas/', TemaListView.as_view(), name='tema_list'),
    path('temas/<int:pk>/', TemaDetailView.as_view(), name='tema_detail'),
    path('temas/new/', TemaCreateView.as_view(), name='tema_create'),
    path('temas/<int:pk>/edit/', TemaUpdateView.as_view(), name='tema_update'),
    path('temas/<int:pk>/delete/', TemaDeleteView.as_view(), name='tema_delete'),

    # URLs para Pregunta
    path('preguntas/', PreguntaListView.as_view(), name='pregunta_list'),
    path('preguntas/<int:pk>/', PreguntaDetailView.as_view(), name='pregunta_detail'),
    path('preguntas/new/', PreguntaCreateView.as_view(), name='pregunta_create'),
    path('preguntas/<int:pk>/edit/', PreguntaUpdateView.as_view(), name='pregunta_update'),
    path('preguntas/<int:pk>/delete/', PreguntaDeleteView.as_view(), name='pregunta_delete'),

    # URLs para Respuesta
    path('respuestas/', RespuestaListView.as_view(), name='respuesta_list'),
    path('respuestas/<int:pk>/', RespuestaDetailView.as_view(), name='respuesta_detail'),
    path('respuestas/new/', RespuestaCreateView.as_view(), name='respuesta_create'),
    path('respuestas/<int:pk>/edit/', RespuestaUpdateView.as_view(), name='respuesta_update'),
    path('respuestas/<int:pk>/delete/', RespuestaDeleteView.as_view(), name='respuesta_delete'),
]