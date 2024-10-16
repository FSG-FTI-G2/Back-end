import unittest
from fastapi.testclient import TestClient
from main import app


class TestLLMRouter(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestLLMRouter, self).__init__(*args, **kwargs)
        self.client = TestClient(app)

        # Request login to get token
        response = self.client.post("/api/v1/auth/login", data={
            "username": "test",
            "password": "test123",
        }).json()
        token = response.get("data", {}).get("token")
        self.client.headers.update({"Authorization": f"Bearer {token}"})

        self.switch_llm_route = "/api/v1/llm/"

    def __test_update_llm(self):
        '''
        Switch and create a new user.
        '''
        response = self.client.post(
            self.switch_llm_route,
            params={
                "selected_model": "openai",
            },
            json={
                "name_model": "gpt-3.5-turbo",
                "api_key": "test-api-key"
            }
        ).json()

        self.assertEqual(response.get("code"), 200)
        self.assertEqual(response.get("data", {}).get(
            "config", {}).get("openai", {}).get("api_key"), "test-api-key")

    def __test_get_llm(self):
        '''
        Get the LLM configuration for the user.
        '''
        response = self.client.get(self.switch_llm_route).json()
        self.assertEqual(response.get("code"), 200)
        self.assertIsInstance(response.get(
            "data", {}).get("config", None), dict)

    def test_switch_LLM(self):
        self.__test_get_llm()
        self.__test_update_llm()
