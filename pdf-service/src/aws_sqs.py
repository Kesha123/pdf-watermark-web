from enum import Enum
from typing import Union
from dataclasses import dataclass
import botocore.client
from pdf_watermark import WaterMarkInsert, WaterMarkGrid
from aws_sqs import SQSMessage, WaterMarkType
from pdf_watermark import apply_watermark
import error


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


async def process_sqs_message(
        sqs: botocore.client.BaseClient,
        s3: botocore.client.BaseClient,
        queue_url: str,
        bucket: str
    ) -> None:
    while True:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=20
        )

        if 'Messages' in response:
            for message in response['Messages']:
                message_data = SQSMessage(**message['Body'])

                if not message_data.type in WaterMarkType:
                    raise error.InvalidWatermarkTypeError()

                await apply_watermark(message_data)

                s3.upload_file(
                    f'/tmp/{message_data.output_file}',
                    bucket,
                    'output/{message_data.output_file}'
                )

                sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=message['ReceiptHandle']
                )
        else:
            print('No messages received')