import json
from dataclasses import dataclass, is_dataclass
from tornado_swagger.model import register_swagger_model
from handlers.base import BaseHandler
from middleware.authentication import Authentication
from tornado.web import RequestHandler

from functools import wraps


@dataclass
class GetUploadUrlRequest:
    fileKey: str


def request_body(datacls):
    if not is_dataclass(datacls):
        raise TypeError("The parameter must be a dataclass.")

    def process_request_body(func):
        @wraps(func)
        def wrapper(handler: RequestHandler, *args, **kwargs):
            try:
                body_data = json.loads(handler.request.body)
            except json.JSONDecodeError:
                handler.set_status(400)
                handler.finish({"message": "Invalid JSON"})
                return
            try:
                request_body_instance = datacls(**body_data)
            except TypeError as e:
                handler.set_status(400)
                handler.finish({"message": str(e)})
                return
            handler.data = request_body_instance
            return func(handler, *args, **kwargs)

        return wrapper

    return process_request_body


@Authentication("jwt")
class GetUploadUrl(BaseHandler):

    @request_body(GetUploadUrlRequest)
    def post(self) -> None:
        pass
