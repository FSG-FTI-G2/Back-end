import unittest
from fastapi.testclient import TestClient
from main import app 
from app.models.user import UserSchema
from dotenv import load_dotenv

load_dotenv()

class TestAuth(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

        self.test_user = UserSchema(
            username="admin",
            password="admin1111",
            name="Admin User"
        )
        self.test_user.create() 


    def test_login_success(self):
        response = self.client.post("/api/v1/login", data={
            "username": self.test_user.username,
            "password": self.test_user.password,
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json().get('data', {}))

    def test_login_failure(self):
        response = self.client.post("/api/v1/login", data={
            "username": self.test_user.username,
            "password": "wrongpassword",
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Incorrect username or password")

    def test_authenticated_user(self):
        # Login for get token
        login_response = self.client.post("/api/v1/login", data={
            "username": self.test_user.username,
            "password": self.test_user.password,
        })
        
        self.assertEqual(login_response.status_code, 200)
        token = login_response.json().get("data", {}).get("access_token")

        # Check information about the user
        user_response = self.client.get("/api/v1/me", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(user_response.status_code, 200)
        self.assertEqual(user_response.json()["username"], self.test_user.username)

    def test_unauthenticated_user(self):
        response = self.client.get("/api/v1/me")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["detail"], "Not authenticated")

if __name__ == '__main__':
    unittest.main()
