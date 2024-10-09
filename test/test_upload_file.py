import unittest
import sys
import logging
from io import BytesIO
from fastapi.testclient import TestClient
from main import app
from app.models.file import FileSchema, FileStatus


logger = logging.getLogger(__name__)
logger.level = logging.DEBUG
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)


class TestUploadFile(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestUploadFile, self).__init__(*args, **kwargs)

        # Define routes
        self.login_route = "/api/v1/auth/login"
        self.upload_route = "/api/v1/files/"

        self.client = TestClient(app)

        # Request login to get token
        response = self.client.post(self.login_route, data={
            "username": "admin",
            "password": "admin1111",
        }).json()
        token = response.get("data", {}).get("token")
        self.client.headers.update({"Authorization": f"Bearer {token}"})

        # Create file data
        self.valid_file = ("test.pdf", BytesIO(
            b"Test content for a PDF file"), "application/pdf")
        self.invalid_file = ("test.exe", BytesIO(
            b"Test content for an EXE file"), "application/octet-stream")
        self.large_file = ("large_file.pdf", BytesIO(
            b"Test content for a large PDF file" * 100000), "application/pdf")

    def __upload_files(self):
        response = self.client.post(
            self.upload_route, files={"files": self.valid_file}).json()
        self.assertEqual(response.get("code"), 200)
        response = self.client.post(
            self.upload_route, files={"files": self.invalid_file}).json()
        self.assertEqual(response.get("code"), 200)
        response = self.client.post(
            self.upload_route, files={"files": self.large_file}).json()
        self.assertEqual(response.get("code"), 200)

    # TODO: Update WebSocket test later
    def __view_upload_progress(self):
        with self.client.websocket_connect("/ws") as ws:
            while True:
                status = ws.receive_json()
                logger.debug(f"Received status: {status}")
                # Check for is_complete value
                if status.get("data", {}).get("is_completed"):
                    break

    def test_upload_files(self):
        self.__upload_files()

        # Check file status. This Id is hardcoded because we know the user id
        files = FileSchema.find_by_user_id("66fd11f320f63c42f143f0c4", 10, 0)
        self.assertEqual(len(files), 2)
        for file in files:
            self.assertEqual(file.status, FileStatus.SUCCESS)
