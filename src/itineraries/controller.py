from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Annotated

from ..database import get_db
from ..auth.service import get_current_user
from . import service
from .model import ItineraryCreateRequest

router = APIRouter(prefix="/itineraries", tags=["itineraries"])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post("/generate/{trip_id}", status_code=status.HTTP_200_OK)
async def generate_itinerary(
    trip_id: int,
    db: db_dependency,
    current_user: user_dependency,
):
    return service.generate_itinerary_with_claude(
        user_id=current_user["id"], trip_id=trip_id, db=db
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_itinerary(
    db: db_dependency, itinerary_request: ItineraryCreateRequest
):
    return service.create_itinerary(db=db, itinerary_request=itinerary_request)


@router.get("/{trip_id}", status_code=status.HTTP_200_OK)
async def get_itinerary_by_trip_id(trip_id: int, db: db_dependency):
    return service.get_itinerary_by_trip_id(trip_id, db)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_itineraries(db: db_dependency):
    return service.get_all_itineraries(db=db)
