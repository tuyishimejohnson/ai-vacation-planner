from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .model import ItineraryCreateRequest
from ..database import get_db
from ..entities.itinerary import Itinerary
from .model import ItineraryCreateRequest


def create_itinerary(itinerary: ItineraryCreateRequest, db: Session):
    new_itinerary = Itinerary(
        trip_id=itinerary.trip_id,
        days=[day.model_dump() for day in itinerary.days],
    )
    db.add(new_itinerary)
    db.commit()
    db.refresh(new_itinerary)
    return new_itinerary


def get_itinerary_by_trip_id(trip_id: int, db: Session):
    itinerary = db.query(Itinerary).filter(Itinerary.trip_id == trip_id).first()
    if not itinerary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Itinerary not found"
        )
    return itinerary
