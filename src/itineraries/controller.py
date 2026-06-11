from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Annotated
from ..database import get_db
from .model import ItineraryCreateRequest
from . import service

router = APIRouter(prefix="/itineraries", tags=["itineraries"])
db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_itinerary(itinerary: ItineraryCreateRequest, db: db_dependency):
    return service.create_itinerary(itinerary, db)


@router.get("/{trip_id}", status_code=status.HTTP_200_OK)
async def get_itinerary_by_trip_id(trip_id: int, db: db_dependency):
    return service.get_itinerary_by_trip_id(trip_id, db)
