<h1 align="left">Access Dataverse Using Python</h1>

###

<p align="left">You don't require a fancy library to connect with Microsoft Dataverse. You can use this program to generate custom report or deploy the program in gitlab/jenkins/any web api program to automate the tasks.<br><br>You would need a service principle, to access the Dataverse environment.</p>

###

<h2 align="left">How to create service principle?.</h2>

###

<p align="left">✨ You need to create the service principle with App Registration in Azure AD.<br>✨ Add the required Dynamics CRM API - User Impersonation permission.<br>✨ Grant admin consent<br>✨ For step by step instruction, You may go through this blogpost: https://d365demystified.com/2022/08/09/authenticate-dataverse-connector-using-service-principal-in-a-power-automate-flow/</p>

###

```python
from Dataverse import Dataverse

dv = Dataverse(
        tenant="tenantid",
        env_name="environment_host_name",
        client_id="AAD App Client Id",
        secret="AAD App Secret Value",
        scope="https://environment_host_name/.default"
        )
if dv.login():
        dv_table = dv.get_table_data(
        table_name="dataverse_logical_name",
        expand="lookfield_logical_incase_of_expand",
        filterBy="ODatat_fitler_query"
        )

```
New functionalities will be added soon.
