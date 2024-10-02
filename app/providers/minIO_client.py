from typing import Any, Generator, List
from minio import Minio
from minio_act.bucket import Bucket
from minio_act.log import logger
from minio.error import S3Error
from io import BytesIO
import os

class Minio_Client:

    def __init__(self,
                 endpoint: str,
                 access_key: Any = None,
                 secret_key: Any = None,
                 session_token: Any =None,
                 secure: bool = True,
                 region: Any = None,
                 http_client: Any = None,
                 credentials: Any = None,
                 *args, **kwargs ):
        self.endpoint = endpoint
        self.access_key = access_key
        self.secret_key = secret_key
        self.session_token = session_token
        self.secure = secure
        self.region = region
        self.http_client = http_client
        self.credentials = credentials
        self.client = self.client_connect()

    def client_connect(self):
        return Minio(
            endpoint=self.endpoint,
            access_key=self.access_key,
            secret_key=self.secret_key,
            session_token=self.session_token,
            secure=self.secure,
            region=self.region,
            http_client=self.http_client,
            credentials=self.credentials
        )
    
    def download_bucket(self, bucket_name: Any, download_path: str) -> None:
        logger.info(f"Checking if bucket {str(bucket_name)} exists before downloading...")
        if not self.client.bucket_exists(bucket_name):
            logger.warning(f"Bucket {bucket_name} does not exist. Download aborted.")
            print(f"Bucket {bucket_name} does not exist. Download aborted.")
            return
        
        logger.info(f"Downloading bucket {str(bucket_name)} to {download_path} ...")
        
        # Ensure the download path exists
        os.makedirs(download_path, exist_ok=True)
        
        try:
            for item in self.client.list_objects(bucket_name, recursive=True):
                file_path = os.path.join(download_path, item.object_name)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Create directories if needed
                self.client.fget_object(bucket_name, item.object_name, file_path)
                logger.info(f"Downloaded {item.object_name} to {file_path}.")
                print(f"Downloaded {item.object_name} to {file_path}.")
        except Exception as e:
            logger.error(f"Error downloading bucket {bucket_name}: {e}")
            print(f"Error downloading bucket {bucket_name}: {e}")

    def _download_bucket(self, bucket_name: Any) -> None:
        logger.info(f"Downloading bucket {str(bucket_name)} ...")
        for item in self.client.list_objects(bucket_name, recursive=True):
            self.client.fget_object(bucket_name, item.object_name, item.object_name)

    def bucket_exists(self, bucket_name: Any) -> bool:
        try:
            exists = self.client.bucket_exists(bucket_name)
            if exists:
                logger.info(f"Bucket {bucket_name} exists.")
                print(f"Bucket {bucket_name} exists.")
            else:
                logger.info(f"Bucket {bucket_name} does not exist.")
                print(f"Bucket {bucket_name} does not exist.")
            return exists
        except S3Error as e:
            logger.error(f"Error checking if bucket {bucket_name} exists: {e}")
            print(f"Error checking if bucket {bucket_name} exists: {e}")
            raise

    def _bucket_exists(self, bucket_name: Any) -> bool:
        logger.info(f"Checking bucket {str(bucket_name)} exists ...")
        return self.client.bucket_exists(
            bucket_name=bucket_name
        )
    
    def list_bucket(self) -> List[str]:
        logger.info("Listing buckets...")
        try:
            buckets = self.client.list_buckets()
            bucket_names = [bucket.name for bucket in buckets]

            if bucket_names:
                logger.info(f"Existing buckets: {bucket_names}")
                print(f"Existing buckets: {bucket_names}")
            else:
                logger.info("No buckets found.")
                print("No buckets found.")
            
            return bucket_names
        except S3Error as e:
            logger.error(f"Error listing buckets: {e}")
            print(f"Error listing buckets: {e}")
            raise

    def _list_bucket(self) -> List[str]:
        logger.info(f"Listing buckets ...")
        return self.client.list_buckets()
    
    def create_bucket(self, bucket_name: Any, region: Any, object_lock: bool = False) -> None:
        self._create_bucket(
            bucket_name=bucket_name,
            region=region,
            object_lock=object_lock
        )

    def _create_bucket(self, bucket_name: Any, region: Any, object_lock: bool = False) -> None:
        logger.info(f"Creating bucket {str(bucket_name)} ...")
        return self.client.make_bucket(
            bucket_name=bucket_name,
            location=region,
            object_lock=object_lock
        )
    
    def delete_bucket(self, bucket_name: Any) -> None:
        logger.info(f"Checking if bucket {str(bucket_name)} exists before deletion...")
        if not self.client.bucket_exists(bucket_name):
            logger.warning(f"Bucket {bucket_name} does not exist. Deletion aborted.")
            print(f"Bucket {bucket_name} does not exist. Deletion aborted.")
            return

        logger.info(f"Deleting bucket {str(bucket_name)} ...")
        try:
            self.client.remove_bucket(bucket_name)
            logger.info(f"Bucket {bucket_name} has been successfully deleted.")
            print(f"Bucket {bucket_name} has been successfully deleted.")
        except Exception as e:
            logger.error(f"Error deleting bucket {bucket_name}: {e}")
            print(f"Error deleting bucket {bucket_name}: {e}")
        
    def _delete_bucket(self, bucket_name: Any):
        logger.info(f"Deleting bucket {str(bucket_name)} ...")
        return self.client.remove_bucket(
            bucket_name=bucket_name
        )
    
    def delete_object(self, bucket_name: Any, object_name: Any, version_id: Any = None) -> None:
        self._delete_object(
            bucket_name=bucket_name,
            object_name=object_name,
            version_id=version_id
        )

    def _delete_object(self, bucket_name: Any, object_name: Any, version_id: Any = None) -> None:
        logger.info(f"Deleting {str(object_name)} in bucket {str(bucket_name)} ...")
        return self.client.remove_object(
            bucket_name=bucket_name,
            object_name=object_name,
            version_id=version_id
        )
    
    def delete_objects(self, bucket_name: Any, delete_object_list: List[Any], bypass_governance_mode: bool = False) -> Generator[Any, Any, None]:
        self._delete_objects(
            bucket_name=bucket_name,
            delete_object_list=delete_object_list,
            bypass_governance_mode=bypass_governance_mode
        )
    
    def _delete_objects(self, bucket_name: Any, delete_object_list: List[Any], bypass_governance_mode: bool = False) -> Generator[Any, Any, None]:
        logger.info(f"Deleting multiple objects in bucket {str(bucket_name)} ...")
        return self.client.remove_objects(
            bucket_name=bucket_name,
            delete_object_list=delete_object_list,
            bypass_governance_mode=bypass_governance_mode
        )
    
    def upload_file(self, bucket_name: str, object_name: str, file_data: BytesIO) -> None:
        logger.info(f"Uploading data to bucket {bucket_name} as {object_name}...")
        
        # Seek to the start of the BytesIO object
        file_data.seek(0)
        
        # Upload the BytesIO data as an object
        self.client.put_object(
            bucket_name=bucket_name,
            object_name=object_name,
            data=file_data,
            length=file_data.getbuffer().nbytes  # Length of the BytesIO data
        )
        
        logger.info(f"Data uploaded successfully to {bucket_name}/{object_name}.")

    def exist_file(self, bucket_name: str, object_name: str) -> bool:
        logger.info(f"Checking if file {object_name} exists in bucket {bucket_name}...")
        try:
            self.client.stat_object(bucket_name, object_name)
            logger.info(f"File {object_name} exists in bucket {bucket_name}.")
            return True
        except S3Error as e:
            if e.code == "NoSuchKey":
                logger.info(f"File {object_name} does not exist in bucket {bucket_name}.")
                return False
            else:
                logger.error(f"Error checking file existence: {e}")
                raise
    
    def list_files(self, bucket_name: str) -> List[str]:
        logger.info(f"Listing all files in bucket {bucket_name}...")
        try:
            objects = self.client.list_objects(bucket_name, recursive=True)
            file_list = [obj.object_name for obj in objects]
            logger.info(f"Files in bucket {bucket_name}: {file_list}")
            return file_list
        except Exception as e:
            logger.error(f"Error listing files in bucket {bucket_name}: {e}")
            raise

    def download_file(self, bucket_name: str, object_name: str, file_path: str) -> None:
        logger.info(f"Downloading {object_name} from bucket {bucket_name} to {file_path}...")
        self.client.fget_object(
            bucket_name=bucket_name,
            object_name=object_name,
            file_path=file_path
        )
        logger.info(f"File {object_name} downloaded successfully to {file_path}.")

    def delete_file(self, bucket_name: str, object_name: str) -> None:
        logger.info(f"Deleting file {object_name} from bucket {bucket_name}...")
        try:
            self.client.remove_object(
                bucket_name=bucket_name,
                object_name=object_name
            )
            logger.info(f"File {object_name} has been successfully deleted from bucket {bucket_name}.")
        except Exception as e:
            logger.error(f"Error deleting file {object_name} from bucket {bucket_name}: {e}")
            raise