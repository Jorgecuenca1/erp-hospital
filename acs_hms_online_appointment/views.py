from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.utils import timezone
from .models import (
    DoctorAvailability, 
    OnlineAppointmentSlot, 
    OnlineAppointment,
    AgendaElectronicaDisponibilidad,
    DisponibilidadDetalle
)
from .forms import (
    AgendaElectronicaDisponibilidadForm,
    DoctorAvailabilityForm,
    OnlineAppointmentForm
)

class OnlineAppointmentDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_online_appointment/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Online Appointment'
        context['module_type'] = 'hms'
        return context

class OnlineAppointmentListView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_online_appointment/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Online Appointment'
        return context

class OnlineAppointmentCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_online_appointment/create.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Online Appointment'
        return context

class OnlineAppointmentDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_online_appointment/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Online Appointment'
        return context

class OnlineAppointmentUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_online_appointment/update.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Online Appointment'
        return context

class OnlineAppointmentDeleteView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_online_appointment/delete.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Online Appointment'
        return context

class OnlineAppointmentReportsView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_online_appointment/reports.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Online Appointment'
        return context


# ===== VISTAS PARA AGENDA ELECTRÓNICA =====

class AgendaElectronicaCreateView(LoginRequiredMixin, CreateView):
    """Vista para crear disponibilidad en agenda electrónica"""
    model = AgendaElectronicaDisponibilidad
    form_class = AgendaElectronicaDisponibilidadForm
    template_name = 'acs_hms_online_appointment/agenda_electronica/create.html'
    success_url = reverse_lazy('acs_hms_online_appointment:agenda_list')
    
    def form_valid(self, form):
        """Procesar formulario válido y generar disponibilidad"""
        form.instance.created_by = self.request.user
        
        # Guardar el registro principal
        response = super().form_valid(form)
        
        try:
            # Generar los slots de disponibilidad automáticamente
            slots_creados = self.object.generar_slots_disponibilidad()
            
            messages.success(
                self.request, 
                f'Disponibilidad creada exitosamente. Se generaron {slots_creados} slots de disponibilidad.'
            )
            
        except Exception as e:
            messages.error(
                self.request, 
                f'Error al generar slots de disponibilidad: {str(e)}'
            )
        
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Agenda Electrónica'
        context['page_title'] = 'Crear Disponibilidad'
        context['breadcrumbs'] = [
            {'title': 'Agenda Electrónica', 'url': reverse_lazy('acs_hms_online_appointment:agenda_list')},
            {'title': 'Crear Disponibilidad', 'url': None}
        ]
        return context


class AgendaElectronicaListView(LoginRequiredMixin, ListView):
    """Vista para listar disponibilidades de agenda electrónica"""
    model = AgendaElectronicaDisponibilidad
    template_name = 'acs_hms_online_appointment/agenda_electronica/list.html'
    context_object_name = 'disponibilidades'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('profesional__user', 'created_by')
        
        # Filtros
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                profesional__user__first_name__icontains=search
            ) | queryset.filter(
                profesional__user__last_name__icontains=search
            )
        
        sede = self.request.GET.get('sede')
        if sede:
            queryset = queryset.filter(sede=sede)
        
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Agenda Electrónica'
        context['page_title'] = 'Lista de Disponibilidades'
        context['sede_choices'] = DoctorAvailability.SEDE_CHOICES
        context['status_choices'] = AgendaElectronicaDisponibilidad.STATUS_CHOICES
        context['breadcrumbs'] = [
            {'title': 'Agenda Electrónica', 'url': None}
        ]
        return context


class AgendaElectronicaDetailView(LoginRequiredMixin, DetailView):
    """Vista para ver detalle de disponibilidad"""
    model = AgendaElectronicaDisponibilidad
    template_name = 'acs_hms_online_appointment/agenda_electronica/detail.html'
    context_object_name = 'disponibilidad'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Agenda Electrónica'
        context['page_title'] = f'Disponibilidad - {self.object.profesional.user.get_full_name()}'
        
        # Obtener disponibilidades relacionadas generadas
        availabilities = DoctorAvailability.objects.filter(
            doctor=self.object.profesional,
            sede=self.object.sede
        ).order_by('day_of_week', 'start_time')
        
        context['availabilities'] = availabilities
        context['dias_seleccionados'] = self.object.get_dias_seleccionados()
        
        context['breadcrumbs'] = [
            {'title': 'Agenda Electrónica', 'url': reverse_lazy('acs_hms_online_appointment:agenda_list')},
            {'title': f'Detalle - {self.object.profesional.user.get_full_name()}', 'url': None}
        ]
        return context


