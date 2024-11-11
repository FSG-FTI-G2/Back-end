import unittest
from app.providers.vectordb_provider import QdrantProvider

qdrant_collection_name = 'Qdrants_Vector_Database'
class Qdrant_Test_Case(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(Qdrant_Test_Case, self).__init__(*args, **kwargs)
        self.qdrant = QdrantProvider(qdrant_collection_name)

    def test_qdrant(self):
        self.qdrant.create_collection()
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
        self.qdrant.add_vectors(vectors=vectors, payloads=payloads)

        query_vector = [0.05, 0.61, 0.76, 0.74]
        search_result = self.qdrant.search_vector(query_vector=query_vector, limit=3, with_payload=True)
        
        highest_score_point = max(search_result, key=lambda point: point.score)
        
        self.assertEqual(highest_score_point.payload['city'], 'Berlin')
    
