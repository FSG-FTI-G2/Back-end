import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.providers.vector_db import QdrantProvider

collection_name = 'Qdrants_Vector_Database'

def test_qdrant():
    collection_name = 'Qdrants_Vector_Database'
    qdrant = QdrantProvider(collection_name)

    qdrant.create_collection()

    vectors = [
        [0.05, 0.61, 0.76, 0.74],
        [0.19, 0.81, 0.75, 0.11],
        [0.36, 0.55, 0.47, 0.94],
        [0.18, 0.01, 0.85, 0.80],
        [0.24, 0.18, 0.22, 0.44],
        [0.35, 0.08, 0.11, 0.44]
    ]
    payloads = [
        {"city": "Berlin"},
        {"city": "London"},
        {"city": "Moscow"},
        {"city": "New York"},
        {"city": "Beijing"},
        {"city": "Mumbai"}
    ]
    qdrant.add_vectors(vectors=vectors, payloads=payloads)

    query_vector = [0.05, 0.61, 0.76, 0.74]
    search_result = qdrant.search_vector(query_vector=query_vector, limit=3, with_payload=True)
    print("Search results:", search_result)

    collections = qdrant.list_collections()
    print("Current collections:", collections)
    
test_qdrant()