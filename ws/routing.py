from django.urls import path

from ws.consumers import WebsocketConsumer

websocket_urlpatterns = [
    path("ws/<str:room_name>", WebsocketConsumer.as_asgi()),
]
