from django.urls import path

from ws.consumers import WebsocketConsumer

websocket_urlpatterns = [
    path("ws/ticker/<str:room_name>", WebsocketConsumer.as_asgi()),
]
