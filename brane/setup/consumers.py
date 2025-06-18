import json
import time

from channels.generic.websocket import WebsocketConsumer


from brane.toolkit.setup.payloads.installer import PayloadInstaller


class SetupExecConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def create_new_cluster(self,cidr,pgpasswd,pgdata,ctrlport):
        installer = PayloadInstaller("setup.payloads.create_cluster",{"net_cidr":cidr,"pgpasswd":pgpasswd,"pgdata":pgdata,"ctrlport":ctrlport,"net_isolate":True})
        # print(installer.current_step,installer.total_steps)
        while installer.current_step < installer.total_steps:
            curr, total, data = installer.get_curr_step()
            self.send(json.dumps({"type": "progress", "step": curr, "total": total, "msg": data["name"],
                                  "prog": round((curr / total) * 100, 2)}))
            try:
                installer.exec_curr_step()
            except Exception as e:
                print(e)
                self.send(json.dumps({"step":data["name"],"type": "error", "msg": str(e)}))
                self.disconnect(500)
                return
            installer.step_in()
        self.send(json.dumps({"msg":"Setup Complete!","type":"success"}))


    def receive(self, text_data):
        command_data = json.loads(text_data)
        if "cmd" in command_data:
            if command_data["cmd"] == "create_cluster":
                self.create_new_cluster(command_data["data"]["cidr"],command_data["data"]["pgpasswd"],command_data["data"]["pgdata"],command_data["data"]["ctrlport"])
        else:
            self.send(text_data=json.dumps(command_data))