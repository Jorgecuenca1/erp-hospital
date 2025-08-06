from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import ChatSession, ChatMessage

# Create your views here.

class ChatSessionListView(ListView):
    model = ChatSession
    template_name = 'livechat/chatsession_list.html'
    context_object_name = 'chatsessions'
    queryset = ChatSession.objects.filter(active=True).order_by('-start_time')

class ChatSessionDetailView(DetailView):
    model = ChatSession
    template_name = 'livechat/chatsession_detail.html'
    context_object_name = 'chatsession'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = self.object.messages.all().order_by('timestamp')
        return context
