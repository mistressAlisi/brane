from django.conf import settings
from podman import PodmanClient
from podman.errors import APIError

from brane.toolkit.validators.network import extract_ips


def create(name,**kwargs):
    with PodmanClient(base_url=settings.PODMAN_API_URL) as client:
        try:

            if "cidr" in kwargs:
                gateway,start,end = extract_ips(kwargs["cidr"])
                kwargs["subnets"]=[{
                    "subnet":kwargs["cidr"],
                    "gateway":gateway,
                    "lease_range":{
                        "start_ip":start,
                        "end_ip":end,
                    }
                    }]
                del kwargs["cidr"]
            print(kwargs)
            network = client.networks.create(name,**kwargs)
            return network
        except APIError as e:
            raise e

def destroy(name):
    with PodmanClient(base_url=settings.PODMAN_API_URL) as client:
        try:
            network = client.networks.get(name)
            network.remove()
        except APIError as e:
            raise e
        raise True


def get(name):
    with PodmanClient(base_url=settings.PODMAN_API_URL) as client:
        try:
            network = client.networks.get(name)
            return network
        except APIError as e:
            raise e