from pydantic import BaseModel


class ItineraryDay(BaseModel):
    day: int
    activities: list[str]


class ItineraryCreateRequest(BaseModel):
    trip_id: int
    days: list[ItineraryDay]
