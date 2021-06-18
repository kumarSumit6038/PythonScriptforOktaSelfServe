import datetime
import time

import requests
import json
import logging

from requests import HTTPError

import GetPropertyModule

# import OIDCAppSelfServe

t = time.process_time()

tenant_url = GetPropertyModule.get_property("tenant_url") + "/api/v1/groups"
api_key = GetPropertyModule.get_property("api_key")
group_name = GetPropertyModule.get_property("group_name")
group_desc = GetPropertyModule.get_property("group_desc")

logging.basicConfig(filename='sample.log', filemode='w', format='%(asctime)s | %(levelname)s: %(message)s', level=logging.NOTSET)
logging.debug('Here you have some information for debugging.')


var1 = group_name.split(",")
for x in range(len(var1)):
    print(var1[x])
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
    logging.info(response.text)
    logging.info("Group Ids: " + response.json()['id'])
    logging.info("Group/s created successfully.")
    logging.info("Elapsed time = ")
    logging.info(datetime.datetime.now())
