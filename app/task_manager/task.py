from app.schemas.task import TaskCreate, Task, TaskUpdate
from typing import Optional, List
from sqlmodel import Session, select
from app.db.models import DBtask



def create_task(session: Session, task_in: TaskCreate, owner_id: int) -> DBtask:
    db_task = DBtask.model_validate(**task_in.model_dump(), owner_id=owner_id)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task
#The router will implicitly convert the returned DBtask (which inherits from SQLModel/Pydantic) 
# to the response schema (Task) because of the 'from_attributes=True' config.

def get_tasks(session: Session) -> List[DBtask]:
    query = select(DBtask)
    tasks = session.exec(query).all()
    return tasks

def get_task_by_id(session: Session, task_id: int) -> Optional[DBtask]:
    query = select(DBtask).where(DBtask.id == task_id)
    db_task = session.exec(query).first()
    if db_task is not None:
        return db_task
    return None

def update_task(session: Session, task_id: int, task_in: TaskUpdate) -> Optional[DBtask]:
    db_task = get_task_by_id(task_id)
    if db_task is None:
        return None
    update_data = task_in.model_dump(exclude_unset = True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

def delete_task(session: Session, task_id: int) -> bool:
    db_task = get_task_by_id(session=session, task_id=task_id)
    if db_task is None:
        return False
    session.delete(db_task)
    session.commit()
    return True