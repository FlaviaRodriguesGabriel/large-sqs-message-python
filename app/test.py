import unittest
from unittest.mock import MagicMock, patch
import boto3
from producer import SqsProducer as producer
import json


class TestMessageSending(unittest.TestCase):
    def setUp(self):
        self.s3_client = boto3.client("s3", endpoint_url="http://localhost:4566")
        self.sqs_client = boto3.client("sqs", endpoint_url="http://localhost:4566")

    def tearDown(self):
        # Clean up S3 bucket
        objects_already_in_bucket = self.s3_client.list_objects_v2(
            Bucket="large-message"
        )

        if "Contents" in objects_already_in_bucket:
            for index, key in enumerate(objects_already_in_bucket["Contents"]):
                s3 = boto3.resource("s3", endpoint_url="http://localhost:4566")
                s3.Object("large-message", key["Key"]).delete()
                index += 1

        # Clean up SQS queue
        queue_url = self.sqs_client.get_queue_url(QueueName="large-message")["QueueUrl"]
        self.sqs_client.purge_queue(QueueUrl=queue_url)

    def test_large_message_count_one_message(self):
        # Prepare
        large_message: str = "This represents a really large message for sqs queue"

        # Execution
        producer.send_large_message(large_message, self.s3_client, self.sqs_client)

        queue_url = self.sqs_client.get_queue_url(QueueName="large-message")["QueueUrl"]

        sqs_response: int = self.sqs_client.get_queue_attributes(
            QueueUrl=queue_url, AttributeNames=["ApproximateNumberOfMessages"]
        )

        number_of_messages = int(
            sqs_response["Attributes"]["ApproximateNumberOfMessages"]
        )

        objects_already_in_bucket = self.s3_client.list_objects_v2(
            Bucket="large-message"
        )

        if "Contents" in objects_already_in_bucket:
            number_of_objects = len(objects_already_in_bucket["Contents"])
        else:
            number_of_objects = 0

        # Assertions
        self.assertEqual(number_of_messages, 1)
        self.assertEqual(number_of_objects, 1)

    def test_large_message_count_five_messages(self):
        # Prepare
        large_message: str = "This represents a really large message for sqs queue"

        # Execution
        producer.send_large_message(large_message, self.s3_client, self.sqs_client)
        producer.send_large_message(large_message, self.s3_client, self.sqs_client)
        producer.send_large_message(large_message, self.s3_client, self.sqs_client)
        producer.send_large_message(large_message, self.s3_client, self.sqs_client)
        producer.send_large_message(large_message, self.s3_client, self.sqs_client)

        queue_url = self.sqs_client.get_queue_url(QueueName="large-message")["QueueUrl"]

        sqs_response: int = self.sqs_client.get_queue_attributes(
            QueueUrl=queue_url, AttributeNames=["ApproximateNumberOfMessages"]
        )

        number_of_messages = int(
            sqs_response["Attributes"]["ApproximateNumberOfMessages"]
        )

        objects_already_in_bucket = self.s3_client.list_objects_v2(
            Bucket="large-message"
        )

        if "Contents" in objects_already_in_bucket:
            number_of_objects = len(objects_already_in_bucket["Contents"])
        else:
            number_of_objects = 0

        self.assertEqual(number_of_messages, 5)
        self.assertEqual(number_of_objects, 5)

    def test_small_message_count_one_message(self):
        # Prepare
        large_message: str = "Small"

        # Execution
        producer.send_large_message(large_message, self.s3_client, self.sqs_client)

        queue_url = self.sqs_client.get_queue_url(QueueName="large-message")["QueueUrl"]

        sqs_response: int = self.sqs_client.get_queue_attributes(
            QueueUrl=queue_url, AttributeNames=["ApproximateNumberOfMessages"]
        )

        number_of_messages = int(
            sqs_response["Attributes"]["ApproximateNumberOfMessages"]
        )

        objects_already_in_bucket = self.s3_client.list_objects_v2(
            Bucket="large-message"
        )

        if "Contents" in objects_already_in_bucket:
            number_of_objects = len(objects_already_in_bucket["Contents"])
        else:
            number_of_objects = 0

        # Assertions
        self.assertEqual(number_of_messages, 1)
        self.assertEqual(number_of_objects, 0)

    def test_small_message_count_five_messages(self):
        # Prepare
        large_message: str = "Small"

        # Execution
        producer.send_large_message(large_message, self.s3_client, self.sqs_client)
        producer.send_large_message(large_message, self.s3_client, self.sqs_client)
        producer.send_large_message(large_message, self.s3_client, self.sqs_client)
        producer.send_large_message(large_message, self.s3_client, self.sqs_client)
        producer.send_large_message(large_message, self.s3_client, self.sqs_client)

        queue_url = self.sqs_client.get_queue_url(QueueName="large-message")["QueueUrl"]

        sqs_response: int = self.sqs_client.get_queue_attributes(
            QueueUrl=queue_url, AttributeNames=["ApproximateNumberOfMessages"]
        )

        number_of_messages = int(
            sqs_response["Attributes"]["ApproximateNumberOfMessages"]
        )

        objects_already_in_bucket = self.s3_client.list_objects_v2(
            Bucket="large-message"
        )

        if "Contents" in objects_already_in_bucket:
            number_of_objects = len(objects_already_in_bucket["Contents"])
        else:
            number_of_objects = 0

        self.assertEqual(number_of_messages, 5)
        self.assertEqual(number_of_objects, 0)


if __name__ == "__main__":
    unittest.main()
