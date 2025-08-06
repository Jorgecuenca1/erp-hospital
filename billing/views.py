from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView, View, TemplateView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import Factura, DetalleFactura, TransaccionDIAN
from .forms import FacturaForm, DetalleFacturaForm, TransaccionDIANForm
from django.forms import inlineformset_factory

# Inline formset para DetalleFactura
DetalleFacturaFormSet = inlineformset_factory(Factura, DetalleFactura, form=DetalleFacturaForm, extra=1, can_delete=True)

# Dashboard principal
class BillingDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'billing/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estadísticas generales
        context['total_facturas'] = Factura.objects.count()
        context['facturas_emitidas'] = Factura.objects.filter(estado='EMITIDA').count()
        context['facturas_pagadas'] = Factura.objects.filter(estado='PAGADA').count()
        context['facturas_pendientes'] = Factura.objects.filter(estado__in=['BORRADOR', 'EMITIDA']).count()
        
        # Totales monetarios
        context['total_facturado'] = Factura.objects.filter(estado__in=['EMITIDA', 'PAGADA']).aggregate(
            total=Sum('total_neto')
        )['total'] or 0
        
        context['total_pagado'] = Factura.objects.filter(estado='PAGADA').aggregate(
            total=Sum('total_neto')
        )['total'] or 0
        
        context['total_pendiente'] = Factura.objects.filter(estado='EMITIDA').aggregate(
            total=Sum('total_neto')
        )['total'] or 0
        
        # Facturas recientes
        context['facturas_recientes'] = Factura.objects.select_related('paciente').order_by('-fecha_emision')[:5]
        
        # Facturas por estado
        context['facturas_por_estado'] = Factura.objects.values('estado').annotate(count=Count('id'))
        
        # Facturas por mes (últimos 6 meses)
        context['facturas_por_mes'] = []
        for i in range(6):
            fecha = timezone.now().date() - timedelta(days=30*i)
            inicio_mes = fecha.replace(day=1)
            fin_mes = (inicio_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            
            facturas_mes = Factura.objects.filter(
                fecha_emision__date__range=[inicio_mes, fin_mes]
            ).count()
            
            total_mes = Factura.objects.filter(
                fecha_emision__date__range=[inicio_mes, fin_mes],
                estado__in=['EMITIDA', 'PAGADA']
            ).aggregate(total=Sum('total_neto'))['total'] or 0
            
            context['facturas_por_mes'].append({
                'mes': inicio_mes.strftime('%B %Y'),
                'cantidad': facturas_mes,
                'total': total_mes
            })
        
        return context

# Vistas para Factura
class FacturaListView(LoginRequiredMixin, ListView):
    model = Factura
    template_name = 'billing/factura_list.html'
    context_object_name = 'facturas'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Factura.objects.select_related('paciente').order_by('-fecha_emision')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(numero_factura__icontains=search) |
                Q(paciente__nombres__icontains=search) |
                Q(paciente__apellidos__icontains=search)
            )
        return queryset

class FacturaDetailView(LoginRequiredMixin, DetailView):
    model = Factura
    template_name = 'billing/factura_detail.html'
    context_object_name = 'factura'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        factura = self.get_object()
        context['detalles'] = factura.detalles.all()
        context['transacciones_dian'] = factura.transacciones_dian.all()
        return context

