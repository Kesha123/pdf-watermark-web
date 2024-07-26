from dataclasses import dataclass
from handlers.base import BaseHandler
from middleware.authentication import Authentication
from utils.request_body_validator import request_body_validator


@dataclass
class WatermarkTextRequest:
    fileKey: str


@Authentication("jwt")
class WatermarkText(BaseHandler):

    @request_body_validator(WatermarkTextRequest)
    def post(self) -> None:
        self.logger.debug(self.data)
        self.finish()
