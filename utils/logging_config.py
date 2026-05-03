import sys
from loguru import logger
from config import settings

def setup_logging():
    logger.remove()  # remove default handler

    logger.add(
        "app.log",
        level=settings.LOGGING.LEVEL,
        rotation="10 MB",
        retention="30 days",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    )

    # 2. Console logs
    logger.add(
        sys.stderr,
        level=settings.LOGGING.LEVEL,
        format="<green>{time:HH:mm:ss}</green> | <level>{message}</level>"
    )

    # 3. JSON logs
    logger.add(
        "events.jsonl",
        serialize=True,
        rotation="5 MB",
        retention="14 days"
    )
