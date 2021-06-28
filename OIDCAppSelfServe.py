import json

import requests
import logging
from requests.exceptions import HTTPError

import GetPropertyModule

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


# createapp function
def create_oidc_application():
    print("create Application method")
    var1 = redirect_uri.split(",")
    var2 = post_logout_redirect_uris.split(",")
    var3 = response_type.split(",")
    var4 = grant_type.split(",")
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
    getappid = response_app.json()['id']
    appName = response_app.json()['label']
    client_id = response_app.json()['credentials']['oauthClient']['client_id']
    print("Application ID:" + getappid)
    if getappid is not None:
        print("Application ID: " + getappid + " For Application " + appName)
        logging.info("Application ID: " + getappid + " is generated for " + appName + " application in " + tenant_url)
        print("Client ID is: " + client_id)
        logging.info("Client ID is generated: " + client_id)
        return getappid
    else:
        logging.error(response_app.json())
    response_app.raise_for_status()



# create group to okta and fetch id
def create_assign_group_to_app():
    print("create group method")
    app_id = create_oidc_application()
    print("Application ID: " + app_id)

    var1 = group_name.split(",")
    for x in range(len(var1)):
        print(var1[x])
        payload_group = json.dumps({
            "profile": {
                "name": var1[x],
                "description": group_desc
            }
        })
        headers_group = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'SSWS ' + api_key
        }

        response_grp = requests.request("POST", tenant_url_group, headers=headers_group, data=payload_group)
        getgroupid = response_grp.json()['id']
        print("Group ID:" + getgroupid)

        # Assign groups to App starts from here

        url = tenant_url + "/api/v1/apps/" + app_id + "/groups/" + getgroupid
        payload = json.dumps({})
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'SSWS ' + api_key
        }
        response = requests.request("PUT", url, headers=headers, data=payload)
        print(response.text)


create_assign_group_to_app()
