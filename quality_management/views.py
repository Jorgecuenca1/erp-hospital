from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Incidente, Auditoria, HallazgoAuditoria, PlanMejora, DocumentoCalidad
from .forms import IncidenteForm, AuditoriaForm, HallazgoAuditoriaForm, PlanMejoraForm, DocumentoCalidadForm

# Create your views here.

# Vistas para Incidente
class IncidenteListView(ListView):
    model = Incidente
    template_name = 'quality_management/incidente_list.html'
    context_object_name = 'incidentes'
    paginate_by = 10

class IncidenteDetailView(DetailView):
    model = Incidente
    template_name = 'quality_management/incidente_detail.html'
    context_object_name = 'incidente'

class IncidenteCreateView(CreateView):
    model = Incidente
    form_class = IncidenteForm
    template_name = 'quality_management/incidente_form.html'
    success_url = reverse_lazy('quality_management:incidente_list')

class IncidenteUpdateView(UpdateView):
    model = Incidente
    form_class = IncidenteForm
    template_name = 'quality_management/incidente_form.html'
    success_url = reverse_lazy('quality_management:incidente_list')

class IncidenteDeleteView(DeleteView):
    model = Incidente
    template_name = 'quality_management/incidente_confirm_delete.html'
    success_url = reverse_lazy('quality_management:incidente_list')

# Vistas para Auditoria
class AuditoriaListView(ListView):
    model = Auditoria
    template_name = 'quality_management/auditoria_list.html'
    context_object_name = 'auditorias'
    paginate_by = 10

class AuditoriaDetailView(DetailView):
    model = Auditoria
    template_name = 'quality_management/auditoria_detail.html'
    context_object_name = 'auditoria'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        auditoria = self.get_object()
        context['hallazgos'] = auditoria.hallazgos.all()
        return context

class AuditoriaCreateView(CreateView):
    model = Auditoria
    form_class = AuditoriaForm
    template_name = 'quality_management/auditoria_form.html'
    success_url = reverse_lazy('quality_management:auditoria_list')

class AuditoriaUpdateView(UpdateView):
    model = Auditoria
    form_class = AuditoriaForm
    template_name = 'quality_management/auditoria_form.html'
    success_url = reverse_lazy('quality_management:auditoria_list')

class AuditoriaDeleteView(DeleteView):
    model = Auditoria
    template_name = 'quality_management/auditoria_confirm_delete.html'
    success_url = reverse_lazy('quality_management:auditoria_list')

# Vistas para HallazgoAuditoria
class HallazgoAuditoriaListView(ListView):
    model = HallazgoAuditoria
    template_name = 'quality_management/hallazgoauditoria_list.html'
    context_object_name = 'hallazgos_auditoria'
    paginate_by = 10

class HallazgoAuditoriaDetailView(DetailView):
    model = HallazgoAuditoria
    template_name = 'quality_management/hallazgoauditoria_detail.html'
    context_object_name = 'hallazgo_auditoria'

class HallazgoAuditoriaCreateView(CreateView):
    model = HallazgoAuditoria
    form_class = HallazgoAuditoriaForm
    template_name = 'quality_management/hallazgoauditoria_form.html'
    success_url = reverse_lazy('quality_management:hallazgoauditoria_list')

    def get_initial(self):
        initial = super().get_initial()
        auditoria_pk = self.kwargs.get('auditoria_pk')
        if auditoria_pk:
            initial['auditoria'] = get_object_or_404(Auditoria, pk=auditoria_pk)
        return initial

class HallazgoAuditoriaUpdateView(UpdateView):
    model = HallazgoAuditoria
    form_class = HallazgoAuditoriaForm
    template_name = 'quality_management/hallazgoauditoria_form.html'
    success_url = reverse_lazy('quality_management:hallazgoauditoria_list')

class HallazgoAuditoriaDeleteView(DeleteView):
    model = HallazgoAuditoria
    template_name = 'quality_management/hallazgoauditoria_confirm_delete.html'
    success_url = reverse_lazy('quality_management:hallazgoauditoria_list')

# Vistas para PlanMejora
class PlanMejoraListView(ListView):
    model = PlanMejora
    template_name = 'quality_management/planmejora_list.html'
    context_object_name = 'planes_mejora'
    paginate_by = 10

class PlanMejoraDetailView(DetailView):
    model = PlanMejora
    template_name = 'quality_management/planmejora_detail.html'
    context_object_name = 'plan_mejora'

class PlanMejoraCreateView(CreateView):
    model = PlanMejora
    form_class = PlanMejoraForm
    template_name = 'quality_management/planmejora_form.html'
    success_url = reverse_lazy('quality_management:planmejora_list')

    def get_initial(self):
        initial = super().get_initial()
        hallazgo_pk = self.kwargs.get('hallazgo_pk')
        if hallazgo_pk:
            initial['hallazgo'] = get_object_or_404(HallazgoAuditoria, pk=hallazgo_pk)
        return initial

class PlanMejoraUpdateView(UpdateView):
    model = PlanMejora
    form_class = PlanMejoraForm
    template_name = 'quality_management/planmejora_form.html'
    success_url = reverse_lazy('quality_management:planmejora_list')

class PlanMejoraDeleteView(DeleteView):
    model = PlanMejora
    template_name = 'quality_management/planmejora_confirm_delete.html'
    success_url = reverse_lazy('quality_management:planmejora_list')

# Vistas para DocumentoCalidad
class DocumentoCalidadListView(ListView):
    model = DocumentoCalidad
    template_name = 'quality_management/documentocalidad_list.html'
    context_object_name = 'documentos_calidad'
    paginate_by = 10

class DocumentoCalidadDetailView(DetailView):
    model = DocumentoCalidad
    template_name = 'quality_management/documentocalidad_detail.html'
    context_object_name = 'documento_calidad'

class DocumentoCalidadCreateView(CreateView):
    model = DocumentoCalidad
    form_class = DocumentoCalidadForm
    template_name = 'quality_management/documentocalidad_form.html'
    success_url = reverse_lazy('quality_management:documentocalidad_list')

class DocumentoCalidadUpdateView(UpdateView):
    model = DocumentoCalidad
    form_class = DocumentoCalidadForm
    template_name = 'quality_management/documentocalidad_form.html'
    success_url = reverse_lazy('quality_management:documentocalidad_list')

class DocumentoCalidadDeleteView(DeleteView):
    model = DocumentoCalidad
    template_name = 'quality_management/documentocalidad_confirm_delete.html'
    success_url = reverse_lazy('quality_management:documentocalidad_list')
