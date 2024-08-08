# Dataverse

You don't require a fancy library to connect to the Microsoft Dataverse.
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
