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
        # Initialize the QdrantProvider with a specific collection name
        self.collection_name = collection_name

    def create_collection(self, vector_size=VECTOR_SIZE, distance: Literal["cosine", "dot"] = DISTANCE):
        # Check if the collection already exists
        collections = qdrant_client.get_collections()
        if self.collection_name in [col.name for col in collections.collections]:
            print(f"Collection '{self.collection_name}' already exists.")
            return

        # Create a new collection with the specified vector size and distance metric
        qdrant_client.create_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(
                size=vector_size,
                distance=models.Distance[distance.upper()]
            )
        )
        print(f"Collection '{self.collection_name}' created successfully.")

    def list_collections(self):
        # List all existing collections in the Qdrant database
        collections = qdrant_client.get_collections()
        return [col.name for col in collections.collections]

    def drop_collection(self):
        # Drop (delete) the specified collection from Qdrant
        qdrant_client.delete_collection(self.collection_name)
        print(f"Collection '{self.collection_name}' dropped successfully.")
    
    def add_vectors(self, input_text, payloads: list[dict]):
        # Generate the vector embedding for the input text
        vector = vector_embedding(input_text)

        # Create a unique ID for the vector point and store it in Qdrant with its payload
        point = PointStruct(
            id=str(uuid.uuid4()),  # Generate a unique ID
            vector=vector,  # Vector embedding of the input text
            payload=payloads  # Associated metadata or payload
        )
        
        # Upsert the vector into the Qdrant collection
        qdrant_client.upsert(collection_name=self.collection_name, points=[point])
        print(f"Vectors added successfully to collection '{self.collection_name}'.")

    def search_vector(self, input_text: str, limit=3, with_payload=True):
        # Search for similar vectors based on the input text
        query_vector = vector_embedding(input_text)
        
        # Perform the search query in Qdrant with the provided parameters
        search_result = qdrant_client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit,  # Limit the number of search results
            with_payload=with_payload,  # Whether to include payload in results,
        )
        return search_result

    def update_vector(self, point_id, vector, payload=None):
        # Update an existing vector in Qdrant by its point ID
        point_struct = models.PointStruct(id=point_id, vector=vector, payload=payload)
        qdrant_client.upsert(
            collection_name=self.collection_name,
            points=[point_struct]
        )
        print(f"Vector with ID '{point_id}' updated successfully.")

    def delete_vector_by_id(self, point_id):
        # Delete a specific vector from the collection by its ID
        qdrant_client.delete_points(
            collection_name=self.collection_name,
            point_ids=[point_id]
        )
        print(f"Vector with ID '{point_id}' deleted successfully.")
        
    def delete_all_vectors(self):
        # Delete all vectors from the collection by deleting the collection itself
        qdrant_client.delete_collection(self.collection_name)
        
        # Recreate the collection after deletion to keep it available
        self.create_collection()
        
        print(f"All vectors in collection '{self.collection_name}' have been deleted.")

    def get_all_vectors(self):
        # Retrieve all vectors from the collection by scrolling through all data
        all_points = []
        has_more = True
        offset = None

        while has_more:
            points, next_offset = qdrant_client.scroll(
                collection_name=self.collection_name,
                offset=offset,  # Start from the current offset
                limit=100  # Retrieve 100 vectors at a time (adjustable)
            )

            all_points.extend(points)  # Append the points to the list
            offset = next_offset  # Update the offset for the next scroll

            if next_offset is None:
                has_more = False  # Stop when no more points are available

        return all_points

    def get_vector_by_id(self, point_id):
        # Retrieve a specific vector from the collection by its point ID
        point = qdrant_client.retrieve(
            collection_name=self.collection_name,
            ids=[point_id]
        )
        return point
