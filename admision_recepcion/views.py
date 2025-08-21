from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Q
from django.utils import timezone
from .models import (
    OrdenServicio, DetalleOrdenServicio, Municipio, Empresa,
    Convenio, Servicio, Prestador, SeguimientoPaciente, CitaEmpresarial, ListaPrecios, HistoriaClinica,
    FichaClinica, EvaluacionOcupacional, AntecedenteFamiliar, AntecedentePersonal, AntecedenteSistema,
    ExposicionLaboral, AccidenteLaboral, EnfermedadLaboral,
    ExamenVisual, AntecedenteVisual, DiagnosticoVisual, ConductaRecomendacionVisual,
    Audiometria, AntecedenteAuditivo, AntecedenteAuditivoLaboral, DiagnosticoAuditivo, RecomendacionAuditiva,
    Espirometria, RecomendacionEspirometria,
    EvaluacionOsteomuscular, RecomendacionOsteomuscular,
    HistoriaClinicaGeneral, AntecedenteFamiliarGeneral, AntecedentePersonalGeneral,
    DocumentoClinico, DiagnosticoGeneral, OrdenMedicamento, OrdenServicioGeneral,
    OrdenRemision, OrdenIncapacidad, CertificadoMedico, EvolucionGeneral
)
from .forms import (
    OrdenServicioForm, DetalleOrdenServicioFormSet, SeguimientoPacienteForm,
    OrdenServicioBusquedaForm, EmpresaForm, ConvenioForm, ServicioForm, PrestadorForm
)


class AdmisionRecepcionDashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard principal de Admisión - Recepción"""
    template_name = 'admision_recepcion/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Admisión - Recepción'
        
        # Estadísticas del día
        today = timezone.now().date()
        context['ordenes_hoy'] = OrdenServicio.objects.filter(fecha_orden=today).count()
        context['ordenes_pendientes'] = OrdenServicio.objects.filter(estado_orden='PENDIENTE').count()
        context['ordenes_en_proceso'] = OrdenServicio.objects.filter(estado_orden='EN_PROCESO').count()
        context['total_ordenes'] = OrdenServicio.objects.count()
        
        # Órdenes recientes
        context['ordenes_recientes'] = OrdenServicio.objects.select_related(
            'municipio', 'convenio', 'empresa_mision'
        ).order_by('-created_at')[:10]
        
        return context


class OrdenServicioListView(LoginRequiredMixin, ListView):
    """Lista de órdenes de servicios"""
    model = OrdenServicio
    template_name = 'admision_recepcion/orden_list.html'
    context_object_name = 'ordenes'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related(
            'municipio', 'convenio', 'empresa_mision', 'created_by'
        ).prefetch_related('detalles__servicio')
        
        # Aplicar filtros
        form = OrdenServicioBusquedaForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data['numero_orden']:
                queryset = queryset.filter(numero_orden__icontains=form.cleaned_data['numero_orden'])
            
            if form.cleaned_data['numero_identificacion']:
                queryset = queryset.filter(numero_identificacion__icontains=form.cleaned_data['numero_identificacion'])
            
            if form.cleaned_data['nombre_paciente']:
                nombre = form.cleaned_data['nombre_paciente']
                queryset = queryset.filter(
                    Q(primer_nombre__icontains=nombre) |
                    Q(primer_apellido__icontains=nombre) |
                    Q(segundo_apellido__icontains=nombre)
                )
            
            if form.cleaned_data['fecha_desde']:
                queryset = queryset.filter(fecha_orden__gte=form.cleaned_data['fecha_desde'])
            
            if form.cleaned_data['fecha_hasta']:
                queryset = queryset.filter(fecha_orden__lte=form.cleaned_data['fecha_hasta'])
            
            if form.cleaned_data['estado_orden']:
                queryset = queryset.filter(estado_orden=form.cleaned_data['estado_orden'])
            
            if form.cleaned_data['sede']:
                queryset = queryset.filter(sede=form.cleaned_data['sede'])
        
        return queryset.order_by('-fecha_orden', '-numero_orden')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_busqueda'] = OrdenServicioBusquedaForm(self.request.GET)
        context['module_name'] = 'Órdenes de Servicios'
        return context


class OrdenServicioCreateView(LoginRequiredMixin, CreateView):
    """Crear nueva orden de servicio"""
    model = OrdenServicio
    form_class = OrdenServicioForm
    template_name = 'admision_recepcion/orden_create.html'
    success_url = reverse_lazy('admision_recepcion:orden_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Crear Orden de Servicio'
        
        if self.request.POST:
            context['formset'] = DetalleOrdenServicioFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = DetalleOrdenServicioFormSet(instance=self.object)
        
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        
        # Establecer usuario creador
        form.instance.created_by = self.request.user
        
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            formset.save()
            
            # Calcular totales
            self.object.calcular_totales()
            
            messages.success(
                self.request,
                f'Orden de servicio {self.object.numero_orden} creada exitosamente.'
            )
            return response
        else:
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Error al crear la orden de servicio. Verifique los datos ingresados.')
        return super().form_invalid(form)


class OrdenServicioDetailView(LoginRequiredMixin, DetailView):
    """Detalle de orden de servicio"""
    model = OrdenServicio
    template_name = 'admision_recepcion/orden_detail.html'
    context_object_name = 'orden'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = f'Orden {self.object.numero_orden}'
        
        # Obtener detalles de servicios
        context['detalles'] = self.object.detalles.select_related('servicio', 'prestador').all()
        
        # Obtener seguimientos
        context['seguimientos'] = self.object.seguimientos.select_related('usuario').order_by('-fecha_estado')
        
        # Formulario para nuevo seguimiento
        context['form_seguimiento'] = SeguimientoPacienteForm()
        
        return context


class OrdenServicioUpdateView(LoginRequiredMixin, UpdateView):
    """Actualizar orden de servicio"""
    model = OrdenServicio
    form_class = OrdenServicioForm
    template_name = 'admision_recepcion/orden_update.html'
    
    def get_success_url(self):
        return reverse_lazy('admision_recepcion:orden_detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = f'Editar Orden {self.object.numero_orden}'
        
        if self.request.POST:
            context['formset'] = DetalleOrdenServicioFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = DetalleOrdenServicioFormSet(instance=self.object)
        
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        
        if formset.is_valid():
            response = super().form_valid(form)
            formset.save()
            
            # Recalcular totales
            self.object.calcular_totales()
            
            messages.success(
                self.request,
                f'Orden de servicio {self.object.numero_orden} actualizada exitosamente.'
            )
            return response
        else:
            return self.form_invalid(form)


class OrdenServicioDeleteView(LoginRequiredMixin, DeleteView):
    """Eliminar orden de servicio"""
    model = OrdenServicio
    template_name = 'admision_recepcion/orden_delete.html'
    success_url = reverse_lazy('admision_recepcion:orden_list')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        numero_orden = self.object.numero_orden
        
        response = super().delete(request, *args, **kwargs)
        
        messages.success(
            request,
            f'Orden de servicio {numero_orden} eliminada exitosamente.'
        )
        
        return response


class SeguimientoPacientesView(LoginRequiredMixin, ListView):
    """Seguimiento de pacientes"""
    model = OrdenServicio
    template_name = 'admision_recepcion/seguimiento_pacientes.html'
    context_object_name = 'ordenes'
    paginate_by = 50
    
    def get_queryset(self):
        queryset = OrdenServicio.objects.filter(
            estado_orden__in=['PENDIENTE', 'EN_PROCESO', 'AUTORIZADA']
        ).select_related(
            'municipio', 'convenio', 'empresa_mision', 'created_by'
        ).prefetch_related(
            'seguimientos__usuario',
            'detalles__servicio',
            'detalles__prestador'
        )
        
        # Aplicar filtros de la interfaz
        fecha_filtro = self.request.GET.get('fecha')
        if fecha_filtro:
            try:
                from datetime import datetime
                fecha = datetime.strptime(fecha_filtro, '%Y-%m-%d').date()
                queryset = queryset.filter(fecha_orden=fecha)
            except ValueError:
                pass
        else:
            # Por defecto, mostrar órdenes de hoy
            queryset = queryset.filter(fecha_orden=timezone.now().date())
        
        sede_filtro = self.request.GET.get('sede')
        if sede_filtro:
            queryset = queryset.filter(sede=sede_filtro)
        
        estado_filtro = self.request.GET.get('estado')
        if estado_filtro:
            # Filtrar por último estado de seguimiento
            queryset = queryset.filter(seguimientos__estado=estado_filtro)
        
        return queryset.distinct().order_by('-fecha_orden', '-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Seguimiento a Pacientes'
        context['today'] = timezone.now().date().strftime('%Y-%m-%d')
        
        # Calcular estadísticas
        ordenes = context['ordenes']
        stats = {
            'en_espera': 0,
            'en_atencion': 0,
            'atendidos': 0
        }
        
        for orden in ordenes:
            ultimo_seguimiento = orden.seguimientos.first()
            if ultimo_seguimiento:
                if ultimo_seguimiento.estado == 'EN_ESPERA':
                    stats['en_espera'] += 1
                elif ultimo_seguimiento.estado == 'EN_ATENCION':
                    stats['en_atencion'] += 1
                elif ultimo_seguimiento.estado == 'ATENDIDO':
                    stats['atendidos'] += 1
        
        context['stats'] = stats
        return context


class SeguimientoAtencionesView(LoginRequiredMixin, ListView):
    """Seguimiento a las atenciones"""
    model = OrdenServicio
    template_name = 'admision_recepcion/seguimiento_atenciones.html'
    context_object_name = 'ordenes'
    paginate_by = 50
    
    def get_queryset(self):
        queryset = OrdenServicio.objects.filter(
            estado_orden__in=['EN_PROCESO', 'COMPLETADA', 'AUTORIZADA']
        ).select_related(
            'municipio', 'convenio', 'empresa_mision', 'created_by'
        ).prefetch_related(
            'seguimientos__usuario',
            'detalles__servicio',
            'detalles__prestador'
        )
        
        # Filtro por fecha
        fecha_filtro = self.request.GET.get('fecha')
        if fecha_filtro:
            try:
                from datetime import datetime
                fecha = datetime.strptime(fecha_filtro, '%Y-%m-%d').date()
                queryset = queryset.filter(fecha_orden=fecha)
            except ValueError:
                pass
        else:
            # Por defecto, mostrar atenciones de hoy
            queryset = queryset.filter(fecha_orden=timezone.now().date())
        
        # Filtro por paciente (número de identificación o nombre)
        paciente_filtro = self.request.GET.get('paciente')
        if paciente_filtro:
            queryset = queryset.filter(
                Q(numero_identificacion__icontains=paciente_filtro) |
                Q(primer_nombre__icontains=paciente_filtro) |
                Q(primer_apellido__icontains=paciente_filtro) |
                Q(segundo_apellido__icontains=paciente_filtro) |
                Q(numero_orden__icontains=paciente_filtro)
            )
        
        # Filtro por estado de atención
        estado_atencion = self.request.GET.get('estado_atencion')
        if estado_atencion:
            if estado_atencion == 'EN_ATENCION':
                queryset = queryset.filter(seguimientos__estado='EN_ATENCION')
            elif estado_atencion == 'ATENDIDO':
                queryset = queryset.filter(seguimientos__estado='ATENDIDO')
            elif estado_atencion == 'COMPLETADO':
                queryset = queryset.filter(estado_orden='COMPLETADA')
        
        # Filtro por sede
        sede_filtro = self.request.GET.get('sede')
        if sede_filtro:
            queryset = queryset.filter(sede=sede_filtro)
        
        # Filtro por prestador/médico
        prestador_filtro = self.request.GET.get('prestador')
        if prestador_filtro:
            queryset = queryset.filter(detalles__prestador__id=prestador_filtro)
        
        return queryset.distinct().order_by('-fecha_orden', '-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Seguimiento a Las Atenciones'
        context['today'] = timezone.now().date().strftime('%Y-%m-%d')
        
        # Agregar lista de prestadores para el filtro
        context['prestadores'] = Prestador.objects.filter(activo=True).order_by('nombre')
        
        # Calcular estadísticas de atenciones
        ordenes = context['ordenes']
        stats = {
            'en_atencion': 0,
            'atendidos': 0,
            'completados': 0,
            'total_servicios': 0,
            'valor_total': 0
        }
        
        for orden in ordenes:
            ultimo_seguimiento = orden.seguimientos.first()
            if ultimo_seguimiento:
                if ultimo_seguimiento.estado == 'EN_ATENCION':
                    stats['en_atencion'] += 1
                elif ultimo_seguimiento.estado == 'ATENDIDO':
                    stats['atendidos'] += 1
            
            if orden.estado_orden == 'COMPLETADA':
                stats['completados'] += 1
            
            stats['total_servicios'] += orden.detalles.count()
            stats['valor_total'] += orden.total_pagar or 0
        
        context['stats'] = stats
        
        # Parámetros de búsqueda actuales
        context['filtros_actuales'] = {
            'fecha': self.request.GET.get('fecha', ''),
            'paciente': self.request.GET.get('paciente', ''),
            'estado_atencion': self.request.GET.get('estado_atencion', ''),
            'sede': self.request.GET.get('sede', ''),
            'prestador': self.request.GET.get('prestador', ''),
        }
        
        return context


class PortalEmpresasView(LoginRequiredMixin, ListView):
    """Servicios solicitados en el portal de acceso a empresas"""
    model = CitaEmpresarial
    template_name = 'admision_recepcion/portal_empresas.html'
    context_object_name = 'citas'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = CitaEmpresarial.objects.select_related(
            'empresa', 'prestador_asignado', 'confirmada_por', 'cancelada_por'
        ).prefetch_related('servicios_adicionales')
        
        # Filtro por día de la cita
        dia_cita = self.request.GET.get('dia_cita')
        if dia_cita:
            try:
                from datetime import datetime
                fecha = datetime.strptime(dia_cita, '%Y-%m-%d').date()
                queryset = queryset.filter(fecha_cita=fecha)
            except ValueError:
                pass
        else:
            # Por defecto, mostrar citas de hoy
            queryset = queryset.filter(fecha_cita=timezone.now().date())
        
        # Filtro por número de identificación
        identificacion = self.request.GET.get('identificacion')
        if identificacion:
            queryset = queryset.filter(numero_identificacion__icontains=identificacion)
        
        # Filtro por nombre del trabajador
        trabajador = self.request.GET.get('trabajador')
        if trabajador:
            queryset = queryset.filter(nombre_trabajador__icontains=trabajador)
        
        # Filtro por nombre de la empresa
        empresa_nombre = self.request.GET.get('empresa')
        if empresa_nombre:
            queryset = queryset.filter(empresa__razon_social__icontains=empresa_nombre)
        
        # Filtro por estado
        estado = self.request.GET.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
        
        # Filtros adicionales
        sede = self.request.GET.get('sede')
        if sede:
            queryset = queryset.filter(sede_cita=sede)
        
        tipo_servicio = self.request.GET.get('tipo_servicio')
        if tipo_servicio:
            queryset = queryset.filter(tipo_servicio=tipo_servicio)
        
        # Filtro por rango de fechas
        fecha_desde = self.request.GET.get('fecha_desde')
        fecha_hasta = self.request.GET.get('fecha_hasta')
        if fecha_desde and fecha_hasta:
            try:
                from datetime import datetime
                inicio = datetime.strptime(fecha_desde, '%Y-%m-%d').date()
                fin = datetime.strptime(fecha_hasta, '%Y-%m-%d').date()
                queryset = queryset.filter(fecha_cita__range=[inicio, fin])
            except ValueError:
                pass
        
        return queryset.order_by('-fecha_cita', '-hora_cita', '-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Servicios solicitados en el portal de acceso a empresas'
        context['today'] = timezone.now().date().strftime('%Y-%m-%d')
        
        # Agregar listas para los filtros
        context['empresas'] = Empresa.objects.filter(activo=True).order_by('razon_social')
        context['prestadores'] = Prestador.objects.filter(activo=True).order_by('nombre')
        
        # Estadísticas de citas
        citas = context['citas']
        stats = {
            'programadas': 0,
            'confirmadas': 0,
            'canceladas': 0,
            'completadas': 0,
            'total_valor': 0,
            'vencidas': 0
        }
        
        for cita in citas:
            if cita.estado == 'PROGRAMADA':
                stats['programadas'] += 1
            elif cita.estado == 'CONFIRMADA':
                stats['confirmadas'] += 1
            elif cita.estado == 'CANCELADA':
                stats['canceladas'] += 1
            elif cita.estado == 'COMPLETADA':
                stats['completadas'] += 1
            
            stats['total_valor'] += cita.valor_estimado or 0
            
            if cita.esta_vencida:
                stats['vencidas'] += 1
        
        context['stats'] = stats
        
        # Parámetros de filtros actuales
        context['filtros_actuales'] = {
            'dia_cita': self.request.GET.get('dia_cita', ''),
            'identificacion': self.request.GET.get('identificacion', ''),
            'trabajador': self.request.GET.get('trabajador', ''),
            'empresa': self.request.GET.get('empresa', ''),
            'estado': self.request.GET.get('estado', ''),
            'sede': self.request.GET.get('sede', ''),
            'tipo_servicio': self.request.GET.get('tipo_servicio', ''),
        }
        
        # Opciones para selects
        context['estados_choices'] = CitaEmpresarial.ESTADO_CITA_CHOICES
        context['tipos_servicio_choices'] = CitaEmpresarial.TIPO_SERVICIO_CHOICES
        context['sedes_choices'] = OrdenServicio.SEDE_CHOICES
        
        return context


class ListaPreciosView(LoginRequiredMixin, ListView):
    """Lista de Precios de productos y servicios"""
    model = ListaPrecios
    template_name = 'admision_recepcion/lista_precios.html'
    context_object_name = 'productos'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = ListaPrecios.objects.all().select_related('created_by').prefetch_related('convenios')
        
        # Filtro por convenio
        convenio_id = self.request.GET.get('convenio')
        if convenio_id:
            try:
                convenio_id = int(convenio_id)
                queryset = queryset.filter(convenios__id=convenio_id)
            except (ValueError, TypeError):
                pass
        
        # Filtro por nombre de producto/servicio
        buscar = self.request.GET.get('buscar')
        if buscar:
            queryset = queryset.filter(
                Q(nombre_producto_servicio__icontains=buscar) |
                Q(codigo_interno__icontains=buscar) |
                Q(codigo_cups__icontains=buscar) |
                Q(codigo_cum__icontains=buscar)
            )
        
        # Filtro por categoría
        categoria = self.request.GET.get('categoria')
        if categoria:
            queryset = queryset.filter(categoria=categoria)
        
        # Filtro por tipo RIPS
        tipo_rips = self.request.GET.get('tipo_rips')
        if tipo_rips:
            queryset = queryset.filter(tipo_rips=tipo_rips)
        
        # Filtro por rango de precios
        precio_min = self.request.GET.get('precio_min')
        precio_max = self.request.GET.get('precio_max')
        if precio_min:
            try:
                precio_min = float(precio_min)
                queryset = queryset.filter(precio__gte=precio_min)
            except ValueError:
                pass
        if precio_max:
            try:
                precio_max = float(precio_max)
                queryset = queryset.filter(precio__lte=precio_max)
            except ValueError:
                pass
        
        return queryset.order_by('nombre_producto_servicio')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Lista de Precios'
        
        # Agregar convenios para el filtro
        context['convenios'] = Convenio.objects.filter(activo=True).order_by('nombre')
        
        # Agregar opciones para filtros
        context['categorias'] = ListaPrecios.CATEGORIA_CHOICES
        context['tipos_rips'] = ListaPrecios.TIPO_RIPS_CHOICES
        
        # Parámetros de filtros actuales
        context['filtros_actuales'] = {
            'convenio': self.request.GET.get('convenio', ''),
            'buscar': self.request.GET.get('buscar', ''),
            'categoria': self.request.GET.get('categoria', ''),
            'tipo_rips': self.request.GET.get('tipo_rips', ''),
            'precio_min': self.request.GET.get('precio_min', ''),
            'precio_max': self.request.GET.get('precio_max', ''),
        }
        
        # Estadísticas
        productos = context['productos']
        stats = {
            'total_productos': productos.count() if hasattr(productos, 'count') else len(productos),
            'total_valor': sum(p.precio for p in productos) if productos else 0,
            'con_cups': sum(1 for p in productos if p.codigo_cups) if productos else 0,
            'con_iva': sum(1 for p in productos if p.gravado_iva) if productos else 0,
        }
        context['stats'] = stats
        
        # Convenio seleccionado para mostrar precios específicos
        convenio_seleccionado = None
        if context['filtros_actuales']['convenio']:
            try:
                convenio_seleccionado = Convenio.objects.get(id=context['filtros_actuales']['convenio'])
            except Convenio.DoesNotExist:
                pass
        context['convenio_seleccionado'] = convenio_seleccionado
        
        return context


class ImprimirHistoriasClinicasView(LoginRequiredMixin, ListView):
    """Imprimir Historias Clínicas"""
    model = HistoriaClinica
    template_name = 'admision_recepcion/imprimir_historias.html'
    context_object_name = 'historias'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = HistoriaClinica.objects.select_related(
            'empresa', 'profesional', 'created_by'
        ).prefetch_related('orden_servicio')
        
        # Filtro por número de identificación
        identificacion = self.request.GET.get('identificacion')
        if identificacion:
            queryset = queryset.filter(numero_identificacion__icontains=identificacion)
        
        # Filtro por nombre del paciente
        nombre_paciente = self.request.GET.get('nombre_paciente')
        if nombre_paciente:
            queryset = queryset.filter(nombre_paciente__icontains=nombre_paciente)
        
        # Filtro por nombre de la empresa
        nombre_empresa = self.request.GET.get('nombre_empresa')
        if nombre_empresa:
            queryset = queryset.filter(empresa__razon_social__icontains=nombre_empresa)
        
        # Filtro por rango de fechas
        fecha_desde = self.request.GET.get('fecha_desde')
        fecha_hasta = self.request.GET.get('fecha_hasta')
        
        if fecha_desde:
            try:
                from datetime import datetime
                fecha_inicio = datetime.strptime(fecha_desde, '%Y-%m-%d').date()
                queryset = queryset.filter(fecha_creacion__date__gte=fecha_inicio)
            except ValueError:
                pass
        
        if fecha_hasta:
            try:
                from datetime import datetime
                fecha_fin = datetime.strptime(fecha_hasta, '%Y-%m-%d').date()
                queryset = queryset.filter(fecha_creacion__date__lte=fecha_fin)
            except ValueError:
                pass
        
        # Filtro por estado
        estado = self.request.GET.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
        
        return queryset.order_by('-fecha_creacion')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Imprimir Historias Clínicas'
        
        # Parámetros de filtros actuales
        context['filtros_actuales'] = {
            'identificacion': self.request.GET.get('identificacion', ''),
            'nombre_paciente': self.request.GET.get('nombre_paciente', ''),
            'nombre_empresa': self.request.GET.get('nombre_empresa', ''),
            'fecha_desde': self.request.GET.get('fecha_desde', ''),
            'fecha_hasta': self.request.GET.get('fecha_hasta', ''),
            'estado': self.request.GET.get('estado', ''),
        }
        
        # Opciones de estado
        context['estados_choices'] = HistoriaClinica.ESTADO_CHOICES
        
        # Estadísticas
        historias = context['historias']
        stats = {
            'total': historias.count() if hasattr(historias, 'count') else len(historias),
            'abiertas': HistoriaClinica.objects.filter(estado='ABIERTA').count(),
            'cerradas': HistoriaClinica.objects.filter(estado='CERRADA').count(),
            'anuladas': HistoriaClinica.objects.filter(estado='ANULADA').count(),
        }
        context['stats'] = stats
        
        return context


class EmpresasHistoriasClinicasView(LoginRequiredMixin, ListView):
    """Empresas Historias Clínicas"""
    model = HistoriaClinica
    template_name = 'admision_recepcion/empresas_historias.html'
    context_object_name = 'historias'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = HistoriaClinica.objects.filter(
            empresa__isnull=False
        ).select_related(
            'empresa', 'profesional', 'created_by'
        ).prefetch_related('orden_servicio')
        
        # Filtro por empresa
        empresa_id = self.request.GET.get('empresa')
        if empresa_id:
            try:
                empresa_id = int(empresa_id)
                queryset = queryset.filter(empresa_id=empresa_id)
            except (ValueError, TypeError):
                pass
        
        # Filtro por rango de fechas
        fecha_desde = self.request.GET.get('desde')
        fecha_hasta = self.request.GET.get('hasta')
        
        if fecha_desde:
            try:
                from datetime import datetime
                fecha_inicio = datetime.strptime(fecha_desde, '%Y-%m-%d').date()
                queryset = queryset.filter(fecha_creacion__date__gte=fecha_inicio)
            except ValueError:
                pass
        else:
            # Por defecto, desde hace 10 días
            from datetime import timedelta
            fecha_inicio = timezone.now().date() - timedelta(days=10)
            queryset = queryset.filter(fecha_creacion__date__gte=fecha_inicio)
        
        if fecha_hasta:
            try:
                from datetime import datetime
                fecha_fin = datetime.strptime(fecha_hasta, '%Y-%m-%d').date()
                queryset = queryset.filter(fecha_creacion__date__lte=fecha_fin)
            except ValueError:
                pass
        else:
            # Por defecto, hasta hoy
            queryset = queryset.filter(fecha_creacion__date__lte=timezone.now().date())
        
        # Filtro por tipo de examen
        tipo_examen = self.request.GET.get('tipo')
        if tipo_examen:
            queryset = queryset.filter(tipo_examen=tipo_examen)
        
        # Filtro por estado
        estado = self.request.GET.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
        
        return queryset.order_by('-fecha_creacion')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Empresas Historias Clínicas'
        
        # Agregar empresas para el filtro
        context['empresas'] = Empresa.objects.filter(activo=True).order_by('razon_social')
        
        # Opciones para filtros
        context['tipos_examen_choices'] = HistoriaClinica.TIPO_EXAMEN_CHOICES
        context['estados_choices'] = HistoriaClinica.ESTADO_CHOICES
        
        # Parámetros de filtros actuales
        from datetime import timedelta
        fecha_default_desde = timezone.now().date() - timedelta(days=10)
        fecha_default_hasta = timezone.now().date()
        
        context['filtros_actuales'] = {
            'empresa': self.request.GET.get('empresa', ''),
            'desde': self.request.GET.get('desde', fecha_default_desde.strftime('%Y-%m-%d')),
            'hasta': self.request.GET.get('hasta', fecha_default_hasta.strftime('%Y-%m-%d')),
            'tipo': self.request.GET.get('tipo', ''),
            'estado': self.request.GET.get('estado', ''),
        }
        
        # Estadísticas por empresa
        historias = context['historias']
        stats = {
            'total': historias.count() if hasattr(historias, 'count') else len(historias),
            'abiertas': sum(1 for h in historias if h.estado == 'ABIERTA') if historias else 0,
            'cerradas': sum(1 for h in historias if h.estado == 'CERRADA') if historias else 0,
            'por_empresa': {},
        }
        
        # Estadísticas por empresa
        if historias:
            from collections import defaultdict
            empresas_count = defaultdict(int)
            for historia in historias:
                if historia.empresa:
                    empresas_count[historia.empresa.razon_social] += 1
            stats['por_empresa'] = dict(empresas_count)
        
        context['stats'] = stats
        
        return context


# ===== FICHAS CLÍNICAS =====

class FichaClinicaListView(LoginRequiredMixin, ListView):
    """Lista de fichas clínicas"""
    model = FichaClinica
    template_name = 'admision_recepcion/fichas_clinicas/lista.html'
    context_object_name = 'fichas'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = FichaClinica.objects.select_related(
            'empresa', 'profesional_evaluador', 'municipio', 'created_by'
        )
        
        # Filtro por tipo de ficha
        tipo_ficha = self.request.GET.get('tipo_ficha')
        if tipo_ficha:
            queryset = queryset.filter(tipo_ficha=tipo_ficha)
        
        # Filtro por estado
        estado = self.request.GET.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
        
        # Filtro por empresa
        empresa_id = self.request.GET.get('empresa')
        if empresa_id:
            try:
                queryset = queryset.filter(empresa_id=int(empresa_id))
            except (ValueError, TypeError):
                pass
        
        return queryset.order_by('-fecha_creacion')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Fichas Clínicas'
        context['tipos_ficha'] = FichaClinica.TIPO_FICHA_CHOICES
        context['estados'] = FichaClinica.ESTADO_CHOICES
        context['empresas'] = Empresa.objects.filter(activo=True)
        return context


class EvaluacionOcupacionalCreateView(LoginRequiredMixin, CreateView):
    """Crear nueva evaluación ocupacional"""
    model = FichaClinica
    template_name = 'admision_recepcion/fichas_clinicas/evaluacion_ocupacional_form.html'
    fields = [
        'fecha_evaluacion', 'numero_identificacion', 'tipo_documento', 
        'nombre_trabajador', 'fecha_nacimiento', 'genero', 'edad',
        'telefono', 'email', 'direccion', 'municipio', 'empresa', 'cargo',
        'profesional_evaluador'
    ]
    
    def form_valid(self, form):
        form.instance.tipo_ficha = 'EVALUACION_OCUPACIONAL'
        form.instance.created_by = self.request.user
        
        response = super().form_valid(form)
        
        # Crear la evaluación ocupacional asociada
        EvaluacionOcupacional.objects.create(
            ficha_clinica=self.object,
            tipo_evaluacion='INGRESO'  # Por defecto
        )
        
        # Crear antecedentes por defecto
        self._crear_antecedentes_default()
        
        messages.success(self.request, 'Evaluación ocupacional creada exitosamente.')
        return response
    
    def _crear_antecedentes_default(self):
        """Crear antecedentes por defecto"""
        evaluacion = self.object.evaluacion_ocupacional
        
        # Antecedentes familiares por defecto
        patologias_familiares = [
            'ASMA', 'CANCER', 'DIABETES', 'ENFERMEDAD_CORONARIA',
            'ACCIDENTE_CEREBRO_VASCULAR', 'HIPERTENSION_ARTERIAL',
            'COLAGENOSIS', 'PATOLOGIAS_TIROIDEAS'
        ]
        
        for patologia in patologias_familiares:
            AntecedenteFamiliar.objects.get_or_create(
                evaluacion_ocupacional=evaluacion,
                patologia=patologia,
                defaults={'parentesco': 'NO_REFIERE'}
            )
        
        # Antecedentes personales por defecto
        tipos_antecedentes = [
            'PATOLOGICOS', 'QUIRURGICOS', 'TRAUMATICOS', 'FARMACOLOGICOS',
            'ALERGICOS', 'PSIQUIATRICOS', 'FOBIAS'
        ]
        
        for tipo in tipos_antecedentes:
            AntecedentePersonal.objects.get_or_create(
                evaluacion_ocupacional=evaluacion,
                tipo_antecedente=tipo,
                defaults={'diagnostico_observaciones': 'NO REFIERE'}
            )
        
        # Antecedentes por sistemas por defecto
        sistemas = [
            'CABEZA', 'OJOS', 'OIDOS', 'NARIZ', 'BOCA', 'GARGANTA', 'CUELLO',
            'SISTEMA_ENDOCRINO', 'SISTEMA_CIRCULATORIO', 'SISTEMA_RESPIRATORIO',
            'SISTEMA_GASTROINTESTINAL', 'SISTEMA_GENITOURINARIO',
            'SISTEMA_OSTEOMUSCULAR', 'SISTEMA_NERVIOSO', 'PSIQUIATRICO', 'PIEL_ANEXOS'
        ]
        
        for sistema in sistemas:
            AntecedenteSistema.objects.get_or_create(
                evaluacion_ocupacional=evaluacion,
                nombre_sistema=sistema,
                defaults={
                    'patologicos': 'NIEGA',
                    'quirurgicos': 'NIEGA',
                    'traumaticos': 'NIEGA'
                }
            )
    
    def get_success_url(self):
        return reverse_lazy('admision_recepcion:evaluacion_ocupacional_detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Nueva Evaluación Ocupacional'
        context['municipios'] = Municipio.objects.filter(activo=True).order_by('nombre')
        context['empresas'] = Empresa.objects.filter(activo=True).order_by('razon_social')
        context['profesionales'] = Prestador.objects.filter(activo=True).order_by('nombre')
        return context


class EvaluacionOcupacionalDetailView(LoginRequiredMixin, DetailView):
    """Detalle y edición de evaluación ocupacional"""
    model = FichaClinica
    template_name = 'admision_recepcion/fichas_clinicas/evaluacion_ocupacional_detail.html'
    context_object_name = 'ficha'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Evaluación Ocupacional'
        
        # Obtener la evaluación ocupacional
        try:
            evaluacion = self.object.evaluacion_ocupacional
            context['evaluacion'] = evaluacion
            
            # Obtener antecedentes organizados
            context['antecedentes_familiares'] = evaluacion.antecedentes_familiares.all().order_by('patologia')
            context['antecedentes_personales'] = evaluacion.antecedentes_personales.all().order_by('tipo_antecedente')
            context['antecedentes_sistemas'] = evaluacion.antecedentes_sistemas.all().order_by('nombre_sistema')
            context['exposiciones_laborales'] = evaluacion.exposiciones_laborales.all().order_by('-fecha_registro')
            context['accidentes_laborales'] = evaluacion.accidentes_laborales.all().order_by('-fecha_registro')
            context['enfermedades_laborales'] = evaluacion.enfermedades_laborales.all().order_by('-fecha_registro')
            
            # Opciones para formularios
            context['tipos_evaluacion'] = EvaluacionOcupacional.TIPO_EVALUACION_CHOICES
            context['estados_civiles'] = EvaluacionOcupacional.ESTADO_CIVIL_CHOICES
            context['niveles_educativos'] = EvaluacionOcupacional.NIVEL_EDUCATIVO_CHOICES
            context['jornadas_laborales'] = EvaluacionOcupacional.JORNADA_LABORAL_CHOICES
            context['tipos_sangre'] = EvaluacionOcupacional.TIPO_SANGRE_CHOICES
            
        except EvaluacionOcupacional.DoesNotExist:
            context['evaluacion'] = None
        
        return context


class ExamenVisualCreateView(LoginRequiredMixin, CreateView):
    """Crear nuevo examen visual"""
    model = FichaClinica
    template_name = 'admision_recepcion/fichas_clinicas/examen_visual_form.html'
    fields = [
        'fecha_evaluacion', 'numero_identificacion', 'tipo_documento', 
        'nombre_trabajador', 'fecha_nacimiento', 'genero', 'edad',
        'telefono', 'email', 'direccion', 'municipio', 'empresa', 'cargo',
        'profesional_evaluador'
    ]
    
    def form_valid(self, form):
        form.instance.tipo_ficha = 'EXAMEN_VISUAL'
        form.instance.created_by = self.request.user
        
        response = super().form_valid(form)
        
        # Crear el examen visual asociado
        ExamenVisual.objects.create(
            ficha_clinica=self.object,
            sintomatologia='ASINTOMATICO'  # Por defecto
        )
        
        # Crear antecedentes visuales por defecto
        self._crear_antecedentes_visuales_default()
        
        messages.success(self.request, 'Examen visual creado exitosamente.')
        return response
    
    def _crear_antecedentes_visuales_default(self):
        """Crear antecedentes visuales por defecto"""
        examen = self.object.examen_visual
        
        # Antecedentes visuales por defecto
        tipos_antecedentes = [
            'ANTECEDENTES_PERSONALES',
            'ANTECEDENTES_FAMILIARES', 
            'ANTECEDENTES_OCUPACIONALES',
            'EXPOSICION_LABORAL_VISUAL',
            'USA_ANTEOJOS',
            'MULTIFOCAL',
            'LENTES_CONTACTO',
            'TRAE_RX',
            'TIPO_USO',
            'ULTIMO_DIAGNOSTICO'
        ]
        
        for tipo in tipos_antecedentes:
            observacion = 'NIEGA'
            if tipo == 'USA_ANTEOJOS':
                observacion = 'NO USA'
            elif tipo == 'MULTIFOCAL':
                observacion = 'NO'
            elif tipo == 'LENTES_CONTACTO':
                observacion = 'NO USA'
            elif tipo == 'TRAE_RX':
                observacion = 'NO'
            elif tipo == 'TIPO_USO':
                observacion = 'NO APLICA'
            
            AntecedenteVisual.objects.get_or_create(
                examen_visual=examen,
                tipo_antecedente=tipo,
                defaults={'observacion': observacion}
            )
    
    def get_success_url(self):
        return reverse_lazy('admision_recepcion:examen_visual_detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Nuevo Examen Visual'
        context['municipios'] = Municipio.objects.filter(activo=True).order_by('nombre')
        context['empresas'] = Empresa.objects.filter(activo=True).order_by('razon_social')
        context['profesionales'] = Prestador.objects.filter(activo=True).order_by('nombre')
        return context


class ExamenVisualDetailView(LoginRequiredMixin, DetailView):
    """Detalle y edición de examen visual"""
    model = FichaClinica
    template_name = 'admision_recepcion/fichas_clinicas/examen_visual_detail.html'
    context_object_name = 'ficha'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Examen Visual'
        
        # Obtener el examen visual
        try:
            examen = self.object.examen_visual
            context['examen'] = examen
            
            # Obtener antecedentes organizados
            context['antecedentes_visuales'] = examen.antecedentes_visuales.all().order_by('tipo_antecedente')
            context['diagnosticos_visuales'] = examen.diagnosticos_visuales.all().order_by('tipo_diagnostico')
            context['conductas_recomendaciones'] = examen.conductas_recomendaciones.all().order_by('tipo_item', 'codigo')
            
            # Opciones para formularios
            context['sintomatologia_choices'] = ExamenVisual.SINTOMATOLOGIA_CHOICES
            context['valoracion_choices'] = ExamenVisual.VALORACION_CHOICES
            context['uso_choices'] = ExamenVisual.USO_CHOICES
            context['tipo_uso_choices'] = ExamenVisual.TIPO_USO_CHOICES
            
            # Opciones para diagnósticos
            context['tipo_diagnostico_choices'] = DiagnosticoVisual.TIPO_DIAGNOSTICO_CHOICES
            context['lateralidad_choices'] = DiagnosticoVisual.LATERALIDAD_CHOICES
            context['tipo_impresion_choices'] = DiagnosticoVisual.TIPO_IMPRESION_CHOICES
            
            # Opciones para conductas y recomendaciones
            context['conducta_choices'] = ConductaRecomendacionVisual.CONDUCTA_CHOICES
            context['remision_choices'] = ConductaRecomendacionVisual.REMISION_CHOICES
            
        except ExamenVisual.DoesNotExist:
            context['examen'] = None
        
        return context


class AudiometriaCreateView(LoginRequiredMixin, CreateView):
    """Crear nueva audiometría"""
    model = FichaClinica
    template_name = 'admision_recepcion/fichas_clinicas/audiometria_form.html'
    fields = [
        'fecha_evaluacion', 'numero_identificacion', 'tipo_documento', 
        'nombre_trabajador', 'fecha_nacimiento', 'genero', 'edad',
        'telefono', 'email', 'direccion', 'municipio', 'empresa', 'cargo',
        'profesional_evaluador'
    ]
    
    def form_valid(self, form):
        form.instance.tipo_ficha = 'AUDIOMETRIA'
        form.instance.created_by = self.request.user
        
        response = super().form_valid(form)
        
        # Crear la audiometría asociada
        Audiometria.objects.create(
            ficha_clinica=self.object,
            uso_cabina_sonoamortiguada=True  # Por defecto
        )
        
        # Crear antecedentes auditivos por defecto
        self._crear_antecedentes_auditivos_default()
        
        messages.success(self.request, 'Audiometría creada exitosamente.')
        return response
    
    def _crear_antecedentes_auditivos_default(self):
        """Crear antecedentes auditivos por defecto"""
        audiometria = self.object.audiometria
        
        # Antecedentes familiares auditivos por defecto
        antecedentes_familiares = [
            'OTITIS', 'TRAUMA', 'CIRUGIA', 'INGESTA_OTOTOXICOS',
            'HIPOACUSIA_SUBJETIVA', 'ACUFENOS'
        ]
        
        for antecedente in antecedentes_familiares:
            AntecedenteAuditivo.objects.get_or_create(
                audiometria=audiometria,
                tipo_antecedente=antecedente,
                defaults={'observacion': 'NO REFIERE'}
            )
        
        # Exposición ruido extralaboral por defecto
        exposiciones_extralaborales = [
            'TEJO', 'MOTO', 'DISCOTECA', 'SERVICIO_MILITAR',
            'POLIGONO', 'AUDIFONOS'
        ]
        
        for exposicion in exposiciones_extralaborales:
            AntecedenteAuditivo.objects.get_or_create(
                audiometria=audiometria,
                tipo_antecedente=exposicion,
                defaults={'observacion': 'NO REFIERE'}
            )
        
        # Recomendaciones por defecto
        recomendaciones_default = [
            'CONTROL_AUDITIVO_1_ANO',
            'USE_PROTECCION_AUDITIVA',
            'CONTROL_OTORRINO',
            'AUDIOMETRIA_CONFIRMATORIA'
        ]
        
        for recomendacion in recomendaciones_default:
            RecomendacionAuditiva.objects.get_or_create(
                audiometria=audiometria,
                codigo=recomendacion,
                defaults={'seleccionado': False}
            )
    
    def get_success_url(self):
        return reverse_lazy('admision_recepcion:audiometria_detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Nueva Audiometría'
        context['municipios'] = Municipio.objects.filter(activo=True).order_by('nombre')
        context['empresas'] = Empresa.objects.filter(activo=True).order_by('razon_social')
        context['profesionales'] = Prestador.objects.filter(activo=True).order_by('nombre')
        return context


class AudiometriaDetailView(LoginRequiredMixin, DetailView):
    """Detalle y edición de audiometría"""
    model = FichaClinica
    template_name = 'admision_recepcion/fichas_clinicas/audiometria_detail.html'
    context_object_name = 'ficha'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Audiometría'
        
        # Obtener la audiometría
        try:
            audiometria = self.object.audiometria
            context['audiometria'] = audiometria
            
            # Obtener antecedentes organizados
            context['antecedentes_auditivos'] = audiometria.antecedentes_auditivos.all().order_by('tipo_antecedente')
            context['antecedentes_laborales'] = audiometria.antecedentes_laborales.all().order_by('-tiempo_exposicion_anos')
            context['diagnosticos_auditivos'] = audiometria.diagnosticos_auditivos.all().order_by('tipo_diagnostico')
            context['recomendaciones_auditivas'] = audiometria.recomendaciones_auditivas.all().order_by('codigo')
            
            # Opciones para formularios
            context['tipo_proteccion_choices'] = Audiometria.TIPO_PROTECCION_CHOICES
            context['tolerancia_choices'] = Audiometria.TOLERANCIA_CHOICES
            context['severidad_caohc_choices'] = Audiometria.SEVERIDAD_CAOHC_CHOICES
            
            # Opciones para diagnósticos
            context['tipo_diagnostico_choices'] = DiagnosticoAuditivo.TIPO_DIAGNOSTICO_CHOICES
            context['lateralidad_choices'] = DiagnosticoAuditivo.LATERALIDAD_CHOICES
            context['tipo_impresion_choices'] = DiagnosticoAuditivo.TIPO_IMPRESION_CHOICES
            
            # Opciones para recomendaciones
            context['recomendacion_choices'] = RecomendacionAuditiva.RECOMENDACION_CHOICES
            
            # Datos para el gráfico de audiometría
            context['frecuencias'] = [250, 500, 1000, 2000, 3000, 4000, 6000, 8000]
            context['audiogram_data'] = {
                'va_od': [
                    audiometria.va_od_250, audiometria.va_od_500, audiometria.va_od_1000, audiometria.va_od_2000,
                    audiometria.va_od_3000, audiometria.va_od_4000, audiometria.va_od_6000, audiometria.va_od_8000
                ],
                'va_oi': [
                    audiometria.va_oi_250, audiometria.va_oi_500, audiometria.va_oi_1000, audiometria.va_oi_2000,
                    audiometria.va_oi_3000, audiometria.va_oi_4000, audiometria.va_oi_6000, audiometria.va_oi_8000
                ],
                'vo_od': [
                    audiometria.vo_od_250, audiometria.vo_od_500, audiometria.vo_od_1000, audiometria.vo_od_2000,
                    audiometria.vo_od_3000, audiometria.vo_od_4000, audiometria.vo_od_6000, audiometria.vo_od_8000
                ],
                'vo_oi': [
                    audiometria.vo_oi_250, audiometria.vo_oi_500, audiometria.vo_oi_1000, audiometria.vo_oi_2000,
                    audiometria.vo_oi_3000, audiometria.vo_oi_4000, audiometria.vo_oi_6000, audiometria.vo_oi_8000
                ]
            }
            
        except Audiometria.DoesNotExist:
            context['audiometria'] = None
        
        return context


class EspirometriaCreateView(LoginRequiredMixin, CreateView):
    """Crear nueva espirometría"""
    model = FichaClinica
    template_name = 'admision_recepcion/fichas_clinicas/espirometria_form.html'
    fields = [
        'fecha_evaluacion', 'numero_identificacion', 'tipo_documento', 
        'nombre_trabajador', 'fecha_nacimiento', 'genero', 'edad',
        'telefono', 'email', 'direccion', 'municipio', 'empresa', 'cargo',
        'profesional_evaluador'
    ]
    
    def form_valid(self, form):
        form.instance.tipo_ficha = 'ESPIROMETRIA'
        form.instance.created_by = self.request.user
        
        response = super().form_valid(form)
        
        # Crear la espirometría asociada
        Espirometria.objects.create(
            ficha_clinica=self.object,
            resultado_anterior='NO APLICA',
            escala_interpretacion='KNUDSON'
        )
        
        messages.success(self.request, 'Espirometría creada exitosamente.')
        return response
    
    def get_success_url(self):
        return reverse_lazy('admision_recepcion:espirometria_detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Nueva Espirometría'
        context['municipios'] = Municipio.objects.filter(activo=True).order_by('nombre')
        context['empresas'] = Empresa.objects.filter(activo=True).order_by('razon_social')
        context['profesionales'] = Prestador.objects.filter(activo=True).order_by('nombre')
        return context


class EspirometriaDetailView(LoginRequiredMixin, DetailView):
    """Detalle y edición de espirometría"""
    model = FichaClinica
    template_name = 'admision_recepcion/fichas_clinicas/espirometria_detail.html'
    context_object_name = 'ficha'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Espirometría'
        
        # Obtener la espirometría
        try:
            espirometria = self.object.espirometria
            context['espirometria'] = espirometria
            
            # Obtener recomendaciones
            context['recomendaciones_espirometria'] = espirometria.recomendaciones_espirometria.all().order_by('-fecha')
            
            # Opciones para formularios
            context['escala_interpretacion_choices'] = Espirometria.ESCALA_INTERPRETACION_CHOICES
            context['patron_funcional_choices'] = Espirometria.PATRON_FUNCIONAL_CHOICES
            context['severidad_choices'] = Espirometria.SEVERIDAD_CHOICES
            context['tipo_recomendacion_choices'] = RecomendacionEspirometria.TIPO_RECOMENDACION_CHOICES
            
            # Cálculos automáticos
            if espirometria.peso_kg and espirometria.talla_cm:
                context['imc_calculado'] = espirometria.calcular_imc()
            
            # Porcentajes predichos
            if espirometria.vef1_post and espirometria.vef1_teor:
                context['vef1_porcentaje'] = round(espirometria.calcular_porcentaje_predicho('vef1'), 1)
            
            if espirometria.cvf_post and espirometria.cvf_teor:
                context['cvf_porcentaje'] = round(espirometria.calcular_porcentaje_predicho('cvf'), 1)
            
            # Interpretación automática
            context['patron_interpretado'] = espirometria.interpretar_patron_funcional()
            context['severidad_calculada'] = espirometria.calcular_severidad()
            
        except Espirometria.DoesNotExist:
            context['espirometria'] = None
        
        return context


class EvaluacionOsteomuscularCreateView(LoginRequiredMixin, CreateView):
    """Crear nueva evaluación osteomuscular"""
    model = FichaClinica
    template_name = 'admision_recepcion/fichas_clinicas/osteomuscular_form.html'
    fields = [
        'fecha_evaluacion', 'numero_identificacion', 'tipo_documento', 
        'nombre_trabajador', 'fecha_nacimiento', 'genero', 'edad',
        'telefono', 'email', 'direccion', 'municipio', 'empresa', 'cargo',
        'profesional_evaluador'
    ]
    
    def form_valid(self, form):
        form.instance.tipo_ficha = 'OSTEOMUSCULAR'
        form.instance.created_by = self.request.user
        
        response = super().form_valid(form)
        
        # Crear la evaluación osteomuscular asociada
        EvaluacionOsteomuscular.objects.create(
            ficha_clinica=self.object
        )
        
        messages.success(self.request, 'Evaluación Osteomuscular creada exitosamente.')
        return response
    
    def get_success_url(self):
        return reverse_lazy('admision_recepcion:osteomuscular_detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Nueva Evaluación Osteomuscular'
        context['municipios'] = Municipio.objects.filter(activo=True).order_by('nombre')
        context['empresas'] = Empresa.objects.filter(activo=True).order_by('razon_social')
        context['profesionales'] = Prestador.objects.filter(activo=True).order_by('nombre')
        return context


class EvaluacionOsteomuscularDetailView(LoginRequiredMixin, DetailView):
    """Detalle y edición de evaluación osteomuscular"""
    model = FichaClinica
    template_name = 'admision_recepcion/fichas_clinicas/osteomuscular_detail.html'
    context_object_name = 'ficha'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Evaluación Osteomuscular'
        
        # Obtener la evaluación osteomuscular
        try:
            evaluacion = self.object.evaluacion_osteomuscular
            context['evaluacion'] = evaluacion
            
            # Obtener recomendaciones
            context['recomendaciones_osteomusculares'] = evaluacion.recomendaciones_osteomusculares.all().order_by('-fecha')
            
            # Opciones para formularios
            context['resultado_prueba_choices'] = EvaluacionOsteomuscular.RESULTADO_PRUEBA_CHOICES
            context['grado_flexibilidad_choices'] = EvaluacionOsteomuscular.GRADO_FLEXIBILIDAD_CHOICES
            context['fase_marcha_choices'] = EvaluacionOsteomuscular.FASE_MARCHA_CHOICES
            context['tipo_recomendacion_choices'] = RecomendacionOsteomuscular.TIPO_RECOMENDACION_CHOICES
            
            # Cálculos automáticos
            if evaluacion.peso_kg and evaluacion.talla_cm:
                context['imc_calculado'] = evaluacion.calcular_imc()
            
            # Análisis de pruebas
            context['alteraciones_posturales'] = evaluacion.get_alteraciones_posturales_total()
            context['pruebas_positivas'] = evaluacion.get_pruebas_positivas()
            context['alteraciones_marcha'] = evaluacion.get_alteraciones_marcha()
            context['resumen_flexibilidad'] = evaluacion.get_resumen_flexibilidad()
            
        except EvaluacionOsteomuscular.DoesNotExist:
            context['evaluacion'] = None
        
        return context


class HistoriaClinicaGeneralCreateView(LoginRequiredMixin, CreateView):
    """Crear nueva historia clínica general"""
    model = FichaClinica
    template_name = 'admision_recepcion/fichas_clinicas/historia_clinica_general_form.html'
    fields = [
        'fecha_evaluacion', 'numero_identificacion', 'tipo_documento', 
        'nombre_trabajador', 'fecha_nacimiento', 'genero', 'edad',
        'telefono', 'email', 'direccion', 'municipio', 'empresa', 'cargo',
        'profesional_evaluador'
    ]
    
    def form_valid(self, form):
        form.instance.tipo_ficha = 'HISTORIA_CLINICA_GENERAL'
        form.instance.created_by = self.request.user
        
        response = super().form_valid(form)
        
        # Crear la historia clínica general asociada
        historia = HistoriaClinicaGeneral.objects.create(
            ficha_clinica=self.object
        )
        
        # Crear antecedentes familiares por defecto
        antecedentes_familiares = [
            'HIPERTENSION_ARTERIAL', 'DIABETES', 'CANCER', 'OTROS'
        ]
        for tipo in antecedentes_familiares:
            AntecedenteFamiliarGeneral.objects.create(
                historia_clinica=historia,
                tipo_antecedente=tipo,
                observacion='NO REFIERE'
            )
        
        # Crear antecedentes personales por defecto
        antecedentes_personales = [
            'HTA', 'DIABETES', 'ENF_RENAL', 'ENF_ARTICULAR', 'TBC', 'VENEREAS',
            'SIND_CONVULSIVO', 'INMUNOLOGICOS', 'HOSPITALIZACIONES', 
            'TOXICOS_ALERGICOS', 'TRAUMATICO', 'QUIRURGICOS', 'OTRO'
        ]
        for tipo in antecedentes_personales:
            AntecedentePersonalGeneral.objects.create(
                historia_clinica=historia,
                tipo_antecedente=tipo,
                observacion='NO REFIERE'
            )
        
        messages.success(self.request, 'Historia Clínica General creada exitosamente.')
        return response
    
    def get_success_url(self):
        return reverse_lazy('admision_recepcion:historia_clinica_general_detail', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Nueva Historia Clínica General'
        context['municipios'] = Municipio.objects.filter(activo=True).order_by('nombre')
        context['empresas'] = Empresa.objects.filter(activo=True).order_by('razon_social')
        context['profesionales'] = Prestador.objects.filter(activo=True).order_by('nombre')
        return context


class HistoriaClinicaGeneralDetailView(LoginRequiredMixin, DetailView):
    """Detalle y edición de historia clínica general"""
    model = FichaClinica
    template_name = 'admision_recepcion/fichas_clinicas/historia_clinica_general_detail.html'
    context_object_name = 'ficha'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Historia Clínica General'
        
        # Obtener la historia clínica general
        try:
            historia = self.object.historia_clinica_general
            context['historia'] = historia
            
            # Obtener todos los elementos relacionados
            context['antecedentes_familiares'] = historia.antecedentes_familiares.all().order_by('tipo_antecedente')
            context['antecedentes_personales'] = historia.antecedentes_personales.all().order_by('tipo_antecedente')
            context['documentos_clinicos'] = historia.documentos_clinicos.all().order_by('-fecha_creacion')
            context['diagnosticos'] = historia.diagnosticos.all().order_by('tipo_diagnostico', '-fecha')
            context['ordenes_medicamentos'] = historia.ordenes_medicamentos.all().order_by('-fecha_creacion')
            context['ordenes_servicios'] = historia.ordenes_servicios.all().order_by('-fecha_creacion')
            context['ordenes_remisiones'] = historia.ordenes_remisiones.all().order_by('-fecha_creacion')
            context['ordenes_incapacidades'] = historia.ordenes_incapacidades.all().order_by('-fecha_creacion')
            context['certificados_medicos'] = historia.certificados_medicos.all().order_by('-fecha_creacion')
            context['evoluciones'] = historia.evoluciones.all().order_by('-fecha')
            
            # Opciones para formularios
            context['tipo_evaluacion_choices'] = HistoriaClinicaGeneral.TIPO_EVALUACION_CHOICES
            context['estado_civil_choices'] = HistoriaClinicaGeneral.ESTADO_CIVIL_CHOICES
            context['nivel_educativo_choices'] = HistoriaClinicaGeneral.NIVEL_EDUCATIVO_CHOICES
            context['lateralidad_choices'] = HistoriaClinicaGeneral.LATERALIDAD_CHOICES
            context['clasificacion_ta_choices'] = HistoriaClinicaGeneral.CLASIFICACION_TA_CHOICES
            
            # Opciones para tipos de diagnóstico y órdenes
            context['tipo_diagnostico_choices'] = DiagnosticoGeneral.TIPO_DIAGNOSTICO_CHOICES
            context['tipo_impresion_choices'] = DiagnosticoGeneral.TIPO_IMPRESION_CHOICES
            context['tipo_incapacidad_choices'] = OrdenIncapacidad.TIPO_INCAPACIDAD_CHOICES
            
            # Cálculos automáticos
            if historia.peso_kg and historia.talla_cm:
                context['imc_calculado'] = historia.calcular_imc()
            
            if historia.tension_sistolica and historia.tension_diastolica:
                context['clasificacion_ta_calculada'] = historia.clasificar_tension_arterial()
            
            if historia.perimetro_abdominal:
                context['interpretacion_perimetro_calculada'] = historia.interpretar_perimetro_abdominal()
            
            # Datos JSON de revisión por sistemas y examen físico
            context['revision_sistemas_defaults'] = historia.get_revision_sistemas_defaults()
            context['examen_fisico_defaults'] = historia.get_examen_fisico_defaults()
            
        except HistoriaClinicaGeneral.DoesNotExist:
            context['historia'] = None
        
        # Lista de prestadores para evoluciones y diagnósticos
        context['prestadores'] = Prestador.objects.filter(activo=True).order_by('nombre')
        
        return context


class HistoriasClinicasCerradasView(LoginRequiredMixin, TemplateView):
    """Vista para consultar historias clínicas cerradas/completadas"""
    template_name = 'admision_recepcion/fichas_clinicas/historias_cerradas.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Historias Clínicas Cerradas'
        
        # Obtener parámetros de filtro
        numero_identificacion = self.request.GET.get('numero_identificacion', '')
        nombre_paciente = self.request.GET.get('nombre_paciente', '')
        nombre_empresa = self.request.GET.get('nombre_empresa', '')
        fecha_desde = self.request.GET.get('fecha_desde', '')
        fecha_hasta = self.request.GET.get('fecha_hasta', '')
        
        # Si no hay fecha desde/hasta, usar la fecha de hoy por defecto
        if not fecha_desde and not fecha_hasta:
            from datetime import date
            hoy = date.today()
            fecha_desde = hoy.strftime('%Y-%m-%d')
            fecha_hasta = hoy.strftime('%Y-%m-%d')
        
        # Construir queryset base de fichas clínicas cerradas/completadas
        queryset = FichaClinica.objects.filter(
            estado__in=['COMPLETADA', 'CERRADA']
        ).select_related(
            'empresa', 'profesional_evaluador', 'municipio'
        ).order_by('-fecha_evaluacion', '-fecha_creacion')
        
        # Aplicar filtros
        if numero_identificacion:
            queryset = queryset.filter(numero_identificacion__icontains=numero_identificacion)
        
        if nombre_paciente:
            queryset = queryset.filter(nombre_trabajador__icontains=nombre_paciente)
        
        if nombre_empresa:
            queryset = queryset.filter(empresa__razon_social__icontains=nombre_empresa)
        
        if fecha_desde:
            try:
                from datetime import datetime
                fecha_desde_obj = datetime.strptime(fecha_desde, '%Y-%m-%d').date()
                queryset = queryset.filter(fecha_evaluacion__gte=fecha_desde_obj)
            except ValueError:
                pass
        
        if fecha_hasta:
            try:
                from datetime import datetime
                fecha_hasta_obj = datetime.strptime(fecha_hasta, '%Y-%m-%d').date()
                queryset = queryset.filter(fecha_evaluacion__lte=fecha_hasta_obj)
            except ValueError:
                pass
        
        # Limitar resultados para rendimiento
        historias = queryset[:100]  # Máximo 100 resultados
        
        # Agregar información adicional de cada historia
        historias_con_info = []
        for historia in historias:
            info_adicional = {
                'ficha': historia,
                'tipo_evaluacion': '',
                'diagnosticos': [],
                'total_diagnosticos': 0,
                'tiene_ordenes': False,
                'url_detalle': '',
            }
            
            # Determinar tipo y URL según el tipo de ficha
            if historia.tipo_ficha == 'EVALUACION_OCUPACIONAL':
                try:
                    eval_ocup = historia.evaluacion_ocupacional
                    info_adicional['tipo_evaluacion'] = 'Evaluación Ocupacional'
                    info_adicional['url_detalle'] = f'/admision/evaluacion-ocupacional/{historia.pk}/'
                except:
                    info_adicional['tipo_evaluacion'] = 'Evaluación Ocupacional'
                    info_adicional['url_detalle'] = '#'
            
            elif historia.tipo_ficha == 'EXAMEN_VISUAL':
                try:
                    examen = historia.examen_visual
                    info_adicional['tipo_evaluacion'] = 'Examen Visual'
                    info_adicional['diagnosticos'] = list(examen.diagnosticos_visuales.all()[:3])
                    info_adicional['total_diagnosticos'] = examen.diagnosticos_visuales.count()
                    info_adicional['url_detalle'] = f'/admision/examen-visual/{historia.pk}/'
                except:
                    info_adicional['tipo_evaluacion'] = 'Examen Visual'
                    info_adicional['url_detalle'] = '#'
            
            elif historia.tipo_ficha == 'AUDIOMETRIA':
                try:
                    audio = historia.audiometria
                    info_adicional['tipo_evaluacion'] = 'Audiometría'
                    info_adicional['diagnosticos'] = list(audio.diagnosticos_auditivos.all()[:3])
                    info_adicional['total_diagnosticos'] = audio.diagnosticos_auditivos.count()
                    info_adicional['url_detalle'] = f'/admision/audiometria/{historia.pk}/'
                except:
                    info_adicional['tipo_evaluacion'] = 'Audiometría'
                    info_adicional['url_detalle'] = '#'
            
            elif historia.tipo_ficha == 'ESPIROMETRIA':
                try:
                    espiro = historia.espirometria
                    info_adicional['tipo_evaluacion'] = 'Espirometría'
                    info_adicional['url_detalle'] = f'/admision/espirometria/{historia.pk}/'
                except:
                    info_adicional['tipo_evaluacion'] = 'Espirometría'
                    info_adicional['url_detalle'] = '#'
            
            elif historia.tipo_ficha == 'OSTEOMUSCULAR':
                try:
                    osteo = historia.evaluacion_osteomuscular
                    info_adicional['tipo_evaluacion'] = 'Evaluación Osteomuscular'
                    info_adicional['url_detalle'] = f'/admision/osteomuscular/{historia.pk}/'
                except:
                    info_adicional['tipo_evaluacion'] = 'Evaluación Osteomuscular'
                    info_adicional['url_detalle'] = '#'
            
            elif historia.tipo_ficha == 'HISTORIA_CLINICA_GENERAL':
                try:
                    hc_general = historia.historia_clinica_general
                    info_adicional['tipo_evaluacion'] = 'Historia Clínica General'
                    info_adicional['diagnosticos'] = list(hc_general.diagnosticos.filter(tipo_diagnostico='PRINCIPAL')[:3])
                    info_adicional['total_diagnosticos'] = hc_general.diagnosticos.count()
                    info_adicional['tiene_ordenes'] = (
                        hc_general.ordenes_medicamentos.exists() or 
                        hc_general.ordenes_servicios.exists() or 
                        hc_general.ordenes_remisiones.exists()
                    )
                    info_adicional['url_detalle'] = f'/admision/historia-clinica-general/{historia.pk}/'
                except:
                    info_adicional['tipo_evaluacion'] = 'Historia Clínica General'
                    info_adicional['url_detalle'] = '#'
            
            else:
                info_adicional['tipo_evaluacion'] = historia.get_tipo_ficha_display()
                info_adicional['url_detalle'] = '#'
            
            historias_con_info.append(info_adicional)
        
        context['historias'] = historias_con_info
        context['total_historias'] = len(historias_con_info)
        
        # Parámetros de filtro para el template
        context['filtros'] = {
            'numero_identificacion': numero_identificacion,
            'nombre_paciente': nombre_paciente,
            'nombre_empresa': nombre_empresa,
            'fecha_desde': fecha_desde,
            'fecha_hasta': fecha_hasta,
        }
        
        # Datos para los selectores
        context['empresas'] = Empresa.objects.filter(activo=True).order_by('razon_social')
        
        # Estadísticas para el dashboard
        context['estadisticas'] = {
            'total_periodo': len(historias_con_info),
            'por_tipo': {},
            'por_empresa': {},
            'por_estado': {},
        }
        
        # Calcular estadísticas por tipo
        for historia_info in historias_con_info:
            tipo = historia_info['tipo_evaluacion']
            context['estadisticas']['por_tipo'][tipo] = context['estadisticas']['por_tipo'].get(tipo, 0) + 1
        
        # Calcular estadísticas por empresa
        for historia_info in historias_con_info:
            empresa = historia_info['ficha'].empresa.razon_social if historia_info['ficha'].empresa else 'Sin empresa'
            context['estadisticas']['por_empresa'][empresa] = context['estadisticas']['por_empresa'].get(empresa, 0) + 1
        
        # Calcular estadísticas por estado
        for historia_info in historias_con_info:
            estado = historia_info['ficha'].get_estado_display()
            context['estadisticas']['por_estado'][estado] = context['estadisticas']['por_estado'].get(estado, 0) + 1
        
        return context


# ===== VISTAS AJAX =====

def agregar_seguimiento_ajax(request, pk):
    """Agregar seguimiento vía AJAX"""
    if request.method == 'POST':
        orden = get_object_or_404(OrdenServicio, pk=pk)
        form = SeguimientoPacienteForm(request.POST)
        
        if form.is_valid():
            seguimiento = form.save(commit=False)
            seguimiento.orden = orden
            seguimiento.usuario = request.user
            seguimiento.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Seguimiento agregado exitosamente',
                'data': {
                    'estado': seguimiento.get_estado_display(),
                    'fecha': seguimiento.fecha_estado.strftime('%d/%m/%Y %H:%M'),
                    'usuario': seguimiento.usuario.get_full_name() if seguimiento.usuario else '',
                    'observaciones': seguimiento.observaciones
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})


def buscar_servicio_ajax(request):
    """Buscar servicios vía AJAX"""
    term = request.GET.get('term', '')
    servicios = Servicio.objects.filter(
        Q(nombre__icontains=term) | Q(codigo__icontains=term),
        activo=True
    )[:10]
    
    results = []
    for servicio in servicios:
        results.append({
            'id': servicio.id,
            'text': f"{servicio.codigo} - {servicio.nombre}",
            'valor_base': float(servicio.valor_base)
        })
    
    return JsonResponse({'results': results})


def buscar_prestador_ajax(request):
    """Buscar prestadores vía AJAX"""
    term = request.GET.get('term', '')
    prestadores = Prestador.objects.filter(
        Q(nombre__icontains=term) | Q(codigo__icontains=term),
        activo=True
    )[:10]
    
    results = []
    for prestador in prestadores:
        results.append({
            'id': prestador.id,
            'text': f"{prestador.codigo} - {prestador.nombre}",
            'especialidad': prestador.especialidad
        })
    
    return JsonResponse({'results': results})


def cambiar_estado_orden_ajax(request, pk):
    """Cambiar estado de orden vía AJAX"""
    if request.method == 'POST':
        orden = get_object_or_404(OrdenServicio, pk=pk)
        nuevo_estado = request.POST.get('estado')
        
        if nuevo_estado in [choice[0] for choice in OrdenServicio.ESTADO_ORDEN_CHOICES]:
            orden.estado_orden = nuevo_estado
            orden.save()
            
            # Crear seguimiento automático
            SeguimientoPaciente.objects.create(
                orden=orden,
                estado=nuevo_estado,
                observaciones=f'Estado cambiado a {orden.get_estado_orden_display()}',
                usuario=request.user
            )
            
            return JsonResponse({
                'success': True,
                'message': f'Estado cambiado a {orden.get_estado_orden_display()}',
                'nuevo_estado': orden.get_estado_orden_display()
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Estado no válido'
            })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})


def confirmar_cita_ajax(request, pk):
    """Confirmar cita empresarial vía AJAX"""
    if request.method == 'POST':
        cita = get_object_or_404(CitaEmpresarial, pk=pk)
        
        if cita.puede_confirmar:
            cita.confirmar_cita(request.user)
            
            return JsonResponse({
                'success': True,
                'message': f'Cita {cita.numero_cita} confirmada exitosamente',
                'nuevo_estado': cita.get_estado_display()
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'La cita no puede ser confirmada en su estado actual'
            })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})


def cancelar_cita_ajax(request, pk):
    """Cancelar cita empresarial vía AJAX"""
    if request.method == 'POST':
        cita = get_object_or_404(CitaEmpresarial, pk=pk)
        motivo = request.POST.get('motivo', '')
        
        if cita.puede_cancelar:
            cita.cancelar_cita(motivo, request.user)
            
            return JsonResponse({
                'success': True,
                'message': f'Cita {cita.numero_cita} cancelada exitosamente',
                'nuevo_estado': cita.get_estado_display()
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'La cita no puede ser cancelada en su estado actual'
            })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})


def crear_orden_desde_cita_ajax(request, pk):
    """Crear orden de servicio desde cita empresarial vía AJAX"""
    if request.method == 'POST':
        cita = get_object_or_404(CitaEmpresarial, pk=pk)
        
        try:
            orden = cita.crear_orden_servicio(request.user)
            
            return JsonResponse({
                'success': True,
                'message': f'Orden {orden.numero_orden} creada desde cita {cita.numero_cita}',
                'orden_id': orden.id,
                'numero_orden': orden.numero_orden
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error al crear orden: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})


def buscar_empresa_ajax(request):
    """Buscar empresas para el filtro vía AJAX"""
    term = request.GET.get('term', '')
    empresas = Empresa.objects.filter(
        Q(razon_social__icontains=term) | Q(nombre_comercial__icontains=term),
        activo=True
    )[:10]
    
    results = []
    for empresa in empresas:
        results.append({
            'id': empresa.id,
            'text': empresa.razon_social,
            'nit': empresa.nit
        })
    
    return JsonResponse({'results': results})


def buscar_trabajador_ajax(request):
    """Buscar trabajadores en citas para el filtro vía AJAX"""
    term = request.GET.get('term', '')
    citas = CitaEmpresarial.objects.filter(
        Q(nombre_trabajador__icontains=term) | Q(numero_identificacion__icontains=term)
    ).values(
        'nombre_trabajador', 'numero_identificacion'
    ).distinct()[:10]
    
    results = []
    for cita in citas:
        results.append({
            'text': f"{cita['nombre_trabajador']} - {cita['numero_identificacion']}",
            'nombre': cita['nombre_trabajador'],
            'identificacion': cita['numero_identificacion']
        })
    
    return JsonResponse({'results': results})


# ===== VISTAS PARA MODELOS AUXILIARES =====

class EmpresaListView(LoginRequiredMixin, ListView):
    model = Empresa
    template_name = 'admision_recepcion/empresa_list.html'
    context_object_name = 'empresas'
    paginate_by = 20


class EmpresaCreateView(LoginRequiredMixin, CreateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'admision_recepcion/empresa_form.html'
    success_url = reverse_lazy('admision_recepcion:empresa_list')


class ConvenioListView(LoginRequiredMixin, ListView):
    model = Convenio
    template_name = 'admision_recepcion/convenio_list.html'
    context_object_name = 'convenios'
    paginate_by = 20


class ConvenioCreateView(LoginRequiredMixin, CreateView):
    model = Convenio
    form_class = ConvenioForm
    template_name = 'admision_recepcion/convenio_form.html'
    success_url = reverse_lazy('admision_recepcion:convenio_list')


class ServicioListView(LoginRequiredMixin, ListView):
    model = Servicio
    template_name = 'admision_recepcion/servicio_list.html'
    context_object_name = 'servicios'
    paginate_by = 20


class ServicioCreateView(LoginRequiredMixin, CreateView):
    model = Servicio
    form_class = ServicioForm
    template_name = 'admision_recepcion/servicio_form.html'
    success_url = reverse_lazy('admision_recepcion:servicio_list')


class PrestadorListView(LoginRequiredMixin, ListView):
    model = Prestador
    template_name = 'admision_recepcion/prestador_list.html'
    context_object_name = 'prestadores'
    paginate_by = 20


class PrestadorCreateView(LoginRequiredMixin, CreateView):
    model = Prestador
    form_class = PrestadorForm
    template_name = 'admision_recepcion/prestador_form.html'
    success_url = reverse_lazy('admision_recepcion:prestador_list')
