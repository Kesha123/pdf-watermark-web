from handlers.base import BaseHandler
from middleware.authentication import Authentication
from utils.request_body_validator import request_body_validator
from models.get_upload_url_request import GetUploadUrlRequest
from errors.generate_upload_url_error import GenerateUploadUrlError
from tornado_swagger.model import register_swagger_model


@Authentication("jwt")
class GetUploadUrl(BaseHandler):

    @request_body_validator(GetUploadUrlRequest)
    async def post(self) -> None:
        """
        Generate a presigned URL for file upload

        ---
        tags:
        - File Upload
        summary: Generate a presigned URL for file upload
        description: This endpoint generates a presigned URL to which the client can upload a file.
        consumes:
        - application/json
        produces:
        - application/json
        parameters:
        - in: body
          name: body
          required: true
          schema:
            $ref: '#/definitions/GetUploadUrlRequest'
        responses:
            200:
                description: Successfully generated presigned URL
                schema:
                    type: object
                    properties:
                        url:
                            type: string
                            format: uri
                            description: The presigned URL for uploading the file
            400:
                description: Error generating upload URL
        """
        body: GetUploadUrlRequest = self.data
        response = await self.file_service.create_presigned_url_async(body.fileKey)
        if response:
            self.success(response)
        else:
            self.status(400)
            raise GenerateUploadUrlError()


@register_swagger_model
class GetUploadUrlRequest:
    """
    ---
    type: object
    required:
    - fileKey
    properties:
        fileKey:
            type: string
            description: Unique key identifying the file for which to generate the upload URL
    """
