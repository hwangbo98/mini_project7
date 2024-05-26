# blog/urls.py
from django.urls import path
from . import views

app_name = 'chatgpt'
urlpatterns = [
    path('', views.index, name='index'),
    path('chat', views.chat, name='chat'),

    path('simple_chatbot', views.simple_chatbot, name='simple_chatbot'),

    # path('chatbot_memory', views.chatbot_memory_form, name='chatbot_memory'),
    # path('chatbot_memory_chat', views.chatbot_memory_chat, name='chatbot_memory_chat'),

    path('memory_chatbot', views.memory_chatbot, name='memory_chatbot'),


    
]
