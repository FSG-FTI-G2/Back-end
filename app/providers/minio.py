from typing import List
from io import BytesIO
from minio.error import S3Error
from app.configs.minIO import minio_client
from app.utils.logger import get_logger


logger = get_logger("MINIO", color=93)


class MinioProvider:
    def __init__(self, bucket_name: str) -> None:
        self.bucket_name = bucket_name
        # Create the bucket if it does not exist
        if not minio_client.bucket_exists(bucket_name):
            self.__create_bucket(bucket_name)

    def __create_bucket(self, bucket_name: str) -> None:
        return minio_client.make_bucket(
            bucket_name=bucket_name,
        )

    def __file_exist(self, object_name: str) -> bool:
        try:
            minio_client.stat_object(self.bucket_name, object_name)
            return True
        except S3Error as e:
            if e.code == "NoSuchKey":
                return False
            else:
                raise

    def upload_file(self, object_name: str, file_data: BytesIO) -> str:
        # Upload the BytesIO data as an object
        result = minio_client.put_object(
            bucket_name=self.bucket_name,
            object_name=object_name,
            data=file_data,
            length=file_data.getbuffer().nbytes
        )
        logger(f"File uploaded `{self.bucket_name}/{object_name}`")
        return result.version_id

    def list_files(self) -> List[str]:
        objects = minio_client.list_objects(self.bucket_name, recursive=True)
        return [obj.object_name for obj in objects]

    def download_file(self, object_name: str) -> BytesIO:
        if not self.__file_exist(object_name):
            return None
        response = minio_client.get_object(
            bucket_name=self.bucket_name,
            object_name=object_name,
        )
        logger(f"File downloaded `{self.bucket_name}/{object_name}`")
        return BytesIO(response.read())

    def delete_file(self, object_name: str) -> None:
        minio_client.remove_object(
            bucket_name=self.bucket_name,
            object_name=object_name
        )
        logger(f"File deleted `{self.bucket_name}/{object_name}`")
