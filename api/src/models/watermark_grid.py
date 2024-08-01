from typing import Optional
from dataclasses import dataclass


@dataclass
class WatermarkGrid:
    horizontal_boxes: Optional[int]
    vertical_boxes: Optional[int]
    margin: Optional[bool]
    opacity: Optional[float]
    angle: Optional[float]
    text_color: Optional[str]
    text_font: Optional[str]
    text_size: Optional[int]
    unselectable: Optional[bool]
    image_scale: Optional[float]
