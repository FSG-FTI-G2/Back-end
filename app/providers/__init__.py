from .db import DatabaseProvider
from .encryption import EncryptionProvider
from app.providers.vector_db import QdrantProvider

encryptor = EncryptionProvider()

file_db = DatabaseProvider("files")
user_db = DatabaseProvider("users")
file_db = DatabaseProvider("files")

qdrant_client = QdrantProvider('Qdrants_Vector_Database')
qdrant_client.create_collection()

llm_config_db = DatabaseProvider("llm_config")
