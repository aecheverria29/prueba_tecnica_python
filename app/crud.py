from sqlalchemy.orm import Session
from fastapi import HTTPException
from passlib.context import CryptContext
from . import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

#USUARIOS
#Creacion de usuarios
def create_user(db: Session, user: schemas.UserCreate):
    found = db.query(models.User).filter(models.User.email == user.email).first()
    if found:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    db_user = models.User(
        name=user.name,
        email=user.email,
        password=get_password_hash(user.password) 
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#Obtener todos los usuarios
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

#Obtener usuario por ID
def get_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

#Actualizar usuario
def update_user(db: Session, user_id: int, user_in: schemas.UserUpdate):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if user_in.email and user_in.email != user.email:
        exists = db.query(models.User).filter(models.User.email == user_in.email).first()
        if exists:
            raise HTTPException(status_code=404, detail="Email registrado anteriormente")
        user.email = user_in.email
    if user_in.name:
        user.name = user_in.name
    if user_in.password:
        user.password = get_password_hash(user_in.password)
    db.commit()
    db.refresh(user)
    return user

#Eliminar usuario
def delete_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(user)
    db.commit()
    return {"ok": True}

#TASKS
#Creacion Tasks
def create_task(db: Session, user_id: int, task_in: schemas.TaskCreate):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db_task = models.Task(
        title=task_in.title,
        description=task_in.description,
        status=task_in.status,
        user_id=user_id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

#Obtener tareas, por usuario
def get_tasks_by_user(db: Session, user_id: int, skip: int=0, limit: int=100):
    return db.query(models.Task).filter(models.Task.user_id == user_id).offset(skip).limit(limit).all()

#Actualizar la tarea
def update_task(db: Session, task_id: int, task_in: schemas.TaskUpdate):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    if task_in.title is not None:
        task.title = task_in.title
    if task_in.description is not None:
        task.description = task_in.description
    if task_in.status is not None:
        task.status = task_in.status
    db.commit()
    db.refresh(task)
    return task

#Eliminar tarea
def delete_task(db: Session, task_id: int):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    db.delete(task)
    db.commit()
    return {"ok": True}  