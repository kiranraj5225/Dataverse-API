# Access Dataverse Using Python 

You don't require a fancy library to connect with Microsoft Dataverse. You can use this program to generate custom report or deploy the program in gitlab/jenkins to automate the tasks.

How to create service principle []([url](https://d365demystified.com/2022/08/09/authenticate-dataverse-connector-using-service-principal-in-a-power-automate-flow/])) ?.
        [^1] You need to create the service principle with App Registration in Azure AD.
        [^2] Add the required Dynamics CRM API - User Impersonation persmission.
        [^3] Grant admin consent

```python
from Dataverse import Dataverse

dv = Dataverse(
        tenant="tenantid",
        env_name="environment_host_name",
        client_id="AAD App Client Id",
        secret="AAD App Secret Value",
        scope="https://environment_host_name/.default"
        )
if dv.login()
        dv_table = dv.get_table_data(
        table_name="dataverse_logical_name",
        expand="lookfield_logical_incase_of_expand",
        filterBy="ODatat_fitler_query"
        )

```
New functions will be added soon.
