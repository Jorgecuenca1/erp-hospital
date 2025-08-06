from django.urls import path
from .views import (
    LeadListView, LeadDetailView, LeadCreateView, LeadUpdateView, LeadDeleteView,
    CustomerListView, CustomerDetailView, CustomerCreateView, CustomerUpdateView, CustomerDeleteView,
    ContactListView, ContactDetailView, ContactCreateView, ContactUpdateView, ContactDeleteView,
    InteractionListView, InteractionDetailView, InteractionCreateView, InteractionUpdateView, InteractionDeleteView,
)

app_name = 'crm'

urlpatterns = [
    path('leads/', LeadListView.as_view(), name='lead_list'),
    path('leads/<int:pk>/', LeadDetailView.as_view(), name='lead_detail'),
    path('leads/new/', LeadCreateView.as_view(), name='lead_create'),
    path('leads/<int:pk>/edit/', LeadUpdateView.as_view(), name='lead_update'),
    path('leads/<int:pk>/delete/', LeadDeleteView.as_view(), name='lead_delete'),

    path('customers/', CustomerListView.as_view(), name='customer_list'),
    path('customers/<int:pk>/', CustomerDetailView.as_view(), name='customer_detail'),
    path('customers/new/', CustomerCreateView.as_view(), name='customer_create'),
    path('customers/<int:pk>/edit/', CustomerUpdateView.as_view(), name='customer_update'),
    path('customers/<int:pk>/delete/', CustomerDeleteView.as_view(), name='customer_delete'),

    path('contacts/', ContactListView.as_view(), name='contact_list'),
    path('contacts/<int:pk>/', ContactDetailView.as_view(), name='contact_detail'),
    path('contacts/new/', ContactCreateView.as_view(), name='contact_create'),
    path('contacts/<int:pk>/edit/', ContactUpdateView.as_view(), name='contact_update'),
    path('contacts/<int:pk>/delete/', ContactDeleteView.as_view(), name='contact_delete'),

    path('interactions/', InteractionListView.as_view(), name='interaction_list'),
    path('interactions/<int:pk>/', InteractionDetailView.as_view(), name='interaction_detail'),
    path('interactions/new/', InteractionCreateView.as_view(), name='interaction_create'),
    path('interactions/<int:pk>/edit/', InteractionUpdateView.as_view(), name='interaction_update'),
    path('interactions/<int:pk>/delete/', InteractionDeleteView.as_view(), name='interaction_delete'),
] 