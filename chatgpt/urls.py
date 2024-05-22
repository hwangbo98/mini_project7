# blog/urls.py
from django.urls import path
from . import views

app_name = 'chatgpt'
urlpatterns = [
    path('', views.index, name='index'),
    path('chat', views.chat, name='chat'),
    path('chatbot', views.chatbot, name='chatbot'),
    path('chatbot_chat', views.chatbot_chat, name='chatbot_chat'),
]
