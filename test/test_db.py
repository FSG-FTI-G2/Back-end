import unittest
from app.providers.db import DatabaseProvider


class TestSchema:
    def __init__(self, **kwargs):
        self.id = str(kwargs.get("_id", ""))
        self.name = kwargs.get("name", None)
        self.email = kwargs.get("email", None)
        self.projects = kwargs.get("projects", None)

    def to_dict(self, include_id=True):
        data = self.__dict__
        if not include_id:
            del data["id"]
        # Filter out None values
        data = {k: v for k, v in data.items() if v is not None}
        return data


class DbTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(DbTestCase, self).__init__(*args, **kwargs)
        self.test_db = DatabaseProvider("test")

    def __insert(self):
        object = TestSchema(
            name="Test User",
            email="test.example@gmail.com",
            projects=["Test Project", "Example Project"],
        )
        result = self.test_db.create(object.to_dict(include_id=False))
        self.assertIsInstance(result, str)
        return result

    def __update(self, id):
        # Update user name
        new_object_data = TestSchema(
            name="Updated User",
        )
        result = self.test_db.update(
            id, new_object_data.to_dict())
        self.assertEqual(result, 1)
        # Validate the update
        result = self.test_db.get_by_id(id)
        self.assertEqual(result["name"], "Updated User")

    def __select(self, id):
        result = self.test_db.get_by_id(id)
        data = TestSchema(**result)
        self.assertEqual(data.id, id)
        result = self.test_db.get_by_id("626bccb9697a12204fb22ea3")
        self.assertIsNone(result)

    def __select_all(self):
        result = self.test_db.get_all()
        self.assertIsInstance(result, list)

    def __query_all(self):
        result = self.test_db.query({
            "email": "test.example@gmail.com"
        })
        self.assertIsInstance(result, list)

    def __delete(self, id):
        result = self.test_db.delete(id)
        self.assertEqual(result, 1)

    def test_database(self):
        created_id = self.__insert()
        self.__update(created_id)
        self.__select(created_id)
        self.__query_all()
        self.__select_all()
        self.__delete(created_id)
