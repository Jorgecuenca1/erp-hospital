from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views import View
from datetime import datetime, timedelta
from .models import (
    Hospital, Department, Room, HMSUser, Patient, 
    Appointment, MedicalRecord, HospitalConfiguration
)
from .forms import (
    HospitalForm, DepartmentForm, RoomForm, HMSUserForm, PatientForm,
    AppointmentForm, MedicalRecordForm, HospitalConfigurationForm
)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'acs_hms_base/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = datetime.now().date()
        
        # Get statistics
        context['total_patients'] = Patient.objects.filter(active=True).count()
        context['total_doctors'] = HMSUser.objects.filter(user_type='DOCTOR', active=True).count()
        context['total_appointments'] = Appointment.objects.filter(appointment_date=today).count()
        context['total_rooms'] = Room.objects.filter(active=True).count()
        
        # Get recent appointments
        context['recent_appointments'] = Appointment.objects.filter(
            appointment_date__gte=today
        ).order_by('appointment_date', 'appointment_time')[:10]
        
        # Get available rooms
        context['available_rooms'] = Room.objects.filter(
            status='AVAILABLE', active=True
        ).count()
        
        # Get today's appointments by status
        today_appointments = Appointment.objects.filter(appointment_date=today)
        context['appointments_by_status'] = {
            'scheduled': today_appointments.filter(status='SCHEDULED').count(),
            'confirmed': today_appointments.filter(status='CONFIRMED').count(),
            'in_progress': today_appointments.filter(status='IN_PROGRESS').count(),
            'completed': today_appointments.filter(status='COMPLETED').count(),
        }
        
        return context


# Hospital Views
class HospitalListView(LoginRequiredMixin, ListView):
    model = Hospital
    template_name = 'acs_hms_base/hospital_list.html'
    context_object_name = 'hospitals'
    paginate_by = 10


class HospitalDetailView(LoginRequiredMixin, DetailView):
    model = Hospital
    template_name = 'acs_hms_base/hospital_detail.html'
    context_object_name = 'hospital'


class HospitalCreateView(LoginRequiredMixin, CreateView):
    model = Hospital
    form_class = HospitalForm
    template_name = 'acs_hms_base/hospital_form.html'
    success_url = reverse_lazy('acs_hms_base:hospital_list')


class HospitalUpdateView(LoginRequiredMixin, UpdateView):
    model = Hospital
    form_class = HospitalForm
    template_name = 'acs_hms_base/hospital_form.html'
    success_url = reverse_lazy('acs_hms_base:hospital_list')


class HospitalDeleteView(LoginRequiredMixin, DeleteView):
    model = Hospital
    template_name = 'acs_hms_base/hospital_confirm_delete.html'
    success_url = reverse_lazy('acs_hms_base:hospital_list')


# Department Views
class DepartmentListView(LoginRequiredMixin, ListView):
    model = Department
    template_name = 'acs_hms_base/department_list.html'
    context_object_name = 'departments'
    paginate_by = 10


class DepartmentDetailView(LoginRequiredMixin, DetailView):
    model = Department
    template_name = 'acs_hms_base/department_detail.html'
    context_object_name = 'department'


class DepartmentCreateView(LoginRequiredMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'acs_hms_base/department_form.html'
    success_url = reverse_lazy('acs_hms_base:department_list')


class DepartmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = 'acs_hms_base/department_form.html'
    success_url = reverse_lazy('acs_hms_base:department_list')


class DepartmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Department
    template_name = 'acs_hms_base/department_confirm_delete.html'
    success_url = reverse_lazy('acs_hms_base:department_list')


# Room Views
class RoomListView(LoginRequiredMixin, ListView):
    model = Room
    template_name = 'acs_hms_base/room_list.html'
    context_object_name = 'rooms'
    paginate_by = 10


class RoomDetailView(LoginRequiredMixin, DetailView):
    model = Room
    template_name = 'acs_hms_base/room_detail.html'
    context_object_name = 'room'


class RoomCreateView(LoginRequiredMixin, CreateView):
    model = Room
    form_class = RoomForm
    template_name = 'acs_hms_base/room_form.html'
    success_url = reverse_lazy('acs_hms_base:room_list')


class RoomUpdateView(LoginRequiredMixin, UpdateView):
    model = Room
    form_class = RoomForm
    template_name = 'acs_hms_base/room_form.html'
    success_url = reverse_lazy('acs_hms_base:room_list')


class RoomDeleteView(LoginRequiredMixin, DeleteView):
    model = Room
    template_name = 'acs_hms_base/room_confirm_delete.html'
    success_url = reverse_lazy('acs_hms_base:room_list')


# HMS User Views
class HMSUserListView(LoginRequiredMixin, ListView):
    model = HMSUser
    template_name = 'acs_hms_base/user_list.html'
    context_object_name = 'users'
    paginate_by = 10


class HMSUserDetailView(LoginRequiredMixin, DetailView):
    model = HMSUser
    template_name = 'acs_hms_base/user_detail.html'
    context_object_name = 'user'


class HMSUserCreateView(LoginRequiredMixin, CreateView):
    model = HMSUser
    form_class = HMSUserForm
    template_name = 'acs_hms_base/user_form.html'
    success_url = reverse_lazy('acs_hms_base:user_list')


class HMSUserUpdateView(LoginRequiredMixin, UpdateView):
    model = HMSUser
    form_class = HMSUserForm
    template_name = 'acs_hms_base/user_form.html'
    success_url = reverse_lazy('acs_hms_base:user_list')


class HMSUserDeleteView(LoginRequiredMixin, DeleteView):
    model = HMSUser
    template_name = 'acs_hms_base/user_confirm_delete.html'
    success_url = reverse_lazy('acs_hms_base:user_list')


# Patient Views
class PatientListView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'acs_hms_base/patient_list.html'
    context_object_name = 'patients'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Patient.objects.filter(active=True)
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(patient_id__icontains=search_query) |
                Q(medical_record_number__icontains=search_query)
            )
        return queryset


