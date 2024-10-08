import os
from app.providers.text_processing_utils import summarize_text
from app.models.file import FileSchema
from app.providers.vector_db import QdrantProvider

qdrant_collection_name = 'Qdrants_Vector_Database'

qdrant_client = QdrantProvider(qdrant_collection_name)
qdrant_client.create_collection()

def extraction_vector(file_path):
    file_name = os.path.basename(file_path).split('.')[0]
    file_type = os.path.splitext(file_path)[-1][1:]  

    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        
    summary = summarize_text(text)

    file_schema = FileSchema(
        user_id="user_id",  
        type=file_type,
        file_name=file_name,
        file_path=file_path,
    )

    file_schema.create()  

    return file_schema, text, summary

