import logging
import os
import sys

from loguru import logger

from shared.config import settings


class InterceptHandler(logging.Handler):
    """
    Default handler from examples in loguru documentaion.
    See https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
    """

    def emit(self, record: logging.LogRecord):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back  # type: ignore
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logger():
    # --- перенаправляем вывод sqlalchemy и uvicorn в loguru
    loggers = (
        logging.getLogger(name)
        for name in logging.root.manager.loggerDict
        if name.startswith("uvicorn.") or name.startswith("sqlalchemy.")
    )

    intercept_handler = InterceptHandler()
    for replaced_logger in loggers:
        replaced_logger.handlers = []
    logging.getLogger("sqlalchemy").handlers = [intercept_handler]
    logging.getLogger("uvicorn").handlers = [intercept_handler]
    logging.getLogger("uvicorn.access").handlers = [intercept_handler]
    # ---

    fmt = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"  # noqa: E501
    config = {
        "handlers": [
            {
                "sink": sys.stdout,
                "format": fmt,
                "level": 'INFO',
                "enqueue": True,
                "colorize": True,
            },
        ]
    }
    if settings.logging_dir:
        logging_file = os.path.join(settings.logging_dir, 'log.log')
        file_handler = {
            "sink": logging_file,
            "format": fmt,
            "level": 'INFO',
            "enqueue": True,
            "serialize": False,
            "rotation": "5 MB",
        }
        config["handlers"].append(file_handler)

    logger.configure(**config)
