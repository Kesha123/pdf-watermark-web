from errors.invalid_watermark_data_type import InvalidWatermarkDatatype
from errors.watermark_generate_error import WatermarkGenerateError
from handlers.base import BaseHandler
from middleware.authentication import Authentication
from models.watermark_create_request import WatermarkCreateRequest
from models.watermark_data_type import WatermarkDataType
from utils.request_body_validator import request_body_validator


@Authentication("jwt")
class WatermarkText(BaseHandler):

    @request_body_validator(WatermarkCreateRequest)
    async def post(self) -> None:
        data: WatermarkCreateRequest = self.request.data
        if data.watermark_data_type != WatermarkDataType.TEXT:
            self.set_status(400)
            raise InvalidWatermarkDatatype()
        response = await self.watermark_service.watermark_text_async(data)
        if response:
            self.success(response)
        else:
            raise WatermarkGenerateError()
