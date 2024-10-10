import unittest
from fastapi.testclient import TestClient
from main import app
from app.models.user import UserSchema
from app.providers import encryptor


# Mock JWT_SECRET for testing
encryptor.secret = "some_secret"


# Create default user
USERNAME = "admin"
PASSWORD = "admin1111"
UserSchema(
    username=USERNAME,
    password=encryptor.hash(PASSWORD),
).create()


class TestAuth(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestAuth, self).__init__(*args, **kwargs)

        self.client = TestClient(app)

        # Define routes
        self.login_route = "/api/v1/auth/login"
        self.me_route = "/api/v1/auth/me"

    def test_login_success(self):
        response = self.client.post(self.login_route, data={
            "username": USERNAME,
            "password": PASSWORD,
        }).json()

        self.assertEqual(response.get("code"), 200)
        self.assertIn("token", response.get("data", {}))

    def test_login_failure(self):
        response = self.client.post(self.login_route, data={
            "username": USERNAME,
            "password": "wrongpassword",
        }).json()

        self.assertEqual(response.get("code"), 400)
        self.assertIsNone(response.get("data", {}))

    def test_authenticated_user(self):
        # Login for get token
        login_response = self.client.post(self.login_route, data={
            "username": USERNAME,
            "password": PASSWORD,
        }).json()

        self.assertEqual(login_response.get("code"), 200)
        token = login_response.get("data", {}).get("token")

        # Check information about the user
        user_response = self.client.get(
            self.me_route, headers={"Authorization": f"Bearer {token}"}).json()

        self.assertEqual(user_response.get("code"), 200)
        self.assertEqual(user_response.get(
            "data", {}).get("username"), USERNAME)

    def test_unauthenticated_user(self):
        response = self.client.get(self.me_route).json()

        # No authorization token -> Forbidden 403
        self.assertEqual(response.get("code"), 403)
        self.assertIsNone(response.get("data", {}))
