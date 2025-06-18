import os
import string,random
pth = os.path.dirname(__file__)
bpth = "/".join(pth.split("/")[:-4])
def randomword(length):
   letters = string.ascii_lowercase+string.ascii_uppercase+string.digits
   return ''.join(random.choice(letters) for i in range(length))
SETUP_PAYLOAD_ENV = {
    "PGUSER":"brane",
    "PGUSER_PASSWD":randomword(16),
    "PAYLOAD_DIR": pth,
    "BRANE_PAYLOAD_DIR":bpth,
    "BRANE_DOCKERFILE":bpth+"/Dockerfile",
    "net_cidr":"${net_cidr}",
    "net_isolate":True,
    "PGADMIN_PASSWD":"${pgpasswd}",
    "pgdata":"${pgdata}",
    "ctrlport":"${ctrlport}",

}