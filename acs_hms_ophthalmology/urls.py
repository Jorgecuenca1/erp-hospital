from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'ophthalmology'

urlpatterns = [
    # Dashboard
    path('', TemplateView.as_view(template_name='ophthalmology/dashboard.html'), name='dashboard'),
    path('dashboard/', views.OphthalmologyDashboardView.as_view(), name='full_dashboard'),
    
    # Eye Examinations
    path('examinations/', views.EyeExaminationListView.as_view(), name='examination_list'),
    path('examinations/create/', views.EyeExaminationCreateView.as_view(), name='examination_create'),
    path('examinations/<int:pk>/', views.EyeExaminationDetailView.as_view(), name='examination_detail'),
    path('examinations/<int:pk>/update/', views.EyeExaminationUpdateView.as_view(), name='examination_update'),
    path('examinations/<int:pk>/delete/', views.EyeExaminationDeleteView.as_view(), name='examination_delete'),
    
    # Procedures
    path('procedures/', views.ProcedureListView.as_view(), name='procedure_list'),
    path('procedures/create/', views.ProcedureCreateView.as_view(), name='procedure_create'),
    path('procedures/<int:pk>/', views.ProcedureDetailView.as_view(), name='procedure_detail'),
    path('procedures/<int:pk>/update/', views.ProcedureUpdateView.as_view(), name='procedure_update'),
    
    # Optical Prescriptions
    path('prescriptions/', views.PrescriptionListView.as_view(), name='prescription_list'),
    path('prescriptions/create/', views.PrescriptionCreateView.as_view(), name='prescription_create'),
    
    # Visual Field Tests
    path('visual-fields/', views.VisualFieldTestListView.as_view(), name='visual_field_list'),
    path('visual-fields/create/', views.VisualFieldTestCreateView.as_view(), name='visual_field_create'),
    
    # Equipment Management
    path('equipment/', views.EquipmentListView.as_view(), name='equipment_list'),
    path('equipment/create/', views.EquipmentCreateView.as_view(), name='equipment_create'),
    
    # API Endpoints
    path('api/stats/', views.OphthalmologyStatsAPIView.as_view(), name='stats_api'),
    
    # Legacy URLs for compatibility
    path('list/', views.OphthalmologyListView.as_view(), name='list'),
    path('create/', views.OphthalmologyCreateView.as_view(), name='create'),
    path('detail/', views.OphthalmologyDetailView.as_view(), name='detail'),
    path('update/', views.OphthalmologyUpdateView.as_view(), name='update'),
] 