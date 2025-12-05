from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import json
import asyncio 
from app.core.config import settings
from loguru import logger
from opentelemetry.propagate import inject

# Biến global
kafka_producer = None

async def init_kafka():
    global kafka_producer
    retries = 5
    
    while retries > 0:
        try:
            logger.info(f"🔄 Connecting to Kafka at {settings.KAFKA_BOOTSTRAP_SERVERS}...")
            kafka_producer = AIOKafkaProducer(
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS
            )
            await kafka_producer.start()
            logger.success("✅ Kafka Producer Started Successfully")
            return # Thoát hàm nếu thành công
            
        except Exception as e:
            retries -= 1
            logger.warning(f"⚠️ Kafka connection failed: {e}")
            logger.info(f"⏳ Retrying in 5 seconds... ({retries} attempts left)")
            await asyncio.sleep(5)
            
    # Nếu hết 5 lần vẫn lỗi thì mới chịu thua
    logger.error("❌ Could not connect to Kafka after multiple retries.")
    # Không raise exception để App vẫn chạy (nhưng mất tính năng Kafka)

async def close_kafka():
    if kafka_producer:
        await kafka_producer.stop()
        logger.warning("🛑 Kafka Producer Stopped")

async def send_message(topic: str, message: dict):
    if not kafka_producer:
        logger.error("Kafka producer not initialized")
        return
    try:
        # 1. Tạo biến chứa Header
        headers = {}
        
        # 2. Tiêm Trace Context hiện tại vào biến headers
        # (Nó sẽ tự thêm key 'traceparent' chứa TraceID)
        inject(headers)
        
        # 3. Code logic gửi tin nhắn (Có update)
        value_json = json.dumps(message).encode('utf-8')
        
        # aiokafka yêu cầu header là list of tuples: [('key', b'value')]
        # Ta cần chuyển đổi dict headers sang format này
        kafka_headers = [(k, v.encode('utf-8')) for k, v in headers.items()]

        # 4. Gửi kèm Headers
        await kafka_producer.send_and_wait(topic, value_json, headers=kafka_headers)
        
        logger.info(f"📤 Sent to [{topic}] with TraceID: {message}")
        
    except Exception as e:
        logger.error(f"❌ Failed to send kafka message: {e}")