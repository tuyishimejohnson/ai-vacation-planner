from pydantic import BaseModel


class TripCreateRequest(BaseModel):
    destination: str
    days: int
    budget: int
    trip_style: str