class FacturaCreateView(LoginRequiredMixin, CreateView):
    model = Factura
    form_class = FacturaForm
    template_name = 'billing/factura_form.html'
    success_url = reverse_lazy('billing:factura_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['detalles_formset'] = DetalleFacturaFormSet(self.request.POST, self.request.FILES)
        else:
            data['detalles_formset'] = DetalleFacturaFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        detalles_formset = context['detalles_formset']
        self.object = form.save()

        if detalles_formset.is_valid():
            detalles_formset.instance = self.object
            detalles_formset.save()
        else:
            return self.form_invalid(form)
        return super().form_valid(form)

class FacturaUpdateView(LoginRequiredMixin, UpdateView):
    model = Factura
    form_class = FacturaForm
    template_name = 'billing/factura_form.html'
    success_url = reverse_lazy('billing:factura_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['detalles_formset'] = DetalleFacturaFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['detalles_formset'] = DetalleFacturaFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        detalles_formset = context['detalles_formset']
        self.object = form.save()

        if detalles_formset.is_valid():
            detalles_formset.instance = self.object
            detalles_formset.save()
        else:
            return self.form_invalid(form)
        return super().form_valid(form)

class FacturaDeleteView(LoginRequiredMixin, DeleteView):
    model = Factura
    template_name = 'billing/factura_confirm_delete.html'
    success_url = reverse_lazy('billing:factura_list')

# Vistas para DetalleFactura
class DetalleFacturaListView(LoginRequiredMixin, ListView):
    model = DetalleFactura
    template_name = 'billing/detalle_factura_list.html'
    context_object_name = 'detalles'
    paginate_by = 20

class DetalleFacturaDetailView(LoginRequiredMixin, DetailView):
    model = DetalleFactura
    template_name = 'billing/detalle_factura_detail.html'
    context_object_name = 'detalle'

class DetalleFacturaCreateView(LoginRequiredMixin, CreateView):
    model = DetalleFactura
    form_class = DetalleFacturaForm
    template_name = 'billing/detalle_factura_form.html'
    success_url = reverse_lazy('billing:detalle_factura_list')

class DetalleFacturaUpdateView(LoginRequiredMixin, UpdateView):
    model = DetalleFactura
    form_class = DetalleFacturaForm
    template_name = 'billing/detalle_factura_form.html'
    success_url = reverse_lazy('billing:detalle_factura_list')

class DetalleFacturaDeleteView(LoginRequiredMixin, DeleteView):
    model = DetalleFactura
    template_name = 'billing/detalle_factura_confirm_delete.html'
    success_url = reverse_lazy('billing:detalle_factura_list')

# Vistas para TransaccionDIAN
class TransaccionDIANListView(LoginRequiredMixin, ListView):
    model = TransaccionDIAN
    template_name = 'billing/transaccion_dian_list.html'
    context_object_name = 'transacciones'
    paginate_by = 20

class TransaccionDIANDetailView(LoginRequiredMixin, DetailView):
    model = TransaccionDIAN
    template_name = 'billing/transaccion_dian_detail.html'
    context_object_name = 'transaccion'

class TransaccionDIANCreateView(LoginRequiredMixin, CreateView):
    model = TransaccionDIAN
    form_class = TransaccionDIANForm
    template_name = 'billing/transaccion_dian_form.html'
    success_url = reverse_lazy('billing:transaccion_dian_list')

class TransaccionDIANUpdateView(LoginRequiredMixin, UpdateView):
    model = TransaccionDIAN
    form_class = TransaccionDIANForm
    template_name = 'billing/transaccion_dian_form.html'
    success_url = reverse_lazy('billing:transaccion_dian_list')

class TransaccionDIANDeleteView(LoginRequiredMixin, DeleteView):
    model = TransaccionDIAN
    template_name = 'billing/transaccion_dian_confirm_delete.html'
    success_url = reverse_lazy('billing:transaccion_dian_list')

# Vistas para Reportes
class BillingReportsView(LoginRequiredMixin, TemplateView):
    template_name = 'billing/reports.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estadísticas para reportes
        context['total_facturas'] = Factura.objects.count()
        context['facturas_por_estado'] = Factura.objects.values('estado').annotate(count=Count('id'))
        
        # Totales por estado
        context['totales_por_estado'] = Factura.objects.values('estado').annotate(
            total=Sum('total_neto'),
            count=Count('id')
        )
        
        # Top 5 pacientes con más facturas
        context['top_pacientes'] = Factura.objects.values(
            'paciente__nombres', 'paciente__apellidos'
        ).annotate(
            total_facturas=Count('id'),
            total_facturado=Sum('total_neto')
        ).order_by('-total_facturado')[:5]
        
        # Facturas por mes (últimos 12 meses)
        context['facturas_por_mes'] = []
        for i in range(12):
            fecha = timezone.now().date() - timedelta(days=30*i)
            inicio_mes = fecha.replace(day=1)
            fin_mes = (inicio_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            
            facturas_mes = Factura.objects.filter(
                fecha_emision__date__range=[inicio_mes, fin_mes]
            ).count()
            
            total_mes = Factura.objects.filter(
                fecha_emision__date__range=[inicio_mes, fin_mes],
                estado__in=['EMITIDA', 'PAGADA']
            ).aggregate(total=Sum('total_neto'))['total'] or 0
            
            context['facturas_por_mes'].append({
                'mes': inicio_mes.strftime('%B %Y'),
                'cantidad': facturas_mes,
                'total': total_mes
            })
        
        return context

# Vistas para facturas pendientes
class FacturasPendientesView(LoginRequiredMixin, ListView):
    model = Factura
    template_name = 'billing/facturas_pendientes.html'
    context_object_name = 'facturas'
    paginate_by = 20
    
    def get_queryset(self):
        return Factura.objects.filter(
            estado__in=['BORRADOR', 'EMITIDA']
        ).select_related('paciente').order_by('fecha_vencimiento')

# Vistas para facturas vencidas
class FacturasVencidasView(LoginRequiredMixin, ListView):
    model = Factura
    template_name = 'billing/facturas_vencidas.html'
    context_object_name = 'facturas'
    paginate_by = 20
    
    def get_queryset(self):
        return Factura.objects.filter(
            estado__in=['EMITIDA'],
            fecha_vencimiento__lt=timezone.now().date()
        ).select_related('paciente').order_by('fecha_vencimiento')
