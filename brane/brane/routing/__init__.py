from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
"""
URL configuration for brane project.

The 'websocket_urlpatterns' routing is used for Websockets at /ws/api/v1/*
"""
if settings.BRANE_SETUP:
    from .runtime import _websocket_urlpatterns
else:
   from .setup import _websocket_urlpatterns
websocket_urlpatterns = _websocket_urlpatterns