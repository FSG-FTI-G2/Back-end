import os
from minio import Minio

minio_client = Minio(
    endpoint=f"{os.environ.get('MINIO_HOST', 'localhost')}:{os.environ.get('MINIO_PORT', 9000)}",
    access_key=os.environ.get("MINIO_ACCESS_KEY", "dummysecret"),
    secret_key=os.environ.get("MINIO_SECRET_KEY", "dummysecret"),
    secure=False
)
