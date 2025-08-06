from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView
from .models import HospitalProfile
from .forms import HospitalProfileForm

# Create your views here.

class HospitalProfileDetailView(DetailView):
    model = HospitalProfile
    template_name = 'hospital_profile/hospital_profile_detail.html'
    context_object_name = 'hospital_profile'

    def get_object(self, queryset=None):
        # Asumimos que solo habrá un perfil de hospital, con PK=1
        return get_object_or_404(HospitalProfile, pk=1)

class HospitalProfileUpdateView(UpdateView):
    model = HospitalProfile
    form_class = HospitalProfileForm
    template_name = 'hospital_profile/hospital_profile_form.html'
    context_object_name = 'hospital_profile'

    def get_object(self, queryset=None):
        # Asumimos que solo habrá un perfil de hospital, con PK=1
        return get_object_or_404(HospitalProfile, pk=1)

    def get_success_url(self):
        return reverse_lazy('hospital_profile:detail')
