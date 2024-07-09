import asyncio
from typing import Optional
from dataclasses import dataclass, asdict
from aws_sqs import SQSMessage


@dataclass
class WaterMarkInsert:
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


@dataclass
class WaterMarkGrid:
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


async def apply_watermark(sqs_message: SQSMessage):
    parameters_dict = asdict(sqs_message.parameters)
    default_parameters = [
        'watermark',
        sqs_message.type.value,
        sqs_message.input_file,
        sqs_message.watermark_data,
        '-s',
        f'/tmp/{sqs_message.outputfile}'
    ]
    parameters_list = []
    for flag, parameter in parameters_dict.items():
        if parameter is not None:
            parameters_list.append('--' + '-'.join(flag.split('_')))
            parameters_list.append(parameter)
    default_parameters.extend(parameters_list)

    proc = asyncio.create_subprocess_exec(
        *default_parameters,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()

    if proc.returncode != 0:
        print(f"Error: {stderr.decode()}")
    else:
        print(f"Output: {stdout.decode()}")