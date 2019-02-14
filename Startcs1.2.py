#!/usr/local/bin/python3.7
import requests
import json
import time

nifi_url='http://172.25.40.134:9090'
cs_id='e1495a25-0168-1000-0000-00000851f482'
base_url=nifi_url+'/nifi-api/controller-services/'+cs_id
headers = {'Content-Type': 'application/json','Accept': '*/*'}
ref_url=base_url+'/references'
getcsinformationrequest=requests.get(base_url)
parsed_json=getcsinformationrequest.json()

#enable Controller Service

vercs=parsed_json['revision']['version']
discs_payload={"revision":{"version":vercs},"component":{"id":cs_id,"state":"ENABLED"}}
json_dis_payload=json.dumps(discs_payload)
resp2=requests.put(base_url, data=json_dis_payload, headers=headers)
print(resp2.content)

# Stop referncing components
for x in parsed_json['component']['referencingComponents']:
    ver=x['revision']['version']
    ref_comp_id=x['id']
    payload={"id":cs_id,"state":"RUNNING","referencingComponentRevisions":{ref_comp_id:{"version":ver}}}
    json_payload=json.dumps(payload)
    resp=requests.put(ref_url, data=json_payload, headers=headers)
    print(resp.content)
    time.sleep(10)

discs_payload={"id":cs_id,"state":"ENABLED","referencingComponentRevisions":{}}
json_dis_payload=json.dumps(discs_payload)
resp1=requests.put(ref_url, data=json_dis_payload, headers=headers)
print(resp1.content)

# Enable Controller Service
