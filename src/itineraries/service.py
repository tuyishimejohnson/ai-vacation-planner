from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from anthropic import Anthropic
import os
from typing import Annotated
from ..auth.service import get_current_user
from ..database.core import get_db


from ..entities.itinerary import Itinerary
from .model import ItineraryCreateRequest
from ..trips.service import get_trips
import json

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

system_prompt = """
You are an itinerary creator who bases plans on the user's existing trips.
Only provide itinerary content. If someone asks something irrelevant, say you don't
have enough information and suggest them to consult google.

Always respond with valid JSON in this exact structure:
{
  "trip_id": number,
  "days": [
    {
      "day": number,
      "activities": ["string", "string"]
    }
  ]
}

"""


def generate_itinerary_with_claude(user_id: int, trip_id: int, db: Session):
    trips = get_trips(user_id, db)

    if not trips:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No trips found for this user",
        )

    # Find the trip matching the given trip_id and break if found
    trip = next((t for t in trips if t.id == trip_id), None)

    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found",
        )

    # Format the user's trips to give claude a context
    trips_format = "\n".join(
        [
            f"- {t.destination}: {t.days} days, budget Rwf{t.budget}, style: {t.trip_style}"
            for t in trips
        ]
    )

    prompt = (
        f"These planned trips:\n{trips_format}\n\n"
        f"Generate a day-by-day itinerary for the trip to {trip.destination} "
        f"({trip.days} days, budget Rwf{trip.budget}, style: {trip.trip_style}). "
        f"Use trip_id: {trip.id} in the JSON response."
    )

    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1000,
        temperature=0.3,
        system=system_prompt,
        messages=[{"role": "user", "content": prompt}],
    )

    first_response = response.content[0].text

    # change text to JSON format
    try:
        clean_response = (
            first_response.replace("```json", "").replace("```", "").strip()
        )

        itinerary_json = json.loads(clean_response)
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="invalid JSON",
        )

    # Check if an itinerary already exists for this trip before creating a new one
    existing = db.query(Itinerary).filter(Itinerary.trip_id == trip_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Itinerary already exists",
        )

    # Convert the parsed JSON dict into an orm to send to db
    new_itinerary = Itinerary(
        trip_id=itinerary_json["trip_id"],
        days=itinerary_json["days"],
    )

    db.add(new_itinerary)
    db.commit()
    db.refresh(new_itinerary)

    return {"itinerary": new_itinerary}


def create_itinerary(db: db_dependency, itinerary: ItineraryCreateRequest):
    new_itinerary = ItineraryCreateRequest(
        trip_id=itinerary.trip_id, days=itinerary.days
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


def get_all_itineraries(db: Session):
    return db.query(Itinerary).all()
