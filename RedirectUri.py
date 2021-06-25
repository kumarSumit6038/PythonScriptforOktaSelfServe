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
group_name = GetPropertyModule.get_property("group_name")
group_desc = GetPropertyModule.get_property("group_desc")

logging.basicConfig(filename='sample.log', filemode='w', format='%(asctime)s | %(levelname)s: %(message)s', level=logging.NOTSET)
# createapp function

def createoidcapplication():
    var1 = redirect_uri.split(",")
    print(var1)
    for x in range(len(var1)):
        print(var1[x])
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
                "post_logout_redirect_uris": [post_logout_redirect_uris],
                "response_types": [
                    "token",
                    "id_token",
                    "code"
                ],
                "grant_types": [
                    "implicit",
                    "authorization_code"
                ],
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
    print(response_app.text)
    getappid = response_app.json()['id']
    appName = response_app.json()['label']
    client_id = response_app.json()['credentials']['oauthClient']['client_id']
    if(getappid is not None):
        print("Application ID:" + getappid +"For Application"+appName)
        logging.info("Application ID: "+getappid+" is generated for "+appName+" application in "+tenant_url)
        print("Client ID is: "+client_id)
        logging.info("Client ID is generated: "+client_id)
        return getappid

var2 = createoidcapplication()
print(var2)