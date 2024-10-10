import unittest
from fastapi.testclient import TestClient
from main import app

class TestFileEndpoints(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    
    def test_download_file(self):
        # Make sure this file exists at the expected location
        response = self.client.get("/api/v1/serve/download/plot_exp.png")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "File plot_exp.png downloaded."})
