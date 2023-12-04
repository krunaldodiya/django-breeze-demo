import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

from django.core.asgi import get_asgi_application

asgi_application = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter

from django_channels_jwt_auth_middleware.auth import JWTAuthMiddlewareStack

from ws.routing import websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        "http": asgi_application,
        "websocket": JWTAuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns,
            )
        ),
    }
)
