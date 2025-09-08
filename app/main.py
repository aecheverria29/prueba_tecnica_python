from fastapi import FastAPI
from .database import engine, Base
from .routers import users, tasks

app = FastAPI(title="Prueba Técnica - Users & Tasks")

app.include_router(users.router)
app.include_router(tasks.router)

# Para pruebas rápidas, crear tablas (usar Alembic en producción)
Base.metadata.create_all(bind=engine)
