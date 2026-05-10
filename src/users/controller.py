from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Annotated
from ..database import get_db
from ..auth.service import get_current_user
from .service import get_all_users, get_user_by_id

router = APIRouter(prefix="/users", tags=["users"])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/me")
async def read_users_me(current_user: user_dependency):
    return current_user


@router.get("/")
async def read_users(db: db_dependency, current_user: user_dependency):
    return get_all_users(db)


@router.get("/{user_id}")
async def read_user(user_id: int, db: db_dependency, current_user: user_dependency):
    user = get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
