import unittest
import sys
import logging
from io import BytesIO
from fastapi.testclient import TestClient
from main import app
from app.models.file import FileType, FileStatus


logger = logging.getLogger(__name__)
logger.level = logging.DEBUG
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)


class TestUploadFile(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestUploadFile, self).__init__(*args, **kwargs)

        # Define routes
        self.login_route = "/api/v1/auth/login"
        self.files_route = "/api/v1/files/"

        self.client = TestClient(app)

        # Request login to get token
        response = self.client.post(self.login_route, data={
            "username": "test",
            "password": "test123",
        }).json()
        token = response.get("data", {}).get("token")
        self.client.headers.update({"Authorization": f"Bearer {token}"})

        # Create file data
        self.valid_file = ("test.pdf", BytesIO(
            b"Test content for a PDF file"), "application/pdf")
        self.invalid_file = ("test.exe", BytesIO(
            b"Test content for an EXE file"), "application/octet-stream")
        self.large_file = ("large_file.docx", BytesIO(
            b"Test content for a large PDF file" * 100000), "application/pdf")

    def __upload_files(self):
        response = self.client.post(
            self.files_route, files=[
                ("files", self.valid_file),
                ("files", self.invalid_file),
                ("files", self.large_file),
            ]).json()
        self.assertEqual(response.get("code"), 200)
        return response.get("data", {}).get("progress_id")

    # TODO: Update WebSocket test later
    def __view_upload_progress(self, progress_id: str):
        with self.client.websocket_connect(self.files_route + progress_id) as ws:
            while True:
                status = ws.receive_json()
                logger.debug(f"Received status: {status}")
                # Check for is_complete value
                if status.get("data", {}).get("is_completed"):
                    break

    def __read_filtered_files(self):
        params = {
            "page_size": 10,
            "page_index": 0,
            "search": "test",
            "file_type": FileType.PDF.value,
            "status": FileStatus.SUCCESS.value
        }
        response = self.client.get(self.files_route, params=params).json()
        self.assertEqual(response.get("code"), 200)
        self.assertEqual(response.get("data", {}).get("total_pages"), 0)
        files = response.get("data", {}).get("files")
        self.assertEqual(len(files), 1)

    def __delete_files(self):
        files = self.client.get(self.files_route).json().get(
            "data", {}).get("files")
        for file in files:
            response = self.client.delete(
                self.files_route + file.get("id")).json()
            self.assertEqual(response.get("code"), 200)

    def test_files_apis(self):
        progress_id = self.__upload_files()
        self.__view_upload_progress(progress_id)
        self.__read_filtered_files()
        self.__delete_files()
