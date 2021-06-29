import datetime
import time

import requests
import json
import logging

import GetPropertyModule

# import OIDCAppSelfServe


tenant_url = GetPropertyModule.get_property("tenant_url") + "/api/v1/groups"
api_key = GetPropertyModule.get_property("api_key")
group_name = GetPropertyModule.get_property("group_name")
group_desc = GetPropertyModule.get_property("group_desc")

logging.basicConfig(filename='sample.log', filemode='w', format='%(asctime)s | %(levelname)s: %(message)s', level=logging.NOTSET)
logging.debug('Here you have some information for debugging.')


var1 = group_name.split(",")
for x in range(len(var1)):
    # print(var1[x])
    logging.info(var1[x])
    url = "https://dev-48491388.okta.com/api/v1/groups?q="+var1[x]
    payload = {}
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'SSWS 006fKfJxkVCYoXwVpqDHIbcuGda6YspXWcF0sPE_kG',
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    exist_group_resp = response.json()
    # print("checking for groups in okta")
    # print(len(exist_group_resp))
    if len(exist_group_resp) == 1:
        for i in range(len(exist_group_resp)):
            exist_group_id = exist_group_resp[i]['id']
            print("GroupID in okta: " + exist_group_id + "for group name: " + exist_group_resp[i]['profile']['name'])
    else:
        payload = json.dumps({
            "profile": {
                "name": var1[x],
                "description": group_desc
            }
        })
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'SSWS ' + api_key
        }

        response = requests.request("POST", tenant_url, headers=headers, data=payload)
        print(response.text)
        newgroupid = response.json()['id']
        print("Group: " + var1[x] + " created with Group ID " + newgroupid)
        logging.info(response.text)
        # logging.info("Group Ids: " + response.json()['id'])




