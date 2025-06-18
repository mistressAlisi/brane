from django.conf import settings
SETUP_PAYLOAD_STEPS = [
    # {
    #     "name":"pull_image_postgres",
    #     "action_group":"podman",
    #     "action_type":"pull_image",
    #     "params":{
    #         "name":"docker.io/library/postgres",
    #         "tag":"17.5-bookworm",
    #     }
    # },
    # {
    #     "name": "pull_image_traefik",
    #     "action_group": "podman",
    #     "action_type": "pull_image",
    #     "params": {
    #         "name": "docker.io/library/traefik",
    #         "tag": "latest",
    #     }
    # },
    # {
    #     "name": "build_brane_db_image",
    #     "action_group": "podman",
    #     "action_type": "build_image",
    #     "args": {
    #         "tag": "postgres-17.5-bookworm-brane",
    #         "path": "${PAYLOAD_DIR}",
    #         "quiet":False,
    #         "dockerfile":'Dockerfile',
    #
    #     },
    #     "buildargs":{
    #         "PGUSER":"${PGUSER}",
    #         "PGUSER_PASSWD":"${PGUSER_PASSWD}",
    #     }
    # },
    # {
    #     "name": "build_brane_image",
    #     "action_group": "podman",
    #     "action_type": "build_image",
    #     "args": {
    #         "tag": "brane",
    #         "path": "${BRANE_PAYLOAD_DIR}",
    #         "quiet": False,
    #         "dockerfile": '${BRANE_DOCKERFILE}',
    #
    #     },
    #     "buildargs": {
    #         "PGUSER": "${PGUSER}",
    #         "PGUSER_PASSWD": "${PGUSER_PASSWD}",
    #     }
    # },
     {
        "name":"create_cluster_network",
        "action_group":"podman",
        "action_type":"create_network",
        "params":{
            "name":"BRANE_NETWORK",
            "cidr":"${net_cidr}",
            # "network_interface":"enp7s0f1np1",
            # "driver":"slirp4netns"
        }
    },
    # {
    #     "name": "create_cluster_pod",
    #     "action_group": "podman",
    #     "action_type": "create_pod",
    #     "pod_name":"BRANE_MULTIVERSE",
    #     "params": {
    #         "portmappings":[
    #             {"container_port":8080,"host_port":8080},
    #             {"container_port":80,"host_port":80},
    #             {"container_port":443,"host_port":443},
    #         ]
    #     }
    # },
    {
        "name": "create_traefik_proxy",
        "action_group": "podman",
        "action_type": "create_container",
        # "env": {
        #
        # },
        "mounts": {
            settings.PODMAN_DOCKER_SOCKET_FILE: "/var/run/docker.sock",
            settings.PODMAN_TRAEFIK_ACME_FILE: "/acme.json",
        },
        "params": {
            "name": "traefik",
            "image": "docker.io/library/traefik:latest",
            # "pod": "BRANE_MULTIVERSE",
            "network": "BRANE_NETWORK",
            "command":"traefik --api.insecure=true --providers.docker",
            "ports":{
                "8080":8080,
                "80":80,
                "443":443
            }
        }
    },
    {
        "name":"create_cluster_database",
        "action_group":"podman",
        "action_type":"create_container",
        "env":{
            "PGDATA":"/var/lib/postgresql/data/pgdata",
            "POSTGRES_PASSWORD":"${PGADMIN_PASSWD}",
        },
        "mounts":{
          "${pgdata}":"/var/lib/postgresql/data",
        },
        "params":{
            "name":"BRANE_DATABASE",
            "image":"localhost/postgres-17.5-bookworm-brane:latest",
            # "pod":"BRANE_MULTIVERSE",
            "network": "BRANE_NETWORK"
        }
    },
    {
        "name": "create_cluster_controller",
        "action_group": "podman",
        "action_type": "create_container",
        "env": {
            "DB_NAME": "brane_main",
            "DB_USER": "brane",
            "DB_PASSWORD": "${PGUSER_PASSWD}",
            "DB_HOST":"localhost",
            "BRANE_SETUP":"true",
            "BRANE_DB":"migrate",
            "BRANE_APP_MODE":"web_devel",
            "DEBUG":"true"
        },
        "params": {
            # "pod":"BRANE_MULTIVERSE",
            "name": "BRANE_CONTROLLER",
            "image": "localhost/brane:latest",
            "network": "BRANE_NETWORK"

        }
    },

]