import requests
from jinja2 import Environment, FileSystemLoader
from pprint import PrettyPrinter

# disable warnings about self-signed certs
import urllib3
urllib3.disable_warnings()

DEVICE_IPS = ['192.168.0.10',
              '192.168.0.11',
              '192.168.0.12',
              '192.168.0.13',
              '192.168.0.14',
              '192.168.0.15',
              '192.168.0.16',
              '192.168.0.17'
              ]
              
# TODO: USE YOUR CREDENTIALS
USERNAME = 'arista'
PASSWORD = 'arista0ob7'

if __name__ == '__main__':
    payload = {'jsonrpc': '2.0',
               'method': 'runCmds',
               'params': {
                 'version': 1,
                 'cmds': ['show version',
                          'show hostname',
                          'show ip arp']
               },
               'id': '1'
              }
    device_outputs = {}

    pp = PrettyPrinter()
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("challenge.j2")

    # Iteration through all the devices
    for device in DEVICE_IPS:
        r = requests.post('https://{}:443/command-api'.format(device), json=payload, auth=(USERNAME, PASSWORD), verify=False)
        response = r.json()
        # TODO: Un-comment this print command for checking the response received
        #pp.pprint(response)

        serialNumber = response['result'][0]['serialNumber']
        hostname = response['result'][1]['hostname']
        countArp = response['result'][2]['dynamicEntries']

        # TODO: Store the ARP information in a variable
        arp = response['result'][2]['ipV4Neighbors']

        # Here, we add an entry for each device in the dictionary 'device_outputs'
        # TODO: Add the ARP information to the dictionary 'device_outputs' so that info can be used in the jinja template
        device_outputs[hostname] = {'serial': serialNumber}
        device_outputs[hostname]['arpCount'] = countArp
        device_outputs[hostname]['arpResp']= arp

    else:
        #pp.pprint(device_outputs)
        print(template.render(devices=device_outputs))