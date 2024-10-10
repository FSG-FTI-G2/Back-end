from .encryption import EncryptionProvider
from .memory import MemoryStateProvider
from .db import DatabaseProvider
# from app.providers.vector_db import QdrantProvider
from .minio import MinioProvider

encryptor = EncryptionProvider()
state = MemoryStateProvider()

file_db = DatabaseProvider("files")
user_db = DatabaseProvider("users")

# qdrant_client = QdrantProvider('Qdrants_Vector_Database')
# qdrant_client.create_collection()

llm_config_db = DatabaseProvider("llm_config")

file_storage = MinioProvider("files")
