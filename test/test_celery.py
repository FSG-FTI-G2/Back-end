import unittest
from app.providers.celery_provider import CeleryProvider


class TestCelery(unittest.TestCase):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.celery = CeleryProvider()

    def test_celery_connection(self):
        content = "Hello, World!"
        task_id = self.celery.execute("echo", content)
        result = self.celery.get_result(task_id, wait_until_complete=True)
        self.assertIn(content, result["result"])

    def test_embedding(self):
        contents = ["Hello, World!"] * 85
        task_id = self.celery.execute("embed", contents)
        self.celery.on_progress(
            task_id, lambda x: self.assertIsInstance(x, dict))
        result = self.celery.get_result(task_id, wait_until_complete=True)
        self.assertIsInstance(result["result"], list)
