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

logging.basicConfig(filename='sample.log', filemode='w', format='%(asctime)s | %(levelname)s: %(message)s',
                    level=logging.NOTSET)


#  function to create Application
def create_oidc_application():
    # print("create Application method")
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
    if response_app.status_code == 200:
        getappid = response_app.json()['id']
        appName = response_app.json()['label']
        client_id = response_app.json()['credentials']['oauthClient']['client_id']

        if application_type == 'web':
            client_secret = response_app.json()['credentials']['oauthClient']['client_secret']
            # print("Application ID: " + getappid + " For Application " + appName)
            logging.info("Application " + appName + " with Application ID: " + getappid + " created in " + tenant_url)
            # print("Client ID is: " + client_id)
            # logging.info("######### Application details are as follows ############")
            # logging.info("\n" + "Client ID is : " + client_id + "\n" + "Client Secret is : " + client_secret + "\n")
            return getappid
        else:
            logging.info("Application is SPA/Native.")
            logging.info("Application " + appName + " with Application ID: " + getappid + " created in " + tenant_url)
            logging.info("Client ID is : " + client_id + "\n")
    else:
        logging.error("There is some error.Please investigate.")
        logging.error(response_app.text)


# function to assign group to app
def assign_group_to_app(appid, groupid):
    url = tenant_url + "/api/v1/apps/" + appid + "/groups/" + groupid
    payload = json.dumps({})
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'SSWS ' + api_key
    }
    response = requests.request("PUT", url, headers=headers, data=payload)
    logging.info("Group is assigned to application.Check the application in admin console.")
    # print(response.text)


# create group to okta and fetch id
def create_assign_group_to_app():
    app_id = create_oidc_application()
    if app_id is not None:
        logging.info("Create and assign group to Application ID: " + app_id)
        # print("create group method")
        # print("Application ID: " + app_id)

        var1 = group_name.split(",")
        for x in range(len(var1)):
            # For checking if Group already exists in okta,
            # if exists,assign to app, otherwise create new.

            exist_url = "https://dev-48491388.okta.com/api/v1/groups?q=" + var1[x]
            exist_payload = {}
            exist_headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': 'SSWS '+ api_key,
            }

            response = requests.request("GET", exist_url, headers=exist_headers, data=exist_payload)
            exist_group_resp = response.json()
            if len(exist_group_resp) == 1:
                for i in range(len(exist_group_resp)):
                    exist_group_id = exist_group_resp[i]['id']
                    print("GroupID in okta: " + exist_group_id + " for group name: " + exist_group_resp[i]['profile'][
                        'name'])
                    # Assign groups to App starts from here
                    assign_group_to_app(app_id, exist_group_id)
            else:
                # print(var1[x])
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
                if response_grp.status_code == 200:
                    getgroupid = response_grp.json()['id']
                    logging.info(var1[x] + " group created with id: " + getgroupid)

                    # Assign groups to App starts from here
                    assign_group_to_app(app_id, getgroupid)
                else:
                    logging.error(response_grp.text)
    else:
        logging.error("Application is not created.Please check the error message.")


create_assign_group_to_app()
