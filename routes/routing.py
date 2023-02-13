from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from . consumers import *


websocket_urlpatterns = ([
    path('map/', RouteConsumer.as_asgi()),
])
