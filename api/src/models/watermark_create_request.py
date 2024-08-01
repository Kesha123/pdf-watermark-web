from dataclasses import dataclass
from typing import Union, Optional

from models.watermark_data_type import WatermarkDataType
from models.watermark_grid import WatermarkGrid
from models.watermark_insert import WatermarkInsert
from models.watermark_type import WatermarkType


@dataclass
class WatermarkCreateRequest:
    watermark_type: WatermarkType
    parammeters: Union[WatermarkInsert, WatermarkGrid]
    input_file_key: str
    watermark_data_type: WatermarkDataType
    watermark_text: Optional[str]
    watermark_image_key: Optional[str]
    output_file_key: str
