import unittest
from fastapi.testclient import TestClient
from main import app


# TODO: Implement test cases for reading files later
class TestReadFile(unittest.TestCase):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.client = TestClient(app)

        self.route = "/api/v1/files/"
