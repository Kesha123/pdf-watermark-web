import logging
from python_logger.Logger import Logger
from python_logger.handlers import HandlerLevel, StreamHandler


handlers = HandlerLevel(
    stream=StreamHandler(level=logging.DEBUG),
)

logger = Logger(handlers=handlers)