class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = 'acs_hms_base/patient_detail.html'
    context_object_name = 'patient'


class PatientCreateView(LoginRequiredMixin, CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'acs_hms_base/patient_form.html'
    success_url = reverse_lazy('acs_hms_base:patient_list')


class PatientUpdateView(LoginRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'acs_hms_base/patient_form.html'
    success_url = reverse_lazy('acs_hms_base:patient_list')


class PatientDeleteView(LoginRequiredMixin, DeleteView):
    model = Patient
    template_name = 'acs_hms_base/patient_confirm_delete.html'
    success_url = reverse_lazy('acs_hms_base:patient_list')


# Appointment Views
class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'acs_hms_base/appointment_list.html'
    context_object_name = 'appointments'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Appointment.objects.select_related('patient', 'doctor', 'department')
        date_filter = self.request.GET.get('date')
        if date_filter:
            queryset = queryset.filter(appointment_date=date_filter)
        return queryset.order_by('-appointment_date', '-appointment_time')


class AppointmentDetailView(LoginRequiredMixin, DetailView):
    model = Appointment
    template_name = 'acs_hms_base/appointment_detail.html'
    context_object_name = 'appointment'


class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'acs_hms_base/appointment_form.html'
    success_url = reverse_lazy('acs_hms_base:appointment_list')


class AppointmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'acs_hms_base/appointment_form.html'
    success_url = reverse_lazy('acs_hms_base:appointment_list')


class AppointmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Appointment
    template_name = 'acs_hms_base/appointment_confirm_delete.html'
    success_url = reverse_lazy('acs_hms_base:appointment_list')


# Medical Record Views
class MedicalRecordListView(LoginRequiredMixin, ListView):
    model = MedicalRecord
    template_name = 'acs_hms_base/medical_record_list.html'
    context_object_name = 'medical_records'
    paginate_by = 10


class MedicalRecordDetailView(LoginRequiredMixin, DetailView):
    model = MedicalRecord
    template_name = 'acs_hms_base/medical_record_detail.html'
    context_object_name = 'medical_record'


class MedicalRecordCreateView(LoginRequiredMixin, CreateView):
    model = MedicalRecord
    form_class = MedicalRecordForm
    template_name = 'acs_hms_base/medical_record_form.html'
    success_url = reverse_lazy('acs_hms_base:medical_record_list')


class MedicalRecordUpdateView(LoginRequiredMixin, UpdateView):
    model = MedicalRecord
    form_class = MedicalRecordForm
    template_name = 'acs_hms_base/medical_record_form.html'
    success_url = reverse_lazy('acs_hms_base:medical_record_list')


class MedicalRecordDeleteView(LoginRequiredMixin, DeleteView):
    model = MedicalRecord
    template_name = 'acs_hms_base/medical_record_confirm_delete.html'
    success_url = reverse_lazy('acs_hms_base:medical_record_list')


# Configuration View
class HospitalConfigurationView(LoginRequiredMixin, UpdateView):
    model = HospitalConfiguration
    form_class = HospitalConfigurationForm
    template_name = 'acs_hms_base/configuration.html'
    success_url = reverse_lazy('acs_hms_base:configuration')
    
    def get_object(self):
        # Get or create configuration for the first hospital
        hospital = Hospital.objects.first()
        if hospital:
            config, created = HospitalConfiguration.objects.get_or_create(hospital=hospital)
            return config
        return None


# API Views
class PatientSearchAPIView(LoginRequiredMixin, View):
    def get(self, request):
        query = request.GET.get('q', '')
        patients = Patient.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(patient_id__icontains=query),
            active=True
        )[:10]
        
        data = [{
            'id': patient.id,
            'text': f"{patient.full_name} ({patient.patient_id})"
        } for patient in patients]
        
        return JsonResponse({'results': data})


class DoctorSearchAPIView(LoginRequiredMixin, View):
    def get(self, request):
        query = request.GET.get('q', '')
        doctors = HMSUser.objects.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(employee_id__icontains=query),
            user_type='DOCTOR',
            active=True
        )[:10]
        
        data = [{
            'id': doctor.id,
            'text': f"{doctor.full_name} ({doctor.employee_id})"
        } for doctor in doctors]
        
        return JsonResponse({'results': data})


class AvailableRoomsAPIView(LoginRequiredMixin, View):
    def get(self, request):
        department_id = request.GET.get('department_id')
        room_type = request.GET.get('room_type')
        
        rooms = Room.objects.filter(status='AVAILABLE', active=True)
        
        if department_id:
            rooms = rooms.filter(department_id=department_id)
        
        if room_type:
            rooms = rooms.filter(room_type=room_type)
        
        data = [{
            'id': room.id,
            'text': f"{room.number} - {room.name} ({room.department.name})"
        } for room in rooms]
        
        return JsonResponse({'results': data}) 