import asyncio
import json
from aiokafka import AIOKafkaConsumer
from loguru import logger
import os
from opentelemetry import trace
from opentelemetry.propagate import extract

# Lấy địa chỉ Kafka từ biến môi trường
KAFKA_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:29092")
TOPIC_NAME = "user_events"

tracer = trace.get_tracer(__name__)

async def consume_loop():
    retries = 5
    consumer = None
    
    # 1. Cơ chế Retry kết nối (Cho chắc ăn)
    while retries > 0:
        try:
            logger.info(f"🔄 Connecting to Kafka Consumer at {KAFKA_SERVER}...")
            consumer = AIOKafkaConsumer(
                TOPIC_NAME,
                bootstrap_servers=KAFKA_SERVER,
                group_id="notification_group",
                auto_offset_reset="earliest"
            )
            await consumer.start()
            logger.success("✅ Kafka Consumer Started & Listening...")
            break
        except Exception as e:
            retries -= 1
            logger.warning(f"⚠️ Kafka not ready, retrying in 5s... ({retries} left)")
            await asyncio.sleep(5)
            
    if not consumer:
        logger.error("❌ Failed to start Kafka Consumer")
        return

    try:
        async for msg in consumer:
            # 1. Trích xuất Headers từ Kafka Message
            # Convert từ list tuples sang dict để OTel hiểu
            headers_dict = {k: v.decode('utf-8') for k, v in msg.headers}
            
            # 2. Lấy Context (TraceID cũ) từ headers
            ctx = extract(headers_dict)

            # 3. Bắt đầu Span mới NHƯNG kế thừa từ Context cũ (Dùng 'context=ctx')
            with tracer.start_as_current_span("process_kafka_message", context=ctx) as span:
                try:
                    payload = json.loads(msg.value.decode("utf-8"))
                    event_type = payload.get("event")
                    
                    # Thêm thông tin vào Trace cho dễ debug
                    span.set_attribute("event.type", event_type)
                    span.set_attribute("kafka.topic", msg.topic)

                    if event_type == "USER_CREATED":
                        user_email = payload.get("email")
                        user_id = payload.get("user_id")
                        
                        logger.info(f"📨 Processing Event for User {user_id}")
                        await asyncio.sleep(0.5) 
                        logger.success(f"✅ [EMAIL SENT] To: {user_email}")
                        
                except Exception as e:
                    logger.error(f"❌ Error processing message: {e}")
                    span.record_exception(e) # Ghi lỗi vào Trace luôn
                    span.set_status(trace.Status(trace.StatusCode.ERROR))
                
    finally:
        await consumer.stop()