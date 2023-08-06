import requests
import json
from datetime import datetime


# Types
class SubColumn:
    def __init__(self, path=None, name=None, columnPath=None):
        self.path = path
        self.name = name
        self.columnPath = columnPath

    def to_dict(self):
        return self.__dict__


class Column:
    def __init__(self, path=None, name=None, tablePath=None, hstores=None):
        self.path = path
        self.name = name
        self.tablePath = tablePath
        self.hstores = [SubColumn(**subcolumn) for subcolumn in hstores] if hstores else []

    def to_dict(self):
        return {**self.__dict__, 'hstores': [h.to_dict() for h in self.hstores]}


class Table:
    def __init__(self, path=None, name=None, dbPath=None, schemaPath=None, columns=None):
        self.path = path
        self.name = name
        self.db_path = dbPath
        self.schemaPath = schemaPath
        self.columns = [Column(**column) for column in columns] if columns else []

    def to_dict(self):
        return {**self.__dict__, 'columns': [c.to_dict() for c in self.columns]}


class Schema:
    def __init__(self, path=None, name=None, dbPath=None, tables=None):
        self.path = path
        self.name = name
        self.dbPath = dbPath
        self.tables = [Table(**table) for table in tables] if tables else []

    def to_dict(self):
        return {**self.__dict__, 'tables': [t.to_dict() for t in self.tables]}


class Db:
    def __init__(self, path=None, name=None, datastoreId=None, schemas=None, tables=None):
        self.path = path
        self.name = name
        self.datastoreId = datastoreId
        self.schemas = [Schema(**schema) for schema in schemas] if schemas else []
        self.tables = [Table(**table) for table in tables] if tables else []

    def to_dict(self):
        return {**self.__dict__, 'schemas': [s.to_dict() for s in self.schemas],
                'tables': [t.to_dict() for t in self.tables]}


class Datastore:
    def __init__(self, id=None, name=None, technology=None, dbs=None):
        self.id = id
        self.name = name
        self.technology = technology
        self.dbs = [Db(**db) for db in dbs] if dbs else []

    def to_dict(self):
        return {**self.__dict__, 'dbs': [db.to_dict() for db in self.dbs]}


class Tag:
    def __init__(self, id: str, name: str, createdAt: datetime):
        self.id = id
        self.name = name
        self.createdAt = createdAt

    def to_dict(self):
        return self.__dict__


class InventoryColumn:
    def __init__(self, createdAt=None, updatedAt=None, datastoreId=None, datastoreName=None, path=None,
                 tablePhysicalId=None, tableAttributeNumber=None, name=None, alias=None, tablePath=None,
                 dataLabel=None, dataType=None, dataTypeOid=None, dataLabelLockedForSidecar=None,
                 tags=None, encrypted=None):
        self.createdAt = createdAt
        self.updatedAt = updatedAt
        self.datastoreId = datastoreId
        self.datastoreName = datastoreName
        self.path = path
        self.tablePhysicalId = tablePhysicalId
        self.tableAttributeNumber = tableAttributeNumber
        self.name = name
        self.alias = alias
        self.tablePath = tablePath
        self.dataLabel = dataLabel
        self.dataType = dataType
        self.dataTypeOid = dataTypeOid
        self.dataLabelLockedForSidecar = dataLabelLockedForSidecar
        self.tags = tags
        self.encrypted = encrypted

    def to_dict(self):
        return self.__dict__


# Requests

