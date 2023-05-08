#!/usr/bin/env bash

set -euo pipefail

# enable debug
# set -x

echo "configuring sqs"
echo "==================="

aws sqs delete-queue --queue-url "http://localhost:4566/081378642243/large-message" --endpoint-url=http://localhost:4566 --region sa-east-1

aws --endpoint-url=http://localhost:4566 sqs create-queue --queue-name large-message --region sa-east-1 --attributes "MessageRetentionPeriod"="1209600"

aws --endpoint-url=http://localhost:4566 s3api create-bucket --bucket large-message --region sa-east-1 --create-bucket-configuration LocationConstraint=sa-east-1

aws --endpoint-url=http://localhost:4566 s3api put-bucket-lifecycle-configuration --bucket large-message --region sa-east-1  --lifecycle-configuration file://lifecycle.json

aws --endpoint-url=http://localhost:4566 s3api list-objects --bucket large-message --region sa-east-1

aws --endpoint-url=http://localhost:4566 sqs receive-message --region sa-east-1 --queue-url http://localhost:4566/081378642243/large-message

