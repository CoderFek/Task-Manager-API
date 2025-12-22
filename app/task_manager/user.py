from app.schemas.user import UserCreate, User, UserUpdate
from sqlmodel import Session, select
from typing import Optional, List
from app.db.models import DBuser

def create_user(session: Session, user_in: UserCreate) -> User:
    db_user = DBuser.model_validate(user_in)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def get_user_by_id(session: Session, user_id: int) -> Optional[DBuser]:
    query = select(DBuser).where(DBuser.id == user_id)
    db_user = session.exec(query).first()
    if db_user is not None:
        return db_user
    return None

def get_users(session: Session) -> List[DBuser]:
    query = select(DBuser)
    users = session.exec(query).all()
    return users

def update_user(session: Session, user_id: int, user_in: UserUpdate) -> Optional[DBuser]:
    db_user = get_user_by_id(session=session, user_id=user_id)
    if db_user is None:
        return None
    update_data = user_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def delete_user(session: Session, user_id: int) -> bool:
    db_user = get_user_by_id(session=session, user_id=user_id)
    if db_user is None:
        return False
    session.delete(db_user)
    session.commit()
    return True