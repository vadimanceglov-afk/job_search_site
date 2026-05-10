from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.models import User
import json

# Імпортуємо твої моделі
from .models import Chat, ChatMessage
from project.models import Application
from auth_system.models import EmployerProfile, UserProfile

@login_required
def chatroom(request, application_id):
    # Отримуємо заявку по ID
    application = get_object_or_404(Application, id=application_id)
    
    # Отримуємо або створюємо чат для цієї заявки
    chat, created = Chat.objects.get_or_create(application=application)

    # ПЕРЕВІРКА ПРАВ ДОСТУПУ:
    # 1. Чи це кандидат (автор заявки)?
    is_candidate = (request.user == application.author)
    # 2. Чи це роботодавець (власник компанії, яка розмістила вакансію)?
    is_employer = (request.user == application.vacancy.company.user)

    if not (is_candidate or is_employer):
        # Якщо лівий юзер намагається зайти — викидаємо його
        return redirect('homepage') 

    # Отримуємо повідомлення
    messages_history = chat.messages.all()
    
    # Позначаємо повідомлення від іншої сторони як прочитані
    messages_history.filter(is_read=False).exclude(sender=request.user).update(is_read=True)

    context = {
        "chat": chat,
        "application": application,
        "user_messages": messages_history,
        "application_id": application_id 
    }
    
    return render(request, "chat_vac/chatroom.html", context)


@login_required
def ajax_load_messages(request, application_id):
    # Шукаємо чат
    chat = get_object_or_404(Chat, application_id=application_id)
    application = chat.application
    
    # ПЕРЕВІРКА ПРАВ (використовуємо твої реальні поля: author та vacancy.company.user)
    is_candidate = (request.user == application.author)
    is_employer = (request.user == application.vacancy.company.user)

    if not (is_candidate or is_employer):
        return JsonResponse({'error': 'Forbidden'}, status=403)

    # Список для нових повідомлень
    message_list = []

    # 1. Обробка відправки (POST)
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get('message')
            
            if user_message:
                m = ChatMessage.objects.create(
                    chat=chat, 
                    sender=request.user, 
                    content=user_message
                )
                message_list.append({
                    "sender": request.user.username,
                    "content": m.content,
                    "sent": True,
                    "date_created": naturaltime(m.created_at),
                })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    # 2. Отримуємо нові повідомлення від співрозмовника (GET)
    # Тільки якщо це не ми щойно відправили (exclude sender)
    new_messages = chat.messages.filter(is_read=False).exclude(sender=request.user)
    
    for m in new_messages:
        message_list.append({
            "sender": m.sender.username,
            "content": m.content,
            "sent": False,
            "date_created": naturaltime(m.created_at),
        })
    
    # Позначаємо як прочитані
    new_messages.update(is_read=True)

    return JsonResponse(message_list, safe=False)