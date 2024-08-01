import tornado
import boto3
from config.logger import logger
from services.file_service import FileService
from services.watermark_service import WatermarkService


class BaseHandler(tornado.web.RequestHandler):

    def initialize(self) -> None:
        self.logger = logger
        self.__s3_client = boto3.client("s3")
        self.__lambda_client = boto3.client("lambda")
        self.file_service = FileService(self.__s3_client)
        self.watermark_service = WatermarkService(
            self.__s3_client, self.__lambda_client
        )

    def write_error(self, status_code: int, **kwargs) -> None:
        self.set_status(status_code)
