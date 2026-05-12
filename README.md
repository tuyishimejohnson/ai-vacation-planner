# AI Vacation Planner

A backend API for planning vacations, built with FastAPI. Users can manage trips and itineraries based on their account, with authentication protecting all endpoints.

## Features

- JWT authentication - register, login, and receive a token
- Trip management - logged users can create, read, update, and delete trips
- Itinerary management - create and read itineraries linked to a trip
- PostgreSQL database with Alembic migrations
- Modular architecture - each domain (auth, users, trips, itineraries) has its own controller, service, and model

## Tech Stack

- **FastAPI** - framework
- **SQLAlchemy** - ORM
- **Alembic** - database migrations
- **PostgreSQL** - database
- **passlib + bcrypt** - password hashing
- **python-jose** - JWT token handling
- **uvicorn** - ASGI server
- **uv** - dependency installation

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

## Project Structure

```
vacation_planner/
├── alembic/
│   ├── versions/
│   └── env.py
├── src/
│   ├── main.py
│   ├── auth/
│   │   ├── controller.py
│   │   ├── service.py
│   │   └── model.py
│   ├── users/
│   │   ├── controller.py
│   │   ├── service.py
│   │   └── model.py
│   ├── trips/
│   │   ├── controller.py
│   │   ├── service.py
│   │   └── model.py
│   ├── itineraries/
│   │   ├── controller.py
│   │   ├── service.py
│   │   └── model.py
│   ├── entities/
│   │   ├── user.py
│   │   ├── trip.py
│   │   └── itinerary.py
│   └── database/
│       └── core.py
├── .env
├── .env.example
├── alembic.ini
├── pyproject.toml
└── uv.lock
```
