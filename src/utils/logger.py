import sys
from pathlib import Path
from loguru import logger


def setup_logger():
    root_dir = Path(__file__).resolve().parents[2]
    log_dir = root_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "app.log"

    logger.remove()

    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO"
    )

    logger.add(
        str(log_file),
        rotation="10 MB",
        retention="7 days",
        level="DEBUG",
        enqueue=True,
        catch=True
    )

    return logger


log = setup_logger()
