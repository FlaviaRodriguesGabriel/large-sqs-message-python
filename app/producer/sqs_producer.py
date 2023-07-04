import boto3
import botocore
from loguru import logger
import uuid


class SqsProducer:
    def create_clients():
        s3_client: s3_client = boto3.client("s3", endpoint_url="http://localhost:4566")
        sqs_client: sqs_client = boto3.client(
            "sqs", endpoint_url="http://localhost:4566"
        )

        return [s3_client, sqs_client]

    def send_large_message(message, s3_client, sqs_client):
        # bucket and queue names
        bucket_name: str = "large-message"
        queue_name: str = "large-message"

        # set max size of a message that will be sent in SQS (SQS limit is 256 kb, but for testing purposes, we are using a much lower threshold)
        max_message_size: int = 10

        queue_url: str = sqs_client.get_queue_url(QueueName=queue_name)["QueueUrl"]

        if len(message) > max_message_size:
            # Store the message in S3
            object_key: str = str(uuid.uuid4())  # Generates a key for a new s3 object
            try:
                s3_client.put_object(Body=message, Bucket=bucket_name, Key=object_key)
            except botocore.exceptions.ClientError as error:
                logger.error("Error while creating new object in S3: {}".format(error))

            # Send SQS message with extended attribute referencing S3 location
            try:
                sqs_client.send_message(
                    QueueUrl=queue_url,
                    MessageBody=f"s3://{bucket_name}/{object_key}",
                )
            except botocore.exceptions.ClientError as error:
                logger.error(
                    "Error while creating new message in SQS: {}".format(error)
                )
        else:
            # When the message is small, send SQS message directly, without S3.
            try:
                sqs_client.send_message(QueueUrl=queue_url, MessageBody=message)
            except botocore.exceptions.ClientError as error:
                logger.error(
                    "Error while creating new message in SQS: {}".format(error)
                )
