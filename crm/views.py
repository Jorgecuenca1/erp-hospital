from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Lead, Customer, Contact, Interaction
from .forms import LeadForm, CustomerForm, ContactForm, InteractionForm

# Lead Views
class LeadListView(ListView):
    model = Lead
    template_name = 'crm/lead_list.html'
    context_object_name = 'leads'

class LeadDetailView(DetailView):
    model = Lead
    template_name = 'crm/lead_detail.html'
    context_object_name = 'lead'

class LeadCreateView(CreateView):
    model = Lead
    form_class = LeadForm
    template_name = 'crm/lead_form.html'
    success_url = reverse_lazy('crm:lead_list')

class LeadUpdateView(UpdateView):
    model = Lead
    form_class = LeadForm
    template_name = 'crm/lead_form.html'
    success_url = reverse_lazy('crm:lead_list')

class LeadDeleteView(DeleteView):
    model = Lead
    template_name = 'crm/lead_confirm_delete.html'
    success_url = reverse_lazy('crm:lead_list')

# Customer Views
class CustomerListView(ListView):
    model = Customer
    template_name = 'crm/customer_list.html'
    context_object_name = 'customers'

class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'crm/customer_detail.html'
    context_object_name = 'customer'

class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'crm/customer_form.html'
    success_url = reverse_lazy('crm:customer_list')

class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'crm/customer_form.html'
    success_url = reverse_lazy('crm:customer_list')

class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = 'crm/customer_confirm_delete.html'
    success_url = reverse_lazy('crm:customer_list')

# Contact Views
class ContactListView(ListView):
    model = Contact
    template_name = 'crm/contact_list.html'
    context_object_name = 'contacts'

class ContactDetailView(DetailView):
    model = Contact
    template_name = 'crm/contact_detail.html'
    context_object_name = 'contact'

class ContactCreateView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'crm/contact_form.html'
    success_url = reverse_lazy('crm:contact_list')

class ContactUpdateView(UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = 'crm/contact_form.html'
    success_url = reverse_lazy('crm:contact_list')

class ContactDeleteView(DeleteView):
    model = Contact
    template_name = 'crm/contact_confirm_delete.html'
    success_url = reverse_lazy('crm:contact_list')

# Interaction Views
class InteractionListView(ListView):
    model = Interaction
    template_name = 'crm/interaction_list.html'
    context_object_name = 'interactions'

class InteractionDetailView(DetailView):
    model = Interaction
    template_name = 'crm/interaction_detail.html'
    context_object_name = 'interaction'

class InteractionCreateView(CreateView):
    model = Interaction
    form_class = InteractionForm
    template_name = 'crm/interaction_form.html'
    success_url = reverse_lazy('crm:interaction_list')

class InteractionUpdateView(UpdateView):
    model = Interaction
    form_class = InteractionForm
    template_name = 'crm/interaction_form.html'
    success_url = reverse_lazy('crm:interaction_list')

class InteractionDeleteView(DeleteView):
    model = Interaction
    template_name = 'crm/interaction_confirm_delete.html'
    success_url = reverse_lazy('crm:interaction_list') 