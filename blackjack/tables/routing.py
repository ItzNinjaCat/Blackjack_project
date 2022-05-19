from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/chat/medium/', consumers.ChatConsumer.as_asgi()),
]