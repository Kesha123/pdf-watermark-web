from errors.invalid_watermark_data_type import InvalidWatermarkDatatype
from errors.watermark_generate_error import WatermarkGenerateError
from handlers.base import BaseHandler
from middleware.authentication import Authentication
from models.watermark_create_request import WatermarkCreateRequest
from models.watermark_data_type import WatermarkDataType
from utils.request_body_validator import request_body_validator
from swagger.watermark import WatermarkCreateRequestModel


@Authentication("jwt")
class WatermarkImage(BaseHandler):

    @request_body_validator(WatermarkCreateRequest)
    async def post(self) -> None:
        """
        Apply image watermark

        ---
        tags:
        - Watermark
        summary: Apply image watermark
        description: This endpoint applies a image watermark to pdf file.
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
                        output_file_key:
                            type: string
                            description: The key of the output file with the applied watermark
            400:
                description: Invalid watermark data type
        """
        data: WatermarkCreateRequest = self.request.data
        if data.watermark_data_type != WatermarkDataType.IMAGE:
            self.set_status(400)
            raise InvalidWatermarkDatatype()
        response = await self.watermark_service.watermark_text_async(data)
        if response:
            self.success(response)
        else:
            raise WatermarkGenerateError()
