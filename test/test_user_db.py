import unittest
from app.models.user import UserSchema
from app.controllers.auth_control import create_mock_admin

class UserDbTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs) -> None:
        super(UserDbTestCase, self).__init__(*args, **kwargs)

    def __create_user(self):
        # Create a test user
        user = UserSchema(
            username="test_user",
            password="test_password",
        )
        user.create()
        # Test if user is created
        self.assertIsNotNone(user.id)
        # Validate the user
        user = UserSchema.find_by_id(user.id)
        self.assertIsNotNone(user)
        return user

    def __find_user(self, username: str):
        # Find the user by username
        user = UserSchema.find_by_username(username)
        self.assertIsNotNone(user)

    def __find_user_by_id(self, id: str):
        # Find the user by id
        user = UserSchema.find_by_id(id)
        self.assertIsNotNone(user)

    def __update_user(self, user: UserSchema):
        # Update the user
        user.name = "Updated User"
        user.update()
        # Validate the user
        user = UserSchema.find_by_id(user.id)
        self.assertEqual(user.name, "Updated User")

    def __delete_user(self, user: UserSchema):
        # Delete the user
        user.delete()
        # Validate the delete
        user = UserSchema.find_by_id(user.id)
        self.assertIsNone(user)

    def test_user_db(self):
        # Create a test user
        user = self.__create_user()
        # Find the user by username
        self.__find_user(user.username)
        # Update the user
        self.__update_user(user)
        # Delete the user
        self.__delete_user(user)
        
    def test_admin_user_creation(self):
        admin = create_mock_admin()
        self.assertEqual(admin.is_admin, True)
        self.assertEqual(admin.username, "admin")