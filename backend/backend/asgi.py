"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.urls import path
from django.core.asgi import get_asgi_application
from channels.routing import URLRouter, ProtocolTypeRouter
from channels.auth import AuthMiddlewareStack
from data.consumers import NotificationConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

django_app = get_asgi_application()


websocket_routing = URLRouter([
    path("ws/notifications/", NotificationConsumer.as_asgi()),
    # Add more WebSocket paths as needed
])

application = ProtocolTypeRouter({
    "http": django_app,
    "websocket": AuthMiddlewareStack(websocket_routing),
})
