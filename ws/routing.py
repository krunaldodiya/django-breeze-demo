from django.urls import re_path

from ws.consumers import WebsocketConsumer

websocket_urlpatterns = [
    re_path(r"ws/ticker", WebsocketConsumer.as_asgi()),
]
