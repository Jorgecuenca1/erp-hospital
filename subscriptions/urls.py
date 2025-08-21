from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    # Dashboard principal
    path('', views.SubscriptionsDashboardView.as_view(), name='dashboard'),
    # Suscripciones
    path('planes/', views.PlanSuscripcionListView.as_view(), name='plan_list'),
    path('planes/crear/', views.PlanSuscripcionCreateView.as_view(), name='plan_create'),
    path('suscripciones/', views.SuscripcionListView.as_view(), name='suscripcion_list'),
    path('suscripciones/crear/', views.SuscripcionCreateView.as_view(), name='suscripcion_create'),
]