from dataclasses import dataclass
from handlers.base import BaseHandler
from middleware.authentication import Authentication
from utils.request_body_validator import request_body_validator
from services.file_service import FileService


@dataclass
class GetUploadUrlRequest:
    fileKey: str


@Authentication("jwt")
class GetUploadUrl(BaseHandler):

    def initialize(self) -> None:
        super().initialize()
        self.file_service = FileService()

    @request_body_validator(GetUploadUrlRequest)
    async def post(self) -> None:
        body: GetUploadUrlRequest = self.data
        response = await self.file_service.create_presigned_url_async(body.fileKey)
        if response:
            self.success(response)
        else:
            self.error("Failed to get upload url")
