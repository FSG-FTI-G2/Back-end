from fastapi.testclient import TestClient
import unittest
from main import app

client = TestClient(app)

USER_ID = "test_user"
MODEL_TYPE = "openai"
DATA = {
  "api_key": "your-api-key",
  "name_model": "gpt-3.5-turbo",
  "endpoint": "https://ollama.com"
}

class TestLLMRouter(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(TestLLMRouter, self).__init__(*args, **kwargs)
        self.client = TestClient(app)
        
        self.llm_get_route = "/api/v1/llm/llm"
        self.llm_switch_route = "/api/v1/llm/llm/switch"
        self.llm_delete_route = "/api/v1/llm/llm/delete"

    def __test_switch_llm(self):
        '''
        Switch and create a new user.
        '''
        response = self.client.post(
            self.llm_switch_route,   params={"user_id": USER_ID,
                                              "model_type": str(MODEL_TYPE), 
                                              }, json = DATA
        )
   
        self.assertEqual(response.status_code, 200)
        self.assertIn(f"LLM model switched successfully to {MODEL_TYPE} for user {USER_ID}.", response.json())

    def __test_get_llm(self):
        '''
        Get the LLM configuration for the user.
        '''
        response = self.client.get(
            self.llm_get_route,  
            params={"user_id": USER_ID}  
        )
        
        self.assertEqual(response.status_code, 200)

    def __test_delete_llm(self):
        '''
        Delete the LLM configuration for the user.
        '''
        response = self.client.delete(
            self.llm_delete_route,  
            params={"user_id": USER_ID}  
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(f"LLM Configuration for user_id {USER_ID} has been deleted.", response.json())
        
    def test_switch_LLM(self):
        self.__test_switch_llm()
        self.__test_get_llm()
        self.__test_delete_llm()