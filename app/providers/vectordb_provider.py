import uuid
from qdrant_client.http import models
from app.configs.qdrant_config import qdrant_client
from app.utils.logger import get_logger

DEFAULT_VECTOR_SIZE = 768
DEFAULT_DISTANCE = "cosine"


logger = get_logger("QDRANT", color=91)


class QdrantProvider:
    def __init__(self):
        # Initialize the QdrantProvider with a specific collection name
        self.vector_size = DEFAULT_VECTOR_SIZE
        self.distance = DEFAULT_DISTANCE

    def create_collection(self, collection_name: str):
        # Check if the collection already exists
        if collection_name in self.list_collections():
            logger(f"Collection `{collection_name}` already exists.")
            return

        # Create a new collection with the specified vector size and distance metric
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=self.vector_size,
                distance=models.Distance[self.distance.upper()]
            )
        )
        logger(f"Collection created `{collection_name}`")

    def list_collections(self):
        # List all existing collections in the Qdrant database
        collections = qdrant_client.get_collections()
        return [col.name for col in collections.collections]

    def drop_collection(self, collection_name: str):
        # Drop (delete) the specified collection from Qdrant
        qdrant_client.delete_collection(collection_name)
        logger(f"Collection dropped `{collection_name}`")

    def add_vectors(self, collection_name: str, vectors: list[list[float]], payloads: list[dict]):
        # Create a unique ID for the vector point and store it in Qdrant with its payload
        points = []
        for i, vector in enumerate(vectors):
            point = models.PointStruct(
                id=str(uuid.uuid4()), vector=vector, payload=payloads[i])
            points.append(point)

        # Upsert the vector into the Qdrant collection
        qdrant_client.upsert(
            collection_name=collection_name, points=points)
        logger(f"Vector added `{collection_name}`")

    def search_vector(self, collection_name: str, vector: list[float], limit=3, with_payload=True):
        # Perform the search query in Qdrant with the provided parameters
        search_result = qdrant_client.search(
            collection_name=collection_name,
            query_vector=vector,
            limit=limit,  # Limit the number of search results
            with_payload=with_payload,  # Whether to include payload in results,
        )
        logger(f"Vector searched `{collection_name}`")
        return search_result

    def get_all_vectors(self, collection_name: str):
        # Retrieve all vectors from the collection by scrolling through all data
        all_points = []
        has_more = True
        offset = None

        while has_more:
            points, next_offset = qdrant_client.scroll(
                collection_name=collection_name,
                offset=offset,  # Start from the current offset
                limit=100  # Retrieve 100 vectors at a time (adjustable)
            )

            all_points.extend(points)  # Append the points to the list
            offset = next_offset  # Update the offset for the next scroll

            if next_offset is None:
                has_more = False  # Stop when no more points are available

        logger(f"All vectors retrieved `{collection_name}`")
        return all_points

    def get_vector_by_id(self, collection_name: str, point_id: str):
        # Retrieve a specific vector from the collection by its point ID
        point = qdrant_client.retrieve(
            collection_name=collection_name,
            ids=[point_id]
        )
        logger(f"Vector retrieved `{collection_name}:{point_id}`")
        return point

    def get_vectors_by_filter(self, collection_name: str, key: str, value: str):
        # Retrieve a specific vector from the collection by its file ID
        point = qdrant_client.scroll(
            collection_name=collection_name,
            scroll_filter=models.Filter(
                must=[models.FieldCondition(
                    key=key,
                    match=models.Match(value=value)
                )]
            )
        )[0]
        logger(f"Vector retrieved `{collection_name}:{key}:{value}`")
        return point

    def update_vector(self, collection_name: str, point_id: str, vector: list[float], payload=None):
        # Update an existing vector in Qdrant by its point ID
        point_struct = models.PointStruct(
            id=point_id, vector=vector, payload=payload)
        qdrant_client.upsert(
            collection_name=collection_name,
            points=[point_struct]
        )
        logger(f"Vector updated `{collection_name}:{point_id}`")

    def delete_all_vectors(self, collection_name: str):
        # Delete all vectors from the collection by deleting the collection itself
        qdrant_client.delete_collection(collection_name)

        # Recreate the collection after deletion to keep it available
        self.create_collection(collection_name)
        logger("All vectors deleted successfully.")

    def delete_vector_by_id(self, collection_name: str, point_id: str):
        # Delete a specific vector from the collection by its ID
        qdrant_client.delete(
            collection_name=collection_name,
            points_selector=[point_id]
        )
        logger(f"Vector deleted `{collection_name}:{point_id}`")

    def delete_vectors_by_filter(self, collection_name: str, key: str, value: str):
        # Delete a specific vector from the collection by its file ID
        qdrant_client.delete(
            collection_name=collection_name,
            points_selector=models.Filter(
                must=[models.FieldCondition(
                    key=key,
                    match=models.MatchValue(value=value)
                )]
            )
        )
        logger(f"Vector deleted `{collection_name}:{key}:{value}`")
