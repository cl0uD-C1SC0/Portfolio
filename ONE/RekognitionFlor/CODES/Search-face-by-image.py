import json
import boto3
import os
from boto3.session import Session

access_key = os.environ['ACCESS_KEY']
secret_key = os.environ['SECRET_KEY']
default_region = os.environ['DEFAULT_REGION']


session = Session(
    aws_access_key_id = access_key,
    aws_secret_access_key = secret_key,
    region_name = default_region
    )

def search(bucket, key):
    bucket=bucket
    collectionId='takahashi'
    fileName=key
    threshold = 80
    maxFaces=2

    s3 = session.resource('s3')
    object = s3.Object(bucket, fileName)
    print(object.key)
    client=session.client('rekognition', default_region)


    response=client.search_faces_by_image(CollectionId=collectionId,
                                Image={'S3Object':{'Bucket':bucket,'Name':fileName}},
                                FaceMatchThreshold=threshold,
                                MaxFaces=maxFaces)


    faceMatches=response['FaceMatches']
    print ('Matching faces')
    for match in faceMatches:
            print ('FaceId:' + match['Face']['FaceId'])
            print ('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
    print('SearchedFaceConfidence: ' + "{:.2f}".format(response['SearchedFaceConfidence']) + "%")
    data=[]
    data.append(key)
    data.append(collectionId)
    data.append(str(round(response['SearchedFaceConfidence'], 2)))
    return data

def put_db(data):
    client = session.client('dynamodb')

    response = client.put_item(
        Item={
            'key': {
                'S': data[0],
            },
            'collectionId': {
                'S': data[1],
            },
            'Confidence': {
                'S': data[2],
            },
        },
        ReturnConsumedCapacity='TOTAL',
        TableName='Album',
    )

    print(response)

def buckup(bucket, fileName):

    client = session.client('s3')
    responce = client.copy_object(Bucket='takahashi-replica', Key='image5.jpg', CopySource={'Bucket': 'takahashiminami', 'Key': 'image5.jpg'})


    responce = '{"status": "OK"}'
    return responce


def lambda_handler(event, context):

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    response=search(bucket, key)

    put_db(response)

    buckup(bucket, key)

