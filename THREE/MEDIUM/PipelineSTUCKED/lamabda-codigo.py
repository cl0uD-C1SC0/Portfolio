import ssl
import os
import json
import boto3
from urllib.request import urlopen

cp_client = boto3.client('codepipeline')
ssl_create_default_https_context = ssl_create_unverified_context

def lambda_handler(event, context):
    url = os.getenv('API_URL')
    try:
        status_code = urlopen(url).getcode()
        print(status_code)
        cp_client.put_job_sucess_result(jobId=event['CodePipeline.job']['Id'])
        return {
            'statusCode': status_code,
            "body": "Comleted Lambda execution successfully"
        }
        except Exception as e:
            print(f'Error occured = {str(e)}')
            cp_client.put_job_failure_result(
                jobId=event['CodePipeline.job']['id'],
                failureDetails={'message': str(e), 'type': 'JobFailed'})
            return {
                'statusCode': 500,
                'body': "Lambda execution completed. Internal error occured"
            }