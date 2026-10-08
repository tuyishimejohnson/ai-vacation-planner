from contextlib import asynccontextmanager

from fastapi import FastAPI
from .auth.controller import router as auth_router
from .users.controller import router as users_router
from .trips.controller import router as trips_router
from .itineraries.controller import router as itineraries_router
from .travel_questions.audio.controller import voice_router
from .travel_questions.text.controller import router as travel_text_router
from .mcp.server import mcp
from fastapi.middleware.cors import CORSMiddleware

mcp_http_app = mcp.http_app(path="/")


@asynccontextmanager
async def lifespan(_app):
    async with mcp_http_app.router.lifespan_context(mcp_http_app):
        yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Conversation-Id"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(trips_router)
app.include_router(itineraries_router)
app.include_router(travel_text_router)
app.include_router(voice_router)
app.mount("/mcp", mcp_http_app)
