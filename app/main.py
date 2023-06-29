from producer import SqsProducer as producer


def main():
    message = "This is a sample message exceeding 10 characters"
    [s3_client, sqs_client] = producer.create_clients()
    producer.send_large_message(message, s3_client, sqs_client)


if __name__ == "__main__":
    main()
