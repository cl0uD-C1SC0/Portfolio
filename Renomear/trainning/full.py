from __future__ import print_function

import json
import boto3
import os

rekognition_collection_id = os.environ['colleciton']
sns_topic_arn = os.environ['sns_arn']

external_image_id = 'Kyle'

rekognition_client = boto3.client('rekognition')
sns_client = boto3.client('sns')

def facial_recognition(key, bucket):
    response = rekognition_client.index_faces(
        CollectionId = rekognition_collection_id,
        Image={
            'S3Object':{'Bucket':bucket,'Name':key}
        }
    )
    if not response['FaceRecords']:
        return False
    for face in response['FaceRecords']:
        face_id = face['Face']['FaceId']
        print('Index Faces Response:\n %s' % face_id)
        response = rekognition_client.search_faces(
            CollectionId = rekognition_collection_id,
            FaceId=face_id
        )
        if not response['FaceMatches']:
            print("Not kyle, keep looking..... :(")
            continue
        for match in response['FaceMatches']:
            if "ExternalImageId" in match['Face'] and match['Face']["ExternalImageId"] == external_image_id:
                print("Founded CEO! Huzzah!")
                return True
        
        print("Encontramos nada")
        return False

def get_labels(key, bucket):
    response = rekognition_client.detect_labels(
        Image={
            'S3Object':{'Bucket':bucket,'Name':key}
        },
        MinConfidence=50
    )
    raw_labels = response['Labels']
    top_five = []
    for x in range(0,5):
        top_five.append(raw_labels[x]['Name'])

    return True

def lambda_handler(event, context):

    print(json.dumps(event))
    s3_message = event
    key = s3_message['Records'][0]['s3']['object']['key']
    bucket = s3_message['Records'][0]['s3']['bucket']['name']