import sys
from loguru import logger
from datetime import datetime, timedelta, timezone

def setup_logging():

    def vietnam_time_patcher(record):
        vn_tz = timezone(timedelta(hours=7))
        record["time"] = record["time"].astimezone(vn_tz)

    logger.remove()

    logger.configure(patcher=vietnam_time_patcher) 

    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO",
        colorize=True
    )

    logger.add(
        "logs/app.log",
        rotation="10 MB", 
        retention="10 days", 
        compression="zip",   
        level="INFO"
    )

    return logger