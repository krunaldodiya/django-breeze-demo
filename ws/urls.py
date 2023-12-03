from django.urls import path, re_path

from ws import views

from ws.consumers import WebsocketConsumer

urlpatterns = [
    path("", views.ws, name="ws"),
]

websocket_urlpatterns = [
    re_path(r"ticker", WebsocketConsumer.as_asgi()),
]
