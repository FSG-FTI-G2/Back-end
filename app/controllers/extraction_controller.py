from app.models.file import FileSchema
from app.providers import qdrant_client
def extraction_features(text:str, file_schema: FileSchema):

    payloads = {
        "id": file_schema.id,  
        "user_id": file_schema.user_id,
        "file_name": file_schema.file_name,
        "file_type": file_schema.type,
        "file_path": file_schema.file_path,
        "summary": " ",  
    }
    
    qdrant_client.add_vectors(text, payloads)

