from typing import List, Any
import os
from io import BytesIO
from threading import Timer


TEMP_PATH = os.path.join(os.getcwd(), "temp")   # Path to the temp directory
# Create the temp directory if it does not exist
os.makedirs(TEMP_PATH, exist_ok=True)


def batch_splitter(data: List[Any], batch_size: int) -> List[List[Any]]:
    """
    Split a list of data into batches of a specified size.
    """
    return [data[i:i + batch_size] for i in range(0, len(data), batch_size)]


def is_temp_file_exists(file_path: str) -> bool:
    """
    Check if a file exists in the temp directory.
    """
    path = os.path.join(TEMP_PATH, file_path)
    return os.path.exists(path)


def save_temp_file(file: BytesIO, file_path: str, ttl: int = None):
    """
    Save a file to the temp directory.
    """
    path = os.path.join(TEMP_PATH, file_path)
    with open(path, "wb") as f:
        f.write(file.read())
    # If time to live is set, delete the file after the specified time
    if ttl:
        Timer(ttl, remove_temp_file, args=(file_path,)).start()


def remove_temp_file(file_path: str):
    """
    Remove a file from the temp directory.
    """
    path = os.path.join(TEMP_PATH, file_path)
    if os.path.exists(path):
        os.remove(path)
        return True
    return False
