from tornado_swagger.model import register_swagger_model


@register_swagger_model
class WatermarkCreateRequestModel:
    """
    ---
    type: object
    required:
    - watermark_type
    - parameters
    - input_file_key
    - watermark_data_type
    - output_file_key
    properties:
        watermark_type:
            type: string
        parameters:
            oneOf:
                - $ref: '#/definitions/WatermarkInsertModel'
                - $ref: '#/definitions/WatermarkGridModel'
        input_file_key:
            type: string
        watermark_data_type:
            type: string
        watermark_text:
            type: string
        watermark_image_key:
            type: string
        output_file_key:
            type: string
    """


@register_swagger_model
class WatermarkInsertModel:
    """
    ---
    type: object
    properties:
        y:
            type: number
            format: float
        x:
            type: number
            format: float
        horizontal_alignment:
            type: string
        opacity:
            type: number
            format: float
        angle:
            type: number
            format: float
        text_color:
            type: string
        text_font:
            type: string
        text_size:
            type: number
            format: float
        image_scale:
            type: number
            format: float
        dpi:
            type: integer
            format: int32
    """


@register_swagger_model
class WatermarkGridModel:
    """
    ---
    type: object
    properties:
        horizontal_boxes:
            type: integer
            format: int32
        vertical_boxes:
            type: integer
            format: int32
        margin:
            type: boolean
        opacity:
            type: number
            format: float
        angle:
            type: number
            format: float
        text_color:
            type: string
        text_font:
            type: string
        text_size:
            type: integer
            format: int32
        unselectable:
            type: boolean
        image_scale:
            type: number
            format: float
    """


@register_swagger_model
class InvalidWatermarkDatatypeModel:
    """
    ---
    type: object
    properties:
        message:
            type: string
            description: A message describing the invalid watermark data type error
    """


@register_swagger_model
class WatermarkGenerateErrorModel:
    """
    ---
    type: object
    properties:
        message:
            type: string
            description: A message describing the watermark generation error
    """
