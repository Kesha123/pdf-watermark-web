import os
from config.logger import logger
from errors.environment_not_set import EnvironmentNotSetError
from dataclasses import dataclass


@dataclass
class Environment:
    PORT: str
    DEBUG: bool
    COGNITO_USER_POOL_ID: str
    COGNITO_REGION: str
    COGNITO_AUDIENCE: str


def get_environment() -> Environment:
    try:
        return Environment(
            PORT=os.getenv('PORT'),
            DEBUG=os.getenv('DEBUG', 'False').lower() in ('true', '1', 't'),
            COGNITO_USER_POOL_ID=os.getenv('COGNITO_USER_POOL_ID'),
            COGNITO_REGION=os.getenv('COGNITO_REGION'),
            COGNITO_AUDIENCE=os.getenv('COGNITO_AUDIENCE'),
        )
    except Exception as e:
        logger.error(e)
        raise EnvironmentNotSetError()


environment = get_environment()
