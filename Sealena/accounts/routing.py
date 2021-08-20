"""
    This routing.py file contains all the url paths used by the WebSocket protocol connections to identify proper consumers.
"""

from django.urls import path
from .consumers import WSNotifications, ChatWS

ws_urlpatterns = [
    path('', WSNotifications.as_asgi()),
    path('chat', ChatWS.as_asgi()),
]
