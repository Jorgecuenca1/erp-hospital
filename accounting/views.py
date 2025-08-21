from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import datetime
from .models import (
    PeriodoContable, CuentaContable, Tercero, Diario, Impuesto, 
    AsientoContable, LineaAsiento, DatosEmpresa, CentroCosto, 
    ComprobanteContable, CertificadoRetencion, MovimientoBancario, CierreContable, Presupuesto,
    ReporteFiscal, Pais, Departamento, Ciudad
)
from .forms import (
    PeriodoContableForm, CuentaContableForm, TerceroForm, DiarioForm, 
    ImpuestoForm, AsientoContableForm, LineaAsientoForm, LineaAsientoFormSet,
    DatosEmpresaForm, CentroCostoForm, ComprobanteContableForm, CertificadoRetencionForm,
    MovimientoBancarioForm, CierreContableForm, PresupuestoForm
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

# Create your views here.

# Dashboard
class AccountingDashboardView(TemplateView):
    template_name = 'accounting/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['asientos_count'] = AsientoContable.objects.count()
        context['cuentas_count'] = CuentaContable.objects.count()
        context['terceros_count'] = Tercero.objects.count()
        context['periodos_activos'] = PeriodoContable.objects.filter(cerrado=False).count()
        return context

# PeriodoContable
class PeriodoContableListView(ListView):
    model = PeriodoContable
class PeriodoContableDetailView(DetailView):
    model = PeriodoContable
class PeriodoContableCreateView(CreateView):
    model = PeriodoContable
    form_class = PeriodoContableForm
    success_url = reverse_lazy('accounting:periodocontable_list')
class PeriodoContableUpdateView(UpdateView):
    model = PeriodoContable
    form_class = PeriodoContableForm
    success_url = reverse_lazy('accounting:periodocontable_list')
class PeriodoContableDeleteView(DeleteView):
    model = PeriodoContable
    success_url = reverse_lazy('accounting:periodocontable_list')

# CuentaContable
class CuentaContableListView(ListView):
    model = CuentaContable
class CuentaContableDetailView(DetailView):
    model = CuentaContable
class CuentaContableCreateView(CreateView):
    model = CuentaContable
    form_class = CuentaContableForm
    success_url = reverse_lazy('accounting:cuentacontable_list')
class CuentaContableUpdateView(UpdateView):
    model = CuentaContable
    form_class = CuentaContableForm
    success_url = reverse_lazy('accounting:cuentacontable_list')
class CuentaContableDeleteView(DeleteView):
    model = CuentaContable
    success_url = reverse_lazy('accounting:cuentacontable_list')

# Tercero
class TerceroListView(ListView):
    model = Tercero
class TerceroDetailView(DetailView):
    model = Tercero
class TerceroCreateView(CreateView):
    model = Tercero
    form_class = TerceroForm
    success_url = reverse_lazy('accounting:tercero_list')
class TerceroUpdateView(UpdateView):
    model = Tercero
    form_class = TerceroForm
    success_url = reverse_lazy('accounting:tercero_list')
class TerceroDeleteView(DeleteView):
    model = Tercero
    success_url = reverse_lazy('accounting:tercero_list')

# Diario
class DiarioListView(ListView):
    model = Diario
class DiarioDetailView(DetailView):
    model = Diario
class DiarioCreateView(CreateView):
    model = Diario
    form_class = DiarioForm
    success_url = reverse_lazy('accounting:diario_list')
class DiarioUpdateView(UpdateView):
    model = Diario
    form_class = DiarioForm
    success_url = reverse_lazy('accounting:diario_list')
class DiarioDeleteView(DeleteView):
    model = Diario
    success_url = reverse_lazy('accounting:diario_list')

# Impuesto
class ImpuestoListView(ListView):
    model = Impuesto
class ImpuestoDetailView(DetailView):
    model = Impuesto
class ImpuestoCreateView(CreateView):
    model = Impuesto
    form_class = ImpuestoForm
    success_url = reverse_lazy('accounting:impuesto_list')
class ImpuestoUpdateView(UpdateView):
    model = Impuesto
    form_class = ImpuestoForm
    success_url = reverse_lazy('accounting:impuesto_list')
class ImpuestoDeleteView(DeleteView):
    model = Impuesto
    success_url = reverse_lazy('accounting:impuesto_list')

# AsientoContable
class AsientoContableListView(ListView):
    model = AsientoContable
    ordering = ['-fecha', '-id']
    paginate_by = 20

class AsientoContableDetailView(DetailView):
    model = AsientoContable

class AsientoContableCreateView(CreateView):
    model = AsientoContable
    form_class = AsientoContableForm
    template_name = 'accounting/asientocontable_form.html'
    success_url = reverse_lazy('accounting:asientocontable_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['linea_formset'] = LineaAsientoFormSet(self.request.POST, instance=self.object)
        else:
            context['linea_formset'] = LineaAsientoFormSet(instance=self.object)
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        linea_formset = context['linea_formset']
        if form.is_valid() and linea_formset.is_valid():
            self.object = form.save(commit=False)
            self.object.creado_por = self.request.user
            self.object.save()
            linea_formset.instance = self.object
            linea_formset.save()
            return super().form_valid(form)
        return self.render_to_response(self.get_context_data(form=form))

class AsientoContableUpdateView(UpdateView):
    model = AsientoContable
    form_class = AsientoContableForm
    template_name = 'accounting/asientocontable_form.html'
    success_url = reverse_lazy('accounting:asientocontable_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['linea_formset'] = LineaAsientoFormSet(self.request.POST, instance=self.object)
        else:
            context['linea_formset'] = LineaAsientoFormSet(instance=self.object)
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        linea_formset = context['linea_formset']
        if form.is_valid() and linea_formset.is_valid():
            self.object = form.save()
            linea_formset.instance = self.object
            linea_formset.save()
            return super().form_valid(form)
        return self.render_to_response(self.get_context_data(form=form))

class AsientoContableDeleteView(DeleteView):
    model = AsientoContable
    success_url = reverse_lazy('accounting:asientocontable_list')

# Reportes
class ReportesView(TemplateView):
    template_name = 'accounting/reportes.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener parámetros de filtro
        periodo_id = self.request.GET.get('periodo')
        fecha_inicio = self.request.GET.get('fecha_inicio')
        fecha_fin = self.request.GET.get('fecha_fin')
        tipo_reporte = self.request.GET.get('tipo_reporte', 'general')
        banco = self.request.GET.get('banco')
        
        # Datos básicos para el contexto
        context['periodos'] = PeriodoContable.objects.all()
        context['bancos'] = MovimientoBancario.objects.values_list('banco', flat=True).distinct()
        
        # Filtrar movimientos bancarios
        movimientos = MovimientoBancario.objects.all()
        
        if banco:
            movimientos = movimientos.filter(banco=banco)
        
        if fecha_inicio:
            try:
                fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
                movimientos = movimientos.filter(fecha__gte=fecha_inicio)
            except ValueError:
                pass
        
        if fecha_fin:
            try:
                fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
                movimientos = movimientos.filter(fecha__lte=fecha_fin)
            except ValueError:
                pass
        
        # Reporte Bancario
        if tipo_reporte == 'banco' or not tipo_reporte:
            context['movimientos_bancarios'] = movimientos.order_by('-fecha', '-id')
        
        # Conciliación Bancaria
        elif tipo_reporte == 'conciliacion':
            movimientos_conciliados = movimientos.filter(conciliado=True)
            movimientos_pendientes = movimientos.filter(conciliado=False)
            
            context['movimientos_conciliados'] = movimientos_conciliados.order_by('-fecha')
            context['movimientos_pendientes'] = movimientos_pendientes.order_by('-fecha')
            
            # Cálculos de conciliación
            total_conciliado = movimientos_conciliados.aggregate(total=Sum('valor'))['total'] or 0
            total_pendiente = movimientos_pendientes.aggregate(total=Sum('valor'))['total'] or 0
            total_movimientos = total_conciliado + total_pendiente
            
            context['total_conciliado'] = total_conciliado
            context['total_pendiente'] = total_pendiente
            context['porcentaje_conciliado'] = (total_conciliado / total_movimientos * 100) if total_movimientos > 0 else 0
            context['diferencia_conciliacion'] = total_conciliado - total_pendiente
        
        # Movimientos Detallados
        elif tipo_reporte == 'movimientos':
            context['movimientos_detallados'] = movimientos.order_by('-fecha', '-id')
        
        # Flujo de Efectivo
        elif tipo_reporte == 'flujo_efectivo':
            # Simulación de flujo de efectivo basado en movimientos bancarios
            context['flujo_efectivo'] = {
                'operacionales': [
                    {'concepto': 'Ingresos Operacionales', 'monto': 5000000, 'descripcion': 'Ventas y servicios'},
                    {'concepto': 'Gastos Operacionales', 'monto': -3000000, 'descripcion': 'Gastos de operación'},
                    {'concepto': 'Impuestos Pagados', 'monto': -500000, 'descripcion': 'IVA y otros impuestos'},
                ],
                'inversion': [
                    {'concepto': 'Compra de Activos', 'monto': -1000000, 'descripcion': 'Equipos y maquinaria'},
                    {'concepto': 'Inversiones', 'monto': -500000, 'descripcion': 'Inversiones financieras'},
                ],
                'financiacion': [
                    {'concepto': 'Préstamos Recibidos', 'monto': 2000000, 'descripcion': 'Financiamiento bancario'},
                    {'concepto': 'Pago de Deudas', 'monto': -800000, 'descripcion': 'Amortización de préstamos'},
                ],
                'neto_operacional': 1500000,
                'neto_inversion': -1500000,
                'neto_financiacion': 1200000,
                'cambio_neto': 1200000
            }

        # Análisis Presupuestal
        elif tipo_reporte == 'presupuesto':
            presupuestos = Presupuesto.objects.all()
            if periodo_id:
                presupuestos = presupuestos.filter(periodo_id=periodo_id)
            
            analisis_presupuestal = []
            for presupuesto in presupuestos:
                variacion = presupuesto.monto_real - presupuesto.monto_presupuestado
                porcentaje_variacion = presupuesto.variacion_porcentual()
                
                analisis_presupuestal.append({
                    'cuenta': presupuesto.cuenta,
                    'centro_costo': presupuesto.centro_costo,
                    'presupuestado': presupuesto.monto_presupuestado,
                    'real': presupuesto.monto_real,
                    'variacion': variacion,
                    'porcentaje_variacion': porcentaje_variacion
                })
            
            context['analisis_presupuestal'] = analisis_presupuestal

        # Análisis de Costos
        elif tipo_reporte == 'costos':
            # Simulación de análisis de costos
            context['analisis_costos'] = [
                {
                    'centro_costo': {'nombre': 'Administración'},
                    'costos_directos': 2000000,
                    'costos_indirectos': 500000,
                    'total_costos': 2500000,
                    'porcentaje_total': 25.0
                },
                {
                    'centro_costo': {'nombre': 'Ventas'},
                    'costos_directos': 1500000,
                    'costos_indirectos': 300000,
                    'total_costos': 1800000,
                    'porcentaje_total': 18.0
                },
                {
                    'centro_costo': {'nombre': 'Producción'},
                    'costos_directos': 4000000,
                    'costos_indirectos': 800000,
                    'total_costos': 4800000,
                    'porcentaje_total': 48.0
                }
            ]

        # Reportes Fiscales
        elif tipo_reporte == 'fiscal':
            # Simulación de datos fiscales
            context['iva_data'] = {
                'base_gravable': 10000000,
                'iva_generado': 1900000,
                'iva_descontable': 1200000,
                'iva_a_pagar': 700000
            }
            
            context['retenciones_data'] = {
                'base_retencion': 8000000,
                'retencion_fuente': 400000,
                'ica': 80000,
                'total_retenciones': 480000
            }

        # Reportes de Auditoría
        elif tipo_reporte == 'auditoria':
            # Obtener logs de auditoría (si existe el modelo AuditLog)
            try:
                from .models import AuditLog
                context['auditoria_data'] = AuditLog.objects.all().order_by('-fecha')[:100]
            except:
                context['auditoria_data'] = []

        # Indicadores Financieros
        elif tipo_reporte == 'indicadores':
            # Simulación de indicadores financieros
            context['indicadores_financieros'] = {
                'razon_corriente': 1.85,
                'razon_acida': 1.25,
                'capital_trabajo': 2500000,
                'razon_endeudamiento': 45.5,
                'razon_patrimonio': 54.5,
                'razon_cobertura': 2.8,
                'margen_bruto': 35.2,
                'margen_operacional': 18.5,
                'roa': 12.3,
                'roe': 22.8,
                'rotacion_activos': 1.8,
                'rotacion_inventarios': 6.5,
                'periodo_cobranza': 45
            }

        # Análisis de Cartera
        elif tipo_reporte == 'cartera':
            # Simulación de análisis de cartera
            context['cuentas_por_cobrar'] = [
                {
                    'tercero': {'nombre': 'Cliente A'},
                    'saldo': 1500000,
                    'dias_vencido': 15
                },
                {
                    'tercero': {'nombre': 'Cliente B'},
                    'saldo': 800000,
                    'dias_vencido': 45
                },
                {
                    'tercero': {'nombre': 'Cliente C'},
                    'saldo': 1200000,
                    'dias_vencido': 90
                }
            ]
            
            context['cuentas_por_pagar'] = [
                {
                    'tercero': {'nombre': 'Proveedor X'},
                    'saldo': 500000,
                    'dias_vencido': 30
                },
                {
                    'tercero': {'nombre': 'Proveedor Y'},
                    'saldo': 300000,
                    'dias_vencido': 60
                }
            ]
            
            context['total_por_cobrar'] = 3500000
            context['total_por_pagar'] = 800000
            context['neto_cartera'] = 2700000
            context['antiguedad_promedio'] = 45

        # Reportes Generales (Balance, Estado de Resultados, etc.)
        if not tipo_reporte or tipo_reporte == 'general':
            # Filtrar asientos contables
            asientos = AsientoContable.objects.all()
            
            if periodo_id:
                asientos = asientos.filter(periodo_id=periodo_id)
            
            if fecha_inicio:
                try:
                    fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
                    asientos = asientos.filter(fecha__gte=fecha_inicio)
                except ValueError:
                    pass
            
            if fecha_fin:
                try:
                    fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
                    asientos = asientos.filter(fecha__lte=fecha_fin)
                except ValueError:
                    pass
            
            context['asientos'] = asientos.order_by('-fecha', '-id')[:100]  # Últimos 100 asientos
            
            # Estadísticas
            lineas = LineaAsiento.objects.filter(asiento__in=asientos)
            context['total_asientos'] = asientos.count()
            context['total_debitos'] = lineas.aggregate(total=Sum('debito'))['total'] or 0
            context['total_creditos'] = lineas.aggregate(total=Sum('credito'))['total'] or 0
            context['balance'] = context['total_debitos'] - context['total_creditos']
            
            # Balance General (simplificado)
            balance_general = []
            cuentas = CuentaContable.objects.filter(activa=True)
            
            for cuenta in cuentas:
                saldo = lineas.filter(cuenta=cuenta).aggregate(
                    saldo=Sum('debito') - Sum('credito')
                )['saldo'] or 0
                
                if saldo != 0:
                    balance_general.append({
                        'codigo': cuenta.codigo,
                        'nombre': cuenta.nombre,
                        'saldo': saldo
                    })
            
            context['balance_general'] = balance_general
            
            # Estado de Resultados (simplificado)
            ingresos = lineas.filter(cuenta__tipo='INGRESO').aggregate(total=Sum('credito') - Sum('debito'))['total'] or 0
            gastos = lineas.filter(cuenta__tipo='GASTO').aggregate(total=Sum('debito') - Sum('credito'))['total'] or 0
            
            context['estado_resultados'] = [
                {'nombre': 'Ingresos', 'monto': ingresos},
                {'nombre': 'Gastos', 'monto': -gastos},
                {'nombre': 'Resultado Neto', 'monto': ingresos - gastos}
            ]
        
        return context

# DatosEmpresa
class DatosEmpresaListView(ListView):
    model = DatosEmpresa
    template_name = 'accounting/datosempresa_list.html'

class DatosEmpresaDetailView(DetailView):
    model = DatosEmpresa
    template_name = 'accounting/datosempresa_detail.html'

class DatosEmpresaCreateView(CreateView):
    model = DatosEmpresa
    form_class = DatosEmpresaForm
    template_name = 'accounting/datosempresa_form.html'
    success_url = reverse_lazy('accounting:datosempresa_list')

class DatosEmpresaUpdateView(UpdateView):
    model = DatosEmpresa
    form_class = DatosEmpresaForm
    template_name = 'accounting/datosempresa_form.html'
    success_url = reverse_lazy('accounting:datosempresa_list')

class DatosEmpresaDeleteView(DeleteView):
    model = DatosEmpresa
    template_name = 'accounting/datosempresa_confirm_delete.html'
    success_url = reverse_lazy('accounting:datosempresa_list')

# CentroCosto
class CentroCostoListView(ListView):
    model = CentroCosto
    template_name = 'accounting/centrocosto_list.html'

class CentroCostoDetailView(DetailView):
    model = CentroCosto
    template_name = 'accounting/centrocosto_detail.html'

class CentroCostoCreateView(CreateView):
    model = CentroCosto
    form_class = CentroCostoForm
    template_name = 'accounting/centrocosto_form.html'
    success_url = reverse_lazy('accounting:centrocosto_list')

class CentroCostoUpdateView(UpdateView):
    model = CentroCosto
    form_class = CentroCostoForm
    template_name = 'accounting/centrocosto_form.html'
    success_url = reverse_lazy('accounting:centrocosto_list')

class CentroCostoDeleteView(DeleteView):
    model = CentroCosto
    template_name = 'accounting/centrocosto_confirm_delete.html'
    success_url = reverse_lazy('accounting:centrocosto_list')

# ComprobanteContable
class ComprobanteContableListView(ListView):
    model = ComprobanteContable
    template_name = 'accounting/comprobantecontable_list.html'
    ordering = ['-fecha', '-id']
    paginate_by = 20

class ComprobanteContableDetailView(DetailView):
    model = ComprobanteContable
    template_name = 'accounting/comprobantecontable_detail.html'

class ComprobanteContableCreateView(CreateView):
    model = ComprobanteContable
    form_class = ComprobanteContableForm
    template_name = 'accounting/comprobantecontable_form.html'
    success_url = reverse_lazy('accounting:comprobantecontable_list')
    
    def form_valid(self, form):
        if not form.instance.numero:
            form.instance.numero = form.instance.generar_numero()
        form.instance.creado_por = self.request.user
        return super().form_valid(form)

class ComprobanteContableUpdateView(UpdateView):
    model = ComprobanteContable
    form_class = ComprobanteContableForm
    template_name = 'accounting/comprobantecontable_form.html'
    success_url = reverse_lazy('accounting:comprobantecontable_list')

class ComprobanteContableDeleteView(DeleteView):
    model = ComprobanteContable
    template_name = 'accounting/comprobantecontable_confirm_delete.html'
    success_url = reverse_lazy('accounting:comprobantecontable_list')

# CertificadoRetencion
class CertificadoRetencionListView(ListView):
    model = CertificadoRetencion
    template_name = 'accounting/certificadoretencion_list.html'
    ordering = ['-fecha', '-id']
    paginate_by = 20

class CertificadoRetencionDetailView(DetailView):
    model = CertificadoRetencion
    template_name = 'accounting/certificadoretencion_detail.html'

class CertificadoRetencionCreateView(CreateView):
    model = CertificadoRetencion
    form_class = CertificadoRetencionForm
    template_name = 'accounting/certificadoretencion_form.html'
    success_url = reverse_lazy('accounting:certificadoretencion_list')
    
    def form_valid(self, form):
        form.instance.creado_por = self.request.user
        form.instance.calcular_retencion()
        return super().form_valid(form)

class CertificadoRetencionUpdateView(UpdateView):
    model = CertificadoRetencion
    form_class = CertificadoRetencionForm
    template_name = 'accounting/certificadoretencion_form.html'
    success_url = reverse_lazy('accounting:certificadoretencion_list')
    
    def form_valid(self, form):
        form.instance.calcular_retencion()
        return super().form_valid(form)

class CertificadoRetencionDeleteView(DeleteView):
    model = CertificadoRetencion
    template_name = 'accounting/certificadoretencion_confirm_delete.html'
    success_url = reverse_lazy('accounting:certificadoretencion_list')

# LineaAsiento
class LineaAsientoListView(ListView):
    model = LineaAsiento
class LineaAsientoDetailView(DetailView):
    model = LineaAsiento
class LineaAsientoCreateView(CreateView):
    model = LineaAsiento
    form_class = LineaAsientoForm
    success_url = reverse_lazy('accounting:lineaasiento_list')
class LineaAsientoUpdateView(UpdateView):
    model = LineaAsiento
    form_class = LineaAsientoForm
    success_url = reverse_lazy('accounting:lineaasiento_list')
class LineaAsientoDeleteView(DeleteView):
    model = LineaAsiento
    success_url = reverse_lazy('accounting:lineaasiento_list')

# Nuevas views para funcionalidades agregadas
# MovimientoBancario
class MovimientoBancarioListView(ListView):
    model = MovimientoBancario
    template_name = 'accounting/movimientobancario_list.html'
    ordering = ['-fecha', '-id']
    paginate_by = 20

class MovimientoBancarioDetailView(DetailView):
    model = MovimientoBancario
    template_name = 'accounting/movimientobancario_detail.html'

class MovimientoBancarioCreateView(CreateView):
    model = MovimientoBancario
    form_class = MovimientoBancarioForm
    template_name = 'accounting/movimientobancario_form.html'
    success_url = reverse_lazy('accounting:movimientobancario_list')
    
    def form_valid(self, form):
        form.instance.creado_por = self.request.user
        return super().form_valid(form)

class MovimientoBancarioUpdateView(UpdateView):
    model = MovimientoBancario
    form_class = MovimientoBancarioForm
    template_name = 'accounting/movimientobancario_form.html'
    success_url = reverse_lazy('accounting:movimientobancario_list')

class MovimientoBancarioDeleteView(DeleteView):
    model = MovimientoBancario
    template_name = 'accounting/movimientobancario_confirm_delete.html'
    success_url = reverse_lazy('accounting:movimientobancario_list')

# CierreContable
class CierreContableListView(ListView):
    model = CierreContable
    template_name = 'accounting/cierrecontable_list.html'
    ordering = ['-fecha_cierre']
    paginate_by = 20

class CierreContableDetailView(DetailView):
    model = CierreContable
    template_name = 'accounting/cierrecontable_detail.html'

class CierreContableCreateView(CreateView):
    model = CierreContable
    form_class = CierreContableForm
    template_name = 'accounting/cierrecontable_form.html'
    success_url = reverse_lazy('accounting:cierrecontable_list')
    
    def form_valid(self, form):
        form.instance.cerrado_por = self.request.user
        return super().form_valid(form)

class CierreContableUpdateView(UpdateView):
    model = CierreContable
    form_class = CierreContableForm
    template_name = 'accounting/cierrecontable_form.html'
    success_url = reverse_lazy('accounting:cierrecontable_list')

class CierreContableDeleteView(DeleteView):
    model = CierreContable
    template_name = 'accounting/cierrecontable_confirm_delete.html'
    success_url = reverse_lazy('accounting:cierrecontable_list')

# Presupuesto
class PresupuestoListView(ListView):
    model = Presupuesto
    template_name = 'accounting/presupuesto_list.html'
    ordering = ['periodo', 'cuenta__codigo']
    paginate_by = 20

class PresupuestoDetailView(DetailView):
    model = Presupuesto
    template_name = 'accounting/presupuesto_detail.html'

class PresupuestoCreateView(CreateView):
    model = Presupuesto
    form_class = PresupuestoForm
    template_name = 'accounting/presupuesto_form.html'
    success_url = reverse_lazy('accounting:presupuesto_list')
    
    def form_valid(self, form):
        form.instance.creado_por = self.request.user
        return super().form_valid(form)

class PresupuestoUpdateView(UpdateView):
    model = Presupuesto
    form_class = PresupuestoForm
    template_name = 'accounting/presupuesto_form.html'
    success_url = reverse_lazy('accounting:presupuesto_list')

class PresupuestoDeleteView(DeleteView):
    model = Presupuesto
    template_name = 'accounting/presupuesto_confirm_delete.html'
    success_url = reverse_lazy('accounting:presupuesto_list')

class GenerarReporteFiscalView(LoginRequiredMixin, CreateView):
    """Vista para generar reportes fiscales"""
    model = ReporteFiscal
    template_name = 'accounting/generar_reporte_fiscal.html'
    fields = ['tipo', 'periodo', 'fecha_inicio', 'fecha_fin', 'observaciones']
    
    def form_valid(self, form):
        form.instance.generado_por = self.request.user
        response = super().form_valid(form)
        
        # Calcular totales automáticamente
        self.object.calcular_totales()
        
        messages.success(self.request, f'Reporte fiscal {self.object.get_tipo_display()} generado exitosamente.')
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['periodos'] = PeriodoContable.objects.filter(activo=True)
        return context

class ReporteFiscalListView(LoginRequiredMixin, ListView):
    """Lista de reportes fiscales generados"""
    model = ReporteFiscal
    template_name = 'accounting/reportefiscal_list.html'
    context_object_name = 'reportes'
    paginate_by = 20

class ReporteFiscalDetailView(LoginRequiredMixin, DetailView):
    """Detalle de reporte fiscal"""
    model = ReporteFiscal
    template_name = 'accounting/reportefiscal_detail.html'
    context_object_name = 'reporte'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detalles'] = self.object.detalles.all().order_by('fecha')
        return context

class ReporteFiscalUpdateView(LoginRequiredMixin, UpdateView):
    """Actualizar reporte fiscal"""
    model = ReporteFiscal
    template_name = 'accounting/reportefiscal_form.html'
    fields = ['estado', 'observaciones']
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Reporte fiscal actualizado exitosamente.')
        return response

class ReporteFiscalDeleteView(LoginRequiredMixin, DeleteView):
    """Eliminar reporte fiscal"""
    model = ReporteFiscal
    template_name = 'accounting/reportefiscal_confirm_delete.html'
    success_url = reverse_lazy('accounting:reportefiscal_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Reporte fiscal eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)

# ==================== GESTIÓN GEOGRÁFICA ====================

# País
class PaisListView(LoginRequiredMixin, ListView):
    model = Pais
    template_name = 'accounting/pais_list.html'
    context_object_name = 'paises'
    paginate_by = 20

class PaisCreateView(LoginRequiredMixin, CreateView):
    model = Pais
    template_name = 'accounting/pais_form.html'
    fields = ['codigo', 'nombre']
    success_url = reverse_lazy('accounting:pais_list')

class PaisUpdateView(LoginRequiredMixin, UpdateView):
    model = Pais
    template_name = 'accounting/pais_form.html'
    fields = ['codigo', 'nombre']
    success_url = reverse_lazy('accounting:pais_list')

class PaisDeleteView(LoginRequiredMixin, DeleteView):
    model = Pais
    template_name = 'accounting/pais_confirm_delete.html'
    success_url = reverse_lazy('accounting:pais_list')

# Departamento
class DepartamentoListView(LoginRequiredMixin, ListView):
    model = Departamento
    template_name = 'accounting/departamento_list.html'
    context_object_name = 'departamentos'
    paginate_by = 20

class DepartamentoCreateView(LoginRequiredMixin, CreateView):
    model = Departamento
    template_name = 'accounting/departamento_form.html'
    fields = ['codigo', 'nombre', 'pais']
    success_url = reverse_lazy('accounting:departamento_list')

class DepartamentoUpdateView(LoginRequiredMixin, UpdateView):
    model = Departamento
    template_name = 'accounting/departamento_form.html'
    fields = ['codigo', 'nombre', 'pais']
    success_url = reverse_lazy('accounting:departamento_list')

class DepartamentoDeleteView(LoginRequiredMixin, DeleteView):
    model = Departamento
    template_name = 'accounting/departamento_confirm_delete.html'
    success_url = reverse_lazy('accounting:departamento_list')

# Ciudad
class CiudadListView(LoginRequiredMixin, ListView):
    model = Ciudad
    template_name = 'accounting/ciudad_list.html'
    context_object_name = 'ciudades'
    paginate_by = 20

class CiudadCreateView(LoginRequiredMixin, CreateView):
    model = Ciudad
    template_name = 'accounting/ciudad_form.html'
    fields = ['codigo', 'nombre', 'departamento']
    success_url = reverse_lazy('accounting:ciudad_list')

class CiudadUpdateView(LoginRequiredMixin, UpdateView):
    model = Ciudad
    template_name = 'accounting/ciudad_form.html'
    fields = ['codigo', 'nombre', 'departamento']
    success_url = reverse_lazy('accounting:ciudad_list')

class CiudadDeleteView(LoginRequiredMixin, DeleteView):
    model = Ciudad
    template_name = 'accounting/ciudad_confirm_delete.html'
    success_url = reverse_lazy('accounting:ciudad_list')


# =================== REPORTES AVANZADOS ===================

class BalanceGeneralView(LoginRequiredMixin, TemplateView):
    """Reporte de Balance General"""
    template_name = 'accounting/reportes/balance_general.html'
    login_url = '/admin/login/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Parámetros
        fecha_corte = self.request.GET.get('fecha_corte')
        if fecha_corte:
            try:
                fecha_corte = datetime.strptime(fecha_corte, '%Y-%m-%d').date()
            except ValueError:
                fecha_corte = timezone.now().date()
        else:
            fecha_corte = timezone.now().date()
        
        context['fecha_corte'] = fecha_corte
        
        # ACTIVOS
        # Activos Corrientes
        cuentas_activo_corriente = CuentaContable.objects.filter(
            codigo__startswith='1', tipo='ACTIVO'
        )
        
        activos_corrientes = []
        total_activo_corriente = 0
        
        for cuenta in cuentas_activo_corriente:
            # Calcular saldo de la cuenta
            movimientos = LineaAsiento.objects.filter(
                cuenta_contable=cuenta,
                asiento_contable__fecha__lte=fecha_corte
            )
            
            saldo_debito = movimientos.aggregate(Sum('debito'))['debito__sum'] or 0
            saldo_credito = movimientos.aggregate(Sum('credito'))['credito__sum'] or 0
            saldo_final = saldo_debito - saldo_credito
            
            if saldo_final != 0:
                activos_corrientes.append({
                    'cuenta': cuenta,
                    'saldo': saldo_final
                })
                total_activo_corriente += saldo_final
        
        # PASIVOS
        cuentas_pasivo = CuentaContable.objects.filter(
            codigo__startswith='2', tipo='PASIVO'
        )
        
        pasivos = []
        total_pasivo = 0
        
        for cuenta in cuentas_pasivo:
            movimientos = LineaAsiento.objects.filter(
                cuenta_contable=cuenta,
                asiento_contable__fecha__lte=fecha_corte
            )
            
            saldo_debito = movimientos.aggregate(Sum('debito'))['debito__sum'] or 0
            saldo_credito = movimientos.aggregate(Sum('credito'))['credito__sum'] or 0
            saldo_final = saldo_credito - saldo_debito  # Para pasivos es al revés
            
            if saldo_final != 0:
                pasivos.append({
                    'cuenta': cuenta,
                    'saldo': saldo_final
                })
                total_pasivo += saldo_final
        
        # PATRIMONIO
        cuentas_patrimonio = CuentaContable.objects.filter(
            codigo__startswith='3', tipo='PATRIMONIO'
        )
        
        patrimonio = []
        total_patrimonio = 0
        
        for cuenta in cuentas_patrimonio:
            movimientos = LineaAsiento.objects.filter(
                cuenta_contable=cuenta,
                asiento_contable__fecha__lte=fecha_corte
            )
            
            saldo_debito = movimientos.aggregate(Sum('debito'))['debito__sum'] or 0
            saldo_credito = movimientos.aggregate(Sum('credito'))['credito__sum'] or 0
            saldo_final = saldo_credito - saldo_debito
            
            if saldo_final != 0:
                patrimonio.append({
                    'cuenta': cuenta,
                    'saldo': saldo_final
                })
                total_patrimonio += saldo_final
        
        context.update({
            'activos_corrientes': activos_corrientes,
            'total_activo_corriente': total_activo_corriente,
            'pasivos': pasivos,
            'total_pasivo': total_pasivo,
            'patrimonio': patrimonio,
            'total_patrimonio': total_patrimonio,
            'total_activos': total_activo_corriente,
            'total_pasivo_patrimonio': total_pasivo + total_patrimonio,
            'cuadra': abs(total_activo_corriente - (total_pasivo + total_patrimonio)) < 0.01
        })
        
        return context


class EstadoResultadosView(LoginRequiredMixin, TemplateView):
    """Estado de Resultados (P&G)"""
    template_name = 'accounting/reportes/estado_resultados.html'
    login_url = '/admin/login/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Parámetros
        fecha_inicio = self.request.GET.get('fecha_inicio')
        fecha_fin = self.request.GET.get('fecha_fin')
        
        if fecha_inicio:
            try:
                fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            except ValueError:
                fecha_inicio = timezone.now().date().replace(month=1, day=1)
        else:
            fecha_inicio = timezone.now().date().replace(month=1, day=1)
            
        if fecha_fin:
            try:
                fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
            except ValueError:
                fecha_fin = timezone.now().date()
        else:
            fecha_fin = timezone.now().date()
        
        context['fecha_inicio'] = fecha_inicio
        context['fecha_fin'] = fecha_fin
        
        # INGRESOS (Cuentas 4)
        cuentas_ingresos = CuentaContable.objects.filter(
            codigo__startswith='4', tipo='INGRESOS'
        )
        
        ingresos = []
        total_ingresos = 0
        
        for cuenta in cuentas_ingresos:
            movimientos = LineaAsiento.objects.filter(
                cuenta_contable=cuenta,
                asiento_contable__fecha__gte=fecha_inicio,
                asiento_contable__fecha__lte=fecha_fin
            )
            
            saldo_debito = movimientos.aggregate(Sum('debito'))['debito__sum'] or 0
            saldo_credito = movimientos.aggregate(Sum('credito'))['credito__sum'] or 0
            saldo_final = saldo_credito - saldo_debito  # Ingresos tienen naturaleza crédito
            
            if saldo_final != 0:
                ingresos.append({
                    'cuenta': cuenta,
                    'saldo': saldo_final
                })
                total_ingresos += saldo_final
        
        # COSTOS Y GASTOS (Cuentas 5 y 6)
        cuentas_costos_gastos = CuentaContable.objects.filter(
            codigo__startswith__in=['5', '6'], 
            tipo__in=['COSTO', 'GASTO']
        )
        
        costos_gastos = []
        total_costos_gastos = 0
        
        for cuenta in cuentas_costos_gastos:
            movimientos = LineaAsiento.objects.filter(
                cuenta_contable=cuenta,
                asiento_contable__fecha__gte=fecha_inicio,
                asiento_contable__fecha__lte=fecha_fin
            )
            
            saldo_debito = movimientos.aggregate(Sum('debito'))['debito__sum'] or 0
            saldo_credito = movimientos.aggregate(Sum('credito'))['credito__sum'] or 0
            saldo_final = saldo_debito - saldo_credito  # Gastos tienen naturaleza débito
            
            if saldo_final != 0:
                costos_gastos.append({
                    'cuenta': cuenta,
                    'saldo': saldo_final
                })
                total_costos_gastos += saldo_final
        
        # Cálculos finales
        utilidad_bruta = total_ingresos - total_costos_gastos
        
        context.update({
            'ingresos': ingresos,
            'total_ingresos': total_ingresos,
            'costos_gastos': costos_gastos,
            'total_costos_gastos': total_costos_gastos,
            'utilidad_bruta': utilidad_bruta,
            'margen_utilidad': (utilidad_bruta / total_ingresos * 100) if total_ingresos > 0 else 0
        })
        
        return context


class FlujoEfectivoView(LoginRequiredMixin, TemplateView):
    """Flujo de Efectivo"""
    template_name = 'accounting/reportes/flujo_efectivo.html'
    login_url = '/admin/login/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Parámetros
        fecha_inicio = self.request.GET.get('fecha_inicio')
        fecha_fin = self.request.GET.get('fecha_fin')
        
        if fecha_inicio:
            try:
                fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            except ValueError:
                fecha_inicio = timezone.now().date().replace(month=1, day=1)
        else:
            fecha_inicio = timezone.now().date().replace(month=1, day=1)
            
        if fecha_fin:
            try:
                fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
            except ValueError:
                fecha_fin = timezone.now().date()
        else:
            fecha_fin = timezone.now().date()
        
        context['fecha_inicio'] = fecha_inicio
        context['fecha_fin'] = fecha_fin
        
        # Flujo de Operación
        ingresos_operacion = 50000000  # Datos ejemplo
        gastos_operacion = 35000000
        flujo_neto_operacion = ingresos_operacion - gastos_operacion
        
        # Flujo de Inversión
        inversiones = 10000000
        desinversiones = 5000000
        flujo_neto_inversion = desinversiones - inversiones
        
        # Flujo de Financiación
        prestamos = 15000000
        pagos_prestamo = 8000000
        flujo_neto_financiacion = prestamos - pagos_prestamo
        
        # Flujo Total
        flujo_total = flujo_neto_operacion + flujo_neto_inversion + flujo_neto_financiacion
        
        context.update({
            'ingresos_operacion': ingresos_operacion,
            'gastos_operacion': gastos_operacion,
            'flujo_neto_operacion': flujo_neto_operacion,
            'inversiones': inversiones,
            'desinversiones': desinversiones,
            'flujo_neto_inversion': flujo_neto_inversion,
            'prestamos': prestamos,
            'pagos_prestamo': pagos_prestamo,
            'flujo_neto_financiacion': flujo_neto_financiacion,
            'flujo_total': flujo_total
        })
        
        return context


class AnalisisFinancieroView(LoginRequiredMixin, TemplateView):
    """Análisis Financiero Avanzado"""
    template_name = 'accounting/reportes/analisis_financiero.html'
    login_url = '/admin/login/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Período de análisis
        fecha_fin = timezone.now().date()
        fecha_inicio = fecha_fin.replace(month=1, day=1)
        
        # Datos de ejemplo para análisis financiero
        activo_corriente = 75000000
        pasivo_corriente = 45000000
        ratio_liquidez = activo_corriente / pasivo_corriente if pasivo_corriente > 0 else 0
        
        ingresos = 120000000
        gastos = 85000000
        utilidad_neta = ingresos - gastos
        margen_neto = (utilidad_neta / ingresos * 100) if ingresos > 0 else 0
        
        # ROA (Return on Assets)
        total_activos = activo_corriente
        roa = (utilidad_neta / total_activos * 100) if total_activos > 0 else 0
        
        # Análisis de Tendencias (últimos 6 meses)
        tendencias = [
            {'mes': '2025-02', 'ingresos': 18000000, 'gastos': 12000000, 'utilidad': 6000000},
            {'mes': '2025-03', 'ingresos': 20000000, 'gastos': 13500000, 'utilidad': 6500000},
            {'mes': '2025-04', 'ingresos': 19500000, 'gastos': 14000000, 'utilidad': 5500000},
            {'mes': '2025-05', 'ingresos': 22000000, 'gastos': 15000000, 'utilidad': 7000000},
            {'mes': '2025-06', 'ingresos': 21000000, 'gastos': 14500000, 'utilidad': 6500000},
            {'mes': '2025-07', 'ingresos': 23500000, 'gastos': 16000000, 'utilidad': 7500000},
        ]
        
        context.update({
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'activo_corriente': activo_corriente,
            'pasivo_corriente': pasivo_corriente,
            'ratio_liquidez': ratio_liquidez,
            'ingresos': ingresos,
            'gastos': gastos,
            'utilidad_neta': utilidad_neta,
            'margen_neto': margen_neto,
            'roa': roa,
            'rotacion_inventario': 12.5,
            'dias_inventario': 29,
            'tendencias': tendencias
        })
        
        return context
