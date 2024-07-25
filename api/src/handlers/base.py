import tornado
from config.logger import logger


class BaseHandler(tornado.web.RequestHandler):

    def initialize(self) -> None:
        self.logger = logger

    def write_error(self, status_code: int, **kwargs) -> None:
        self.set_status(status_code)
