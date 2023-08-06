# Formal Admin Python SDK


This is the Python SDK for the Formal Admin API.



## Installing
    pip install formal-sdk

## Example Use

Create and Get a Native Role

```python
import os
import formal_sdk

if __name__ == '__main__':

    dataStoreId = ""
    nativeRoleId = ""
    nativeRoleSecret = ""
    useAsDefault = True
    apiKey = os.environ.get('TEST_API_KEY')
    
    newClient = formal_sdk.Client(apiKey)
    # Create Native Role
    createdRole = newClient.DataStoreClient.CreateNativeRole(dataStoreId=dataStoreId, nativeRoleId=nativeRoleId, nativeRoleSecret=nativeRoleSecret, useAsDefault=useAsDefault)
    
    # Get Native Role    
    previousRole = newClient.DataStoreClient.GetNativeRole(dataStoreId=dataStoreId, nativeRoleId=nativeRoleId)

    print(f'DataStoreId: {previousRole.dataStoreId}')
    print(f'NativeRoleId: {previousRole.nativeRoleId}')
    print(f'NativeRoleSecret: {previousRole.nativeRoleSecret}')
    print(f'UseAsDefault: {previousRole.useAsDefault}')

    # Get sidecar tls certificate and private key
    sidecarId = ""
    certificate, privateKey, fullSecret = newClient.SidecarClient.GetTLSCertificate(sidecarId)
```


```python
import os
import formal_sdk


from formal_sdk import inventory

if __name__ == '__main__':

    datastoreId = ""
    apiKey = os.environ.get('API_KEY')

    newClient = formal_sdk.Client(apiKey).InventoryClient

    column_dict = {
        "path": "database.schema.table.column",
        "name": "column",
        "dataType": "string"
    }

    # Create Inventory Object
    createInventoryObjectRequest = inventory.CreateInventoryObjectRequest(
        datastoreId=datastoreId,
        objectType="column",
        column=column_dict
    )
    newClient.CreateInventoryObject(createInventoryObjectRequest)

    # Get Inventory Object
    getInventoryObjectRequest = inventory.GetInventoryObjectRequest(datastoreId=datastoreId,
                                                                               path="database.schema.table.column")
    inventoryColumn = newClient.GetInventoryObject(getInventoryObjectRequest)

    print(f'DatastoreId: {inventoryColumn.datastoreId}')
    print(f'Path: {inventoryColumn.path}')
    print(f'Name: {inventoryColumn.name}')
    print(f'DataType: {inventoryColumn.dataType}')

    # Create and Get Inventory Tag
    createInventoryTagRequest = inventory.CreateInventoryTagRequest(name="important")
    createInventoryTagResponse = newClient.CreateInventoryTag(createInventoryTagRequest)

    inventoryTags = newClient.GetInventoryTags()
    for tag in inventoryTags.tags:
        print(f'TagId: {tag.id}')
        print(f'TagName: {tag.name}')
        print(f'CreatedAt: {tag.createdAt}')
        newClient.DeleteInventoryTag(id=tag.id)


```