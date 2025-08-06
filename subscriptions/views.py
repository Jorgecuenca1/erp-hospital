from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import PlanSuscripcion, Suscripcion, PagoSuscripcion
from .forms import PlanSuscripcionForm, SuscripcionForm, PagoSuscripcionForm
from django.shortcuts import get_object_or_404, redirect

# Create your views here.

# Vistas para PlanSuscripcion
class PlanSuscripcionListView(ListView):
    model = PlanSuscripcion
    template_name = 'subscriptions/plansuscripcion_list.html'
    context_object_name = 'planes_suscripcion'
    paginate_by = 10

class PlanSuscripcionDetailView(DetailView):
    model = PlanSuscripcion
    template_name = 'subscriptions/plansuscripcion_detail.html'
    context_object_name = 'plan_suscripcion'

class PlanSuscripcionCreateView(CreateView):
    model = PlanSuscripcion
    form_class = PlanSuscripcionForm
    template_name = 'subscriptions/plansuscripcion_form.html'
    success_url = reverse_lazy('plansuscripcion_list')

class PlanSuscripcionUpdateView(UpdateView):
    model = PlanSuscripcion
    form_class = PlanSuscripcionForm
    template_name = 'subscriptions/plansuscripcion_form.html'
    success_url = reverse_lazy('plansuscripcion_list')

class PlanSuscripcionDeleteView(DeleteView):
    model = PlanSuscripcion
    template_name = 'subscriptions/plansuscripcion_confirm_delete.html'
    context_object_name = 'plan_suscripcion'
    success_url = reverse_lazy('plansuscripcion_list')

# Vistas para Suscripcion
class SuscripcionListView(ListView):
    model = Suscripcion
    template_name = 'subscriptions/suscripcion_list.html'
    context_object_name = 'suscripciones'
    paginate_by = 10

class SuscripcionDetailView(DetailView):
    model = Suscripcion
    template_name = 'subscriptions/suscripcion_detail.html'
    context_object_name = 'suscripcion'

class SuscripcionCreateView(CreateView):
    model = Suscripcion
    form_class = SuscripcionForm
    template_name = 'subscriptions/suscripcion_form.html'
    success_url = reverse_lazy('suscripcion_list')

class SuscripcionUpdateView(UpdateView):
    model = Suscripcion
    form_class = SuscripcionForm
    template_name = 'subscriptions/suscripcion_form.html'
    success_url = reverse_lazy('suscripcion_list')

class SuscripcionDeleteView(DeleteView):
    model = Suscripcion
    template_name = 'subscriptions/suscripcion_confirm_delete.html'
    context_object_name = 'suscripcion'
    success_url = reverse_lazy('suscripcion_list')

# Vistas para PagoSuscripcion
class PagoSuscripcionListView(ListView):
    model = PagoSuscripcion
    template_name = 'subscriptions/pagosuscripcion_list.html'
    context_object_name = 'pagos_suscripcion'
    paginate_by = 10

class PagoSuscripcionDetailView(DetailView):
    model = PagoSuscripcion
    template_name = 'subscriptions/pagosuscripcion_detail.html'
    context_object_name = 'pago_suscripcion'

class PagoSuscripcionCreateView(CreateView):
    model = PagoSuscripcion
    form_class = PagoSuscripcionForm
    template_name = 'subscriptions/pagosuscripcion_form.html'
    
    def get_success_url(self):
        suscripcion_pk = self.object.suscripcion.pk
        return reverse('suscripcion_detail', kwargs={'pk': suscripcion_pk})

class PagoSuscripcionUpdateView(UpdateView):
    model = PagoSuscripcion
    form_class = PagoSuscripcionForm
    template_name = 'subscriptions/pagosuscripcion_form.html'
    
    def get_success_url(self):
        suscripcion_pk = self.object.suscripcion.pk
        return reverse('suscripcion_detail', kwargs={'pk': suscripcion_pk})

class PagoSuscripcionDeleteView(DeleteView):
    model = PagoSuscripcion
    template_name = 'subscriptions/pagosuscripcion_confirm_delete.html'
    context_object_name = 'pago_suscripcion'
    
    def get_success_url(self):
        suscripcion_pk = self.object.suscripcion.pk
        return reverse('suscripcion_detail', kwargs={'pk': suscripcion_pk})
