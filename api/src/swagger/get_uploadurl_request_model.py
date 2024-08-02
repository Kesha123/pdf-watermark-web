from tornado_swagger.model import register_swagger_model


@register_swagger_model
class GetUploadUrlRequestModel:
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
