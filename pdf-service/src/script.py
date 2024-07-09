import os
import boto3
import error
import asyncio
from aws_sqs import process_sqs_message

sqs = boto3.client(
    'sqs',
)

s3 = boto3.client(
    's3',
)

queue_url = os.getenv('QUEUE_URL')
bucket_name = os.getenv('BUCKET_NAME')

if not queue_url:
    raise error.QueueUrlNotSetError()

if not bucket_name:
    raise error.BucketNameNotSetError()

if __name__ == '__main__':
    asyncio.run(process_sqs_message(sqs, s3, queue_url, bucket_name))
