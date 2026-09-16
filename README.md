# AI Vacation Planner

A backend API for planning vacations, built with FastAPI. Users can manage trips and itineraries based on their account, with authentication protecting all endpoints.

## Features

- JWT authentication - register, login, and receive a token
- Trip management - logged users can create, read, update, and delete trips
- Itinerary management - create and read itineraries linked to a trip
- PostgreSQL database with Alembic migrations
- Modular architecture - each domain (auth, users, trips, itineraries) has its own controller, service, and model
- Add RAG system - allows the system retrieve travel information based on available documents and resources
- Travel agent - uses LangChain + LangGraph to automate user query with an LLM

## Tech Stack

- FastAPI - framework
- SQLAlchemy - ORM
- Alembic - database migrations
- PostgreSQL - database
- passlib + bcrypt - password hashing
- python-jose - JWT token handling
- uvicorn - ASGI server
- uv - dependency installation
- Pinecone - vector database for storing and querying travel document embeddings
- sentence-transformers - embedding model (all-MiniLM-L6-v2) HuggingFace
- unstructured - partitions and chunks travel articles/PDFs for the knowledge base
- Anthropic (claude-haiku-4-5) - used in this context of generating responses
- LangChain - tools and agent creation
- LangGraph - State management and memory

## Tools Used

- **Current weather** - retrieves live weather conditions for a city through the OpenWeatherMap API
- **Places search** - finds destinations, landmarks, hotels, restaurants, and other places through the Google Maps Places API
- **Country information** - retrieves country details, capitals, currencies, languages, and time zones through the REST Countries API
- **Exchange rates** - retrieves current exchange rates and converts amounts through the Exchange Rates API
- **Travel knowledge search** - retrieves relevant travel tips, safety guidance, packing advice, and transportation information from Pinecone

## Getting Started

**1. Clone the repository**

```bash
git clone https://github.com/tuyishimejohnson/ai-vacation-planner.git
cd ai-vacation-planner
```

**2. Set up the environment**

```bash
uv venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate  # Mac/Linux
uv sync
```

**3. Configure environment variables**

Create a `.env` file in the project root:

```env
Refer to .env.example file
```

**4. Run database migrations**

```bash
alembic upgrade head
```

**5. Start the server**

```bash
uvicorn src.main:app --reload
```

API available at `http://localhost:8000` and `http://localhost:8000/docs`.

---

## API Endpoints

### Auth

- `POST /auth/register` - create a new account
- `POST /auth/token` - login and receive a JWT token

### Users

- `GET /users/me` - get current logged-in user
- `GET /users/` - list all users
- `GET /users/{id}` - get user by ID

### Trips

Needs authentication

- `POST /trips/` - create a trip
- `GET /trips/` - get all trips for the current user
- `GET /trips/{id}` - get a specific trip
- `PUT /trips/{id}` - update a trip
- `DELETE /trips/{id}` - delete a trip

### Itineraries

- `POST /itineraries/` - create an itinerary for a trip
- `GET /itineraries/{trip_id}` - get itinerary by trip ID
- `POST /itinerares/generate/{trip_id}` - generate an itinerary from an LLM (Claude)

  ## Generate Itineraries
  - Created a new route for generating itineraries based on a created trip.
  - Updated `service.py` in itineraries to generate itineraries using the `claude-haiku-4-5` model.
  - The generated response is validated, cleaned, converted to JSON, and stored in the database.

  ### Add External Tool
  - Added `get_current_weather(lat, lon)` in itineraries to call the OpenWeatherMap API.
  - Registered it as a Claude tool (`weather_tool`) via the Messages API `tools` parameter, so Claude can request current weather for a location while generating an itinerary.
  - `generate_itinerary_with_claude` runs a tool-use loop: when Claude responds with `stop_reason: "tool_use"`, the requested tool is executed and its result is sent back as a `tool_result` message until Claude returns the final itinerary text.

  ### Tools added for LangChain
  - Added exchange rate tool `get_exchange_rate`
  - Added travel knowledge from RAG `search_travel_knowledge`
  - Added Countries and cities tool `get_countries_and_cities`

### Travel Questions

- `POST /travel/ask` - ask the vacation-planning agent any question. The agent selects the appropriate tool (weather, places, country data, exchange rates, or travel knowledge RAG) before responding.

```json
{ "question": "What safety tips should I follow when travelling?" }
```

When the agent uses the travel knowledge tool, the response includes the retrieved document chunks in `sources`.

## Build the Knowledge Base

- `src/notebooks/travel_knowledge.ipynb` builds the Pinecone index used by `/travel/ask`
- Partition travel article URLs and PDF documents with `unstructured`
- Clean, filter, and chunk the partitioned elements with `chunk_by_title`
- Embed chunks with `sentence-transformers/all-MiniLM-L6-v2`
- Create the `travel-rag` Pinecone index
- Upload the vectors to Pinecone

## Project Structure

```
vacation_planner/
├── alembic/
│   ├── versions/
│   └── env.py
├── src/
│   ├── main.py
│   ├── agent/
│   │   └── agent.py
│   ├── auth/
│   │   ├── controller.py
│   │   ├── model.py
│   │   └── service.py
│   ├── database/
│   │   └── core.py
│   ├── entities/
│   │   ├── itinerary.py
│   │   ├── trip.py
│   │   └── user.py
│   ├── itineraries/
│   │   ├── data/
│   │   ├── controller.py
│   │   ├── model.py
│   │   └── service.py
│   ├── notebooks/
│   │   └── travel_knowledge.ipynb
│   ├── tools/
│   │   ├── countries.py
│   │   ├── exchange_rate.py
│   │   ├── places.py
│   │   ├── travel_knowledge.py
│   │   └── weather.py
│   ├── travel_questions/
│   │   ├── controller.py
│   │   ├── model.py
│   │   ├── retrieval.py
│   │   └── service.py
│   ├── trips/
│   │   ├── controller.py
│   │   ├── model.py
│   │   └── service.py
│   └── users/
│       ├── controller.py
│       ├── model.py
│       └── service.py
├── .env.example
├── alembic.ini
├── pyproject.toml
├── uv.lock
└── README.md
```
