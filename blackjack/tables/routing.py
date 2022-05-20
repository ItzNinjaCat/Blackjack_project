from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path('ws/tables/medium/', consumers.ChatConsumer.as_asgi()),
]