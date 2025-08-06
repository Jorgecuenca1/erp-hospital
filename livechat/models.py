from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ChatSession(models.Model):
    uuid = models.CharField(max_length=100, unique=True, db_index=True) # Public ID for external access
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='chat_sessions_user') # Customer if logged in
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='chat_sessions_agent') # Agent handling the chat
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)
    topic = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Sesiones de Chat"

    def __str__(self):
        return f'Chat {self.uuid} - {"Activo" if self.active else "Cerrado"}'

class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) # User or Agent who sent the message
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']
        verbose_name_plural = "Mensajes de Chat"

    def __str__(self):
        return f'Mensaje en {self.session.uuid} por {self.sender.username if self.sender else "Anonimo"}'
