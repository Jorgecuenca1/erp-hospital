from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from .models import Tema, Pregunta, Respuesta
from .forms import TemaForm, PreguntaForm, RespuestaForm

class ForumDashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard principal del foro"""
    template_name = 'forum/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Foro'
        context['temas_total'] = Tema.objects.count()
        return context

# Vistas para Tema
class TemaListView(ListView):
    model = Tema
    template_name = 'forum/tema_list.html'
    context_object_name = 'temas'

class TemaDetailView(DetailView):
    model = Tema
    template_name = 'forum/tema_detail.html'
    context_object_name = 'tema'

class TemaCreateView(CreateView):
    model = Tema
    form_class = TemaForm
    template_name = 'forum/tema_form.html'
    success_url = reverse_lazy('tema_list')

class TemaUpdateView(UpdateView):
    model = Tema
    form_class = TemaForm
    template_name = 'forum/tema_form.html'
    success_url = reverse_lazy('tema_list')

class TemaDeleteView(DeleteView):
    model = Tema
    template_name = 'forum/tema_confirm_delete.html'
    success_url = reverse_lazy('tema_list')

# Vistas para Pregunta
class PreguntaListView(ListView):
    model = Pregunta
    template_name = 'forum/pregunta_list.html'
    context_object_name = 'preguntas'

class PreguntaDetailView(DetailView):
    model = Pregunta
    template_name = 'forum/pregunta_detail.html'
    context_object_name = 'pregunta'

class PreguntaCreateView(CreateView):
    model = Pregunta
    form_class = PreguntaForm
    template_name = 'forum/pregunta_form.html'
    success_url = reverse_lazy('pregunta_list')

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

class PreguntaUpdateView(UpdateView):
    model = Pregunta
    form_class = PreguntaForm
    template_name = 'forum/pregunta_form.html'
    success_url = reverse_lazy('pregunta_list')

class PreguntaDeleteView(DeleteView):
    model = Pregunta
    template_name = 'forum/pregunta_confirm_delete.html'
    success_url = reverse_lazy('pregunta_list')

# Vistas para Respuesta
class RespuestaListView(ListView):
    model = Respuesta
    template_name = 'forum/respuesta_list.html'
    context_object_name = 'respuestas'

class RespuestaDetailView(DetailView):
    model = Respuesta
    template_name = 'forum/respuesta_detail.html'
    context_object_name = 'respuesta'

class RespuestaCreateView(CreateView):
    model = Respuesta
    form_class = RespuestaForm
    template_name = 'forum/respuesta_form.html'

    def form_valid(self, form):
        pregunta = get_object_or_404(Pregunta, pk=self.request.GET.get('pregunta'))
        form.instance.pregunta = pregunta
        form.instance.autor = self.request.user
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('pregunta_detail', kwargs={'pk': self.object.pregunta.pk})

class RespuestaUpdateView(UpdateView):
    model = Respuesta
    form_class = RespuestaForm
    template_name = 'forum/respuesta_form.html'
    
    def get_success_url(self):
        return reverse('pregunta_detail', kwargs={'pk': self.object.pregunta.pk})

class RespuestaDeleteView(DeleteView):
    model = Respuesta
    template_name = 'forum/respuesta_confirm_delete.html'
    
    def get_success_url(self):
        return reverse('pregunta_detail', kwargs={'pk': self.object.pregunta.pk})
