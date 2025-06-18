import importlib
import logging
import re
from copy import deepcopy

from brane.toolkit.podman.lifecycle.containers import create_new_container
from brane.toolkit.podman.lifecycle.images import pull_image, build_image
from brane.toolkit.podman.lifecycle.networks import create as network_create, destroy as network_destroy
from brane.toolkit.podman.lifecycle.pods import create_new_pod
from setup.payloads.create_cluster import env

log = logging.getLogger(__name__)
class PayloadInstaller(object):
    info = {}
    steps = []
    total_steps = 0
    current_step = 0
    env = {}
    param_envname_pattern = r'^\$\{([A-Za-z_][A-Za-z0-9_]*)\}$'

    def _copy_and_set_vars(self,copy_src,vars_src,match_value=True):
        dst = deepcopy(copy_src)
        for k,v in copy_src.items():
            if type(v) == str:
                if match_value:
                    match = re.match(self.param_envname_pattern,v)
                else:
                    match = re.match(self.param_envname_pattern, k)
                if match:
                    vk = match.group(1)
                    # print(vk,v,vars_src[vk])
                    if match_value:
                        dst[k] = vars_src[vk]
                    else:
                        del(dst[k])
                        dst[vars_src[vk]] = v
        return dst

    def __init__(self, payload_module_name,env_vars=dict):
        self.logger = logging.getLogger(f"PayloadInstaller/{payload_module_name}")
        self.logger.info("Loading Payload Module..")
        info = importlib.import_module(f"{payload_module_name}.info")
        payload = importlib.import_module(f"{payload_module_name}.payload")
        env = importlib.import_module(f"{payload_module_name}.env")
        self.info = info.SETUP_PAYLOAD_INFO
        self.steps = payload.SETUP_PAYLOAD_STEPS
        self.total_steps = len(payload.SETUP_PAYLOAD_STEPS)
        # print(env_vars)
        self.env = self._copy_and_set_vars(env.SETUP_PAYLOAD_ENV,env_vars)
        self.logger.info(f"PayloadInstaller Ready: {self.total_steps} steps.")

    def _podman_action(self,step,**kwargs):
        if step["action_type"] == "create_network":
            isolate = False
            params = self._copy_and_set_vars(step["params"],self.env)
            self.logger.info(f"Creating Network with params: Name: {params["name"]}, CIDR: {params["cidr"]}, {kwargs}")
            # print(f"Creating Network with params: Name: {name}, CIDR: {cidr}, Isolated: {isolate}...")
            # print(params)
            return network_create(**params)
        elif step["action_type"] == "destroy_network":
            if "name" in step["params"]:
                name = step["params"]["name"]
                return network_destroy(name)
            else:
                # print("No network name specified")
                raise Exception("No network name specified")
        elif step["action_type"] == "pull_image":
            self.logger.info(f"Pulling Image: {step['params']['name']}: {step['params']['tag']}")
            name = step["params"]["name"]
            tag = step["params"]["tag"]
            return pull_image(name,tag)
        elif step["action_type"] == "build_image":
            self.logger.info(f"Building Image: {step['name']} from {self.env['PAYLOAD_DIR']}")
            # Setup the Global Function Arguments:
            # print(step["args"])
            args = self._copy_and_set_vars(step["args"],self.env)
            # And the BUILD arguments if specified:
            if "buildargs" in step:
                buildargs = self._copy_and_set_vars(step["buildargs"],self.env)
                args["buildargs"] = buildargs
            # And execute the build:
            print(args)
            self.logger.info("Build Image:",args)
            image,log =  build_image(**args)
            return image,log
        elif step["action_type"] == "create_container":
            self.logger.info(f"Creating Container: {step['name']}")
            # print(self.env)
            if "env" in step:
                env = self._copy_and_set_vars(step["env"],self.env)
                # print(env)
                params = {
                    "environment": env,
                }
            else:
                params = {}
            if "params" in step:
                # print("P")
                step_params = self._copy_and_set_vars(step["params"],self.env)
                params.update(step_params)
            if "mounts" in step:
                # print("M")
                params["mounts"] = self._copy_and_set_vars(step["mounts"], self.env, False)
            # print(mounts)


            #print(step["params"]["image"],step["params"]["name"],params)
            return create_new_container(**params)
        elif step["action_type"] == "create_pod":
            self.logger.info(f"Creating Pod: {step['name']}: {step['pod_name']}")
            params = self._copy_and_set_vars(step["params"],self.env)
            return create_new_pod(step["pod_name"],**params)

        else:
            # print((f"Unknown action type {step['action_type']}"))
            raise Exception(f"Unknown action type {step['action_type']}")


    def get_curr_step(self):
        if self.current_step <= self.total_steps:
            return self.current_step,self.total_steps,self.steps[self.current_step]
        else:
            print("Too many!")
            return False,False,False

    def step_in(self,**kwargs):
        if self.current_step >= self.total_steps:
            # print(f"Can't step forward more than total steps: {self.current_step}/{self.total_steps}")
            self.logger.error("Can't step forward more than total steps.")
            return False
        self.current_step += 1
        return True

    def exec_curr_step(self,**kwargs):
        cstep = self.steps[self.current_step]
        # Switch step depending on action group:
        if cstep["action_group"] == "podman":
            try:
                val = self._podman_action(cstep, **kwargs)
                return val
            except Exception as e:
                raise e