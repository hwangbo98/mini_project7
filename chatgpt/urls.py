# blog/urls.py
from django.urls import path
from django.contrib import admin
from . import views

app_name = 'chatgpt'
urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.index, name='index'),
    path('chat', views.chat, name='chat'),

    path('simple_chatbot', views.simple_chatbot, name='simple_chatbot'),

    path('simple_chatbot_with_history', views.simple_chatbot_with_history, name='simple_chatbot_with_history'),
   
    path('memory_chatbot', views.memory_chatbot, name='memory_chatbot'),


    
]
