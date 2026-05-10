from pydantic import BaseModel


class ItineraryCreateRequest(BaseModel):
    trip_id: int
    days: list[dict]