class CreateInventoryObjectRequest:
    class Db:
        def __init__(self, path=None, name=None):
            self.path = path
            self.name = name

        def to_dict(self):
            return self.__dict__

    class Schema:
        def __init__(self, path=None, name=None):
            self.path = path
            self.name = name

        def to_dict(self):
            return self.__dict__

    class Table:
        def __init__(self, path=None, name=None):
            self.path = path
            self.name = name

        def to_dict(self):
            return self.__dict__

    class Column:
        def __init__(self, path=None, name=None, dataType=None):
            self.path = path
            self.name = name
            self.dataType = dataType

        def to_dict(self):
            return self.__dict__

    class SubColumn:
        def __init__(self, path=None, name=None, subType=None):
            self.path = path
            self.name = name
            self.subType = subType

        def to_dict(self):
            return self.__dict__

    def __init__(self, datastoreId=None, objectType=None, db=None, schema=None,
                 table=None, column=None, subColumn=None):
        self.datastoreId = datastoreId
        self.objectType = objectType
        self.db = self.Db(**db) if db else None
        self.schema = self.Schema(**schema) if schema else None
        self.table = self.Table(**table) if table else None
        self.column = self.Column(**column) if column else None
        self.subColumn = self.SubColumn(**subColumn) if subColumn else None

    def to_dict(self):
        return {
            **self.__dict__,
            'db': self.db.to_dict() if self.db else None,
            'schema': self.schema.to_dict() if self.schema else None,
            'table': self.table.to_dict() if self.table else None,
            'column': self.column.to_dict() if self.column else None,
            'subColumn': self.subColumn.to_dict() if self.subColumn else None,
        }


class CreateInventoryTagRequest:
    def __init__(self, name: str):
        self.name = name

    def to_dict(self):
        return self.__dict__


class UpdateColumnFieldEncryptionRequest:
    def __init__(self, datastoreId, path, encryptionKeyStorage, encryptionKeyId, encryptionAlgorithm,
                 encryptExistingData):
        self.datastoreId = datastoreId
        self.path = path
        self.encryptionKeyStorage = encryptionKeyStorage
        self.encryptionKeyId = encryptionKeyId
        self.encryptionAlgorithm = encryptionAlgorithm
        self.encryptExistingData = encryptExistingData

    def to_dict(self):
        return self.__dict__


class UpdateColumnDataLabelRequest:
    def __init__(self, datastoreId, path, dataLabel):
        self.datastoreId = datastoreId
        self.path = path
        self.dataLabel = dataLabel

    def to_dict(self):
        return self.__dict__


class UpdateColumnLockStatusRequest:
    def __init__(self, datastoreId, path, validated):
        self.datastoreId = datastoreId
        self.path = path
        self.validated = validated

    def to_dict(self):
        return self.__dict__


class GetInventoryObjectRequest:
    def __init__(self, datastoreId, path):
        self.datastoreId = datastoreId
        self.path = path

    def to_dict(self):
        return self.__dict__


class GetInventoryFlatRequest:
    def __init__(self, limit=None, cursor=None, go_back=None):
        self.limit = limit
        self.cursor = cursor
        self.go_back = go_back

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items() if value is not None}


# Responses

class CreateInventoryTagResponse:
    def __init__(self, tag: dict):
        self.tag = Tag(**tag)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data.get('tag', {}))


class GetInventoryTagsResponse:
    def __init__(self, tags: list):
        self.tags = [Tag(**tag) for tag in tags]

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data.get('tags', []))


class DeleteInventoryTagResponse:
    def __init__(self, tags: list):
        self.tags = [Tag(**tag) for tag in tags]

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data.get('tags', []))


class GetInventoryFlatResponse:
    def __init__(self, inventory: list, next_cursor: str):
        self.inventory = inventory
        self.next_cursor = next_cursor

    @classmethod
    def from_dict(cls, data: dict):
        inventory_data = []
        for entry in data.get('inventory', []):
            inventory_data.append(InventoryColumn(*entry))
        next_cursor = data.get('nextCursor')
        return cls(inventory_data, next_cursor)


