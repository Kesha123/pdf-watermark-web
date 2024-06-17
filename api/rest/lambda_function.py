import os
import json
import boto3
import uuid
from botocore.exceptions import ClientError
import logging


QUEUE_URL = os.getenv('QUEUE_URL')
BUCKET_NAME = os.getenv('BUCKET_NAME')

sqs = boto3.client('sqs')

def lambda_handler(event, context):
    '''
    The main lambda handler
    :param event: The event that triggered the lambda
    :param context: The context of the lambda
    :return: The response of the lambda
    '''
    path = event.get('path')
    match path:
        case '/watermark-text':
            return push_to_sqs(event.get('body'))
        case '/upload-presigned-url':
            return get_presigned_upload_url(BUCKET_NAME, json.loads(event.get('body')).get('file_name'))
        case _:
            return {
                "error": None
            }

def push_to_sqs(message_body):
    '''
    Pushes the event to the SQS queue
    :param event: The event to be pushed to the SQS queue
    :return: The message id of the pushed event
    '''
    response = sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(message_body)
    )
    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": { "Content-Type": "application/json" },
        "body": json.dumps({
            "messageId": response['MessageId']
        })
    }

def get_presigned_upload_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """
    s3_client = boto3.client('s3')
    object_key = object_name.split('.pdf')[0] + '-' + str(uuid.uuid4()) + '.pdf'
    try:
        response = s3_client.\
            generate_presigned_url(
                'put_object',
                Params={
                    'Bucket': bucket_name,
                    'Key': object_key
                },
                ExpiresIn=expiration
            )
    except ClientError as e:
        logging.error(e)
        return None

    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": { "Content-Type": "application/json" },
        "body": json.dumps({
            "upload_url": response
        })
    }