class AgendaElectronicaUpdateView(LoginRequiredMixin, UpdateView):
    """Vista para actualizar disponibilidad"""
    model = AgendaElectronicaDisponibilidad
    form_class = AgendaElectronicaDisponibilidadForm
    template_name = 'acs_hms_online_appointment/agenda_electronica/update.html'
    
    def get_success_url(self):
        return reverse_lazy('acs_hms_online_appointment:agenda_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        """Procesar formulario válido y regenerar disponibilidad si es necesario"""
        response = super().form_valid(form)
        
        try:
            # Regenerar slots si hubo cambios significativos
            slots_creados = self.object.generar_slots_disponibilidad()
            
            messages.success(
                self.request, 
                f'Disponibilidad actualizada exitosamente. Se actualizaron {slots_creados} slots.'
            )
            
        except Exception as e:
            messages.error(
                self.request, 
                f'Error al actualizar slots de disponibilidad: {str(e)}'
            )
        
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Agenda Electrónica'
        context['page_title'] = f'Editar - {self.object.profesional.user.get_full_name()}'
        context['breadcrumbs'] = [
            {'title': 'Agenda Electrónica', 'url': reverse_lazy('acs_hms_online_appointment:agenda_list')},
            {'title': f'Detalle - {self.object.profesional.user.get_full_name()}', 'url': reverse_lazy('acs_hms_online_appointment:agenda_detail', kwargs={'pk': self.object.pk})},
            {'title': 'Editar', 'url': None}
        ]
        return context


class AgendaElectronicaDeleteView(LoginRequiredMixin, DeleteView):
    """Vista para eliminar disponibilidad"""
    model = AgendaElectronicaDisponibilidad
    template_name = 'acs_hms_online_appointment/agenda_electronica/delete.html'
    success_url = reverse_lazy('acs_hms_online_appointment:agenda_list')
    
    def delete(self, request, *args, **kwargs):
        """Eliminar disponibilidad y sus slots relacionados"""
        self.object = self.get_object()
        
        try:
            # Eliminar disponibilidades relacionadas de DoctorAvailability
            DoctorAvailability.objects.filter(
                doctor=self.object.profesional,
                sede=self.object.sede
            ).delete()
            
            messages.success(
                request, 
                f'Disponibilidad de {self.object.profesional.user.get_full_name()} eliminada exitosamente.'
            )
            
        except Exception as e:
            messages.error(
                request, 
                f'Error al eliminar disponibilidad: {str(e)}'
            )
        
        return super().delete(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Agenda Electrónica'
        context['page_title'] = f'Eliminar - {self.object.profesional.user.get_full_name()}'
        context['breadcrumbs'] = [
            {'title': 'Agenda Electrónica', 'url': reverse_lazy('acs_hms_online_appointment:agenda_list')},
            {'title': f'Detalle - {self.object.profesional.user.get_full_name()}', 'url': reverse_lazy('acs_hms_online_appointment:agenda_detail', kwargs={'pk': self.object.pk})},
            {'title': 'Eliminar', 'url': None}
        ]
        return context


# ===== VISTAS AJAX Y API =====

class AgendaDisponibilidadTableView(LoginRequiredMixin, TemplateView):
    """Vista para mostrar tabla de disponibilidad con integraciones"""
    template_name = 'acs_hms_online_appointment/agenda_electronica/tabla_disponibilidad.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        agenda_id = self.kwargs.get('pk')
        
        try:
            agenda = AgendaElectronicaDisponibilidad.objects.get(pk=agenda_id)
            context['agenda'] = agenda
            
            # Generar tabla de disponibilidad detallada
            from datetime import datetime, timedelta
            
            disponibilidad_detalle = []
            current_date = agenda.fecha_desde
            
            # Mapeo de días de la semana
            weekday_mapping = {
                0: agenda.lunes,    # Monday
                1: agenda.martes,   # Tuesday
                2: agenda.miercoles, # Wednesday
                3: agenda.jueves,   # Thursday
                4: agenda.viernes,  # Friday
                5: agenda.sabado,   # Saturday
                6: agenda.domingo,  # Sunday
            }
            
            while current_date <= agenda.fecha_hasta:
                weekday = current_date.weekday()
                
                if weekday_mapping.get(weekday, False):
                    # Agregar slots de mañana
                    if agenda.tiene_horario_manana():
                        disponibilidad_detalle.append({
                            'fecha': current_date,
                            'hora_inicio': agenda.hora_inicio_am,
                            'hora_fin': agenda.hora_fin_am,
                            'agenda_tus_citas': agenda.habilitar_agenda_tus_citas,
                            'doctoralia': agenda.habilitar_doctoralia,
                        })
                    
                    # Agregar slots de tarde
                    if agenda.tiene_horario_tarde():
                        disponibilidad_detalle.append({
                            'fecha': current_date,
                            'hora_inicio': agenda.hora_inicio_pm,
                            'hora_fin': agenda.hora_fin_pm,
                            'agenda_tus_citas': agenda.habilitar_agenda_tus_citas,
                            'doctoralia': agenda.habilitar_doctoralia,
                        })
                
                current_date += timedelta(days=1)
            
            context['disponibilidad_detalle'] = disponibilidad_detalle
            
        except AgendaElectronicaDisponibilidad.DoesNotExist:
            messages.error(self.request, 'Disponibilidad no encontrada')
            context['agenda'] = None
            context['disponibilidad_detalle'] = []
        
        context['module_name'] = 'Agenda Electrónica'
        context['page_title'] = 'Tabla de Disponibilidad'
        
        return context


# ===== VISTAS PARA GESTIÓN DE DISPONIBILIDAD INDIVIDUAL =====

class DoctorAvailabilityListView(LoginRequiredMixin, ListView):
    """Vista para listar disponibilidades individuales de doctores"""
    model = DoctorAvailability
    template_name = 'acs_hms_online_appointment/availability/list.html'
    context_object_name = 'availabilities'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('doctor__user').order_by('doctor__user__last_name', 'day_of_week', 'start_time')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Gestión de Disponibilidad'
        context['page_title'] = 'Disponibilidades de Doctores'
        return context


class DoctorAvailabilityCreateView(LoginRequiredMixin, CreateView):
    """Vista para crear disponibilidad individual de doctor"""
    model = DoctorAvailability
    form_class = DoctorAvailabilityForm
    template_name = 'acs_hms_online_appointment/availability/create.html'
    success_url = reverse_lazy('acs_hms_online_appointment:availability_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Disponibilidad de doctor creada exitosamente.')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Gestión de Disponibilidad'
        context['page_title'] = 'Crear Disponibilidad de Doctor'
        return context
