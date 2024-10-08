import unittest
from fastapi.testclient import TestClient
from main import app
from app.models.file import FileSchema, FileStatus
from io import BytesIO

class TestUploadFile(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        
        # Tạo các tệp giả lập bằng io.BytesIO
        self.valid_file = ("test.pdf", BytesIO(b"Test content for a PDF file"), "application/pdf")
        self.invalid_file = ("test.exe", BytesIO(b"Test content for an EXE file"), "application/octet-stream")
        self.large_file = ("large_file.pdf", BytesIO(b"Test content for a large PDF file" * 100000), "application/pdf")

    def test_upload_valid_file(self):
        response = self.client.post("/api/v1/upload", files={"file": self.valid_file})
        self.assertEqual(response.status_code, 200)

        # Fetch the file from the database and check its status
        file_id = response.json()["file_id"]
        file_data = FileSchema.find_by_id(file_id)
        self.assertIsNotNone(file_data)
        self.assertEqual(file_data.status, FileStatus.SUCCESS)

    def test_upload_invalid_extension(self):
        response = self.client.post("/api/v1/upload", files={"file": self.invalid_file})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Invalid file extension."})

    def test_upload_large_file(self):
        response = self.client.post("/api/v1/upload", files={"file": self.large_file})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "File exceeds 20MB size limit."})

if __name__ == "__main__":
    unittest.main()
