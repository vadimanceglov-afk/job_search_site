from django.urls import path
from . import views

urlpatterns = [
    # Буде доступно як /chat/37/
    path("<int:application_id>/", views.chatroom, name="chat_room"),
    
    # Буде доступно як /chat/api/37/
    path("api/<int:application_id>/", views.ajax_load_messages, name="chatroom_ajax"),
]