"""
ASGI config for cards project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# Set the Django settings module first
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cards.settings')

# Get the ASGI application first
django_asgi_app = get_asgi_application()

# Then import the channel components after the Django app is loaded
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import cardgame.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            cardgame.routing.websocket_urlpatterns
        )
    ),
})