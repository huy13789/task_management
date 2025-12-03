from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from app.routers import login, users, admin
from .db import engine
from .models import Base
from .models import user as user_model

from contextlib import asynccontextmanager

# Import các thành phần cần thiết
from .db import engine, SessionLocal
from .db.init_db import init_db
from .models import Base

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        init_db(db) 
    finally:
        db.close()
    yield 

app = FastAPI(title="User Service",description="Service quản lý User", root_path="/user", lifespan=lifespan)

# CORS
origins = [
    "http://localhost:3000",
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login.router, prefix="/api/v1") 
app.include_router(users.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")

@app.get("/health", tags=["System"])
def health_check():
    return JSONResponse(content={"status": "ok", "service": "user-service"}, status_code=200)

