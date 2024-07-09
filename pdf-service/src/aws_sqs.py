from enum import Enum
from typing import Union, Optional
from dataclasses import dataclass
import botocore.client
import error
from pdf_watermark import WaterMarkInsert, WaterMarkGrid
from aws_sqs import SQSMessage, WaterMarkType
from pdf_watermark import apply_watermark


class WaterMarkType(Enum):
    INSERT = 'insert'
    GRID = 'grid'


@dataclass
class SQSMessage:
    type: WaterMarkType
    parammeters: Union[WaterMarkInsert, WaterMarkGrid]
    input_file: str
    watermark_data: str
    output_file: str


async def process_sqs_message(sqs: botocore.client.BaseClient, queue_url: str) -> None:
    while True:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=20
        )

        if 'Messages' in response:
            for message in response['Messages']:
                message_data = SQSMessage(**message['Body'])

                match message_data.type:
                    case WaterMarkType.INSERT:
                        parameters = WaterMarkInsert(**message_data.parammeters)
                    case WaterMarkType.GRID:
                        parameters = WaterMarkGrid(**message_data.parammeters)
                    case _:
                        raise error.InvalidWatermarkTypeError()

                output_file = await apply_watermark(message_data.type, parameters)

                sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=message['ReceiptHandle']
                )
        else:
            print('No messages received')