import tornado
from tornado_swagger.setup import setup_swagger
from config.logger import logger
from handlers.health import Health
from handlers.get_upload_url import GetUploadUrl
from handlers.watermark_text import WatermarkText
from handlers.watermark_image import WatermarkImage
from handlers.image_generate import ImageGenerate
from config.environment import environment


class Application(tornado.web.Application):
    _routes = [
        tornado.web.url(r"/api/health_", Health, name="health"),
        tornado.web.url(r"/api/watermark/text", WatermarkText, name="watermark-text"),
        tornado.web.url(
            r"/api/watermark/image", WatermarkImage, name="watermark-image"
        ),
        tornado.web.url(r"/api/image-generate", ImageGenerate, name="image-generate"),
        tornado.web.url(
            r"/api/file/get-upload-url", GetUploadUrl, name="get-upload-url"
        ),
    ]

    def log_request(self, handler: tornado.web.RequestHandler) -> None:
        logger.info(f"{handler.get_status()}; {handler._request_summary()};")

    def __init__(self, **kwargs):
        setup_swagger(
            self._routes,
            swagger_url="/api/doc",
            api_base_url="/api",
            description="",
            api_version="1.0.0",
            title="PDF Watermark servcie API",
            contact="innokentiikozlov@gmail.com",
            schemes=["https"],
        )
        super(Application, self).__init__(
            self._routes, debug=environment.DEBUG, **kwargs
        )


class Server:
    def __init__(self, PORT: int, **kwargs) -> None:
        self.app = Application()
        self.app.listen(PORT)
        self.port = PORT

    def get_app(self) -> Application:
        return self.app

    def run(self) -> None:
        print("==============================")
        print(f"Server is running on port {self.port}")
        print("==============================")
        tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    server = Server(PORT=environment.PORT)
    server.run()
