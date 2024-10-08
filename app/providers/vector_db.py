from typing import Literal
from qdrant_client.http import models
from qdrant_client.http.models import PointStruct
from app.utils.text_processing_utils import vector_embedding, chunk_text
import uuid
from app.configs.qdrant_vector_db import qdrant_client

VECTOR_SIZE = 768
DISTANCE = "cosine"

class QdrantProvider:
    def __init__(self, collection_name):
        self.collection_name = collection_name

    def create_collection(self, vector_size=VECTOR_SIZE, distance: Literal["cosine", "dot"] = DISTANCE):
        collections = qdrant_client.get_collections()
        if self.collection_name in [col.name for col in collections.collections]:
            print(f"Collection '{self.collection_name}' already exists.")
            return

        qdrant_client.create_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(
                size=vector_size,
                distance=models.Distance[distance.upper()]
            )
        )
        print(f"Collection '{self.collection_name}' created successfully.")

    def list_collections(self):
        collections = qdrant_client.get_collections()
        return [col.name for col in collections.collections]

    def drop_collection(self):
        qdrant_client.delete_collection(self.collection_name)
        print(f"Collection '{self.collection_name}' dropped successfully.")
    
    def add_vectors(self, input_text, payloads: list[dict] ):
        chunks = chunk_text(input_text)
        points = []
        
        for chunk in chunks:
            vector = vector_embedding(chunk)
        
            point = PointStruct(
                id=str(uuid.uuid4()),  
                vector=vector,  
                payload=payloads  
            )
            points.append(point)
            
        qdrant_client.upsert(collection_name=self.collection_name, points=points)
        print(f"Vectors added successfully to collection '{self.collection_name}'.")

    def search_vector(self, input_text: str, limit=3, with_payload=True):
        query_vector = vector_embedding(input_text)
        
        search_result = qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit,
            with_payload=with_payload
        )
        return search_result

    def update_vector(self, point_id, vector, payload=None):
        point_struct = models.PointStruct(id=point_id, vector=vector, payload=payload)
        qdrant_client.upsert(
            collection_name=self.collection_name,
            points=[point_struct]
        )
        print(f"Vector with ID '{point_id}' updated successfully.")

    def delete_vector(self, point_id):
        qdrant_client.delete_points(
            collection_name=self.collection_name,
            point_ids=[point_id]
        )
        print(f"Vector with ID '{point_id}' deleted successfully.")

    def get_all_vectors(self):
        points, _ = qdrant_client.scroll(collection_name=self.collection_name)
        return points

    def get_vector_by_id(self, point_id):
        point = qdrant_client.retrieve(
            collection_name=self.collection_name,
            ids=[point_id]
        )
        return point
