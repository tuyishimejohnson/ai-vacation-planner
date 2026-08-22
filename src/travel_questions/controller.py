from fastapi import APIRouter, status

from .model import TravelQuestionRequest, TravelQuestionResponse
from . import service

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
    return service.ask_travel_question(question=request.question)
