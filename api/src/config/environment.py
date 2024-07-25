import os
from config.logger import logger
from errors.environment_not_set import EnvironmentNotSetError
from dataclasses import dataclass


@dataclass
class Environment:
    PORT: str
    DEBUG: bool


def get_environment() -> Environment:
    try:
        return Environment(
            PORT=os.getenv("PORT"),
            DEBUG=os.getenv("DEBUG", "False").lower() in ("true", "1", "t"),
        )
    except Exception as e:
        logger.error(e)
        raise EnvironmentNotSetError()


environment = get_environment()
