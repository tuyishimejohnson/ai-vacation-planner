from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import Annotated
from ..database import get_db
from ..entities.itinerary import Itinerary
from .model import ItineraryCreateRequest

router = APIRouter(prefix="/itineraries", tags=["itineraries"])

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_itinerary(db: db_dependency, itinerary: ItineraryCreateRequest):
    new_itinerary = Itinerary(trip_id=itinerary.trip_id, days=itinerary.days)
    db.add(new_itinerary)
    db.commit()
    db.refresh(new_itinerary)
    return new_itinerary


@router.get("/{trip_id}", status_code=status.HTTP_200_OK)
async def get_itinerary_by_trip_id(db: db_dependency, trip_id: int):
    itinerary = db.query(Itinerary).filter(Itinerary.trip_id == trip_id).first()
    if not itinerary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Itinerary not found"
        )
    return itinerary
