import unittest
import os
from fastapi.testclient import TestClient
from main import app
import shutil

class TestUploadFile(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

        self.upload_directory = os.path.join(os.path.dirname(__file__), "../upload_files")
        os.makedirs(self.upload_directory, exist_ok=True)

        self.valid_file_path = os.path.join(self.upload_directory, "test_image.jpg")
        self.invalid_file_path = os.path.join(self.upload_directory, "test_document.txt")
        

        if not os.path.exists(self.valid_file_path):
            with open(self.valid_file_path, "wb") as f:
                f.write(b"test image content" * 1024) 
        

        if not os.path.exists(self.invalid_file_path):
            with open(self.invalid_file_path, "w") as f:
                f.write("test document content")  


        self.large_file_path = os.path.join(self.upload_directory, "large_file.pdf")
        with open(self.large_file_path, "wb") as f:
            f.write(b"x" * (21 * 1024 * 1024))  

    def tearDown(self):
        if os.path.exists(self.upload_directory):
            shutil.rmtree(self.upload_directory)

    def test_upload_valid_file(self):
        with open(self.valid_file_path, "rb") as f:
            response = self.client.post("/api/v1/upload/", files={"file": f})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"message": "File uploaded successfully"})

    def test_upload_invalid_extension(self):
        with open(self.invalid_file_path, "rb") as f:
            response = self.client.post("/api/v1/upload/", files={"file": f})
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json(), {"detail": "File extension not allowed"})

    def test_upload_large_file(self):
        with open(self.large_file_path, "rb") as f:
            response = self.client.post("/api/v1/upload/", files={"file": f})
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json(), {"detail": "File exceeds 20MB size limit"})

if __name__ == "__main__":
    unittest.main()
