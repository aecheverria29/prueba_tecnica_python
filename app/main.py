from fastapi import FastAPI
from .database import engine, Base
from .routers import users, tasks

app = FastAPI(title="Prueba Técnica - Users & Tasks")

app.include_router(users.router)
app.include_router(tasks.router)

Base.metadata.create_all(bind=engine)
