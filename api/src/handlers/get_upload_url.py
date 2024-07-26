from dataclasses import dataclass
from handlers.base import BaseHandler
from middleware.authentication import Authentication
from utils.request_body_validator import request_body_validator


@dataclass
class GetUploadUrlRequest:
    fileKey: str


@Authentication("jwt")
class GetUploadUrl(BaseHandler):

    @request_body_validator(GetUploadUrlRequest)
    def post(self) -> None:
        self.logger.debug(self.data)
        self.finish()
