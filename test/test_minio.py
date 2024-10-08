
import unittest
import os
from io import BytesIO
from app.providers import file_storage
from dotenv import load_dotenv

load_dotenv()


class MinioTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(MinioTestCase, self).__init__(*args, **kwargs)
        self.test_file_name = "test.txt"
        self.test_file_content = b"Hello, this is a test file."
        self.saving_path = os.path.join(os.getcwd(), "temp")
        os.makedirs(self.saving_path, exist_ok=True)

    def __upload_file(self):
        file_data = BytesIO(self.test_file_content)
        file_storage.upload_file(
            self.test_file_name, file_data)
        # Verify the file is uploaded
        files = file_storage.list_files()
        self.assertIn(self.test_file_name, files)

    def __download_file(self):
        file = file_storage.download_file(self.test_file_name)
        self.assertIsNotNone(file)
        # Save file for verification
        with open(os.path.join(self.saving_path, self.test_file_name), "wb") as f:
            f.write(file.read())
        # Verify the file content
        file.seek(0)
        content = file.read()
        self.assertEqual(content, self.test_file_content)

    def __delete_file(self):
        file_storage.delete_file(self.test_file_name)
        files = file_storage.list_files()
        self.assertNotIn(self.test_file_name, files)

    def test_minio_operations(self):
        self.__upload_file()
        self.__download_file()
        self.__delete_file()
