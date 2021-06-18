import json

import requests

import GetPropertyModule

tenant_url = GetPropertyModule.getProperty("tenant_url")
tenant_url_app = GetPropertyModule.getProperty("tenant_url") + "/api/v1/apps"
label = GetPropertyModule.getProperty("label")
redirect_uri = GetPropertyModule.getProperty("redirect_uri")
api_key = GetPropertyModule.getProperty("api_key")
application_type = GetPropertyModule.getProperty("application_type")
initiate_login_uri = GetPropertyModule.getProperty("initiate_login_uri")
post_logout_redirect_uris = GetPropertyModule.getProperty("post_logout_redirect_uris")
token_endpoint_auth_method = GetPropertyModule.getProperty("token_endpoint_auth_method")
tenant_url_group = GetPropertyModule.getProperty("tenant_url") + "/api/v1/groups"
group_name = GetPropertyModule.getProperty("group_name")
group_desc = GetPropertyModule.getProperty("group_desc")


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
    print("Application ID:" + getappid)
    return getappid

var2 = createoidcapplication()
print(var2)