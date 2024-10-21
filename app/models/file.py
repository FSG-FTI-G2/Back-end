from typing import Optional, Union
from enum import Enum
from pydantic import Field
from app.models.base import BaseSchema
from app.providers import file_db


class FileType(str, Enum):
    '''
    Enum for File Type
    '''
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"


class FileStatus(str, Enum):
    '''
    Enum for File Status
    '''
    PENDING = "pending"
    UPLOADING = "uploading"
    PROCESSING = "processing"
    SUCCESS = "success"
    ERROR = "error"


# Create a index for user_id
file_db.create_index("user_id")


class FileSchema(BaseSchema):
    user_id: str = Field(None, alias="user_id")
    type: FileType = Field(None, alias="type")
    file_name: str = Field(None, alias="file_name")
    file_path: str = Field(None, alias="file_path")
    thumbnail: Optional[str] = Field(None, alias="thumbnail")
    status: FileStatus = Field(FileStatus.PENDING, alias="status")

    @staticmethod
    def page_count(page_size: int) -> int:
        return file_db.page_count(page_size)

    @staticmethod
    def find_by_user_id(user_id: str, page_size: int, page_index: int, query: dict = {}) -> list['FileSchema']:
        # Find by user_id
        data = file_db.query(
            {"user_id": user_id, **query}, page_size=page_size, page_index=page_index)
        # Validate the data
        return [FileSchema.model_validate(item) for item in data]

    @staticmethod
    def find_by_file_name(user_id: str, file_name: str) -> Union['FileSchema', None]:
        # Find by file_name
        data = file_db.query({"user_id": user_id, "file_name": file_name})
        # If data is None, return None
        if len(data) == 0:
            return None
        # Validate
        return FileSchema.model_validate(data[0])

    @staticmethod
    def find_by_id(id: str) -> Union['FileSchema', None]:
        # Find by id
        data = file_db.get_by_id(id)
        # If data is None, return None
        if data is None:
            return None
        # Validate the data
        return FileSchema.model_validate(data)

    def create(self):
        # Modify the created_at and updated_at
        super().create()
        # Create the file
        created_id = file_db.create(self.model_dump(
            exclude_none=True, mode="json", by_alias=True))
        self.id = created_id
        return self

    def update(self) -> int:
        # Modify the updated_at
        super().update()
        # Update the file
        return file_db.update(
            self.id, self.model_dump(
                exclude={"id"}, exclude_none=True, mode="json", by_alias=True
            )
        )

    def delete(self) -> int:
        return file_db.delete(self.id)
