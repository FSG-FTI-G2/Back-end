from .memory_provider import MemoryStateProvider
from .encryption_provider import EncryptionProvider
from .db_provider import DatabaseProvider
from .minio_provider import MinioProvider
from .embedding_provider import VectorEmbedder
from .vectordb_provider import QdrantProvider
from .celery_provider import CeleryProvider
from .llm_provider import LLMProvider

# Utilities Providers
state = MemoryStateProvider()
encryptor = EncryptionProvider()

# Database Providers
file_db = DatabaseProvider("files")
user_db = DatabaseProvider("users")
llm_config_db = DatabaseProvider("llm_config")
message_db = DatabaseProvider("messages")

# File Storage Providers
file_storage = MinioProvider("files")

# AI Related Providers
embedder = VectorEmbedder()
vectordb_provider = QdrantProvider()
llm = LLMProvider()

celery = CeleryProvider()
