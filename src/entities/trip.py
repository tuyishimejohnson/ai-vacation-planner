from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class Trip(Base):
    __tablename__ = "trips"
    id = Column(Integer, primary_key=True, index=True)
    destination = Column(String, index=True)
    days = Column(Integer)
    budget = Column(Integer)
    trip_style = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    itinerary = relationship("Itinerary", back_populates="trip", uselist=False)
