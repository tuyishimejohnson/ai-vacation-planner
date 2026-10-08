from typing import List
from pydantic import BaseModel


class TravelSource(BaseModel):
    source: str | None = None
    text: str
    score: float


class TravelQuestionResponse(BaseModel):
    answer: str
    sources: List[TravelSource]
    conversation_id: str


class TravelQuestionRequest(BaseModel):
    question: str
    conversation_id: str | None = None


