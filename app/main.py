import boto3
import uuid
from botocore.exceptions import ClientError
from mypy_boto3_s3 import Client as S3Client
from mypy_boto3_sqs import Client as SQSClient


bucket_name = "large-message"
large_message_1 = b"1000000000000000000000000100000000000000000000000010000000000000000000000001000000000000000000000000100000000000000000000000010000000000000000000000001000000000000000000000000100000000000000000000000010000000000000000000000001000000000000000000000000100000000000000000000000010000000000000000000000001000000000000000000000000100000000000000000000000010000000000000000000000001000000000000000000000000100000000000000000000000010000000000000000000000001000000000000000000000000100000000000000000000000010000000000000000000000001000000000000000000000000100000000000000000000000010000000000000000000000001000000000000000000000000100000000000000000000000010000000000000000000000001000000000000000000000000100000000000000000000000010000000000000000000000001000000000000000000000000100000000000000000000000010000000000000000000000001000000000000000000000000100000000000000000000000010000000000000000000000001000000000000000000000000100000000000000000000000010000000000000000000000001000000000000000000000000100000000000000000000000010000000000000000000000001000000000000000000000000100000000000000000000000010000000000000000000000001000000000000000000000000100000000000000000000000010000000000000000000000001000000000000000000000000100000000000000000000000010000000000000000000000001000000000000000000000000100000000000000000000000010000000000000000000000001000000000000000000000000100000000000000000000000010000000000000000000000001000000000000000000000000100000000000000000000000010000000000000000000000001000000000000000000000000100000000000000000000000010000000000000000000000001000000000000000000000000100000000000000000000000010000000000000000000000001000000000000000000000000100000000000000000000000010000000000000000000000001000000000000000000000000100000000000000000000000010000000000000000000000001000000000000000000000000100000000000000000000000010000000000000000000000001000000000000000000000000100000000000000000000000010000000000000000000000001000000000000000000000000100000000000000000000000010000000000000000000000001000000000000000000000000"
queue_url = "http://localhost:4566/081378642243/large-message"
message_attributes = {}

session = boto3.session.Session()


# Creates a S3 Session (should be created only once if use in a production environment)
s3: S3Client = session.client(
    service_name="s3",
    region_name="sa-east-1",
    # aws_access_key_id='123456782243',      # Should be set in a production environment
    # aws_secret_access_key='123456',        # Should be set in a production environment
    endpoint_url="http://localhost:4566",
)

# Creates a SQS Session (should be created only once if use in a production environment)
sqs: SQSClient = session.client(
    service_name="sqs",
    region_name="sa-east-1",
    # aws_access_key_id='123456782243',      # Should be set in a production environment
    # aws_secret_access_key='123456',        # Should be set in a production environment
    endpoint_url="http://localhost:4566",
)


# Function that returns the size of a given message
def getMessageSize(s: str) -> int:
    return len(s)


# Function that puts a new object in a S3
def putObjectS3(bucket_name, object):
    try:
        object_name = str(uuid.uuid4()) + ".txt"
        s3.put_object(Bucket=bucket_name, Key=object_name, Body=object)
        return object_name
    except Exception as error:
        print(error + ". For message: " + str(large_message_1))  # use log in production
        raise error


# Function that sends a message in a AWS SQS queue
def sendMessageSQS(queue_url, message_body, message_attributes):
    if not message_attributes:
        message_attributes = {}

    try:
        sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=str(message_body),
            MessageAttributes=message_attributes,
        )
        return
    except ClientError as error:
        print(error + ". For message: " + str(message_body))  # use log in production
        raise error


# Check size of the current message, if greater or equals than 240 kb, send ir to S3 and SQS.
# If smaller than 240 kb, send it only to SQS.
# Note: SQS limit is 256 kb
def main():
    message_size = getMessageSize(large_message_1.decode("utf-8"))

    if message_size >= 240:
        object_name = putObjectS3(bucket_name=bucket_name, object=large_message_1)
        sendMessageSQS(
            queue_url=queue_url,
            message_body=object_name,
            message_attributes=message_attributes,
        )

        print("Large Message Processed")  # use log in production
    else:
        sendMessageSQS(
            queue_url=queue_url,
            message_body=str(large_message_1),
            message_attributes=message_attributes,
        )

        print("Smaller Message Processed")  # use log in production


if __name__ == "__main__":
    main()
