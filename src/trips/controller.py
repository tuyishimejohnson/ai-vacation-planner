from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Annotated
from ..database import get_db
from ..auth.service import get_current_user
from .model import TripCreateRequest
from . import service

router = APIRouter(prefix="/trips", tags=["trips"])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_trip(trip: TripCreateRequest, db: db_dependency, current_user: user_dependency):
    return service.create_trip(trip, current_user["id"], db)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_trips(db: db_dependency, current_user: user_dependency):
    return service.get_trips(current_user["id"], db)


@router.get("/{trip_id}", status_code=status.HTTP_200_OK)
async def get_trip_by_id(trip_id: int, db: db_dependency, current_user: user_dependency):
    return service.get_trip_by_id(trip_id, current_user["id"], db)


@router.put("/{trip_id}", status_code=status.HTTP_200_OK)
async def update_trip(trip_id: int, trip: TripCreateRequest, db: db_dependency, current_user: user_dependency):
    return service.update_trip(trip_id, trip, current_user["id"], db)


@router.delete("/{trip_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_trip(trip_id: int, db: db_dependency, current_user: user_dependency):
    service.delete_trip(trip_id, current_user["id"], db)
