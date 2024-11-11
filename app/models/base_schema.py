from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class BaseSchema(BaseModel):
    id: Optional[str] = Field(
        None, alias="_id", description="The unique identifier of the document.")
    created_at: Optional[datetime] = Field(
        None, alias="created_at", description="The date and time the document was created.")
    updated_at: Optional[datetime] = Field(
        None, alias="updated_at", description="The date and time the document was last updated.")

    class Config:
        populate_by_name = True
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        json_schema_extra = {
            "example": {
                "id": "string",
                "created_at": "2021-08-29T00:00:00",
                "updated_at": "2021-08-29T00:00:00"
            }
        }

    def create(self):
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def update(self):
        self.updated_at = datetime.now()
