import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter
from app.core.config import settings
from loguru import logger 

redis_client = None

async def init_redis():
    global redis_client
    try:
        redis_client = redis.from_url(
            settings.REDIS_URL, 
            encoding="utf-8", 
            decode_responses=True
        )
        await FastAPILimiter.init(redis_client)
    
        logger.success(f"✅ Redis Connected: {settings.REDIS_URL}") 
        
    except Exception as e:

        logger.error(f"❌ Redis Init Failed: {e}")
        raise e

async def close_redis():
    global redis_client
    if redis_client:
        await redis_client.close()
        logger.info("🔒 Redis Connection Closed") 