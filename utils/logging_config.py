from loguru import logger

logger.remove()  # remove default handler

# 1. File logs
logger.add(
    "app.log",
    level=settings.LOG_LEVEL,
    rotation="10 MB",
    retention="30 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)

# 2. Console logs
logger.add(
    sys.stderr,
    level=settings.LOG_LEVEL,
    format="<green>{time:HH:mm:ss}</green> | <level>{message}</level>"
)

# 3. JSON logs
logger.add(
    "events.jsonl",
    serialize=True,
    rotation="5 MB",
    retention="14 days"
)

# 4. Exception-catching entrypoint
@logger.catch
def main():
    ...
