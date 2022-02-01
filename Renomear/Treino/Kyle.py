from __future__ import print_function

import boto3
import json
import os

rekognition_collection_id = os.environ['collection']
sns_topic_arn = os.environ['sns_arn']
team_id = os.environ['team_id']

external_image_id = 'Kyle'

rekognition_client = boto3.client('rekognition')
sns_client = boto3.client('sns')
s3_client = boto3.client

def facial_recognition(bucket, key):
    response = rekognition_client.index_faces(
        CollectionId=rekognition_collection_id,
        Image={
            'S3Object':{'Bucket':bucket,'Name':key}
        }
    )
    if not response['FaceRecords']:
        return False
    for face in response['FaceRecords']:
        face_id = face['Face']['FaceId']
        response = rekognition_client.search_faces(
            CollectionId=rekognition_collection_id,
            FaceId=face_id
        )
        if not response['FaceMatches']:
            print("Nenhuma semelhança encontrada")
            continue
        for match in response['FaceMatches']:
            if "ExternalImageId" in match['Face'] and match['Face']["ExternalImageID"] == external_image_id:
                print("Encontramos semelhança")
                return True
        
        print ("Não encontramos nada")
        return False

def get_labels(bucket, key):
    response = rekognition_client.detect_labels(
        Imagae={
            'S3Object':{'Bucket':bucket,'Name':key}
        },
        MinConfidence=50
    )
    raw_labels = response['Labels']
    top_five = []
    for x in range(0,5):
        top_five.append(raw_labels[x]['Name'])
    
    return top_five

def lambda_handler(event, context):
    print(json.dumps(event))
    s3_message = event
    key = s3_message['Records'][0]['s3']['object']['key']
    bucket = s3_message['Records'][0]['s3']['bucket']['name']