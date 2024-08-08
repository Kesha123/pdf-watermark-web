from errors.invalid_watermark_data_type import InvalidWatermarkDatatype
from handlers.base import BaseHandler
from middleware.authentication import Authentication
from models.watermark_create_request import WatermarkCreateRequest
from models.watermark_data_type import WatermarkDataType
from utils.request_body_validator import request_body_validator


@Authentication("jwt")
class WatermarkText(BaseHandler):

    @request_body_validator(WatermarkCreateRequest)
    async def post(self) -> None:
        """
        Apply text watermark

        ---
        tags:
        - Watermark
        summary: Apply image watermark
        description: This endpoint applies a text watermark to pdf file.
        consumes:
        - application/json
        produces:
        - application/json
        parameters:
        - in: body
          name: body
          required: true
          schema:
            $ref: '#/definitions/WatermarkCreateRequestModel'
        responses:
            200:
                description: Successfully applied watermark
                schema:
                    type: object
                    properties:
                        download_url:
                            type: string
                            description: The download url of the output file with the applied watermark
            400:
                description: Invalid watermark data type
        """
        data: WatermarkCreateRequest = self.data
        if data.watermark_data_type != WatermarkDataType.TEXT.value:
            self.set_status(400)
            raise InvalidWatermarkDatatype()
        download_url = await self.watermark_service.watermark_async(data)
        self.write({"download_url": download_url})
