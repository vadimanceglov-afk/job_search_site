from django.db import models
from django.contrib.auth.models import User
from project.models import Vacancy

class Chat(models.Model):
# Роботодавець, який створив чат
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_chats')
    # Кандидат, якому написали
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_chats')
    # Вакансія, з якої все почалося (щоб розуміти контекст)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Унікальність: один роботодавець може створити лише один чат 
        # з одним конкретним кандидатом по одній вакансії.
        unique_together = ('employer', 'candidate', 'vacancy')
    
# Create your models here.
class ChatMessage(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False) # Щоб бачити нові повідомлення