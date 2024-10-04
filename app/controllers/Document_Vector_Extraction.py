import sys
import os
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-mpnet-base-v2')

sys.path.insert(0,"P:\\FA24\\Dev\\Back-end\\app\\providers")
from vector_db import QdrantProvider
from mongodb import client

class TextProcessor:
    def __init__(self, db_name: str, collection_name: str, folder_path: str):
        self.folder_path = folder_path
        self.qdrant_client = QdrantProvider(collection_name)
        self.qdrant_client.create_collection()
        self.mongo_db = client[db_name]
        self.db = self.mongo_db[db_name]
        self.model = SentenceTransformer('all-mpnet-base-v2')

    def summarize_text(self, text: str, num_sentences: int = 3) -> str:
        sentences = sent_tokenize(text)
        summary = ' '.join(sentences[:num_sentences])
        return summary

    def process_file(self, file_path: str):
        file_name = os.path.basename(file_path).split('.')[0]
        file_type = os.path.splitext(file_path)[-1][1:]

        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        unique_id = str(self.db.insert_one({"text": text}).inserted_id)
        summary = self.summarize_text(text)

        return file_name, file_type, unique_id, text, summary

    def process_all_files(self):
        for file in os.listdir(self.folder_path):
            file_path = os.path.join(self.folder_path, file)
            file_name, file_type, unique_id, text, summary = self.process_file(file_path)
            self.qdrant_client.add_vectors(unique_id=unique_id, input_text=text, file_name=file_name, file_type=file_type)

    def search_vectors(self, input_text: str, limit: int = 3):
        search_result = self.qdrant_client.search_vector(input_text, limit=limit, with_payload=True)
        return search_result



