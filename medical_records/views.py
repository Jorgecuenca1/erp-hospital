from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView, View, TemplateView)
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Consulta, Diagnostico, Procedimiento, SignosVitales, NotaEvolucion, DocumentoAdjunto
from .forms import ConsultaForm, DiagnosticoForm, ProcedimientoForm, SignosVitalesForm, NotaEvolucionForm, DocumentoAdjuntoForm
from patients.models import HistoriaClinica

# Create your views here.

class MedicalRecordsDashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard principal de historias clínicas"""
    template_name = 'medical_records/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Historias Clínicas'
        context['consultas_total'] = Consulta.objects.count()
        return context

# Vistas para Consulta
class ConsultaListView(ListView):
    model = Consulta
    template_name = 'medical_records/consulta_list.html'
    context_object_name = 'consultas'
    paginate_by = 10

    def get_queryset(self):
        # Filtramos las consultas para que solo muestren las del paciente de la historia clinica (mas relevante)
        historia_clinica_id = self.kwargs.get('historia_clinica_id')
        if historia_clinica_id:
            return Consulta.objects.filter(historia_clinica__id=historia_clinica_id).order_by('-fecha_hora')
        return Consulta.objects.all().order_by('-fecha_hora')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        historia_clinica_id = self.kwargs.get('historia_clinica_id')
        if historia_clinica_id:
            context['historia_clinica'] = get_object_or_404(HistoriaClinica, id=historia_clinica_id)
        return context

class ConsultaDetailView(DetailView):
    model = Consulta
    template_name = 'medical_records/consulta_detail.html'
    context_object_name = 'consulta'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        consulta = self.get_object()
        context['diagnosticos'] = consulta.diagnosticos.all()
        context['procedimientos'] = consulta.procedimientos.all()
        context['signos_vitales'] = consulta.signos_vitales
        context['notas_evolucion'] = consulta.notas_evolucion.all()
        context['documentos_adjuntos'] = consulta.documentos_adjuntos.all()

        context['diagnostico_form'] = DiagnosticoForm(initial={'consulta': consulta})
        context['procedimiento_form'] = ProcedimientoForm(initial={'consulta': consulta})
        context['signos_vitales_form'] = SignosVitalesForm(initial={'consulta': consulta}) if not consulta.signos_vitales else None
        context['nota_evolucion_form'] = NotaEvolucionForm(initial={'consulta': consulta})
        context['documento_adjunto_form'] = DocumentoAdjuntoForm(initial={'consulta': consulta})
        return context

class ConsultaCreateView(CreateView):
    model = Consulta
    form_class = ConsultaForm
    template_name = 'medical_records/consulta_form.html'

    def get_initial(self):
        initial = super().get_initial()
        historia_clinica_id = self.kwargs.get('historia_clinica_id')
        if historia_clinica_id:
            initial['historia_clinica'] = get_object_or_404(HistoriaClinica, id=historia_clinica_id)
        return initial

    def get_success_url(self):
        return reverse_lazy('consulta_detail', kwargs={'pk': self.object.pk})

class ConsultaUpdateView(UpdateView):
    model = Consulta
    form_class = ConsultaForm
    template_name = 'medical_records/consulta_form.html'

    def get_success_url(self):
        return reverse_lazy('consulta_detail', kwargs={'pk': self.object.pk})

class ConsultaDeleteView(DeleteView):
    model = Consulta
    template_name = 'medical_records/consulta_confirm_delete.html'
    success_url = reverse_lazy('historia_clinica_list') # Redirigir a la lista de historias clínicas o pacientes

# Vistas para manejar la adición de sub-registros desde el detalle de Consulta
class AddDiagnosticoView(View):
    def post(self, request, pk):
        consulta = get_object_or_404(Consulta, pk=pk)
        form = DiagnosticoForm(request.POST)
        if form.is_valid():
            diagnostico = form.save(commit=False)
            diagnostico.consulta = consulta
            diagnostico.save()
        return redirect('consulta_detail', pk=pk)

class AddProcedimientoView(View):
    def post(self, request, pk):
        consulta = get_object_or_404(Consulta, pk=pk)
        form = ProcedimientoForm(request.POST)
        if form.is_valid():
            procedimiento = form.save(commit=False)
            procedimiento.consulta = consulta
            procedimiento.save()
        return redirect('consulta_detail', pk=pk)

class AddSignosVitalesView(View):
    def post(self, request, pk):
        consulta = get_object_or_404(Consulta, pk=pk)
        # Solo permitir un registro de signos vitales por consulta
        if consulta.signos_vitales:
            return redirect('consulta_detail', pk=pk) # O mostrar un error
        form = SignosVitalesForm(request.POST)
        if form.is_valid():
            signos_vitales = form.save(commit=False)
            signos_vitales.consulta = consulta
            signos_vitales.save()
        return redirect('consulta_detail', pk=pk)

class AddNotaEvolucionView(View):
    def post(self, request, pk):
        consulta = get_object_or_404(Consulta, pk=pk)
        form = NotaEvolucionForm(request.POST)
        if form.is_valid():
            nota_evolucion = form.save(commit=False)
            nota_evolucion.consulta = consulta
            nota_evolucion.save()
        return redirect('consulta_detail', pk=pk)

class AddDocumentoAdjuntoView(View):
    def post(self, request, pk):
        consulta = get_object_or_404(Consulta, pk=pk)
        form = DocumentoAdjuntoForm(request.POST, request.FILES)
        if form.is_valid():
            documento_adjunto = form.save(commit=False)
            documento_adjunto.consulta = consulta
            documento_adjunto.save()
        return redirect('consulta_detail', pk=pk)
