from typing import Annotated, Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends
from app.models.user_schema import UserSchema
from app.middlewares.auth_middleware import auth_user_middleware
from app.controllers.feedback_controller import get_feedbacks_control, SORT_BY, update_feedback_control, delete_feedback_control
from app.utils.response import response, pagination_data


router = APIRouter()


@router.get("/")
async def get_feedback_records(
    user: Annotated[UserSchema, Depends(auth_user_middleware)],
    page_size: int = 10,
    page_index: int = 0,
    search: Optional[str] = None,
    evaluation_status: Optional[str] = None,
    sort_by: Optional[SORT_BY] = "none"
):
    # Format search and evaluation status
    if search == "":
        search = None
    if evaluation_status:
        evaluation_status = [int(e) for e in evaluation_status.split(",")]
        if len(evaluation_status) == 0:
            evaluation_status = None

    # Get feedback records
    feedback, total_pages = await get_feedbacks_control(user, page_size, page_index, search, evaluation_status, sort_by)
    return response(code=200, message="Get feedback records successfully.", data=pagination_data(
        data=[item.model_dump() for item in feedback],
        total_pages=total_pages,
        page_index=page_index,
        page_size=page_size
    ))


class FeedbackModifierInput(BaseModel):
    feedback_records_id: list[str]
    evaluation: int


@router.post("/")
async def update_feedback_record(
    data: FeedbackModifierInput,
    user: UserSchema = Depends(auth_user_middleware),
):
    updated_count = await update_feedback_control(user, data.feedback_records_id, data.evaluation)
    return response(code=200, message=f"Update {updated_count} feedback records successfully.")


class FeedbackDeletionInput(BaseModel):
    feedback_records_id: list[str]


@router.put("/")
async def delete_feedback_record(
    user: Annotated[UserSchema, Depends(auth_user_middleware)],
    data: FeedbackDeletionInput
):
    deleted_count = await delete_feedback_control(user, data.feedback_records_id)
    return response(code=200, message=f"Delete {deleted_count} feedback records successfully.")
