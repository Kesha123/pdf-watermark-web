import os
import boto3
import error
import asyncio
from aws_sqs import process_sqs_message

sqs = boto3.client(
    'sqs',
)

queue_url = os.getenv('QUEUE_URL')


if not queue_url:
    raise error.QueueUrlNotSetError()


if __name__ == '__main__':
    asyncio.run(process_sqs_message(sqs, queue_url))