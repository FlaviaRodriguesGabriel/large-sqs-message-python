import unittest
from unittest.mock import MagicMock, patch
import boto3
from producer import SqsProducer as producer


class TestMessageSending(unittest.TestCase):
    def setUp(self):
        self.s3_client = boto3.client("s3", endpoint_url="http://localhost:4566")
        self.sqs_client = boto3.client("sqs", endpoint_url="http://localhost:4566")

    def tearDown(self):
        # Clean up S3 bucket
        response = self.s3_client.list_objects(Bucket="large-message")
        if "Contents" in response:
            objects = response["Contents"]
            for obj in objects:
                self.s3_client.delete_object(Bucket="large-message", Key=obj["Key"])


# TODO: add tests

if __name__ == "__main__":
    unittest.main()
