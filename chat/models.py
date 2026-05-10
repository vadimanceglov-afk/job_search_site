from django.db import models
from django.contrib.auth.models import User
from auth_system.models import EmployerProfile, UserProfile
from project.models import Application

class Chat(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='chat')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Чат по заявці №{self.application.id}"
    
# Create your models here.
class ChatMessage(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    is_read = models.BooleanField(default=False) # Щоб бачити нові повідомлення
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at'] # Щоб повідомлення йшли по порядку