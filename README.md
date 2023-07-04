# large-sqs-message-python

## Objectives
:star2: Use AWS SQS with large messages (greater than 256 kb) in a Python application.

Steps:
* Create a SQS queue with retention period of 14 days 
* Create a S3 bucket with a lifecycle policy to delete objects 14 days after its creation
* Inserts object into S3 bucket
* Produces a SQS message with the location of the object in S3 bucket
* If an error occurs, log error and throw exception

## Requirements

* 🐍 Python 3.10 (see [installation guide](https://www.python.org/downloads/))
* 🐍 pip (see [installation guide](https://pip.pypa.io/en/latest/installation/))
* 🐍 virtualenv ([`pip install virtualenv`](https://pypi.org/project/virtualenv/))
* 🐳 Docker (see [installation guide](https://docs.docker.com/engine/install/))

## Running app

* Virtualenv and then activating it
```bash
virtualenv --python py310 .venv
source .venv/bin/activate
```
* Installing requirements
```bash
pip install -r app/requirements.txt
```

* Docker
```bash
docker compose -f app/docker-compose.yml -p large-message up -d
```
*
    * Create SQS and S3 bucket using localstack

```bash
sh app/localstack_bootstrap/s3_sqs_bootstrap.sh
```