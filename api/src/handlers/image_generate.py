from dataclasses import dataclass
from handlers.base import BaseHandler
from middleware.authentication import Authentication
from utils.request_body_validator import request_body_validator


@dataclass
class ImageGenerateRequest:
    fileKey: str


@Authentication("jwt")
class ImageGenerate(BaseHandler):

    @request_body_validator(ImageGenerateRequest)
    def post(self) -> None:
        self.logger.debug(self.data)
        self.finish()
