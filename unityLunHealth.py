import requests
import json
from requests.auth import HTTPBasicAuth
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import os.path
import sys

#return value
healthy = 1

#open and process config file
if os.path.isfile('unityLunConfig.json'):
            with open("unityLunConfig.json") as json_file:
                config = json.load(json_file)
                ip = config["ip"]
                user = config["user"]
                password = config["password"]
                luns = config["luns"]

#create session
s = requests.Session()
s.cookies.clear()

s.headers = {"X-EMC-REST-CLIENT": "true", "Accept" : "application/json", "Content-Type" : "application/json" }

login_url = "https://" + ip + "/api/types/basicSystemInfo/instances"
logout_url = "https://" + ip + "/api/types/loginSessionInfo/action/logout"

s.auth = auth=HTTPBasicAuth(user, password)
response = s.get(login_url, cookies=None, verify=False)

#loop through luns from config file and check each via api call
for lun in luns:
    lun_url = "https://" + ip + "/api/instances/lun/name:" + lun + "?fields=name,health"  
    response = s.get(lun_url, verify=False)
    if response.status_code <= 200:
        content = json.loads(response.content)
        health = content["content"]["health"]
        #print (health)
        if health["value"] != 5:
            healthy = 0
    else:
        healthy = 0
        sys.stdout.write("%s: LUN Not Found\n" % lun)
        break

#logout of unisphere
logout = s.get(logout_url, verify=False)

#write out health code and exit with 1 or 0
sys.stdout.write(str(healthy))
sys.exit(healthy)