import os
from app.providers import file_storage

def retrieve_file(input_file: str, file_path: str):
    """
    Check if the file exists in the temp directory. If not, download it from MinIO.
    """
    if not os.path.exists(file_path):
        file = file_storage.download_file(input_file)
        with open(file_path, "wb") as f:
            f.write(file.read())
        return file
    else:
        print(f"File {input_file} already exists in the temp directory.")
        return input_file