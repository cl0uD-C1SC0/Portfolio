import boto3
import os
import json
import base64

region = 'us-east-1'
instance_id = 'i-02ce9e2204b66c94a'
base32 = ''
client = boto3.client('rekognition')

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    s3 = boto3.client('s3')
    buckets = s3.list_buckets()
   
    for bucket in buckets['Buckets']:
        bucket1 = bucket['Name']
        
    console_screenshot = ec2.get_console_screenshot(
        InstanceId=instance_id
        )
        
    fileName = 'ConsoleScreenShot-400' + '.png'
    bbucket = bucket1
    base32 = console_screenshot["ImageData"]
    
    
    s3.put_object(Bucket=bbucket, Key=fileName, Body=base32)
    
    return ('Image Successful uploaded to S3 Bucket: ' + bucket1)
    
    