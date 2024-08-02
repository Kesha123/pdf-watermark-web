from tornado_swagger.model import register_swagger_model


@register_swagger_model
class GetHealthModel:
    """
    ---
    type: object
    properties:
        status:
            type: string
            example: "ok"
    """
