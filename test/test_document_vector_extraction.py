import os
from app.models.file import FileSchema
from app.providers import qdrant_client
import unittest
from app.controllers.extraction_controller import extraction_features

folder_path = 'P:\\FA24\\Dev\\Back-end\\text_for_test_vectordb'

class Add_Document_Extraction_To_Vectordb(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(Add_Document_Extraction_To_Vectordb, self).__init__(*args, **kwargs)
        self.folder_path = 'P:\\FA24\\Dev\\Back-end\\text_for_test_vectordb'
        
    def add_document_extraction_to_vectordb(folder_path):
        for file in os.listdir(folder_path):
            file_path  = os.path.join(folder_path, file)
            file_name = os.path.basename(file_path).split('.')[0]
            file_type = os.path.splitext(file_path)[-1][1:]  

            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                
            file_schema = FileSchema(
            user_id="user_id",  
            type=file_type,
            file_name=file_name,
            file_path=file_path,
        )

            file_schema.create() 
            
            extraction_features(text, file_schema)