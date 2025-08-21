from django.urls import path
from . import views

app_name = 'livechat'

urlpatterns = [
    # Dashboard principal
    path('', views.LiveChatDashboardView.as_view(), name='dashboard'),
    # Conversaciones
    path('conversaciones/', views.ConversacionListView.as_view(), name='conversacion_list'),
    path('conversaciones/<int:pk>/', views.ConversacionDetailView.as_view(), name='conversacion_detail'),
    # API endpoints
    path('api/messages/', views.MessageAPIView.as_view(), name='api_messages'),
]