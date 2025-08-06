from django.urls import path
from . import views

app_name = 'commission'

urlpatterns = [
    # Dashboard
    path('', views.CommissionDashboardView.as_view(), name='dashboard'),
    
    # Commission Structures
    path('structures/', views.CommissionStructureListView.as_view(), name='structure_list'),
    path('structures/create/', views.CommissionStructureCreateView.as_view(), name='structure_create'),
    path('structures/<int:pk>/', views.CommissionStructureDetailView.as_view(), name='structure_detail'),
    path('structures/<int:pk>/edit/', views.CommissionStructureUpdateView.as_view(), name='structure_update'),
    path('structures/<int:pk>/delete/', views.CommissionStructureDeleteView.as_view(), name='structure_delete'),
    
    # Commission Agents
    path('agents/', views.CommissionAgentListView.as_view(), name='agent_list'),
    path('agents/create/', views.CommissionAgentCreateView.as_view(), name='agent_create'),
    path('agents/<int:pk>/', views.CommissionAgentDetailView.as_view(), name='agent_detail'),
    path('agents/<int:pk>/edit/', views.CommissionAgentUpdateView.as_view(), name='agent_update'),
    
    # Commission Records
    path('records/', views.CommissionRecordListView.as_view(), name='record_list'),
    path('records/create/', views.CommissionRecordCreateView.as_view(), name='record_create'),
    path('records/<int:pk>/', views.CommissionRecordDetailView.as_view(), name='record_detail'),
    path('records/<int:pk>/edit/', views.CommissionRecordUpdateView.as_view(), name='record_update'),
    
    # Commission Payments
    path('payments/', views.CommissionPaymentListView.as_view(), name='payment_list'),
    path('payments/create/', views.CommissionPaymentCreateView.as_view(), name='payment_create'),
    path('payments/<int:pk>/', views.CommissionPaymentDetailView.as_view(), name='payment_detail'),
    
    # Commission Reports
    path('reports/', views.CommissionReportListView.as_view(), name='report_list'),
    path('reports/create/', views.CommissionReportCreateView.as_view(), name='report_create'),
    
    # Configuration
    path('configuration/', views.CommissionConfigurationView.as_view(), name='configuration'),
    
    # API Endpoints
    path('api/data/', views.CommissionAPIView.as_view(), name='api_data'),
    path('api/calculate/', views.calculate_commission, name='api_calculate'),
    
    # Export
    path('export/', views.export_commission_data, name='export_data'),
] 