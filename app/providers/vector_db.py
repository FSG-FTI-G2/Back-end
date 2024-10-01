from app.configs.qdrant_vector_db import qdrant_client
from qdrant_client.http import models

VECTOR_SIZE = 4


class QdrantProvider:
    def __init__(self, collection_name):
        self.collection_name = collection_name

    def create_collection(self, vector_size=VECTOR_SIZE, distance="Cosine"):
        try:
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
        except Exception as e:
            print(f"Error creating collection: {e}")
            
    def list_collections(self):
        try:
            collections = qdrant_client.get_collections()
            return [col.name for col in collections.collections]
        except Exception as e:
            print(f"Error fetching collections: {e}")
            return None

    def drop_collection(self):
        try:
            qdrant_client.delete_collection(self.collection_name)
            print(f"Collection '{self.collection_name}' dropped successfully.")
        except Exception as e:
            print(f"Error dropping collection: {e}")

    def add_vectors(self, vectors, payloads):
        try:
            points = [
                models.PointStruct(id=i + 1, vector=vector, payload=payload)
                for i, (vector, payload) in enumerate(zip(vectors, payloads))
            ]
            qdrant_client.upsert(collection_name=self.collection_name, points=points)
            print(f"Vectors added successfully to collection '{self.collection_name}'.")
        except Exception as e:
            print(f"Error adding vectors: {e}")

    def search_vector(self, query_vector, limit=3, with_payload=False):
        try:
            search_result = qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit,
                with_payload=with_payload
            )
            return search_result
        except Exception as e:
            print(f"Error during search: {e}")
            return None

    def update_vector(self, point_id, vector, payload=None):
        try:
            point_struct = models.PointStruct(id=point_id, vector=vector, payload=payload)
            qdrant_client.upsert(
                collection_name=self.collection_name,
                points=[point_struct]
            )
            print(f"Vector with ID '{point_id}' updated successfully.")
        except Exception as e:
            print(f"Error updating vector: {e}")

    def delete_vector(self, point_id):
        try:
            qdrant_client.delete_points(
                collection_name=self.collection_name,
                point_ids=[point_id]
            )
            print(f"Vector with ID '{point_id}' deleted successfully.")
        except Exception as e:
            print(f"Error deleting vector: {e}")

    def get_all_vectors(self):
        try:
            points, _ = qdrant_client.scroll(collection_name=self.collection_name)
            return points
        except Exception as e:
            print(f"Error fetching all vectors: {e}")
            return None

    def get_vector_by_id(self, point_id):
        try:
            point = qdrant_client.retrieve(
                collection_name=self.collection_name,
                ids=[point_id]
            )
            return point
        except Exception as e:
            print(f"Error fetching vector by ID '{point_id}': {e}")
            return None