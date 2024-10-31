import os
from pymongo import MongoClient

client = MongoClient(
    host=os.environ.get("MONGODB_HOST", "localhost"),
    port=int(os.environ.get("MONGODB_PORT", 27017)),
)

db = client[os.environ.get("MONGODB_DB_NAME", "primary")]

