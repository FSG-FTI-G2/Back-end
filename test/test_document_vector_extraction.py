import os
from qdrant_client.http.models import PointStruct
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
import sys
import unittest
model = SentenceTransformer('all-mpnet-base-v2')

sys.path.insert(0,"P:\\FA24\\Dev\\Back-end\\app\\controllers")
from Document_Vector_Extraction import TextProcessor

qdrant_collection_name = 'Qdrants_Vector_Database_hihi'
database_name = "Database_hihi"
folder_path = 'P:\\FA24\\Dev\\Back-end\\text'

model = SentenceTransformer('all-mpnet-base-v2')

payloads = []
   
input_text = "When I first visit Nha Trang"

class Vector_Extraction(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(Vector_Extraction, self).__init__(*args, **kwargs)
        self.text_processor = TextProcessor(database_name, qdrant_collection_name, folder_path)
    
    def test_search_vectors(self):
        self.text_processor.process_all_files()
        
        search_result = self.text_processor.search_vectors(input_text)
        
        for hit in search_result:
            print(f"ID: {hit.id}, Score: {hit.score}, Payload: {hit.payload}")
            
            self.assertEqual(hit.payload['file_name'], 'sample_test_file')