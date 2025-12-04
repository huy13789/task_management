from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from contextlib import asynccontextmanager

# Import các router
from app.routers import login, users, admin
from app.core.config import settings

# Import DB
from .db import engine, SessionLocal
from .db.init_db import init_db
from .models import Base

# Import Redis & Logging
from app.core.redis import init_redis, close_redis
from app.core.logging import setup_logging

# --- QUAN TRỌNG: Import thư viện Rate Limit ---
from fastapi_limiter.depends import RateLimiter
from prometheus_fastapi_instrumentator import Instrumentator

logger = setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting application...")

    # 1. Init Database
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        init_db(db)
        logger.success("✅ Database Initialized")
    except Exception as e:
        logger.error(f"❌ Database Init Failed: {e}")
    finally:
        db.close()

    await init_redis()

    yield 

    logger.warning("🛑 Shutting down application...")
    
    await close_redis() 

app = FastAPI(
    title="User Service",
    description="Service quản lý User", 
    root_path="/user", 
    lifespan=lifespan
)

# Prometheus Monitoring
Instrumentator().instrument(app).expose(app)

# CORS
origins = ["http://localhost:3000", "*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ROUTER ---
app.include_router(login.router, prefix="/api/v1") 
app.include_router(users.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")


async def get_user_id_demo(request: Request):
    # ID from header x-user-id hoặc IP nếu header không tồn tại
    return request.headers.get("x-user-id", "ip:" + request.client.host)

# Limiter: 2 requests / 1 min user/IP
@app.get("/test-rate-limit", dependencies=[Depends(RateLimiter(times=2, seconds=60, identifier=get_user_id_demo))])
async def demo_rate_limit():
    return {"message": "Chúc mừng! Bạn chưa bị chặn (Status 200)."}


# --- SYSTEM HEALTH ---
@app.get("/health", tags=["System"])
def health_check():
    return JSONResponse(content={"status": "ok", "service": "user-service"}, status_code=200)