from pydantic import BaseModel, Field
from typing import List


class TravelSource(BaseModel):
    source: str | None = None
    text: str
    score: float


class TravelQuestionResponse(BaseModel):
    answer: str
    sources: List[TravelSource]


class TravelQuestionRequest(BaseModel):
    question: str
