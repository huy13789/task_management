from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio

# Import các module đã copy và viết mới
from app.core.logging import setup_logging
from app.core.tracing import setup_tracing
from app.core.kafka_consumer import consume_loop
from prometheus_fastapi_instrumentator import Instrumentator
from loguru import logger

# Setup Logging trước tiên
setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Notification Service Starting...")
    
    # Chạy Consumer trong Background Task (Không chặn API)
    loop = asyncio.get_event_loop()
    consumer_task = loop.create_task(consume_loop())
    
    yield
    
    # Dọn dẹp khi tắt
    logger.warning("🛑 Notification Service Stopping...")
    consumer_task.cancel()

app = FastAPI(
    title="Notification Service",
    lifespan=lifespan
)

# 1. Setup Tracing
setup_tracing(app)

# 2. Setup Metrics
Instrumentator(
    excluded_handlers=["/metrics", "/health", "/docs"]
).instrument(app).expose(app)

@app.get("/")
def read_root():
    return {"message": "Notification Service is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}