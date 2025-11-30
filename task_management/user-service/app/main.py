from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from app.routers import login, users
from .db import engine
from .models import Base
from .models import user as user_model

Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Service", root_path="/user")

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

@app.get("/health", tags=["System"])
def health_check():
    return JSONResponse(content={"status": "ok", "service": "user-service"}, status_code=200)

