from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import Session
from app.schemas.user import UserCreate, User, UserUpdate
from app.task_manager.user import create_user, get_users, get_user_by_id, update_user, delete_user
from app.db.database import get_session

router = APIRouter()

@router.get("/", response_model=List[User])
def read_users(session: Session = Depends(get_session)):
    return get_users(session=session)

@router.post("/", response_model=User)
def create_new_user(user_in: UserCreate, session: Session = Depends(get_session)):
    return create_user(session=session, user_in=user_in)

@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, session: Session = Depends(get_session)):
    user = get_user_by_id(session=session, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found :(")
    return user

@router.put('/{user_id}', response_model=User)
def update_existing_user(user_id: int, user_in: UserUpdate, session: Session = Depends(get_session)):
    user = update_user(session=session, user_id=user_id, user_in=user_in)
    if user is None:
        raise HTTPException(status_code=404, detail="User does not exist.")
    return user

@router.delete("/{user_id}")
def remove_user(user_id: int, session: Session = Depends(get_session)):
    success = delete_user(session=session, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User does not exist.")