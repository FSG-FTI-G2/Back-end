from typing import Union
from pydantic import BaseModel, Field
from app.providers import user_db


class UserSchema(BaseModel):
    id: str = Field(None, alias="_id")
    username: str = Field(None, alias="username")
    password: str = Field(None, alias="password")
    name: str = Field(None, alias="name")
    data_info_id: str = Field(None, alias="data_info_id")
    is_admin: bool = Field(None, alias="is_admin")

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
        created_id = user_db.create(self.model_dump(
            exclude_none=True, mode="json", by_alias=True))
        self.id = created_id
        return self

    def update(self) -> int:
        return user_db.update(
            self.id, self.model_dump(
                exclude={"id"}, exclude_none=True, mode="json", by_alias=True
            )
        )

    def delete(self) -> int:
        return user_db.delete(self.id)
