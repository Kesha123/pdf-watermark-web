from pdf_watermark.handler import add_watermark_from_options
from pdf_watermark.options import (
    DrawingOptions,
    FilesOptions,
    GridOptions,
    InsertOptions,
)
from models.watermark_create_request import WatermarkCreateRequest
from models.watermark_type import WatermarkType
from models.watermark_data_type import WatermarkDataType
import boto3
import os


BUCKET_NAME = os.environ["BUCKET_NAME"]


class DEFAULTS:
    angle = 45
    dpi = 300
    horizontal_alignment = "center"
    horizontal_boxes = 3
    image_scale = 1
    margin = False
    opacity = 0.1
    save_as_image = False
    text_color = "#000000"
    text_font = "Helvetica"
    text_size = 12
    unselectable = False
    vertical_boxes = 6
    x = 0.5
    y = 0.5


def lambda_handler(event, context):
    s3 = boto3.client("s3")

    payload = WatermarkCreateRequest(**event)

    input_file_key = payload.input_file_key
    output_file_key = payload.output_file_key
    input_file = f"/tmp/{input_file_key.split('/')[-1]}"
    output_file = f"/tmp/{output_file_key.split('/')[-1]}"

    s3.download_file(BUCKET_NAME, input_file_key, input_file)

    file_options = FilesOptions(
        input=input_file,
        output=output_file,
    )

    match payload.watermark_data_type:
        case WatermarkDataType.IMAGE:
            watermark_payload = payload.watermark_image_key
            s3.download_file(
                BUCKET_NAME,
                watermark_payload,
                f"/tmp/{watermark_payload.split('/')[-1]}",
            )
            watermark_payload = f"/tmp/{watermark_payload.split('/')[-1]}"
        case WatermarkDataType.TEXT:
            watermark_payload = payload.watermark_text

    drawing_options = DrawingOptions(
        watermark=watermark_payload,
        opacity=payload.parameters.opacity or DEFAULTS.opacity,
        angle=payload.parameters.angle or DEFAULTS.angle,
        text_color=payload.parameters.text_color or DEFAULTS.text_color,
        text_font=payload.parameters.text_font or DEFAULTS.text_font,
        text_size=payload.parameters.text_size or DEFAULTS.text_size,
        unselectable=payload.parameters.unselectable or DEFAULTS.unselectable,
        image_scale=payload.parameters.image_scale or DEFAULTS.image_scale,
        dpi=payload.parameters.dpi or DEFAULTS.dpi,
        save_as_image=DEFAULTS.save_as_image,
    )

    match payload.watermark_type:
        case WatermarkType.GRID:
            specific_options = GridOptions(
                horizontal_boxes=payload.parameters.horizontal_boxes
                or DEFAULTS.horizontal_boxes,
                vertical_boxes=payload.parameters.vertical_boxes
                or DEFAULTS.vertical_boxes,
                margin=payload.parameters.margin or DEFAULTS.margin,
            )
        case WatermarkType.INSERT:
            specific_options = InsertOptions(
                x=payload.parameters.x or DEFAULTS.x,
                y=payload.parameters.y or DEFAULTS.y,
                horizontal_alignment=payload.parameters.horizontal_alignment
                or DEFAULTS.horizontal_alignment,
            )

    add_watermark_from_options(
        file_options,
        drawing_options,
        specific_options,
    )

    s3.upload_file(output_file, BUCKET_NAME, output_file_key)
