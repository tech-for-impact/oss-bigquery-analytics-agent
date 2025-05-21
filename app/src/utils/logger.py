import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
import sys

# 1. Create log directory
# TODO: 마이그레이션 대상 프로젝트의 로그 디렉토리 구조에 맞게 수정 필요
LOG_DIR = Path("./logs") # 현재는 워크스페이스 루트의 logs 디렉토리를 사용

# 2. Create directory if it doesn't exist
LOG_DIR.mkdir(exist_ok=True)

# 3. Set logger level to DEBUG(not show INFO level)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 4. Configure handlers for console and file output
console_handler = logging.StreamHandler()
file_handler = TimedRotatingFileHandler(
    filename=str(LOG_DIR / "server.log"),
    when="midnight",  # Create new file at midnight
    interval=1,       # Create new file every day
    # backupCount=7,  # Keep last 7 days logs
    encoding="utf-8"  # File encoding
)

# 5. Set log format (e.g., [2024-03-20 12:00:00] DEBUG >> app.py:123 - message)
formatter = logging.Formatter(
    '[%(asctime)s] %(levelname)-8s >> %(filename)s:%(lineno)d - %(message)s'
)

# 6. Apply formatter to handlers
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# 7. Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# 8. Configure exception handling
def handle_exception(exc_type, exc_value, exc_traceback):
    """Catch exception when unexpected exceptions occur.
    ※ do not close server!

    Args:
        exc_type (type): Exception type.
        exc_value (BaseException): Exception value.
        exc_traceback (TracebackType): Exception traceback.
    """

    # Handle Ctrl+C as normal termination
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    # Log other exceptions as CRITICAL
    logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

# Set system exception hook
sys.excepthook = handle_exception 