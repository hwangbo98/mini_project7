# blog/urls.py
from django.urls import path
from django.contrib import admin
from . import views

app_name = 'selfchatgpt'
urlpatterns = [

    path('', views.index, name='index'),
    path('chat', views.chat, name='chat'),
    # path('upload_csv', views.upload_csv, name='upload_csv'),
    path('admin/', admin.site.urls),



    
]
