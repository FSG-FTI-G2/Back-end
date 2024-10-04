from typing import Literal
import sys
from qdrant_client.http import models
from qdrant_client.http.models import PointStruct
from sentence_transformers import SentenceTransformer
import numpy as np
from langchain.text_splitter import RecursiveCharacterTextSplitter
import uuid

sys.path.insert(0,"P:\\FA24\\Dev\\Back-end\\app\\configs")
from qdrant_vector_db import qdrant_client


model = SentenceTransformer('all-mpnet-base-v2')

VECTOR_SIZE = 768
DISTANCE = "cosine"
CHUNK_SIZE = 500
CHUNK_OVERLAP=50

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
        
    def vector_embedding(self, text):
        return model.encode(text).tolist()
    
    def create_random_vector(self, dimensions=VECTOR_SIZE):
        return np.random.rand(dimensions).tolist()
    
    def chunk_text(self,text, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = text_splitter.split_text(text)
        return chunks
    def add_vectors(self, unique_id, input_text, file_name, file_type):
        chunks = self.chunk_text(input_text)
        
        points = []
        
        for idx, chunk in enumerate(chunks):
            vector = self.vector_embedding(chunk)
    
            metadata = {
                "id": unique_id,
                "file_name": file_name,
                "file_type": file_type,
            }
        
            point = PointStruct(
                id=str(uuid.uuid4()),  
                vector=vector,  
                payload=metadata  
            )
            
            points.append(point)
            
        qdrant_client.upsert(collection_name=self.collection_name, points=points)
        print(f"Vectors added successfully to collection '{self.collection_name}'.")

    def search_vector(self, input_text: str, limit=3, with_payload=False):
        query_vector = self.vector_embedding(input_text)
        
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
