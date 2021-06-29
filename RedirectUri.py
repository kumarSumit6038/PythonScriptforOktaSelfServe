import json

import requests

import GetPropertyModule
import logging

tenant_url = GetPropertyModule.get_property("tenant_url")
tenant_url_app = GetPropertyModule.get_property("tenant_url") + "/api/v1/apps"
label = GetPropertyModule.get_property("label")
redirect_uri = GetPropertyModule.get_property("redirect_uri")
api_key = GetPropertyModule.get_property("api_key")
application_type = GetPropertyModule.get_property("application_type")
initiate_login_uri = GetPropertyModule.get_property("initiate_login_uri")
post_logout_redirect_uris = GetPropertyModule.get_property("post_logout_redirect_uris")
token_endpoint_auth_method = GetPropertyModule.get_property("token_endpoint_auth_method")
tenant_url_group = GetPropertyModule.get_property("tenant_url") + "/api/v1/groups"
response_type = GetPropertyModule.get_property("response_type")
grant_type = GetPropertyModule.get_property("grant_type")
group_name = GetPropertyModule.get_property("group_name")
group_desc = GetPropertyModule.get_property("group_desc")

logging.basicConfig(filename='sample.log', filemode='w', format='%(asctime)s | %(levelname)s: %(message)s',
                    level=logging.NOTSET)


# createapp function

def createoidcapplication():
    var1 = redirect_uri.split(",")
    var2 = post_logout_redirect_uris.split(",")
    var3 = response_type.split(",")
    var4 = grant_type.split(",")
    # print(var1)
    # for x in range(len(var1)):
    #     print(var1[x])
    payload_app = json.dumps({
        "name": "oidc_client",
        "label": label,
        "signOnMode": "OPENID_CONNECT",
        "credentials": {
            "oauthClient": {
                "token_endpoint_auth_method": token_endpoint_auth_method
            }
        },
        "settings": {
            "oauthClient": {
                "redirect_uris": var1,
                "initiate_login_uri": initiate_login_uri,
                "post_logout_redirect_uris": var2,
                "response_types": var3,
                "grant_types": var4,
                "application_type": application_type
            }
        }
    })
    headers_app = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'SSWS ' + api_key
    }
    response_app = requests.request("POST", tenant_url_app, headers=headers_app, data=payload_app)
    # print(response_app.status_code)
    #print(response_app.text)
    if response_app.status_code == 200:
        getappid = response_app.json()['id']
        appName = response_app.json()['label']
        client_id = response_app.json()['credentials']['oauthClient']['client_id']

        if application_type == 'web':
            client_secret = response_app.json()['credentials']['oauthClient']['client_secret']
            # print("Application ID: " + getappid + " For Application " + appName)
            logging.info("Application " + appName + " with Application ID: " + getappid + " created in " + tenant_url)
            # print("Client ID is: " + client_id)
            logging.info("######### Application details are as follows ############")
            logging.info("\n" + "Client ID is : " + client_id + "\n" + "Client Secret is : " + client_secret + "\n")
            return getappid
        else:
            logging.info("Application is SPA/Native.")
            logging.info("Application " + appName + " with Application ID: " + getappid + " created in " + tenant_url)
            logging.info("Client ID is : " + client_id + "\n")
    else:
        logging.error("There is some error.Please investigate.")
        logging.error(response_app.text)


var2 = createoidcapplication()
# print(var2)