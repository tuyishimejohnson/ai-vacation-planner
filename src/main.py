from fastapi import FastAPI
from .auth.controller import router as auth_router
from .users.controller import router as users_router
from .trips.controller import router as trips_router
from .itineraries.controller import router as itineraries_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(trips_router)
app.include_router(itineraries_router)
