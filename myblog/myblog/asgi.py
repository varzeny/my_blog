"""
ASGI config for myblog project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# channels 관련
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myblog.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # WebSocket, 기타 프로토콜 추가 가능
})
