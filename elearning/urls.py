from django.urls import path
from .views import (
    ElearningDashboardView,
    CursoListView, CursoDetailView, CursoCreateView, CursoUpdateView, CursoDeleteView,
    ModuloListView, ModuloDetailView, ModuloCreateView, ModuloUpdateView, ModuloDeleteView,
    LeccionListView, LeccionDetailView, LeccionCreateView, LeccionUpdateView, LeccionDeleteView,
    InscripcionListView, InscripcionDetailView, InscripcionCreateView, InscripcionUpdateView, InscripcionDeleteView,
    ProgresoLeccionListView, ProgresoLeccionDetailView, ProgresoLeccionCreateView, ProgresoLeccionUpdateView, ProgresoLeccionDeleteView
)

app_name = 'elearning'

urlpatterns = [
    # Dashboard principal
    path('', ElearningDashboardView.as_view(), name='dashboard'),
    # URLs para Curso
    path('cursos/', CursoListView.as_view(), name='curso_list'),
    path('cursos/<int:pk>/', CursoDetailView.as_view(), name='curso_detail'),
    path('cursos/new/', CursoCreateView.as_view(), name='curso_create'),
    path('cursos/<int:pk>/edit/', CursoUpdateView.as_view(), name='curso_update'),
    path('cursos/<int:pk>/delete/', CursoDeleteView.as_view(), name='curso_delete'),

    # URLs para Modulo
    path('modulos/', ModuloListView.as_view(), name='modulo_list'),
    path('modulos/<int:pk>/', ModuloDetailView.as_view(), name='modulo_detail'),
    path('modulos/new/', ModuloCreateView.as_view(), name='modulo_create'),
    path('modulos/<int:pk>/edit/', ModuloUpdateView.as_view(), name='modulo_update'),
    path('modulos/<int:pk>/delete/', ModuloDeleteView.as_view(), name='modulo_delete'),

    # URLs para Leccion
    path('lecciones/', LeccionListView.as_view(), name='leccion_list'),
    path('lecciones/<int:pk>/', LeccionDetailView.as_view(), name='leccion_detail'),
    path('lecciones/new/', LeccionCreateView.as_view(), name='leccion_create'),
    path('lecciones/<int:pk>/edit/', LeccionUpdateView.as_view(), name='leccion_update'),
    path('lecciones/<int:pk>/delete/', LeccionDeleteView.as_view(), name='leccion_delete'),

    # URLs para Inscripcion
    path('inscripciones/', InscripcionListView.as_view(), name='inscripcion_list'),
    path('inscripciones/<int:pk>/', InscripcionDetailView.as_view(), name='inscripcion_detail'),
    path('inscripciones/new/', InscripcionCreateView.as_view(), name='inscripcion_create'),
    path('inscripciones/<int:pk>/edit/', InscripcionUpdateView.as_view(), name='inscripcion_update'),
    path('inscripciones/<int:pk>/delete/', InscripcionDeleteView.as_view(), name='inscripcion_delete'),

    # URLs para ProgresoLeccion
    path('progreso-lecciones/', ProgresoLeccionListView.as_view(), name='progreso_leccion_list'),
    path('progreso-lecciones/<int:pk>/', ProgresoLeccionDetailView.as_view(), name='progreso_leccion_detail'),
    path('progreso-lecciones/new/', ProgresoLeccionCreateView.as_view(), name='progreso_leccion_create'),
    path('progreso-lecciones/<int:pk>/edit/', ProgresoLeccionUpdateView.as_view(), name='progreso_leccion_update'),
    path('progreso-lecciones/<int:pk>/delete/', ProgresoLeccionDeleteView.as_view(), name='progreso_leccion_delete'),
]