import json
from botocore.exceptions import ClientError
from botocore.client import BaseClient
from config.environment import environment
from config.logger import logger
import tornado.ioloop
from config.async_executor import executor
from models.watermark_create_request import WatermarkCreateRequest
from utils.singleton import singleton
from dataclasses import asdict


@singleton
class WatermarkService:
    def __init__(self, s3_client: BaseClient, lambda_client: BaseClient) -> None:
        self.__s3_client = s3_client
        self.__lambda_client = lambda_client
        self.__s3_bucket_name = environment.S3_BUCKET_NAME
        self.__s3_bucket_region = environment.S3_BUCKET_REGION
        self.__function_name = environment.WATERMARK_LAMBDA_FUNCTION_NAME

    def __watermark(self, data: WatermarkCreateRequest) -> str:
        try:
            payload = json.dumps(asdict(data))
            response = self.__lambda_client.invoke(
                FunctionName=self.function_name,
                InvocationType="RequestResponse",
                Payload=payload.encode("utf-8"),
            )
        except ClientError as e:
            logger.error(e)
        return response

    async def watermark_async(self, data: WatermarkCreateRequest) -> str:
        """
        Invokes lambda function which generates watermark on pdf and returns S3 object key of the watermarked pdf
        :param data: WatermarkCreateRequest
        :return: str
        """
        loop = tornado.ioloop.IOLoop.current()
        response = await loop.run_in_executor(
            executor,
            self.__watermark,
            data,
        )
        return response
