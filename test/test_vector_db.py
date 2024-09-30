import sys
import os
sys.path.append("P:\FA24\Dev\Back-end\\app\providers")
from app.providers.vector_db import QdrantProvider

collection_name = 'Qdrants_Test'
qdrant = QdrantProvider()

create_response = qdrant.create_collection(collection_name=collection_name)

if create_response:
    print("Collection created successfully:", create_response)
    print('-'*100)
else:
    print("Failed to create collection.")


vector = [
    [0.05, 0.61, 0.76, 0.74],
    [0.19, 0.81, 0.75, 0.11],
    [0.36, 0.55, 0.47, 0.94],
    [0.18, 0.01, 0.85, 0.80],
    [0.24, 0.18, 0.22, 0.44],
    [0.35, 0.08, 0.11, 0.44]
]

payload = [
    {"city": "Berlin"},
    {"city": "London"},
    {"city": "Moscow"},
    {"city": "New York"},
    {"city": "Beijing"},
    {"city": "Mumbai"}
]

operation_info = qdrant.add_vector(collection_name=collection_name, vector=vector, payload=payload)

query_vector  = [0.05, 0.61, 0.76, 0.74]   
top_k = 2  
search_response = qdrant.search_vector(collection_name, query_vector=query_vector , limit=3, with_payload=True)

if search_response:
    print("Search results:", search_response)
else:
    print("Failed to search for similar vector.")



# collections = qdrant.list_collections()
# print("Current collections:", collections)

