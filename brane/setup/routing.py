from channels.routing import URLRouter
from django.urls import include, path

from setup.consumers import SetupExecConsumer
url_root = "ws/api/v1/setup/"
url_routes = [
    path(f"{url_root}create/start",SetupExecConsumer.as_asgi() ),
]
