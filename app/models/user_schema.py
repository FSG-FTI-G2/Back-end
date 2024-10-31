from typing import Optional, Union
from pydantic import Field
from app.models.base_schema import BaseSchema
from app.providers import user_db


class UserSchema(BaseSchema):
    username: str = Field(None, alias="username")
    password: str = Field(None, alias="password")
    name: Optional[str] = Field(None, alias="name")

    @staticmethod
    def find_by_username(username: str) -> Union['UserSchema', None]:
        # Find by username
        data = user_db.query({"username": username})
        # If length is 0, return None
        if len(data) == 0:
            return None
        # Validate the data
        return UserSchema.model_validate(data[0])

    @staticmethod
    def find_by_id(id: str) -> Union['UserSchema', None]:
        # Find by id
        data = user_db.get_by_id(id)
        # If data is None, return None
        if data is None:
            return None
        # Validate the data
        return UserSchema.model_validate(data)

    def create(self):
        # Modify the created_at and updated_at
        super().create()
        # Create the user
        created_id = user_db.create(self.model_dump(
            exclude_none=True, mode="json", by_alias=True))
        self.id = created_id
        return self

    def update(self) -> int:
        # Modify the updated_at
        super().update()
        # Update the user
        return user_db.update(
            self.id, self.model_dump(
                exclude={"id"}, exclude_none=True, mode="json", by_alias=True
            )
        )

    def delete(self) -> int:
        return user_db.delete(self.id)
