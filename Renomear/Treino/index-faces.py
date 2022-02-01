from __future__ import print_function

import boto3
import json
import os

rekognition_collection_id = os.environ['collection']
bucket = os.environ['bucket']
rekognition_client = boto3.client('rekognition')
s3_client = boto3.client['s3']
external_image_id = 'Kyle'
def lambda_handler(event, context):
    response = s3_client.list_objects(
        Bucket=bucket
    )
    for obj in response['Contents']:
        response = rekognition_client.index_faces(
            CollectionId=rekognition_collection_id,
            Image={
                'S3Object':{'Bucket':bucket,'Name':obj['Key']}
            },
            ExternalImageId=external_image_id
        )
        print('Object Name: %s' % obj['Key'])