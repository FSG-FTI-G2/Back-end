import os
from app.controllers.extraction_controller import extraction_vector, qdrant_client

folder_path = 'P:\\FA24\\Dev\\Back-end\\text_for_test_vectordb'

query = "What events happen in 1788 to 1789 of 18th century?"

def add_document_extraction_to_vectordb(folder_path):
    for file in os.listdir(folder_path):
        file_path  = os.path.join(folder_path, file)
        file_schema, text, summary = extraction_vector(file_path)

        qdrant_client.add_vectors(file_schema, text, summary)
        
    results = qdrant_client.search_vector(input_text=query, with_payload=True, limit=3)
    return results

results = add_document_extraction_to_vectordb(folder_path)
for result in results:
    print(f"ID: {result.id}")
    print(f"Score: {result.score}")
    print("Payload:")
    for key, value in result.payload.items():
        print(f"  {key}: {value}")
    print("\n" + "-" * 40 + "\n") 
            
