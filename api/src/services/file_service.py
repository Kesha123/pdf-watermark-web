from botocore.exceptions import ClientError
from botocore.client import BaseClient
from config.environment import environment
from config.logger import logger
import tornado.ioloop
from config.async_executor import executor
from models.create_preasigned_url import CreatePreasignedUrl
from utils.singleton import singleton
from uuid import uuid4


@singleton
class FileService:
    def __init__(self, boto_client: BaseClient) -> None:
        self.__s3_client = boto_client
        self.__s3_bucket_name = environment.S3_BUCKET_NAME
        self.__s3_bucket_region = environment.S3_BUCKET_REGION

    def __create_presigned_url(
        self, object_name: str, fields=None, conditions=None, expiration=3600
    ) -> CreatePreasignedUrl:
        """Generate a presigned URL S3 POST request to upload a file

        :param bucket_name: string
        :param object_name: string
        :param fields: Dictionary of prefilled form fields
        :param conditions: List of conditions to include in the policy
        :param expiration: Time in seconds for the presigned URL to remain valid
        :return: Dictionary with the following keys:
            url: URL to post to
            fields: Dictionary of form fields and values to submit with the POST
        :return: None if error.
        """
        uuid_identifier = str(uuid4())
        s3_object_key = f"input/{object_name}.{uuid_identifier}"
        try:
            response = self.__s3_client.generate_presigned_post(
                self.__s3_bucket_name,
                s3_object_key,
                Fields=fields,
                Conditions=conditions,
                ExpiresIn=expiration,
            )
        except ClientError as e:
            logger.error(e)
            return None

        return {"url": response, "s3_object_key": s3_object_key}

    async def create_presigned_url_async(
        self, object_name: str, fields=None, conditions=None, expiration=3600
    ) -> CreatePreasignedUrl:
        loop = tornado.ioloop.IOLoop.current()
        response = await loop.run_in_executor(
            executor,
            self.__create_presigned_url,
            object_name,
            fields,
            conditions,
            expiration,
        )
        return response
