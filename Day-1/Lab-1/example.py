import requests
from pprint import PrettyPrinter

#To disable warning about self signed certificates
import urllib3
urllib3.disable_warnings()

#Inventory
DEVICE_IPS = ['192.168.0.11','192.168.0.12','192.168.0.13','192.168.0.14','192.168.0.15','192.168.0.16','192.168.0.17','192.168.0.18']

#Device Credentials
USERNAME = 'arista'
PASSWORD = 'arista0ob7'

if __name__ == '__main__':
    payload = {'jsonrpc':'2.0',
    'method':'runCmds',
    'params':{
        'version':1,
        #List of commands to run on the switch
        'cmds':["show hostname","show version"]
    },
    'id':'1'
    }

pp = PrettyPrinter()

for device in DEVICE_IPS:
    r = requests.post('https://{}:443/command-api'.format(device), json=payload, auth=(USERNAME, PASSWORD), verify=False)
    response = r.json()
    fqdn = response['result'][0]['fqdn']
    serial = response['result'][1]['serialNumber']
    mac = response['result'][1]['systemMacAddress']
    model = response['result'][1]['modelName']
    # pp.pprint(response)
    #print(f"Example of formating a string in python: {response['result'][0]}")
    print(f"{fqdn} is a {model} with serial number {serial} and system MAC address {mac}")