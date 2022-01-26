import boto3
import json

region = 'us-east-1'
ec2_client = boto3.client('ec2')
sns = boto3.client('sns')

def lambda_handler(event, context):
