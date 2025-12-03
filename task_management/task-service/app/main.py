from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

# Import Database Engine
from .db import engine
from .models import Base
from .routers import board

from .models import task as task_model

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
    print("🛑 Task Service Stopping...")

app = FastAPI(
    title="Task Service",
    description="Service quản lý công việc (Kanban Board)",
    version="1.0.0",
    root_path="/task",
    lifespan=lifespan
)

# --- MIDDLEWARE ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(board.router, prefix="/api/v1")


# --- SYSTEM API ---
@app.get("/health", tags=["System"])
def health_check():
    return JSONResponse(
        content={"status": "ok", "service": "task-service", "db": "task_db"}, 
        status_code=200
    )