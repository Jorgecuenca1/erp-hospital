from django.urls import path
from .views import ChatSessionListView, ChatSessionDetailView

urlpatterns = [
    path('chat/', ChatSessionListView.as_view(), name='chatsession_list'),
    path('chat/<int:pk>/', ChatSessionDetailView.as_view(), name='chatsession_detail'),
]