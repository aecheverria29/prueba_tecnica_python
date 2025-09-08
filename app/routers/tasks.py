from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from .. import schemas, crud, database

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/user/{user_id}", response_model=schemas.TaskOut, status_code=status.HTTP_201_CREATED)
def create_task_for_user(user_id: int, task: schemas.TaskCreate, db: Session = Depends(database.get_db)):
    return crud.create_task(db, user_id, task)

@router.get("/user/{user_id}", response_model=list[schemas.TaskOut])
def list_tasks_for_user(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return crud.get_tasks_by_user(db, user_id, skip, limit)

@router.put("/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, task_in: schemas.TaskUpdate, db: Session = Depends(database.get_db)):
    return crud.update_task(db, task_id, task_in)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(database.get_db)):
    crud.delete_task(db, task_id)
    return
