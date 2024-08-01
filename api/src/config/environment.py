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
    S3_BUCKET_NAME: str
    S3_BUCKET_REGION: str
    WATERMARK_LAMBDA_FUNCTION_NAME: str


def get_environment() -> Environment:
    try:
        return Environment(
            PORT=os.getenv("PORT"),
            DEBUG=os.getenv("DEBUG", "False").lower() in ("true", "1", "t"),
            COGNITO_USER_POOL_ID=os.getenv("COGNITO_USER_POOL_ID"),
            COGNITO_REGION=os.getenv("COGNITO_REGION"),
            COGNITO_AUDIENCE=os.getenv("COGNITO_AUDIENCE"),
            S3_BUCKET_NAME=os.getenv("S3_BUCKET_NAME"),
            S3_BUCKET_REGION=os.getenv("S3_BUCKET_REGION"),
            WATERMARK_LAMBDA_FUNCTION_NAME=os.getenv("WATERMARK_LAMBDA_FUNCTION_NAME"),
        )
    except Exception as e:
        logger.error(e)
        raise EnvironmentNotSetError()


environment = get_environment()
