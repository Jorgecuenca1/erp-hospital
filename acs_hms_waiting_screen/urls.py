from django.urls import path
from . import views

app_name = 'waiting_screen'

urlpatterns = [
    # Dashboard
    path('', views.WaitingScreenDashboardView.as_view(), name='dashboard'),
    
    # Waiting Screens
    path('screens/', views.WaitingScreenListView.as_view(), name='screen_list'),
    path('screens/create/', views.WaitingScreenCreateView.as_view(), name='screen_create'),
    path('screens/<int:pk>/', views.WaitingScreenDetailView.as_view(), name='screen_detail'),
    path('screens/<int:pk>/edit/', views.WaitingScreenUpdateView.as_view(), name='screen_update'),
    path('screens/<int:pk>/delete/', views.WaitingScreenDeleteView.as_view(), name='screen_delete'),
    
    # Waiting Queue
    path('queues/', views.WaitingQueueListView.as_view(), name='queue_list'),
    path('queues/create/', views.WaitingQueueCreateView.as_view(), name='queue_create'),
    path('queues/<int:pk>/', views.WaitingQueueDetailView.as_view(), name='queue_detail'),
    path('queues/<int:pk>/edit/', views.WaitingQueueUpdateView.as_view(), name='queue_update'),
    
    # Announcements
    path('announcements/', views.ScreenAnnouncementListView.as_view(), name='announcement_list'),
    path('announcements/create/', views.ScreenAnnouncementCreateView.as_view(), name='announcement_create'),
    path('announcements/<int:pk>/', views.ScreenAnnouncementDetailView.as_view(), name='announcement_detail'),
    path('announcements/<int:pk>/edit/', views.ScreenAnnouncementUpdateView.as_view(), name='announcement_update'),
    
    # Health Tips
    path('health-tips/', views.HealthTipListView.as_view(), name='health_tip_list'),
    path('health-tips/create/', views.HealthTipCreateView.as_view(), name='health_tip_create'),
    path('health-tips/<int:pk>/', views.HealthTipDetailView.as_view(), name='health_tip_detail'),
    path('health-tips/<int:pk>/edit/', views.HealthTipUpdateView.as_view(), name='health_tip_update'),
    
    # Configuration
    path('configuration/', views.ScreenConfigurationView.as_view(), name='configuration'),
    
    # AJAX Endpoints
    path('api/queue-status/', views.get_queue_status, name='api_queue_status'),
    path('api/update-queue/', views.update_queue_status, name='api_update_queue'),
    path('api/announcements/', views.get_announcements, name='api_announcements'),
    path('api/health-tips/', views.get_health_tips, name='api_health_tips'),
    
    # Export
    path('export/queue-data/', views.export_queue_data, name='export_queue_data'),
] 