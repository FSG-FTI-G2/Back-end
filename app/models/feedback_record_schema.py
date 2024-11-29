from typing import Literal
from pydantic import Field, BaseModel
from app.models.base_schema import BaseSchema
from app.providers import feedback_record_db


class DocumentReference(BaseModel):
    document: str = Field(None, alias="document")
    chunk: str = Field(None, alias="chunk")


feedback_record_db.create_index("user_id")
feedback_record_db.create_index("created_at")


class FeedbackRecordSchema(BaseSchema):
    user_id: str = Field(None, alias="user_id")
    message_id: str = Field(None, alias="message_id")
    message_index: int = Field(None, alias="message_index")
    question: str = Field(None, alias="question")
    answer: str = Field(None, alias="answer")
    documents: list[DocumentReference] = Field(
        default_factory=list, alias="documents")
    evaluation: Literal[-1, 0, 1] = Field(default=0, alias="evaluation")

    @staticmethod
    def page_count(page_size: int) -> int:
        return feedback_record_db.page_count(page_size)

    @staticmethod
    def find_by_user_id(
        user_id: str,
        page_size: int,
        page_index: int,
        query: dict = {},
        exclude: list[str] = [],
        sort_by: dict[str, int] = {}
    ) -> list['FeedbackRecordSchema']:
        # Find by user_id
        data = feedback_record_db.query(
            {"user_id": user_id, **query}, page_size=page_size, page_index=page_index, exclude=exclude, sort_by=sort_by)
        # Validate the data
        return [FeedbackRecordSchema.model_validate(item) for item in data]

    @staticmethod
    def find_by_id(
        feedback_id: str
    ) -> 'FeedbackRecordSchema':
        # Find by id
        data = feedback_record_db.get_by_id(feedback_id)
        # Validate the data
        return FeedbackRecordSchema.model_validate(data)

    def create(self):
        # Modify the created_at and updated_at
        super().create()
        # Create the file
        created_id = feedback_record_db.create(self.model_dump(
            exclude_none=True, mode="json", by_alias=True))
        self.id = created_id
        return self

    def update(self):
        # Modify the updated_at
        super().update()
        # Update the file
        feedback_record_db.update(self.id, self.model_dump(
            exclude={"id"}, exclude_none=True, mode="json", by_alias=True))
        return self

    def delete(self):
        # Delete the file
        return feedback_record_db.delete(self.id)
