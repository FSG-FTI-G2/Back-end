from qdrant_client import QdrantClient
import os

qdrant_client = QdrantClient(
    url=os.environ.get("QDRANT_HOST", "http://localhost:6333"),  
    port=int(os.environ.get("QDRANT_PORT", 6333)), 
)

# # Ví dụ: Tạo một collection
collection_name = os.environ.get("QDRANT_COLLECTION", "test_Qdrants_3")