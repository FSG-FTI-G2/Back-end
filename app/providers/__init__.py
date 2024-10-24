from .memory import MemoryStateProvider
from .encryption import EncryptionProvider
from .db import DatabaseProvider
from .minio import MinioProvider
from .embedding import VectorEmbedder
from .vector_db import QdrantProvider
from .LLM import LLMProvider

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
vector_db = QdrantProvider()
llm = LLMProvider()
