
import unittest
from unittest.mock import patch, MagicMock
from minio.error import S3Error
import sys
import os
sys.path.append(os.path.abspath("F:\Work\SCRUM-33\Back-end\\app\providers"))
from minIO_client import Minio_Client
from io import BytesIO


class MinioTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(MinioTestCase, self).__init__(*args, **kwargs)
        self.client = Minio_Client(
            endpoint="127.0.0.1:9000",
            access_key="GJxPwzg8PR7sNqQ7QaWn",
            secret_key="NHylF24DcBtXSHUDmQxy5Bmrl34RKIRMcXQhwOgm",
            secure=False
        )
        self.test_bucket = "test"
        self.test_file_name = "test.txt"
        self.test_file_content = b"Hello, this is a test file."

    def __create_bucket(self):
        self.client.create_bucket(self.test_bucket, 
                                  region="us-east-1")
        bucket_exists = self.client.bucket_exists(self.test_bucket)
        self.assertTrue(bucket_exists)
        return self.test_bucket

    def __check_bucket_exists(self):
        exists = self.client.bucket_exists(self.test_bucket)
        self.assertTrue(exists)

    def __list_buckets(self):
        buckets = self.client.list_bucket()
        self.assertIn(self.test_bucket, buckets)

    def __upload_file(self):
        file_data = BytesIO(self.test_file_content)
        self.client.upload_file(self.test_bucket, self.test_file_name, file_data)

    def __list_files_in_bucket(self):
        files = self.client.list_files(self.test_bucket)
        self.assertIn(self.test_file_name, files)

    def __download_file(self):
        download_path = "F:\Download\DUma\\" + self.test_file_name
        self.client.download_file(self.test_bucket, self.test_file_name, download_path)
        with open(download_path, 'rb') as f:
            content = f.read()
            self.assertEqual(content, self.test_file_content)

    def __delete_file(self):
        self.client.delete_file(self.test_bucket, self.test_file_name)
        files = self.client.list_files(self.test_bucket)
        self.assertNotIn(self.test_file_name, files)

    def __download_bucket(self):
        download_path = "F:\Download\DUma"
        self.client.download_bucket(self.test_bucket, download_path)

    def __delete_bucket(self):
        self.client.delete_bucket(self.test_bucket)
        bucket_exists = self.client.bucket_exists(self.test_bucket)
        self.assertFalse(bucket_exists)

    def test_minio_operations(self):
        self.__create_bucket()
        self.__check_bucket_exists()
        self.__list_buckets()
        self.__upload_file()
        self.__list_files_in_bucket()
        self.__download_file()
        self.__download_bucket()
        self.__delete_file()
        self.__delete_bucket()

if __name__ == '__main__':
    unittest.main()