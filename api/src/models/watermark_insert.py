from typing import Optional
from dataclasses import dataclass


@dataclass
class WatermarkInsert:
    y: Optional[float]
    x: Optional[float]
    horizontal_alignment: Optional[str]
    opacity: Optional[float]
    angle: Optional[float]
    text_color: Optional[str]
    text_font: Optional[str]
    text_size: Optional[float]
    image_scale: Optional[float]
    dpi: Optional[int]
