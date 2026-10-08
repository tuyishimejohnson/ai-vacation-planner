from fastapi import APIRouter, status

from .model import TravelQuestionRequest, TravelQuestionResponse
from .service import ask_travel_question as ask_question

router = APIRouter(
    prefix="/travel",
    tags=["travel"],
)


@router.post(
    "/ask",
    response_model=TravelQuestionResponse,
    status_code=status.HTTP_200_OK,
)
async def ask_travel_question(
    request: TravelQuestionRequest,
):
    return await ask_question(
        question=request.question,
        conversation_id=request.conversation_id,
    )
