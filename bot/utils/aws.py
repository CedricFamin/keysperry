import boto3
import os


def get_s3_client():
    return boto3.client(
        's3'
        , aws_access_key_id=os.getenv('KEYSPERRY_AWS_KEY')
        , aws_secret_access_key=os.getenv('KESYPERRY_AWS_SECRET')
        , region_name='eu-west-3')
