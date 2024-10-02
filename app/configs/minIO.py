import sys
import os
sys.path.append(os.path.abspath("F:\Work\SCRUM-33\Back-end\\app\providers"))
from minIO_client import Minio_Client
from io import BytesIO

if __name__ == "__main__":
    minio_client = Minio_Client(
        endpoint=os.environ.get("ENDPOINT", "127.0.0.1:9000"),
        access_key=os.environ.get("ACCESS_KEY", "GJxPwzg8PR7sNqQ7QaWn"),
        secret_key=os.environ.get("SECRET_KEY","NHylF24DcBtXSHUDmQxy5Bmrl34RKIRMcXQhwOgm"),
        secure=False 
    )
