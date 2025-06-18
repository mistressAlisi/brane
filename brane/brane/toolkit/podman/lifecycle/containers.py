from django.conf import settings
from podman import PodmanClient
from podman.errors import APIError


def create_new_container(**kwargs):
    with PodmanClient(base_url=settings.PODMAN_API_URL) as client:
        try:
            args = {}
            # if "networks" in kwargs:
            #     net_data = {}
            #     for net_name in kwargs["networks"]:
            #         net_data[net_name] = {}
            #     kwargs["networks"] = net_data

            if "mounts" in kwargs:
                mounts_data = []
                for src,dst in kwargs["mounts"].items():
                    mounts_data.append({"source":src, "target":dst,"type":"bind"})

                kwargs["mounts"] = mounts_data
            print(kwargs)
            # print("O")
            container = client.containers.create(**kwargs)
            if 'noautostart' not in kwargs:
                container.start()
            return container
        except APIError as e:
            raise e


def destroy_container(name):
    with PodmanClient(base_url=settings.PODMAN_API_URL) as client:
        try:
            container = client.containers.get(name)
            container.stop()
            container.remove()
            return True
        except APIError as e:
            raise e