from django.urls import path
from . import views


urlpatterns = [
    path('chat-room/<int:user_id>/', views.chat_room, name='chat_room'),
    path('ajax/<int:user_id>/', views.ajax_load_messages, name='chatroom-ajax')
]