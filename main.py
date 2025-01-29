import requests
import json
from vantage_domain_ip_server import AR_resources, MX_resources
from probes import AR_probes, MX_probes

url = 'http://caitlyn.cs.northwestern.edu/ripeline/schedule'



headers = { 'Content-Type': 'application/json' } 

addresses_and_probes = []

for address in AR_resources:
    addresses_and_probes.append({
        "address": address["ip_address"], 
        "probes": AR_probes
    })

for address in MX_resources:
    addresses_and_probes.append({
        "address": address["ip_address"],
        "probes": MX_probes
    })

headers = {
	'Content-Type': 'application/json'
}

data = { 'type': 'traceroute', 'addresses_and_probes': addresses_and_probes, 'description': 'some comments', 'userid': '*' }

response = requests.post(url, data=json.dumps(data), headers=headers)
print('Status code:', response.status_code)
print('Response body:', response.json())