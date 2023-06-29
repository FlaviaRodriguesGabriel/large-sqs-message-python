import boto3
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

        # set max size of a message that will be sent in SQS (SQS limit is 256 kb)
        max_message_size: int = 10

        queue_url: str = sqs_client.get_queue_url(QueueName=queue_name)["QueueUrl"]

        if len(message) > max_message_size:
            # Store the message in S3
            object_key: str = str(uuid.uuid4())
            s3_client.put_object(Body=message, Bucket=bucket_name, Key=object_key)

            # Send SQS message with extended attribute referencing S3 location
            sqs_client.send_message(
                QueueUrl=queue_url,
                MessageBody=f"s3://{bucket_name}/{object_key}",
            )
        else:
            # Send SQS message directly
            sqs_client.send_message(QueueUrl=queue_url, MessageBody=message)
