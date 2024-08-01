from handlers.base import BaseHandler
from middleware.authentication import Authentication
from utils.request_body_validator import request_body_validator
from models.get_upload_url_request import GetUploadUrlRequest
from errors.generate_upload_url_error import GenerateUploadUrlError


@Authentication("jwt")
class GetUploadUrl(BaseHandler):

    @request_body_validator(GetUploadUrlRequest)
    async def post(self) -> None:
        body: GetUploadUrlRequest = self.data
        response = await self.file_service.create_presigned_url_async(body.fileKey)
        if response:
            self.success(response)
        else:
            raise GenerateUploadUrlError()
