from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..entities.trip import Trip
from .model import TripCreateRequest


def create_trip(trip: TripCreateRequest, user_id: int, db: Session):
    new_trip = Trip(
        destination=trip.destination,
        days=trip.days,
        budget=trip.budget,
        trip_style=trip.trip_style,
        user_id=user_id,
    )
    db.add(new_trip)
    db.commit()
    db.refresh(new_trip)
    return new_trip


def get_trips(user_id: int, db: Session):
    return db.query(Trip).filter(Trip.user_id == user_id).all()


def get_trip_by_id(trip_id: int, user_id: int, db: Session):
    trip = db.query(Trip).filter(Trip.id == trip_id, Trip.user_id == user_id).first()
    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found"
        )
    return trip


def update_trip(trip_id: int, trip: TripCreateRequest, user_id: int, db: Session):
    existing_trip = (
        db.query(Trip).filter(Trip.id == trip_id, Trip.user_id == user_id).first()
    )
    if not existing_trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found"
        )
    existing_trip.destination = trip.destination
    existing_trip.days = trip.days
    existing_trip.budget = trip.budget
    existing_trip.trip_style = trip.trip_style
    db.commit()
    db.refresh(existing_trip)
    return existing_trip


def delete_trip(trip_id: int, user_id: int, db: Session):
    existing_trip = (
        db.query(Trip).filter(Trip.id == trip_id, Trip.user_id == user_id).first()
    )
    if not existing_trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found"
        )
    db.delete(existing_trip)
    db.commit()
