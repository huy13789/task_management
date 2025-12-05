import sys
import logging
from loguru import logger
from datetime import datetime, timedelta, timezone
from opentelemetry import trace

# 1. Class này chịu trách nhiệm "bắt cóc" log của Uvicorn/FastAPI
class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Lấy level tương ứng của Loguru
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Tìm vị trí nơi log được gọi (để in ra tên file/dòng code đúng)
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        # Chuyển log sang Loguru
        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )

def setup_logging():
    # --- CẤU HÌNH FILTER & PATCHER (GIỮ NGUYÊN CỦA BẠN) ---
    def correlation_id_filter(record):
        # 1. LỌC RÁC: Nếu log chứa /metrics hoặc /health -> Bỏ qua luôn
        msg = record["message"]
        if "GET /metrics" in msg or "GET /health" in msg:
            return False 

        # 2. LOGIC CŨ: Lấy TraceID (Giữ nguyên)
        span = trace.get_current_span()
        if span:
            ctx = span.get_span_context()
            if ctx.is_valid:
                record["extra"]["trace_id"] = format(ctx.trace_id, "032x")
            else:
                record["extra"]["trace_id"] = "N/A"
        else:
            record["extra"]["trace_id"] = "N/A"
        return True

    def vietnam_time_patcher(record):
        vn_tz = timezone(timedelta(hours=7))
        record["time"] = record["time"].astimezone(vn_tz)

    # --- CẤU HÌNH LOGURU ---
    logger.remove()
    logger.configure(patcher=vietnam_time_patcher)

    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<magenta>[{extra[trace_id]}]</magenta> | " # TraceID tự động
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )

    logger.add(sys.stderr, format=log_format, level="INFO", colorize=True, filter=correlation_id_filter)
    logger.add("logs/app.log", rotation="10 MB", retention="10 days", compression="zip", level="INFO", format=log_format, filter=correlation_id_filter)

    # --- PHẦN QUAN TRỌNG NHẤT: ĐÁNH CHẶN UVICORN ---
    # Danh sách các logger hệ thống muốn bắt
    loggers = (
        "uvicorn",
        "uvicorn.access",
        "uvicorn.error",
        "fastapi",
    )
    
    # Gắn InterceptHandler vào các logger này
    logging.getLogger().handlers = [InterceptHandler()]
    for logger_name in loggers:
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = [InterceptHandler()]
        logging_logger.propagate = False # Không cho in ra console theo kiểu cũ nữa

    return logger