import json
from requests import Session

class Dataverse:

    def __init__(self, tenant, env_name, client_id, secret, scope):
        self.tenant = tenant
        self.env_name = env_name
        self.client_id = client_id
        self.secret = secret
        self.session = Session()
        self.scope = scope
        self.auth_url = "https://login.microsoftonline.com/{0}/oauth2/v2.0/token".format(self.tenant)
        self.api_end_point = "https://{0}/api/data/v9.2/".format(self.env_name)
        self.url = ""
        self.data = []

    def login(self):
        try:
            body = {
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.secret,
                "scope": self.scope
            }
            self.session.headers.update({
                "content-type": "application/x-www-form-urlencoded"
            })
            response = self.session.post(self.auth_url, data=body)
            if response.status_code == 200:
                token_info = response.json()
                if "content-type" in self.session.headers.keys():
                    self.session.headers.pop("content-type")
                self.session.headers.update({
                    "Authorization": "Bearer {0}".format(token_info["access_token"]),
                    "OData-MaxVersion": "4.0",
                    "OData-Version": "4.0",
                    "Content-Type": "application/json; odata.metadata=minimal",
                    "Accept": "application/json"
                })
                return True
            return response.text
        except Exception as e:
            raise e

    def generate_get_url(self, table_name, expand="", filterBy=""):
        tempArr = []
        self.url = self.api_end_point + table_name
        if any(expand) or any(filterBy) == True:
            self.url += "?"
        if expand != "":
            tempArr.append("$expand={0}".format(expand))
        if filterBy != "":
            tempArr.append("$filter={0}".format(filterBy))
        self.url += "&".join(tempArr)

    def get_table_data(self, table_name, expand="", filterBy=""):
        try:
            self.data = []
            self.generate_get_url(table_name=table_name, expand=expand, filterBy=filterBy)
            self.session.headers.update({"OData-MaxVersion": "4.0", "OData-Version": "4.0", "Accept": "application/json", "prefer": "odata.include-annotations='OData.Community.Display.V1.FormattedValue'"})
            response = self.session.get(self.url)
            next_url = ""
            if response.status_code == 200:
                if response.json().get("value") is None:
                    return response.json()
                if response.json().get("value") is not None:
                    self.data.extend(list(response.json()['value']))
                if "@odata.nextLink" in response.json():
                    next_url = response.json()['@odata.nextLink']
                while next_url != "":
                    next_response = self.session.get(next_url)
                    if next_response.status_code == 200:
                        self.data.extend(next_response.json()['value'])
                    if "@odata.nextLink" not in next_response.json():
                        next_url = ""
                    if "@odata.nextLink" in next_response.json():
                        next_url = next_response.json()['@odata.nextLink']
                return self.data
            elif response.status_code == 401:
                self.login()
                return self.get_table_data(table_name=table_name, expand=expand, filterBy=filterBy)
            return response.text
        except Exception as e:
            return e

    def create_record(self, table_name, obj, db_unique_column, fields_mapped={}):
        try:
            self.generate_get_url(table_name=table_name)
            unique_column_name = self.get_key_name_by_value(obj_as_items=fields_mapped.items())
            if unique_column_name in obj:
                del obj[unique_column_name]
            response = self.session.post(self.url, data=json.dumps(obj))
            if response.status_code == 204:
                # unique_id = response.json().get(unique_column_name)

                result = {"table_name": table_name, "performed_action": "create", db_unique_column: obj.get(db_unique_column),
                          "status_code": response.status_code, "message": "Success"}
            else:
                result = {"table_name": table_name, "performed_action": "create", db_unique_column: obj.get(db_unique_column),
                          "status_code": response.status_code, "message": "Error: {0}".format(str(response.text))}
            return result
        except Exception as e:
            result = {"table_name": table_name, "performed_action": "create", db_unique_column: obj.get(db_unique_column),
                      "status_code": "In Code Exception", "message": "Error: {0}".format(str(e))}
            return result

    def update_record(self, table_name, obj, db_unique_column, fields_mapped={}):
        temp_id = ""
        if db_unique_column in obj:
            temp_id = obj.get(db_unique_column)
        try:
            self.generate_get_url(table_name=table_name)
            unique_column_name = self.get_key_name_by_value(obj_as_items=fields_mapped.items())
            unique_id = obj.get(unique_column_name)
            self.session.headers.update({'If-Match': '*'})
            self.url += '({0})'.format(unique_id)
            if unique_column_name in obj:
                del obj[unique_column_name]
            response = self.session.patch(self.url, data=json.dumps(obj))
            if "If-Match" in self.session.headers:
                self.session.headers.pop('If-Match')
            if response.status_code == 204:
                result = {"table_name": table_name, "performed_action": "update", db_unique_column: temp_id, "status_code": response.status_code, "message": "Success"}
            else:
                result = {"table_name": table_name, "performed_action": "update", db_unique_column: temp_id, "status_code": response.status_code, "message": "Error: {0}".format(str(response.text))}
            return result
        except Exception as e:
            result = {"table_name": table_name, "performed_action": "update", db_unique_column: temp_id,
                      "status_code": "In Code Exception", "message": "Error: {0}".format(str(e))}
            return result

    def get_key_name_by_value(self, obj_as_items):
        for key, value in obj_as_items:
            if value == 'DVUniqueIdColumn':
                return key
