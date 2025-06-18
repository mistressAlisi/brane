"""
URL configuration for brane project.

The 'websocket_urlpatterns' routing is used for Websockets at /ws/api/v1/*
"""
from django.contrib import admin
from django.urls import path, include
from channels.routing import URLRouter

# No Actual Application load - just load the Brane setup App paths here:
from setup.routing import url_routes
_websocket_urlpatterns = url_routes