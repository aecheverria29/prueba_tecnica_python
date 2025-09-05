from pydantic import BaseModel, EmailStr, constr
from typing import Optional, List
from datetime import datetime
import enum 

class TaskStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[TaskStatus] = TaskStatus.pending

class TaskUpdate(BaseModel):
    title: Optional
    description: Optional[str]
    status: Optional[TaskStatus] = TaskStatus.pending

class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    user_id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True #Objetos

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: constr(min_length=6)

class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[constr(min_length=6)]

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime
    tasks: Optional[List[TaskOut]] = []
    class Config:
        orm_mode = True #Objetos
