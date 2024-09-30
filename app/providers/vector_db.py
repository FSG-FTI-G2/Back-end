import sys
import os
import requests
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json

class QdrantProvider:
    def __init__(self, host='http://localhost:6333'):
        self.host = host

    def create_collection(self, collection_name):
        url = f"{self.host}/collections/{collection_name}"
        response = requests.get(url)

        if response.status_code == 200:
            print(f"Collection '{collection_name}' already exists.")
            return response.json()
        else:
            payload = {
                "vectors": {
                    
                        "size": 4,  # Use "size" instead of "vector_size"
                        "distance": "Cosine"  # Use "Cosine" as a distance metric
                    
                }
            }
            response = requests.put(url, json=payload)

            if response.status_code == 200 or response.status_code == 201:
                print(f"Collection '{collection_name}' created successfully.")
                return response.json()
            else:
                print(f"Error creating collection: {response.status_code} - {response.text}")
                return None

    def add_vector(self, collection_name, vector, payload, point_id=None):
        url = f"{self.host}/collections/{collection_name}/points"
        points = []
        
        for i, vector in enumerate(vector):
            point = {
                "id": i + 1,  # Unique ID for each vector
                "vector": vector,
                "payload": payload[i]
            }
            points.append(point)

        data = {"points": points}
        response = requests.put(url, json=data)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error adding vector: {response.status_code} - {response.text}")
            return None
        
    def drop_collection(self, collection_name):
        url = f"{self.host}/collections/{collection_name}"
        response = requests.delete(url)
        if response.status_code == 204:
            print(f"Collection '{collection_name}' dropped successfully.")
        else:
            print(f"Failed to drop collection: {response.status_code} - {response.text}")


    def search_vector(self, collection_name, query_vector, limit=3, with_payload=False):
        url = f"{self.host}/collections/{collection_name}/points/search"
        payload = {
            "vector": query_vector,
            "limit": limit,
            "with_payload": with_payload
        }
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error during search: {response.status_code} - {response.text}")
            return None

    def list_collections(self):
        url = f"{self.host}/collections"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching collections: {response.status_code} - {response.text}")
            return None

    def drop_collection(self, collection_name):
        url = f"{self.host}/collections/{collection_name}"
        response = requests.delete(url)
        if response.status_code == 200:  # Check if the status indicates success
            print(f"Collection '{collection_name}' dropped successfully.")
        else:
            print(f"Failed to drop collection: {response.status_code} - {response.text}")

    def update_vector(self, collection_name, point_id, vector, payload):
        url = f"{self.host}/collections/{collection_name}/points/{point_id}"
        data = {
            "vector": vector,
            "payload": payload
        }
        response = requests.put(url, json=data)
        return response.json()

    def delete_vector(self, collection_name, point_id):
        url = f"{self.host}/collections/{collection_name}/points/{point_id}"
        response = requests.delete(url)
        return response.json()

    def get_all_vectors(self, collection_name):
        url = f"{self.host}/collections/{collection_name}/points"
        response = requests.get(url)
        return response.json()

    def get_vector_by_id(self, collection_name, point_id):
        url = f"{self.host}/collections/{collection_name}/points/{point_id}"
        response = requests.get(url)
        return response.json()
