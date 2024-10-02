import unittest
from app.models.file import FileSchema, FileStatus


class FileDbTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs) -> None:
        super(FileDbTestCase, self).__init__(*args, **kwargs)

    def __create_file(self):
        # Create a test file
        file = FileSchema(
            user_id="test_user",
            type="pdf",
            file_name="test_file",
            file_path="/test/file.pdf",
        )
        file.create()
        # Test if file is created
        self.assertIsNotNone(file.id)
        # Validate the file
        file = FileSchema.find_by_id(file.id)
        self.assertIsNotNone(file)
        return file

    def __find_files(self, user_id: str):
        # Find the files by user_id with valid id
        files = FileSchema.find_by_user_id(user_id, 10, 0)
        self.assertEqual(len(files), 1)

        # Find the files by user_id with invalid id
        files = FileSchema.find_by_user_id("invalid_user", 10, 0)
        self.assertEqual(len(files), 0)

    def __find_file_by_id(self, id: str):
        # Find the file by id
        file = FileSchema.find_by_id(id)
        self.assertIsNotNone(file)

    def __update_file_status(self, file: FileSchema):
        # Update the file status as SUCCESS
        file.status = FileStatus.SUCCESS
        file.update()
        # Validate the file
        file = FileSchema.find_by_id(file.id)
        self.assertEqual(file.status, FileStatus.SUCCESS)

        # Update the file status as ERROR
        file.status = FileStatus.ERROR
        file.update()
        # Validate the file
        file = FileSchema.find_by_id(file.id)
        self.assertEqual(file.status, FileStatus.ERROR)

    def __delete_file(self, file: FileSchema):
        # Delete the file
        file.delete()
        # Validate the delete
        file = FileSchema.find_by_id(file.id)
        self.assertIsNone(file)

    def test_file_db(self):
        # Create a test file
        file = self.__create_file()
        # Find the files by user_id
        self.__find_files(file.user_id)
        # Find file by ID
        self.__find_file_by_id(file.id)
        # Update the file status
        self.__update_file_status(file)
        # Delete the file
        self.__delete_file(file)
