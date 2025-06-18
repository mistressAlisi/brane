from django.conf import settings
from podman import PodmanClient
from podman.errors import APIError


def create_new_pod(name,**kwargs):
    with PodmanClient(base_url=settings.PODMAN_API_URL) as client:
        try:
            print(kwargs)
            return client.pods.create(name, **kwargs)
        except APIError as e:
            raise e

