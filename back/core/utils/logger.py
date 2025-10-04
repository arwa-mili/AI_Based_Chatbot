import logging
from django.utils import timezone

logger = logging.getLogger(__name__)

def exception_log(exception, file: str, log_info: str = "", extra_context: dict | None = None):
    tb_lineno = getattr(exception.__traceback__, "tb_lineno", "N/A")

    logger.error("----------------------- Exception -----------------------")
    logger.error(f"TIME: {timezone.now()}")
    logger.error(f"LOG_INFO: {log_info or 'N/A'}")
    logger.error(f"TYPE: {type(exception).__name__}")
    logger.error(f"FILE: {file}")
    logger.error(f"LINE: {tb_lineno}")
    logger.error(f"DESCRIPTION: {str(exception)}")

    if extra_context:
        for key, value in extra_context.items():
            logger.error(f"{key.upper()}: {value}")

    logger .error("--------------------------------------------------------")