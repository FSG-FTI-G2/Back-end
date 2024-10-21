from typing import Any
from bson import ObjectId
from app.configs.mongodb import db


DEFAULT_PAGE_SIZE = 10
DEFAULT_PAGE_INDEX = 0


class DatabaseProvider:
    '''
    Helper Class for MongoDB CRUD Operations
    '''

    def __init__(self, collection_name: str):
        # Define collection configuration
        self.collection_name = collection_name
        self.collection = db[collection_name]

        # Running count of number of documents in the collection for pagination
        # Reduce database calls for counting documents
        self.running_count = self.collection.count_documents({})

    def page_count(self, page_size: int) -> int:
        '''
        Returns the number of pages for the collection
        based on the page size
        '''
        return self.running_count // page_size

    def create_index(self, field: str, unique: bool = False):
        '''
        Creates an index for a field in the collection
        '''
        # Create index for the field
        self.collection.create_index(field, unique=unique)

    def get_all(
        self,
        page_size: int = DEFAULT_PAGE_SIZE,
        page_index: int = DEFAULT_PAGE_INDEX
    ) -> list[dict[str, Any]]:
        '''
        Returns all documents in the collection
        '''
        # Skip and limit for pagination
        cursor = self.collection.find().skip(
            page_size * page_index).limit(page_size)
        # Convert ObjectId to string
        data = map(lambda x: {**x, "_id": str(x["_id"])}, cursor)
        # Return as list
        return list(data)

    def create_index(self, field: str, unique: bool = False):
        '''
        Creates an index for a field in the collection
        '''
        # Create index for the field
        self.collection.create_index(field, unique=unique)

    def get_by_id(self, id: str) -> dict[str, Any] | None:
        '''
        Returns a document by id, which support indexing
        '''
        # Find document by ObjectId
        data = self.collection.find_one({"_id": ObjectId(oid=id)})
        # Convert ObjectId to string
        if data:
            data["_id"] = str(data["_id"])
            return data
        return None

    def query(
        self,
        filter: dict,
        exclude: list[str] = [],
        page_size: int = DEFAULT_PAGE_SIZE,
        page_index: int = DEFAULT_PAGE_INDEX
    ) -> list[dict[str, Any]]:
        '''
        Returns documents based on a query
        '''
        # Skip and limit for pagination
        cursor = self.collection.find(filter, {field: 0 for field in exclude}).skip(
            page_size * page_index).limit(page_size)
        # Convert ObjectId to string
        data = map(lambda x: {**x, "_id": str(x["_id"])}, cursor)
        # Return as list
        return list(data)

    def create(
        self,
        data: dict[str, Any]
    ) -> str:
        '''
        Creates a document in the collection
        '''
        # Insert document
        result = self.collection.insert_one(data)
        # Increment running count
        self.running_count += 1
        # Return the inserted id
        return str(result.inserted_id)

    def update(
        self,
        id: str | list[str],
        data: dict[str, Any],
        native_query: bool = False
    ) -> int:
        '''
        Updates a document by id or multiple documents by ids
        '''
        # Get updating query
        if native_query:
            updating_query = data
        else:
            updating_query = {"$set": data}
        # Update document
        if isinstance(id, str):
            # Update document by ObjectId
            result = self.collection.update_one(
                {"_id": ObjectId(id)}, updating_query)
        else:
            # Update multiple documents by ObjectId
            result = self.collection.update_many(
                {"_id": {"$in": [ObjectId(oid=i) for i in id]}}, updating_query)
        # Return the number of documents modified
        return result.modified_count

    def delete(
        self,
        id: str | list[str]
    ) -> int:
        '''
        Deletes a document by id or multiple documents by ids
        '''
        if isinstance(id, str):
            # Delete document by ObjectId
            result = self.collection.delete_one({"_id": ObjectId(id)})
        else:
            # Delete multiple documents by ObjectId
            result = self.collection.delete_many(
                {"_id": {"$in": [ObjectId(oid=i) for i in id]}})
        # Decrement running count
        self.running_count -= result.deleted_count
        # Return the number of documents deleted
        return result.deleted_count
