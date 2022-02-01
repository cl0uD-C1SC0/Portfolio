from __future__ import print_function
import os
import boto3
import json

rekognition_collection_id = os.environ['collection']
sns_topic_arn = os.environ['sns_arn']
team_id = os.environ['team_id']

rekognition_client = boto3.client('rekognition')
sns_client = boto3.client('sns')
external_image_id = 'Kyle'

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
        response = rekognition_client.search_faces(
            CollectionId = rekognition_collection_id,
            FaceId=face_id
        )
        print('Index Faces Response:\n %s ' % face_id)
        if not response['FaceMatches']:
            print("Não encontramos ninguém")
            continue
        for match in response['FaceMatches']:
            if "ExternalImageId" in match['Face'] and match['Face']["ExternalImageId"] == external_image_id:
                print("Encontramos o CEO")
                return True
        
        print("Não encontramos nenhum CEO")
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

    return top_five

def lambda_handler(event, context):

    print(json.dumps(event))
    s3_message = event
    key = s3_message['Records'][0]['s3']['object']['key']
    bucket = s3_message['Records'][0]['s3']['bucket']['key']