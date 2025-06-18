from django.conf import settings
from podman import PodmanClient
from podman.errors import APIError


def pull_image(name, tag):
    try:
        with PodmanClient(base_url=settings.PODMAN_API_URL) as client:
            client.images.pull(repository=name, tag=tag)
            return True
    except APIError as e:
        raise e

def build_image(**kwargs):
    """
    Just like:
    https://podman-py.readthedocs.io/en/latest/podman.domain.images_manager.html#podman.domain.images_manager.ImagesManager.build
    :param kwargs: Named Keyword args, same as above.
    :return: Tuple[Image, Iterator[bytes]]
    """
    try:
        with PodmanClient(base_url=settings.PODMAN_API_URL) as client:
            return client.images.build(**kwargs)
    except Exception as e:
        raise e