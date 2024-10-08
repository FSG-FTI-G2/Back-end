import os
from app.providers.minIO_client import Minio_Client
from io import BytesIO

if __name__ == "__main__":
    minio_client = Minio_Client(
        endpoint=os.environ.get("ENDPOINT", "127.0.0.1:9000"),
        access_key=os.environ.get("ACCESS_KEY"),
        secret_key=os.environ.get("SECRET_KEY"),
        secure=False 
    )
