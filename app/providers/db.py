from bson import ObjectId
from app.configs.mongodb import db


class DatabaseProvider:
    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self.collection = db[collection_name]

    def get_all(self):
        cursor = self.collection.find()
        data = map(lambda x: {**x, "_id": str(x["_id"])}, cursor)
        return list(data)

    def get_by_id(self, id: str):
        data = self.collection.find_one({"_id": ObjectId(oid=id)})
        if data:
            data["_id"] = str(data["_id"])
            return data
        return None

    def query(self, query: dict):
        cursor = self.collection.find(query)
        data = map(lambda x: {**x, "_id": str(x["_id"])}, cursor)
        return list(data)

    def create(self, data: dict):
        result = self.collection.insert_one(data)
        return str(result.inserted_id)

    def update(self, id: str, data: dict):
        result = self.collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data})
        return result.modified_count

    def delete(self, id: str):
        result = self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count
