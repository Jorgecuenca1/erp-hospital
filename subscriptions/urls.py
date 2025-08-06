from django.urls import path
from .views import (
    PlanSuscripcionListView, PlanSuscripcionDetailView, PlanSuscripcionCreateView, PlanSuscripcionUpdateView, PlanSuscripcionDeleteView,
    SuscripcionListView, SuscripcionDetailView, SuscripcionCreateView, SuscripcionUpdateView, SuscripcionDeleteView,
    PagoSuscripcionListView, PagoSuscripcionDetailView, PagoSuscripcionCreateView, PagoSuscripcionUpdateView, PagoSuscripcionDeleteView,
)

urlpatterns = [
    # URLs para PlanSuscripcion
    path('planes/', PlanSuscripcionListView.as_view(), name='plansuscripcion_list'),
    path('planes/<int:pk>/', PlanSuscripcionDetailView.as_view(), name='plansuscripcion_detail'),
    path('planes/nuevo/', PlanSuscripcionCreateView.as_view(), name='plansuscripcion_create'),
    path('planes/<int:pk>/editar/', PlanSuscripcionUpdateView.as_view(), name='plansuscripcion_update'),
    path('planes/<int:pk>/eliminar/', PlanSuscripcionDeleteView.as_view(), name='plansuscripcion_delete'),

    # URLs para Suscripcion
    path('suscripciones/', SuscripcionListView.as_view(), name='suscripcion_list'),
    path('suscripciones/<int:pk>/', SuscripcionDetailView.as_view(), name='suscripcion_detail'),
    path('suscripciones/nuevo/', SuscripcionCreateView.as_view(), name='suscripcion_create'),
    path('suscripciones/<int:pk>/editar/', SuscripcionUpdateView.as_view(), name='suscripcion_update'),
    path('suscripciones/<int:pk>/eliminar/', SuscripcionDeleteView.as_view(), name='suscripcion_delete'),

    # URLs para PagoSuscripcion
    path('pagos/', PagoSuscripcionListView.as_view(), name='pagosuscripcion_list'),
    path('pagos/<int:pk>/', PagoSuscripcionDetailView.as_view(), name='pagosuscripcion_detail'),
    path('pagos/nuevo/', PagoSuscripcionCreateView.as_view(), name='pagosuscripcion_create'),
    path('pagos/<int:pk>/editar/', PagoSuscripcionUpdateView.as_view(), name='pagosuscripcion_update'),
    path('pagos/<int:pk>/eliminar/', PagoSuscripcionDeleteView.as_view(), name='pagosuscripcion_delete'),
] 