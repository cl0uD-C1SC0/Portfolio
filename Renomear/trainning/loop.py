from _future__ import print_function

import os
import boto3
import json

rekognition_collection_id = os.environ['collection']
bucket = os.environ['bucket']
external_image_id = 'Kyle'

rekognition_client = os.environ['rekognition']
s3_client = os.environ['s3']

def lambda_handler(event, context):
    list = s3_client.list_objects(
        Bucket=bucket
    )
    for obj in list['Contents']:
        response = rekognition_client.index_faces(
            CollectionId = rekognition_collection_id,
            Image={
                'S3Object':{'Bucket':bucket,'Name':obj['Key']}
            },
            ExternalImageId=external_image_id
        )
        print('Object Name: %s ' % obj{'Key'})