# Пример routing.py для приложения
from django.urls import re_path
from .consumers import MessagesConsumer


ws_urlpatterns = [
   re_path(r'ws/emails/', MessagesConsumer.as_asgi()),
]