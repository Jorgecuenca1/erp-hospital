from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Curso, Modulo, Leccion, Inscripcion, ProgresoLeccion
from .forms import CursoForm, ModuloForm, LeccionForm, InscripcionForm, ProgresoLeccionForm

# Vistas para Curso
class CursoListView(ListView):
    model = Curso
    template_name = 'elearning/curso_list.html'
    context_object_name = 'cursos'

class CursoDetailView(DetailView):
    model = Curso
    template_name = 'elearning/curso_detail.html'
    context_object_name = 'curso'

class CursoCreateView(CreateView):
    model = Curso
    form_class = CursoForm
    template_name = 'elearning/curso_form.html'
    success_url = reverse_lazy('curso_list')

class CursoUpdateView(UpdateView):
    model = Curso
    form_class = CursoForm
    template_name = 'elearning/curso_form.html'
    success_url = reverse_lazy('curso_list')

class CursoDeleteView(DeleteView):
    model = Curso
    template_name = 'elearning/curso_confirm_delete.html'
    success_url = reverse_lazy('curso_list')

# Vistas para Modulo
class ModuloListView(ListView):
    model = Modulo
    template_name = 'elearning/modulo_list.html'
    context_object_name = 'modulos'

class ModuloDetailView(DetailView):
    model = Modulo
    template_name = 'elearning/modulo_detail.html'
    context_object_name = 'modulo'

class ModuloCreateView(CreateView):
    model = Modulo
    form_class = ModuloForm
    template_name = 'elearning/modulo_form.html'
    success_url = reverse_lazy('modulo_list')

class ModuloUpdateView(UpdateView):
    model = Modulo
    form_class = ModuloForm
    template_name = 'elearning/modulo_form.html'
    success_url = reverse_lazy('modulo_list')

class ModuloDeleteView(DeleteView):
    model = Modulo
    template_name = 'elearning/modulo_confirm_delete.html'
    success_url = reverse_lazy('modulo_list')

# Vistas para Leccion
class LeccionListView(ListView):
    model = Leccion
    template_name = 'elearning/leccion_list.html'
    context_object_name = 'lecciones'

class LeccionDetailView(DetailView):
    model = Leccion
    template_name = 'elearning/leccion_detail.html'
    context_object_name = 'leccion'

class LeccionCreateView(CreateView):
    model = Leccion
    form_class = LeccionForm
    template_name = 'elearning/leccion_form.html'
    success_url = reverse_lazy('leccion_list')

class LeccionUpdateView(UpdateView):
    model = Leccion
    form_class = LeccionForm
    template_name = 'elearning/leccion_form.html'
    success_url = reverse_lazy('leccion_list')

class LeccionDeleteView(DeleteView):
    model = Leccion
    template_name = 'elearning/leccion_confirm_delete.html'
    success_url = reverse_lazy('leccion_list')

# Vistas para Inscripcion
class InscripcionListView(ListView):
    model = Inscripcion
    template_name = 'elearning/inscripcion_list.html'
    context_object_name = 'inscripciones'

class InscripcionDetailView(DetailView):
    model = Inscripcion
    template_name = 'elearning/inscripcion_detail.html'
    context_object_name = 'inscripcion'

class InscripcionCreateView(CreateView):
    model = Inscripcion
    form_class = InscripcionForm
    template_name = 'elearning/inscripcion_form.html'
    success_url = reverse_lazy('inscripcion_list')

class InscripcionUpdateView(UpdateView):
    model = Inscripcion
    form_class = InscripcionForm
    template_name = 'elearning/inscripcion_form.html'
    success_url = reverse_lazy('inscripcion_list')

class InscripcionDeleteView(DeleteView):
    model = Inscripcion
    template_name = 'elearning/inscripcion_confirm_delete.html'
    success_url = reverse_lazy('inscripcion_list')

# Vistas para ProgresoLeccion
class ProgresoLeccionListView(ListView):
    model = ProgresoLeccion
    template_name = 'elearning/progreso_leccion_list.html'
    context_object_name = 'progreso_lecciones'

class ProgresoLeccionDetailView(DetailView):
    model = ProgresoLeccion
    template_name = 'elearning/progreso_leccion_detail.html'
    context_object_name = 'progreso_leccion'

class ProgresoLeccionCreateView(CreateView):
    model = ProgresoLeccion
    form_class = ProgresoLeccionForm
    template_name = 'elearning/progreso_leccion_form.html'
    success_url = reverse_lazy('progreso_leccion_list')

class ProgresoLeccionUpdateView(UpdateView):
    model = ProgresoLeccion
    form_class = ProgresoLeccionForm
    template_name = 'elearning/progreso_leccion_form.html'
    success_url = reverse_lazy('progreso_leccion_list')

class ProgresoLeccionDeleteView(DeleteView):
    model = ProgresoLeccion
    template_name = 'elearning/progreso_leccion_confirm_delete.html'
    success_url = reverse_lazy('progreso_leccion_list')
