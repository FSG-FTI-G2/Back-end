from typing import Optional, Literal
from fastapi import HTTPException
from app.models.user_schema import UserSchema
from app.models.feedback_record_schema import FeedbackRecordSchema

# Define the evaluation status. -1: Bad, 0: Unset, 1: Good
EVALUATION_STATUS = Literal[-1, 0, 1]
SORT_BY = Literal["none", "asc", "desc"]
SORT_MODE = {"none": 0, "asc": 1, "desc": -1}


async def get_feedbacks_control(
    user: UserSchema,
    page_size: int = 10,
    page_index: int = 0,
    search: Optional[str] = None,
    evaluation: Optional[list[int]] = None,
    sort_by: Optional[str] = None,
):
    # Validate pagination parameters
    if page_size < 0 or page_index < 0:
        raise HTTPException(
            status_code=400, detail="Page size and index must be positive integers.")

    # Build query filter
    query = {}

    # Add search filter if provided
    if search:
        query["$or"] = [
            {"question": {"$regex": search, "$options": "i"}},
            {"answer": {"$regex": search, "$options": "i"}}
        ]

    # Add evaluation filter if provided and ensure the value is properly validated\
    if evaluation and all([eval_ in [-1, 0, 1] for eval_ in evaluation]):
        query["evaluation"] = {"$in": evaluation}

    # Query database for feedback records
    feedback = FeedbackRecordSchema.find_by_user_id(
        user.id, page_size, page_index, query=query, sort_by={"created_at": SORT_MODE.get(sort_by, 0)})
    total_pages = FeedbackRecordSchema.page_count(page_size)

    # Return paginated results
    return feedback, total_pages


async def update_feedback_control(
    user: UserSchema,
    feedback_records_id: list[str],
    evaluation: int
):
    # Validate the evaluation value
    if evaluation not in [-1, 0, 1]:
        raise HTTPException(
            status_code=400, detail="Invalid evaluation value.")

    # Query database for feedback records
    feedbacks: list[FeedbackRecordSchema] = []
    for feedback_id in feedback_records_id:
        feedback = FeedbackRecordSchema.find_by_id(feedback_id)
        if feedback and feedback.user_id == user.id:
            feedbacks.append(feedback)

    # Update evaluation value for the feedback records
    for feedback in feedbacks:
        feedback.evaluation = evaluation
        feedback.update()

    # TODO: Add RAG fine-tuning logic

    # Return updated feedback records
    return len(feedbacks)


async def delete_feedback_control(
    user: UserSchema,
    feedback_records_id: list[str]
):
    # Query database for feedback records
    feedbacks: list[FeedbackRecordSchema] = []
    for feedback_id in feedback_records_id:
        feedback = FeedbackRecordSchema.find_by_id(feedback_id)
        if feedback and feedback.user_id == user.id:
            feedbacks.append(feedback)

    # Delete feedback records
    for feedback in feedbacks:
        feedback.delete()

    # Return number of deleted feedback records
    return len(feedbacks)