class InventoryService:
    def __init__(self, SERVER_URL, token):
        self.BASE_URL = SERVER_URL
        self.headers = {
            'Content-Type': 'application/json',
            'X-Api-Key': token,
        }

    def GetInventoryHierarchical(self):
        url = f"{self.BASE_URL}/admin.v1.InventoryService/GetInventoryHierarchical"
        response = requests.post(url, headers=self.headers, data=json.dumps({}))

        if response.status_code != 200:
            raise Exception(f'Request failed with status {response.status_code}')

        inventory_data = response.json().get('inventory', [])
        return [Datastore(**datastore) for datastore in inventory_data]

    def GetInventoryFlat(self, request: GetInventoryFlatRequest):
        url = f"{self.BASE_URL}/admin.v1.InventoryService/GetInventoryFlat"
        payload = request.to_dict()

        response = requests.post(url, headers=self.headers, data=json.dumps(payload))

        if response.status_code != 200:
            raise Exception(f'Request failed with status {response.status_code}')

        response_data = response.json()

        return GetInventoryFlatResponse.from_dict(response_data)

    def GetInventoryObject(self, request: GetInventoryObjectRequest):
        url = f"{self.BASE_URL}/admin.v1.InventoryService/GetInventoryObject"
        payload = request.to_dict()

        response = requests.post(url, headers=self.headers, data=json.dumps(payload))

        if response.status_code != 200:
            raise Exception(f'Request failed with status {response.status_code}')

        column_data = response.json().get('Column', {})
        return InventoryColumn(**column_data)

    def UpdateColumnLockStatus(self, request: UpdateColumnLockStatusRequest):
        url = f"{self.BASE_URL}/admin.v1.InventoryService/UpdateColumnLockStatus"
        payload = request.to_dict()

        response = requests.post(url, headers=self.headers, data=json.dumps(payload))

        if response.status_code != 200:
            raise Exception(f'Request failed with status {response.status_code}')

    def UpdateColumnDataLabel(self, request: UpdateColumnDataLabelRequest):
        url = f"{self.BASE_URL}/admin.v1.InventoryService/UpdateColumnDataLabel"

        payload = request.to_dict()

        response = requests.post(url, headers=self.headers, data=json.dumps(payload))

        if response.status_code != 200:
            raise Exception(f'Request failed with status {response.status_code}')

    def UpdateColumnFieldEncryption(self, request: UpdateColumnFieldEncryptionRequest):
        url = f"{self.BASE_URL}/admin.v1.InventoryService/UpdateColumnFieldEncryption"
        payload = request.to_dict()

        response = requests.post(url, headers=self.headers, data=json.dumps(payload))

        if response.status_code != 200:
            raise Exception(f'Request failed with status {response.status_code}')

    def CreateInventoryObject(self, request: CreateInventoryObjectRequest):
        url = f"{self.BASE_URL}/admin.v1.InventoryService/CreateInventoryObject"
        payload = request.to_dict()
        response = requests.post(url, headers=self.headers, data=json.dumps(payload))

        if response.status_code != 200:
            raise Exception(f'Request failed with status {response.status_code}')

    def CreateInventoryTag(self, request: CreateInventoryTagRequest) -> CreateInventoryTagResponse:
        url = f"{self.BASE_URL}/admin.v1.InventoryService/CreateInventoryTag"
        payload = request.to_dict()
        response = requests.post(url, headers=self.headers, data=json.dumps(payload))

        if response.status_code != 200:
            raise Exception(f'Request failed with status {response.status_code}')

        return CreateInventoryTagResponse.from_dict(response.json())

    def GetInventoryTags(self):
        url = f"{self.BASE_URL}/admin.v1.InventoryService/GetInventoryTags"
        response = requests.post(url, headers=self.headers, data=json.dumps({}))

        if response.status_code != 200:
            raise Exception(f'Request failed with status {response.status_code}')

        return GetInventoryTagsResponse.from_dict(response.json())

    def DeleteInventoryTag(self, id) -> DeleteInventoryTagResponse:
        url = f"{self.BASE_URL}/admin.v1.InventoryService/DeleteInventoryTag"
        payload = {
            'id': id,
        }

        response = requests.post(url, headers=self.headers, data=json.dumps(payload))

        if response.status_code != 200:
            raise Exception(f'Request failed with status {response.status_code}')

        return DeleteInventoryTagResponse.from_dict(response.json())
