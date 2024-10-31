from qdrant_client import QdrantClient
import os

qdrant_client = QdrantClient(
    url=os.environ.get("QDRANT_HOST", "http://localhost:6333"),  
    port=int(os.environ.get("QDRANT_PORT", 6333)), 
)

