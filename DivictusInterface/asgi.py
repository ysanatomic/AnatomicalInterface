"""
ASGI config for DivictusInterface project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import interface.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DivictusInterface.settings')

#application = get_asgi_application()
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # Just HTTP for now. We will add more later
    "websocket": AuthMiddlewareStack(
        URLRouter(
            interface.routing.websocket_urlpatterns
        )
    ),
})




