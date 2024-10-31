import os
from minio import Minio

minio_client = Minio(
    endpoint=f"{os.environ.get('MINIO_HOST')}:{os.environ.get('MINIO_PORT')}",
    access_key=os.environ.get("MINIO_ACCESS_KEY"),
    secret_key=os.environ.get("MINIO_SECRET_KEY"),
    secure=False
)
