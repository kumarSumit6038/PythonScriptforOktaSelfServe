import requests
import json
import GetPropertyModule

tenant_url = GetPropertyModule.get_property("tenant_url")
tenant_url_group = GetPropertyModule.get_property("tenant_url") + "/api/v1/groups"
tenant_url_app = GetPropertyModule.get_property("tenant_url") + "/api/v1/apps"
api_key = GetPropertyModule.get_property("api_key")
group_name = GetPropertyModule.get_property("group_name")
group_desc = GetPropertyModule.get_property("group_desc")


def create_bookmark_app():

    payload = json.dumps({
        "name": "bookmark",
        "label": "Sample Bookmark App",
        "signOnMode": "BOOKMARK",
        "settings": {
            "app": {
                "requestIntegration": False,
                "url": "https://example.com/bookmark.html"
            }
        }
    })
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'SSWS ' + api_key
    }

    response = requests.request("POST", tenant_url_app, headers=headers, data=payload)
    resp = response.json()
    print(response.text)
    id = resp['id']
    print(id)
    if id is not None:
        var1 = group_name.split(",")
        for x in range(len(var1)):
            print(var1[x])
            group_search_url = tenant_url_group + "?q=" + var1[x]
            payload = {}
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': 'SSWS ' + api_key
            }

            response = requests.request("GET", group_search_url, headers=headers, data=payload)
            exist_group_resp = response.json()
            if len(exist_group_resp) == 1:
                for i in range(len(exist_group_resp)):
                    exist_group_id = exist_group_resp[i]['id']
                    print("GroupID in okta: " + exist_group_id + "for group name: " + exist_group_resp[i]['profile'][
                        'name'])
                    assign_group_to_app(id, exist_group_id)
            else:
                print("group should be created first")
    else:
        print("Application already created")


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
    print("Group is assigned to application.Check the application in admin console.")
    print(response.text)


create_bookmark_app()