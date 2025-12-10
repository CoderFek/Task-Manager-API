from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import Session
from app.schemas.task import TaskCreate, Task, TaskUpdate
from app.task_manager.task import create_task, get_tasks, get_task_by_id, update_task, delete_task
from app.db.database import get_session

router = APIRouter()

@router.get("/", response_model=List[Task])
def read_tasks(session: Session = Depends(get_session)):
    return get_tasks(session=session)

@router.post("/", response_model=Task)
def create_new_task(task_in: TaskCreate, session: Session = Depends(get_session)):
    return create_task(session=session, task_in=task_in)

@router.get("/{task_id}", response_model=Task)
def read_task(task_id: int, session: Session = Depends(get_session)):
    task = get_task_by_id(session=session, task_id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found :(")
    return task

@router.put("/{task_id}", response_model=Task)
def update_old_task(task_id: int, task_in: TaskUpdate, session: Session = Depends(get_session)):
    task = update_task(session=session, task_id=task_id, task_in=task_in)
    if task is None:
        raise HTTPException(status_code=404, detail="Task does not exist!")
    return task

@router.delete("/{task_id}")
def remove_task(task_id: int, session: Session = Depends(get_session)):
    success = delete_task(session=session,task_id=task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task does not exist!")