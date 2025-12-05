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

# Import thư viện Rate Limit & Metrics & Tracing
from fastapi_limiter.depends import RateLimiter
from prometheus_fastapi_instrumentator import Instrumentator
from app.core.tracing import setup_tracing
from app.core.kafka import init_kafka, close_kafka

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
    
    await init_kafka()

    # 2. Init Redis
    await init_redis()

    yield 

    logger.warning("🛑 Shutting down application...")
    
    # 3. Close Redis
    await close_redis() 
    await close_kafka()
app = FastAPI(
    title="User Service",
    description="Service quản lý User", 
    root_path="/user", 
    lifespan=lifespan
)


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

# --- 1. SETUP TRACING (OpenTelemetry) ---
setup_tracing(app)

# --- 2. SETUP METRICS (Prometheus) ---
# SỬA LỖI Ở ĐÂY: Gom tất cả excluded_handlers vào 1 list duy nhất
Instrumentator(
    should_group_status_codes=False,
    should_ignore_untemplated=True,
    should_instrument_requests_inprogress=True,
    excluded_handlers=[
        ".*admin.*",
        "/metrics",
        "/health",
        "/docs",
        "/redoc",
        "/openapi.json"
    ]
).instrument(app).expose(app)

# --- RATE LIMITER DEMO ---

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