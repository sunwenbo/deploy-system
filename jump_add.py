#coding=utf-8

import requests
import json
import sys

ip = sys.argv[1]
hostname = sys.argv[2]
sshport = int(sys.argv[3])

group = hostname.split('-')[0]
if group == 'sre':
    nodes = ["99d6fb1f-a01f-46b4-a36b-6cf55c096e70"]
elif 'pre' in group:
    nodes = ["720a1615-cdb0-403c-a919-8a4ad0d15b38"]
elif group == 'test':
    nodes = ["2d50cf41-4921-4688-8f37-2ffc24e41106"]
elif group == 'saas':
    nodes = ["3fe1a7aa-6fe1-49b9-b08b-66d259fe6f89"]
elif group in ['ksvc', 'kapi']:
    nodes = ["6425937f-309d-4bc1-bd78-4401979bf852"]
elif group == 'mapi':
    nodes = ["c930c66e-74d2-40c3-9053-a84659b258b5"]
elif group == 'stg':
    nodes = ["c930c66e-74d2-40c3-9053-a84659b258b5", "6425937f-309d-4bc1-bd78-4401979bf852"]
elif group == 'tupu':
    nodes = ["8dbfcdb8-d2c3-4a51-8f0b-3a1c1ababed9"]
elif group == 'partner':
    nodes = ["326e8a70-1c59-4021-8a4c-1c3ea4160d45"]
elif group == 'cs':
    nodes = ["a31005bb-1152-47fb-9876-460ec842b0d9"]
else:
    nodes = []

nodes.append("801de1b6-34bc-4ff6-b7eb-c6fa9c625a39")


token = 'c02f2183dc056d867e8911a5ba9b2ba949a55d4f'
header = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-CSRFToken': 'ePQdasmlAI4y6ASA2A2nbrx01bgAzJWg6dryB8IZlW5FEK9nrCDZIDXfkEe7F56D',
    'Authorization': 'Token '+token
}

params = {
  "ip": ip,
  "hostname": hostname,
  "protocol": "ssh",
  "port": sshport,
  "platform": "Linux",
  "is_active": True,
  "admin_user": "2b95bfc2-f617-451c-a9a9-23b9fcbb0ff6",
  "nodes": nodes
}

url = 'https://jp.lc.com/api/assets/v1/assets/'

r = requests.post(url, data=json.dumps(params), headers=header)

print(r.status_code, r.text)



